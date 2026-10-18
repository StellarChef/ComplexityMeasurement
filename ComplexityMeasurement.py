from itertools import count
import random
import timeit
import math
import sys
import logging as logs
import json

"""
Napisz moduł (klasę, pakiet, itp.), służącą do pomiaru złożoności obliczeniowej
według wzorów na średnią arytmetyczną, wariancję,
odchylenie standardowe oraz błąd względny.
Należy przygotować dwa zestawy: pierwszy dla obliczania średniej liczby iteracji,
drugi do średniego czasu wykonania.

"""


class ComplexityMeasurement:

    def __init__(self, algo: function, n: int):
        self.algo = algo
        self.n = n
        self._iters: list[int] = []
        self._times: list[float] = []

    _sum_t = 0
    _sum_i = 0
    avarage_i: float = 0
    avarage_t: float = 0
    variance_i: float = 0
    variance_t: float = 0
    std_dev_i: float = 0
    std_dev_t: float = 0

    def _get_count_of_iterations(self, *args):
        mon = sys.monitoring
        TOOL = mon.PROFILER_ID
        count = 0

        def on_jump(code, src, dst):
            nonlocal count
            if dst < src:
                count += 1

        mon.use_tool_id(TOOL, "iter_counter")
        mon.register_callback(TOOL, mon.events.JUMP, on_jump)
        mon.set_local_events(TOOL, self.algo.__code__, mon.events.JUMP)
        try:
            self.algo(*args)
        finally:
            mon.set_local_events(TOOL, self.algo.__code__, 0)
            mon.register_callback(TOOL, mon.events.JUMP, None)
            mon.free_tool_id(TOOL)
        return count

    def measure_time_of_resolving(self, *args):
        return timeit.timeit(lambda: self.algo(*args), number=1000)

    def _run_n_times(self, n: int, *args) -> tuple[list[int], list[float]]:
        for i in range(n):
            self._iters.append(self._get_count_of_iterations(*args))
            self._times.append(self.measure_time_of_resolving(*args))

        return self._iters, self._times

    def sum(self, iters, times):
        sum_i = 0
        sum_t = 0
        for i in iters:
            sum_i += i
        for t in times:
            sum_t += t
        self._sum_i = sum_i
        self._sum_t = sum_t
        return self._sum_t, self._sum_i

    def _avarage(self, n: int):
        self.avarage_t = self._sum_t / n
        self.avarage_i = self._sum_i / n
        return self.avarage_t, self.avarage_i

    def _variance(self, n):
        sum_i: int = 0
        sum_t: float = 0
        for _ in range(n):
            sum_i += math.pow(self._iters[_] - self.avarage_i, 2)
            sum_t += math.pow(self._times[_] - self.avarage_t, 2)
        self.variance_i = 1 / n * sum_i
        self.variance_t = 1 / n * sum_t

        return self.variance_t, self.variance_i

    def _standard_deviation(self):
        self.std_dev_i = math.sqrt(self.variance_i)
        self.std_dev_t = math.sqrt(self.variance_t)

        return self.std_dev_t, self.std_dev_i

    def to_json(self) -> str:
        results = {
            "algorithm": getattr(self.algo, "__name__", str(self.algo)),
            "runs": len(self._iters),
            "iterations": {
                "sum": self._sum_i,
                "average": self.avarage_i,
                "variance": self.variance_i,
                "standard_deviation": self.std_dev_i,
                "measurements": self._iters,
            },
            "time": {
                "sum": self._sum_t,
                "average": self.avarage_t,
                "variance": self.variance_t,
                "standard_deviation": self.std_dev_t,
                "measurements": self._times,
            },
        }

        return json.dumps(results, indent=4, ensure_ascii=False)
