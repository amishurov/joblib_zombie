from joblib import delayed
import time
from joblib import Parallel as JoblibParallel



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
    jobs = [delayed(nope_function)(i) for i in range(8)]
    Parallel(n_jobs=8)(jobs)


if __name__ == "__main__":
    main()