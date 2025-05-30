# ADAM - Architectural Design Automation Module

ADAM is a Python-based computational design framework that facilitates structured geometry creation and parametric design through a data flow system.
Developed as a part of my PhD research.
## Core Concepts

### Data Structure

ADAM's foundation is built on a hierarchical data system:

- **Path**: An identifier representing a branch's position in the hierarchy (e.g., `Path(0,1,2)`)
- **Branch**: A container of atomic values labeled with a specific Path
- **DataTree**: A collection of branches organized by their paths

### Component System

Components are the processing units that transform data:

- Accept inputs as DataTrees, Branches, or scalar values
- Normalize and align data structures automatically
- Process information and generate output DataTrees

## Usage Example

```python
# Creating data trees
x = DataTree()
x.add_branch(Branch(Path(0,0), [1.0, 2.0]))
y = DataTree()
y.add_branch(Branch(Path(0,0), [5.0]))
z = DataTree()
z.add_branch(Branch(Path(0,0), [0.0, 0.0]))

# Creating a Point component
pt = Point(x, y, z)

# Result: DataTree with Points at path (0,0)
# {
#   Path(0,0): [Point(1.0, 5.0, 0.0), Point(2.0, 5.0, 0.0)]
# }
```

## Path Behavior System

Components define how they handle paths through `path_mode`:

- `preserve`: Output maintains input path structure
- `extend`: Output path is input path with one additional level
- `custom`: Custom path behavior via `define_output_path()`

## Branch and Element Matching

When branch paths or element counts differ across inputs:

- **Branch Matching**: Uses `strict` (exact match) or `auto` (fallback) modes
- **Element Matching**: Handles mismatched counts via `longest` (repeat last), `first` (repeat first), or `shortest` (truncate) modes

## Atomic Elements

Atomic elements are the indivisible units inside branches:

```python
class AtomicPoint(Atomic):
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z
        
    def serialize(self):
        return {"type": "point", "x": self.x, "y": self.y, "z": self.z}
```

## Creating Components

Components inherit from `CreateDataTree` and implement a `compute` method:

```python
class Point(CreateDataTree):
    path_mode = 'preserve'
    
    def compute(self, *branches: Branch):
        path = branches[0].path
        points = []
        for x, y, z in zip(*[b.elements for b in branches]):
            points.append(AtomicPoint(x, y, z))
        return Branch(path, points)
```

## Styling

Components can accept optional `Style` objects for appearance control:

```python
style = Style(stroke="red", stroke_width=2)
line = Line(pt1, pt2, style=style)
```
