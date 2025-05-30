
from adam.components.Core.DataTree import CreateDataTree, Branch
import random
from adam.components.Maths.Domain.ConstructDomain import AtomicDomain

class Random(CreateDataTree):
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.__init__(*args, **kwargs)
        return instance.get_output()

    def run(self, domain, count, seed=0, path=None):
        if seed == 0:
            seed = random.randint(0, 1000000)
        if not isinstance(domain, AtomicDomain):
            raise TypeError(f"Expected AtomicDomain, got {type(domain)}")

        random.seed(seed)
        return Branch(path, [random.uniform(domain.start, domain.end) for _ in range(int(count))])
