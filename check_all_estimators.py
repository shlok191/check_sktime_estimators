import multiprocessing as mp
import time
import traceback

from sktime.registry import all_estimators
from sktime.utils import check_estimator
from tqdm import tqdm


def check_estimator_wrapper(args):
    """Wrapper function to run check_estimator in parallel"""
    try:
        estimator, num_runs = args
        results = []
        for _ in range(num_runs):
            start_time = time.time()
            status = check_estimator(estimator, verbose=False)
            end_time = time.time()
            results.append((status, end_time - start_time))
    
        return estimator, results
    
    except Exception as e:
        print(f"Error while checking estimator {estimator}: {e}")
        traceback.print_exc()
        return estimator, [str(e)]


def check_all_estimators(num_processes=4):
    """Runs `check_estimator()` for all the estimators in sk-time
    Returns
    -------
    list[list[obj]]
        Returns a list of lists consisting of each estimator,
        the status of their checks and the total time taken
    """
    estimators = all_estimators(return_names=False)
    num_runs = 10

    # Create a pool of worker processes
    pool = mp.Pool(processes=num_processes)

    # Run check_estimator_wrapper in parallel
    try:
        results = pool.map(
            check_estimator_wrapper, [(est, num_runs) for est in estimators]
        )
    except Exception as e:
        print(f"Error occurred during parallel execution: {e}")
        traceback.print_exc()
        pool.terminate()
        pool.join()
        return []

    # Close the pool and wait for the tasks to finish
    pool.close()
    pool.join()

    # Write the results to a text file
    with open("estimator_results.txt", "w") as f:
        for estimator, result in results:
            f.write(f"Estimator: {estimator}\n")
            f.write("Results:\n")
            for status, time_taken in result:
                f.write(f"Status: {status}, Time taken: {time_taken:.6f} seconds\n")
            f.write("\n")

    return results


# Attempting to check all the estimators
try:
    status = check_all_estimators()
    print("Results written to estimator_results.txt")
except Exception as e:
    print(f"Error occurred while checking all estimators: {e}")
    traceback.print_exc()
