import random


class DataMaker:

    def __init__(
        self,
        seed: int | None = None,
    ):
        # Own random number generator; the same seed gives the same data
        self.r = random.Random(seed)

    def make_list(self, n: int, min, max):
        return [self.r.randint(min, max) for _ in range(n)]

    def make_float_list(self, n: int, min: float, max: float):
        return [self.r.uniform(min, max) for _ in range(n)]

    def random_value(self, tab):
        return self.r.choice(tab)
