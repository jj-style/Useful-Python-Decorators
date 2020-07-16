import functools

class Stats:
    """Useful statistics for a function.
    Includes:
        call_count - a counter for the number of times the function is called
        last_returned - stores the last value returned by the function
    """
    def __init__(self, f):
        self.__f = f
        self.call_count = 0
        self.last_returned = None
        functools.update_wrapper(self, f)

    def __call__(self, *args, **kwargs):
        self.call_count += 1
        self.last_returned = self.__f(*args, **kwargs)
        return self.last_returned
    
class Debugger:
    """Returns a debugger decorator.

    Keyword arguments:
        display -- outputs the name, arguments and keyword arguments of a called function (default True)
        catch -- catches exceptions, reports the function it occured in and the message of the exception (default True)
    """
    def __init__(self, display=True, catch=True):
        self.display = display
        self.catch = catch
 
    def __call__(self, f):
        @functools.wraps(f)
        def wrap(*args, **kwargs):
            if self.display:
                pad = 17
                print("-"*pad)
                print(f"{'function':{pad}}: {f.__name__}")
                print(f"{'arguments':{pad}}: {args}")
                print(f"{'keyword arguments':{pad}}: {kwargs}")
                print("-"*pad)
            if self.catch:
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    print(f"EXCEPTION OCCURED IN {f}: {e}")
                    exit()
            else:
                return f(*args, **kwargs)
        return wrap

class Cache:
    """Cache results for a function based on the arguments given."""
    def __init__(self, f):
        self.__f = f
        self._cache = {}
        functools.update_wrapper(self, f)

    def __call__(self, *args, **kwargs):
        if not kwargs:
            if not self._cache.get(args):
                self._cache[args] = self.__f(*args, **kwargs)
            else:
                print(f"cache hit: {self._cache[args]}")
            return self._cache[args]
        return self.__f(*args, **kwargs)

    def empty_cache(self):
        self._cache = {}


def check_non_negative(index, *indices):
    """Returns a non-negative checker for arguments.
    Arguments:
        index - index of argument to check for being non-negative (required)
        indices - indices of arguments to check for being non-negative (optional)
    """
    def validator(f):
        @functools.wraps(f)
        def wrap(*args, **kwargs):
            if args[index] < 0:
                raise ValueError(f"Argument {index} must be non-negative")
            for i in indices:
                if args[i] < 0:
                    raise ValueError(f"Argument {i} must be non-negative")
            return f(*args, **kwargs)
        return wrap
    return validator

def check_type(tiep, index, *indices):
    """Returns a type checker decorator for arguments.
    Arguments:
        tiep - type to check arguments against (required)
        index - index of argument to check for being of the given type (required)
        indices - indices of arguments to check for being of the given type (optional)
    """
    def validator(f):
        @functools.wraps(f)
        def wrap(*args, **kwargs):
            if not isinstance(args[index], tiep):
                raise ValueError(f"Argument {index} must be of type {tiep}")
            for i in indices:
                if not isinstance(args[i], tiep):
                    raise ValueError(f"Argument {i} must be of type {tiep}")
            return f(*args, **kwargs)
        return wrap
    return validator
