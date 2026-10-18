import random

from ComplexityMeasurement import ComplexityMeasurement
from benchmark_data_maker import DataMaker
from algorytm import search

# Size of a single array (N) and number of measurements (n)
ARRAY_SIZE = 1000
RUNS = 100

if __name__ == "__main__":
    cm = ComplexityMeasurement(search, RUNS)
    dm = DataMaker()

    # Every run gets a fresh random array and a random value that is in it
    for run in range(RUNS):
        tab = dm.make_list(ARRAY_SIZE, 0, 10 * ARRAY_SIZE)
        target = dm.random_value(tab)
        cm.run_n_times(1, target, tab)
        print(
            f"run {run + 1:>2}: "
            f"position = {tab.index(target) + 1:>4}, "
            f"iterations = {cm.iters[-1]:>4}, "
            f"time (1000 calls) = {cm.times[-1]:.6f} s"
        )

    cm.compute_stats()

    print()
    print(f"average iterations:     {cm.avarage_i:.2f}")
    print(f"theoretical average:    {(ARRAY_SIZE + 1) / 2:.2f}")
    print(f"standard deviation:     {cm.std_dev_i:.2f}")
    print(f"relative error (iters): {cm.relative_error_i * 100:.2f} %")
    print(f"relative error (time):  {cm.relative_error_t * 100:.2f} %")
    print()
    print(cm.to_json())
