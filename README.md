# Decorators

A collection of useful decorators to aid Python development and debugging.


## What Is There
* Stats
    * Provides useful statistics for a function including a call count and a last returned value
* Debugger
    * Contains 2 features:
        * displays the name of the function, arguments and keyword arguments passed when the function is called
        * catch exceptions and provide a shorter error message stating the function it occured in
    
    Both options can be turned on and off.
* Cache
    * Caches arguments passed to a function and the return value so next call is faster. Ignores caching if keyword arguments are given. Also provides a method to clear the cache.
* check_non_negative
    * Decorator function to specify 1 or more arguments that should be non-negative. A `ValueError` is raised if any of the arguments are not non-negative. Arguments are specified by their index.
    * example to check arguments 0 and 2 are integers - `@check_non_negative(0, 2)` 
* check_type
    * Decorator function to specify 1 or more arguments that should be a certain type. A `ValueError` is raised if any of the arguments are not of the correct type. Arguments are specified by their index.
    * example to check arguments 0, 3 and 4 are integers - `@check_type(int, 0, 3, 4)` 

# Examples

```python
debugger = Debugger(display=True, catch=True) # this is the default configuration

@Stats
@Cache
@debugger
@check_non_negative(0)
@check_type(int, 0)
def factorial(n):
    """returns the factorial for a number n"""
    return 1 if n == 0 or n == 1 else n * factorial(n-1)

>>> factorial(3)
-----------------
function         : factorial
arguments        : (3,)
keyword arguments: {}
-----------------
-----------------
function         : factorial
arguments        : (2,)
keyword arguments: {}
-----------------
-----------------
function         : factorial
arguments        : (1,)
keyword arguments: {}
-----------------
6

>>> debugger.display=False

>>> factorial(3)
6 # from cache
>>> factorial.last_returned
6
>>> factorial.call_count
4 # (3 times calculating 3! and once for the cache hit)
>>> factorial.clear_cache()
>>> factorial(3)
6
>>> factorial.call_count
7 # ran factorial 3 times as no longer using cached result
>>> factorial(-1)
EXCEPTION OCCURED IN <function factorial at 0x7f262ee97160>: Argument 0 must be non-negative
>>> factorial(5.5)
EXCEPTION OCCURED IN <function factorial at 0x7f262ee97160>: Argument 0 must be of type <class 'int'>
```