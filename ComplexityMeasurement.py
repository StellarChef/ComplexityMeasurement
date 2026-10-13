import random
import timeit
import math
import sys
import logging as logs
"""
Napisz moduł (klasę, pakiet, itp.), służącą do pomiaru złożoności obliczeniowej
według wzorów na średnią arytmetyczną, wariancję,
odchylenie standardowe oraz błąd względny.
Należy przygotować dwa zestawy: pierwszy dla obliczania średniej liczby iteracji,
drugi do średniego czasu wykonania.

"""

class ComplexityMeasurement:

    def __init__(self, algo):
        self.algo = algo

    _sum_t = 0
    _sum_i = 0
    _iters: int = []
    _times:float = []
    _avarage_i: float = 0
    _avarage_t: float = 0

    def _tracer(self, frame, event, arg):
        return event, frame.f_code.co_name, frame.f_lineno, arg

    def _get_count_of_iterations(self):     
        sys.settrace(self._tracer)
        self.data.append(self.algo)
        sys.settrace(None)  

    def _getavaragei():
        pass
    def measure_iterations(self):
        pass

    def measure_time_of_resolving(self):
        pass

    def _run_n_times(self, n: int) -> list:
        for i in range(n):
            self._iters.append(self._get_count_of_iterations(self.algo))
            self._times.append(self.measure_time_of_resolving(self.algo))

        return self.iters, self.times

    def sum(self,iters, times):
        sum_i = 0
        sum_t = 0
        for i in iters: sum_i += i
        for t in times: sum_t += t

        return self._sum_t, self._sum_i


    def _avarage(self, n:int):
        self._avarage_t = self.sum_i/n
        self._avarage_i =  self.sum_t/n
        return self._avarage_i, self._avarage_t

        

    def printresults():
        pass
