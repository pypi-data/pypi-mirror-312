

class Proxy(object):
    __slots__ = ['_obj', '__weakref__']

    def __init__(self, obj):
        object.__setattr__(self, '_obj', obj)

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            return getattr(object.__getattribute__(self, '_obj'), name)

    @property
    def _origin(self):
        return object.__getattribute__(self, '_obj')

    def set(self, name, value):
        object.__setattr__(self, name, value)

    def get(self, name):
        return object.__getattribute__(self, name)

    def __delattr__(self, name):
        delattr(object.__getattribute__(self, '_obj'), name)

    def __setattr__(self, name, value):
        setattr(object.__getattribute__(self, '_obj'), name, value)

    def __enter__(self):
        return object.__getattribute__(self, '_obj').__enter__()

    def __exit__(self, *args, **kwargs):
        return object.__getattribute__(self, '_obj').__exit__(*args, **kwargs)

    def __nonzero__(self):
        return bool(object.__getattribute__(self, '_obj'))

    def __str__(self):
        return str(object.__getattribute__(self, '_obj'))

    def __repr__(self):
        return repr(object.__getattribute__(self, '_obj'))

    _special_names = [
        '__abs__', '__add__', '__and__', '__call__', '__cmp__', '__coerce__',
        '__contains__', '__delitem__', '__delslice__', '__div__', '__divmod__',
        '__eq__', '__float__', '__floordiv__', '__ge__', '__getitem__',
        '__getslice__', '__gt__', '__hash__', '__hex__', '__iadd__', '__iand__',
        '__idiv__', '__idivmod__', '__ifloordiv__', '__ilshift__', '__imod__',
        '__imul__', '__int__', '__invert__', '__ior__', '__ipow__',
        '__irshift__',
        '__isub__', '__iter__', '__itruediv__', '__ixor__', '__le__', '__len__',
        '__long__', '__lshift__', '__lt__', '__mod__', '__mul__', '__ne__',
        '__neg__', '__oct__', '__or__', '__pos__', '__pow__', '__radd__',
        '__rand__', '__rdiv__', '__rdivmod__', '__reduce__', '__reduce_ex__',
        '__repr__', '__reversed__', '__rfloorfiv__', '__rlshift__', '__rmod__',
        '__rmul__', '__ror__', '__rpow__', '__rrshift__', '__rshift__',
        '__rsub__',
        '__rtruediv__', '__rxor__', '__setitem__', '__setslice__', '__sub__',
        '__truediv__', '__xor__', 'next',
    ]

    @classmethod
    def _create_class_proxy(cls, the_class):

        def make_method(method_name):
            def method(self, *args, **kw):
                return getattr(object.__getattribute__(self, '_obj'), method_name)(*args, **kw)

            return method

        namespace = {}

        for name in cls._special_names:
            if hasattr(the_class, name):
                namespace[name] = make_method(name)

        return type("%s(%s)" % (cls.__name__, the_class.__name__), (cls,), namespace)

    def __new__(cls, obj, *args, **kwargs):
        try:
            cache = cls.__dict__['_class_proxy_cache']
        except KeyError:
            cls._class_proxy_cache = cache = {}
        try:
            the_class = cache[obj.__class__]
        except KeyError:
            cache[obj.__class__] = the_class = cls._create_class_proxy(obj.__class__)
        ins = object.__new__(the_class)
        the_class.__init__(ins, obj, *args, **kwargs)

        return ins
