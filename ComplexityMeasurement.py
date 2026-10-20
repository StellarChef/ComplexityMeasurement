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

    def __init__(self, algo, n: int):
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
    relative_error_i: float = 0
    relative_error_t: float = 0

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
        return timeit.timeit(lambda: self.algo(*args), number=1)

    def run_n_times(self, n: int, *args) -> tuple[list[int], list[float]]:
        for i in range(n):
            self._iters.append(self._get_count_of_iterations(*args))
            self._times.append(self.measure_time_of_resolving(*args))

        return self._iters, self._times

    # Read-only access to the collected measurements
    @property
    def iters(self) -> list[int]:
        return self._iters

    @property
    def times(self) -> list[float]:
        return self._times

    # Computes all statistics in the required order and returns them
    # as a dictionary. Call it after all measurements are collected.
    def compute_stats(self) -> dict:
        n = len(self._iters)
        if n == 0:
            raise ValueError("No measurements - call run_n_times first")

        self._sum(self._iters, self._times)
        self._avarage(n)
        self._variance(n)
        self._standard_deviation()
        self._relative_error(n)

        return {
            "iterations": {
                "sum": self._sum_i,
                "average": self.avarage_i,
                "variance": self.variance_i,
                "standard_deviation": self.std_dev_i,
                "relative_error": self.relative_error_i,
            },
            "time": {
                "sum": self._sum_t,
                "average": self.avarage_t,
                "variance": self.variance_t,
                "standard_deviation": self.std_dev_t,
                "relative_error": self.relative_error_t,
            },
        }

    # ------------------------------------------------------------------
    # Statistical functions
    # Order of computation: sum -> average -> variance
    #                       -> standard deviation -> relative error
    # Each step uses the results of the previous ones.
    # ------------------------------------------------------------------

    # Sum of all measurements: S = x_1 + x_2 + ... + x_n
    def _sum(self, iters, times):
        sum_i = 0
        sum_t = 0
        for i in iters:
            sum_i += i
        for t in times:
            sum_t += t
        self._sum_i = sum_i
        self._sum_t = sum_t
        return self._sum_t, self._sum_i

    # Arithmetic mean: x_avg = S / n
    def _avarage(self, n: int):
        self.avarage_t = self._sum_t / n
        self.avarage_i = self._sum_i / n
        return self.avarage_t, self.avarage_i

    # Variance: sigma^2 = (1 / n) * sum((x_k - x_avg)^2)
    def _variance(self, n):
        sum_i: int = 0
        sum_t: float = 0
        for _ in range(n):
            sum_i += math.pow(self._iters[_] - self.avarage_i, 2)
            sum_t += math.pow(self._times[_] - self.avarage_t, 2)
        self.variance_i = 1 / n * sum_i
        self.variance_t = 1 / n * sum_t

        return self.variance_t, self.variance_i

    # Standard deviation: sigma = sqrt(sigma^2)
    def _standard_deviation(self):
        self.std_dev_i = math.sqrt(self.variance_i)
        self.std_dev_t = math.sqrt(self.variance_t)

        return self.std_dev_t, self.std_dev_i

    # Relative error of the mean: delta = (sigma / sqrt(n)) / x_avg
    # sigma / sqrt(n) is the standard error of the mean, so delta tells
    # how precisely the average is known and shrinks as n grows.
    # Multiply by 100 to get the value in percent.
    def _relative_error(self, n: int):
        # Avoid division by zero when the average is 0
        if self.avarage_i != 0:
            self.relative_error_i = (self.std_dev_i / math.sqrt(n)) / self.avarage_i
        if self.avarage_t != 0:
            self.relative_error_t = (self.std_dev_t / math.sqrt(n)) / self.avarage_t

        return self.relative_error_t, self.relative_error_i

    # ------------------------------------------------------------------
    # End of statistical functions
    # ------------------------------------------------------------------

    def to_json(self) -> str:
        results = {
            "algorithm": getattr(self.algo, "__name__", str(self.algo)),
            "runs": len(self._iters),
            "iterations": {
                "sum": self._sum_i,
                "average": self.avarage_i,
                "variance": self.variance_i,
                "standard_deviation": self.std_dev_i,
                "relative_error": self.relative_error_i,
                "measurements": self._iters,
            },
            "time": {
                "sum": self._sum_t,
                "average": self.avarage_t,
                "variance": self.variance_t,
                "standard_deviation": self.std_dev_t,
                "relative_error": self.relative_error_t,
                "measurements": self._times,
            },
        }

        return json.dumps(results, indent=4, ensure_ascii=False)
