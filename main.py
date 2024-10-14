import contextlib
from typing import Any

import joblib
from joblib import delayed
import time
from joblib import Parallel as JoblibParallel
from tqdm import tqdm

@contextlib.contextmanager
def tqdm_joblib(tqdm_object: Any) -> Any:
    """Context manager to patch joblib to report into tqdm progress bar given as argument"""
    class TqdmBatchCompletionCallback(joblib.parallel.BatchCompletionCallBack):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, **kwargs)

        def __call__(self, *args: Any, **kwargs: Any) -> Any:
            tqdm_object.update(n=self.batch_size)
            return super().__call__(*args, **kwargs)

    old_batch_callback = joblib.parallel.BatchCompletionCallBack
    joblib.parallel.BatchCompletionCallBack = TqdmBatchCompletionCallback
    try:
        yield tqdm_object
    finally:
        joblib.parallel.BatchCompletionCallBack = old_batch_callback
        tqdm_object.close()



class Parallel(JoblibParallel):
    def __call__(self, iterable):
        if self.n_jobs == 1:
            return [function(*args, **kwargs) for function, args, kwargs in iterable]
        else:
            return super(Parallel, self).__call__(iterable)

def nope_function(task):
    if task == 4:
        raise Exception("Error in parallel job")
    else:
        time.sleep(task)


def main():
    import os

    # Needs to be done before numpy is imported!
    os.environ['OPENBLAS_NUM_THREADS'] = '1'
    os.environ["OMP_NUM_THREADS"] = '1'
    os.environ["MKL_NUM_THREADS"] = '1'
    os.environ["VECLIB_MAXIMUM_THREADS"] = '1'
    os.environ["NUMEXPR_NUM_THREADS"] = '1'

    import torch  # noqa: E402

    torch.set_num_interop_threads(1)


    jobs = [delayed(nope_function)(i) for i in range(8)]
    with tqdm_joblib(tqdm(desc="debug joblib", total=len(jobs))):
        Parallel(n_jobs=8)(jobs)


if __name__ == "__main__":
    main()