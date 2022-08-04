import os
import time
from math import sqrt

from joblib import delayed, Parallel
import joblib

def slow_power(x, p):
    return x ** p

start = time.time()
nums =  [slow_power(i, 5) for i in range(10000)]
print( time.time() - start )

number_of_cpu = joblib.cpu_count()

print( number_of_cpu )

delayed_funcs = [delayed(slow_power)(i, 5) for i in range(1000)]
parallel_pool = Parallel(n_jobs=number_of_cpu)

start = time.time()
parallel_pool(delayed_funcs)
print( time.time() - start )




