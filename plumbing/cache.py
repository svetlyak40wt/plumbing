# Built-in modules #
import os, time, pickle, inspect

# Internal modules #

# Third party modules #
from decorator import decorator

################################################################################
def property_cached(f):
    """Decorator for properties evaluated only once.
    It can be used to created a cached property like this:

        class Employee(object):
            @property_cached
            def salary(self):
                print "Evaluating..."
                return time.time()
        bob = Employee()
        print bob.salary
        bob.salary = "10000$"
        print bob.salary
    """
    # Called when you access the property #
    def retrieve_from_cache(self):
        if '__cache__' not in self.__dict__: self.__cache__ = {}
        if f.__name__ not in self.__cache__:
            if inspect.isgeneratorfunction(f): result = tuple(f(self))
            else: result = f(self)
            self.__cache__[f.__name__] = result
        return self.__cache__[f.__name__]
    # Called when you set the property #
    def overwrite_cache(self, value):
        if '__cache__' not in self.__dict__: self.__cache__ = {}
        self.__cache__[f.__name__] = value
    # Return a wrapper #
    retrieve_from_cache.__doc__ = f.__doc__
    return property(retrieve_from_cache, overwrite_cache)

################################################################################
def property_pickled(f):
    """Same thing as above but the result will be stored on disk
    The path will be determined by questioning the `p` attribue
    of the class containing the method with the function name."""
    # Called when you access the property #
    def retrieve_from_cache(self):
        # Is it in the cache ? #
        if '__cache__' not in self.__dict__: self.__cache__ = {}
        if f.__name__ in self.__cache__: return self.__cache__[f.__name__]
        # Is it on disk ? #
        path = getattr(self.p, f.func_name)
        if path.exists:
            with open(path) as handle: result = pickle.load(handle)
            self.__cache__[f.__name__] = result
            return result
        # Otherwise let's compute it #
        result = f(self)
        with open(path, 'w') as handle: pickle.dump(result, handle)
        self.__cache__[f.__name__] = result
        return result
    # Called when you set the property #
    def overwrite_cache(self, value):
        path = getattr(self.p, f.func_name)
        if value is None: os.remove(path)
        else: raise Exception("You can't set a pickled property, you can only delete it")
    # Return a wrapper #
    retrieve_from_cache.__doc__ = f.__doc__
    return property(retrieve_from_cache, overwrite_cache)

################################################################################
def expiry_every(seconds=0):
    def memoize_with_expiry(func, *args, **kwargs):
        # Get the cache #
        if not hasattr(func, '__cache__'): func.__cache__ = [(0,0)]
        cache = func.__cache__
        # Check the cache #
        if cache:
            result, timestamp = cache[0]
            age = time.time() - timestamp
            if age < seconds: return result
        # Update the cache #
        result = func(*args, **kwargs)
        cache[0] = (result, time.time())
        # Return #
        return result
    return decorator(memoize_with_expiry)

###############################################################################
class LazyString(object):
    """A string-like object that will only compute its value once when accessed"""
    def __str__(self): return self.value
    def __init__(self, function):
        self._value = None
        self.function = function

    @property
    def value(self):
        if self._value == None: self._value = self.function()
        return self._value