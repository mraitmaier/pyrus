"""
This class can be used as decorator (new in python 2.6 & 3.0) to speed up
the recursive functions.
The classic example is very simple Fibonacci number generator:

def fibonacci(n):
    if n in (0, 1): return n
    return fibonacci(n - 1) + fibonacci(n - 2)

It’s clear this is a very inefficient algorithm: the amount of function calls 
increases exponentially for increasing values of n—this is because the function
calls values that it has already calculated again and again. The easy way to 
optimize this would be to cache the values in a dictionary and check to see if 
that value of n has been called previously. If it has, return it’s value in 
the dictionary, if not, proceed to call the function. This is memoization.
There is now a dictionary, self.memoized, that acts as our cache, and a change 
in the exception handling that looks for KeyError, which throws an error if a 
key doesn’t exist in a dictionary. Again, this class is generalized, and will 
work for any recursive function that could benefit from memoization.
New version of the function is now:

@memoize
def fibonacci_memoized(n):
    if n in (0, 1): return n
    return fibonacci_memoized(n - 1) + fibonacci_memoized(n - 2)

Notice how fibonacci_memoized is extremely clean — it’s the exact same function.
We don’t have any extraneous cache = {} calls outside the function, and there
is nothing in the algorithm that detracts from the natural flow of the process. 
The new version with decorator class gives speed improvements of several orders 
of magnitude.

Source: http://avinashv.net/2008/04/python-decorators-syntactic-sugar/
"""
class memoize:
    def __init__(self, function):
        self.function = function
        self.memoized = {}

    def __call__(self, *args):
        try:
             return self.memoized[args]
        except KeyError:
             self.memoized[args] = self.function(*args)
             return self.memoized[args]

