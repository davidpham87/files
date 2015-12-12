# https://unpythonic.com/02_02_multimethods/

def multi(dispatch_fn):
    def _inner(*args, **kwargs):
        return _inner.__multi__.get(
            dispatch_fn(*args, **kwargs),
            _inner.__multi_default__
        )(*args, **kwargs)

    _inner.__multi__ = {}
    _inner.__multi_default__ = lambda *args, **kwargs: None  # Default default
    return _inner


def multimethod(dispatch_fn=None, dispatch_key=None):
    def apply_decorator(fn):
        if dispatch_key is None:
            # Default case
            dispatch_fn.__multi_default__ = fn
        else:
            dispatch_fn.__multi__[dispatch_key] = fn
        return dispatch_fn
    return apply_decorator


def method(dispatch_type, *args):
    def get_dispatch_type(t, *args, **kwargs):
        return type(t)

    def not_implemented(*args, **kwargs):
        raise Exception("Method not implemented for %s" % get_dispatch_type(*args, **kwargs))

    def _inner(fn):
        dispatch_fn = globals().get(fn.__name__, None)  # Search for existing multimethod
        if dispatch_fn is None or not hasattr(dispatch_fn, '__multi__'):
            dispatch_fn = multi(get_dispatch_type)
            dispatch_fn = multimethod(dispatch_fn)(not_implemented)  # default

        return multimethod(dispatch_fn, dispatch_type)(fn)
    return _inner
