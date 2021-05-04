from functools import wraps

def memoize(f):
    cache = dict()
    @wraps(f)
    def helper(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]
    return helper