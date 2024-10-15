import contextlib
from typing import Any

import joblib
from joblib import delayed
from joblib import Parallel as JoblibParallel
from tqdm import tqdm
from joblib_zombie import nope_function


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

def main():
    jobs = [delayed(nope_function)(i) for i in range(8)]
    with tqdm_joblib(tqdm(desc="debug joblib", total=len(jobs))):
        Parallel(n_jobs=8)(jobs)


if __name__ == "__main__":
    main()