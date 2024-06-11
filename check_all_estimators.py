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
        total_time = 0
        for _ in range(num_runs):
            start_time = time.time()

            status = check_estimator(estimator, verbose=False)
            end_time = time.time()
            total_time += end_time - start_time

            results.append((str(status), end_time - start_time))
        average_time = total_time / num_runs
        return estimator, results, average_time
    except Exception as e:
        print(f"Error while checking estimator {estimator}: {e}")
        traceback.print_exc()
        return estimator, [str(e)], 0


def check_all_estimators(num_processes=4):
    """Runs `check_estimator()` for all the estimators in sk-time
    Returns
    -------
    dict
        A dictionary containing the results for each estimator,
        including the status, time taken for each run, and the average time.
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
        return {}
    # Close the pool and wait for the tasks to finish
    pool.close()
    pool.join()

    # Organize the results into a dictionary
    estimator_results = {}
    for estimator, result, average_time in results:

        estimator_results[str(estimator)] = {
            "results": result,
            "average_time": average_time,
        }

    # Write the results to a JSON file
    import json

    with open("estimator_results.json", "w") as f:
        json.dump(estimator_results, f, indent=4)

    return estimator_results


# Attempting to check all the estimators
try:
    results = check_all_estimators()
    print("Results written to estimator_results.json")
except Exception as e:
    print(f"Error occurred while checking all estimators: {e}")
    traceback.print_exc()
