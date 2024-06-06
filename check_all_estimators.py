import multiprocessing as mp
import time

from sktime.registry import all_estimators
from sktime.utils import check_estimator
from tqdm import tqdm


def check_estimator_wrapper(args):
    """Wrapper function to run check_estimator in parallel"""
    estimator, num_runs = args
    results = []
    for _ in range(num_runs):
        start_time = time.time()
        status = check_estimator(estimator, verbose=False)
        end_time = time.time()
        results.append((status, end_time - start_time))
    return results


def check_all_estimators(num_processes=4):
    """Runs `check_estimator()` for all the estimators in sk-time
    Returns
    -------
    list[list[obj]]
    Returns a list of lists consisting of each estimator,
    the status of their checks and the total time taken
    """
    statuses = []
    estimators = all_estimators(return_names=False)
    num_runs = 10

    # Creating a progress bar to gauge progress
    progress_bar = tqdm(estimators, total=len(estimators), unit="estimator")

    # Create a pool of worker processes
    pool = mp.Pool(processes=num_processes)

    # Run check_estimator_wrapper in parallel
    results = pool.map(check_estimator_wrapper, [(est, num_runs) for est in estimators])

    # Close the pool and wait for the tasks to finish
    pool.close()
    pool.join()

    # Collect the results
    for estimator, result in zip(estimators, results):
        metadata = {}
        metadata["name"] = str(estimator)
        metadata["results"] = result
        statuses.append(metadata)

        # Update the progress bar
        progress_bar.set_postfix(estimator=metadata["name"])

    return statuses


# Attempting to check all the estimators
status = check_all_estimators()
print(status)

