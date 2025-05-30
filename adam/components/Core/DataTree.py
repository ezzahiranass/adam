from adam.components.Core.Style import Style
from typing import List, Dict
from adam.components.Core.AtomicTypes.Atomic import Atomic
from adam.components.Core.AtomicTypes.AtomicBrep import AtomicBrep




class Path:
    def __init__(self, *indices: int):
        self.indices = tuple(indices) if indices else (0,)

    def __hash__(self): return hash(self.indices)
    def __eq__(self, other): return self.indices == other.indices
    def __lt__(self, other): return self.indices < other.indices
    def __repr__(self):
        return f"Path{self.indices}"


    def is_parent_of(self, other): ...
    def append(self, index: int): return Path(*self.indices, index)
    def depth(self): return len(self.indices)



class Branch:
    def __init__(self, path: Path=Path(0,), elements: List['Atomic']=[]):
        self.path = path
        self.elements = elements

    def __repr__(self):
        if len(self.elements) == 0:
            return f"<Branch {self.path.indices}: empty>"
        if len(self.elements) == 1:
            return f"<Branch {self.path.indices}: 1 element>"
        return f"<Branch {self.path.indices}: {len(self.elements)} elements>"

    def map(self, func): return Branch(self.path, [func(e) for e in self.elements])
    def serialize(self): return [el.serialize() for el in self.elements]


class DataTree:
    def __init__(self):
        self.tree: Dict[Path, Branch] = {}

    def add_branch(self, branch: Branch):
        self.tree[branch.path] = branch
    
    def __iter__(self):
        return iter(self.tree.values())

    @property
    def branches(self): return list(self.tree.values())

    @property
    def atoms(self):
        return {
            path: branch.elements
            for path, branch in self.tree.items()
        }
    
    def __repr__(self): 
        if len(self.branches) == 0:
            return "<DataTree empty>"
        if len(self.branches) == 1:
            return f"<DataTree 1 branch>"
        return f"<DataTree {len(self.branches)} branches>"
    
    def assign_type(self, type):
        for branch in self.branches:
            for element in branch.elements:
                if isinstance(element, AtomicBrep):
                    element.assign_type(type)

    def serialize(self, flatten=False):
        if flatten:
            return [el.serialize() for branch in self.branches for el in branch.elements]
        else:
            return {
                tuple(path.indices): branch.serialize()
                for path, branch in self.tree.items()
            }

    def traverse(self):
        return self.tree.items()

    def map(self, func):  # Map over elements
        new_tree = DataTree()
        for path, branch in self.tree.items():
            new_tree.add_branch(branch.map(func))
        return new_tree
    
    def graft(self):
        new_tree = DataTree()
        for path, branch in self.tree.items():
            for i, element in enumerate(branch.elements):
                new_path = Path(*path.indices, i)
                new_tree.add_branch(Branch(new_path, [element]))
        
        self.tree = new_tree.tree
        return self


    def flatten(self):
        new_tree = DataTree()
        all_elements = []
        for _, branch in self.tree.items():
            all_elements.extend(branch.elements)
        new_tree.add_branch(Branch(Path(0), all_elements))
        self.tree = new_tree.tree
        return self


    def shift_paths(self, offset: int):
        new_tree = DataTree()
        for path, branch in self.tree.items():
            new_path = Path(*(i + offset for i in path.indices))
            new_tree.add_branch(Branch(new_path, branch.elements))
        return new_tree



class CreateDataTree:
    path_mode = 'extend' # 'preserve', 'extend', 'custom'
    branch_mode = 'auto' # 'auto', 'strict'
    element_mode = 'longest' # 'longest', 'first', 'shortest'

    def __new__(cls, *inputs: DataTree, style=None):
        instance = super().__new__(cls)
        instance.__init__(*inputs, style=style)
        return instance.output_tree

    def __init__(self, *inputs, style=None):
        self.inputs = [self.normalize_input(i) for i in inputs]
        self.style = style
        self.output_tree = DataTree()
        self.compute_all()


    
    def normalize_input(self, input_val):
        if isinstance(input_val, DataTree):
            return input_val
        elif isinstance(input_val, Branch):
            tree = DataTree()
            tree.add_branch(input_val)
            return tree
        else:
            # Wrap any scalar or atomic value into a default DataTree
            # CALL A FUNCTION TO ASSIGN RAW VALUES TO CORRECT PATHS
            branch = Branch(Path(0), [input_val])
            tree = DataTree()
            tree.add_branch(branch)
            return tree



    def compute_all(self):
        all_paths = self.get_all_paths()
        for path in all_paths:
            input_branches = self.gather_branches_for_path(path)
            max_len = self.get_max_length_for_path(input_branches)
            aligned_branches = [self.align_branch_elements(b, max_len) for b in input_branches]

            result = self.compute(*aligned_branches, style=self.style)

            if self.path_mode == 'extend':
                # Must be a list of branches
                for sub_index, branch in enumerate(result):
                    new_path = path.append(sub_index)
                    branch.path = new_path
                    self.output_tree.add_branch(branch)
            else:
                out_path = self.resolve_output_path(path, aligned_branches, result)
                result.path = out_path
                self.output_tree.add_branch(result)



    def resolve_output_path(self, input_path: Path, input_branches: List[Branch], result_branch: Branch) -> Path:
        if self.path_mode == 'preserve':
            return input_path
        elif self.path_mode == 'extend':
            return input_path.append(0)
        elif self.path_mode == 'custom':
            return self.define_output_path(input_path, input_branches, result_branch)
        else:
            raise ValueError(f"Unknown path_mode: {self.path_mode}")

    def define_output_path(self, input_path: Path, input_branches: List[Branch], result_branch: Branch) -> Path:
        return input_path  # default override hook

    def get_all_paths(self):
        if hasattr(self, 'structure_inputs'):
            paths = set()
            for i in self.structure_inputs:
                paths.update(self.inputs[i].tree.keys())
            return sorted(paths)
        else:
            all_paths = set()
            for tree in self.inputs:
                all_paths.update(tree.tree.keys())
            return sorted(all_paths)



    def gather_branches_for_path(self, path: Path) -> List[Branch]:
        result = []
        for tree in self.inputs:
            if path in tree.tree:
                branch = tree.tree[path]
            else:
                if self.branch_mode == 'auto' and tree.tree:
                    branch = list(tree.tree.values())[-1]
                else:
                    branch = Branch(path, [])
            result.append(branch)
        return result

    def get_max_length_for_path(self, branches: List[Branch]) -> int:
        return max((len(b.elements) for b in branches), default=0)


    def align_branch_elements(self, branch: Branch, max_len: int) -> Branch:
        elements = branch.elements
        if len(elements) == max_len:
            return branch
        elif self.element_mode == 'longest' and elements:
            return Branch(branch.path, elements + [elements[-1]] * (max_len - len(elements)))
        elif self.element_mode == 'first' and elements:
            return Branch(branch.path, elements + [elements[0]] * (max_len - len(elements)))
        elif self.element_mode == 'shortest':
            return Branch(branch.path, elements[:max_len])
        else:
            return branch  # fallback if empty or can't align

