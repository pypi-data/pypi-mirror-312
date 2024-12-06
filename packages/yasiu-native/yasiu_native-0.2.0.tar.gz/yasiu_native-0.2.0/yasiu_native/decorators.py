from functools import update_wrapper


def flexible_decorator(decorator):
    """
    Decorator for decorators.
    Turns Single Level decorator into two leveled decorator,
    by passing decoration parameters alongside function signature for ease of use.
    Decorators wrapped with `Flexible` can be used both with `()` and without `()` operator.
    Child decorator receive function signature, decoration parameters and function arguments.
    Supports both positional and key arguments on any level.

    Args:
        decorator - decorator for wrapping

    Returns:
        your decorated decorator: for decorating other functions.

    Warning:
        Do not pass functions as decoration parameter as FIRST positional argument!

        @decor1(sum)
        def funTest():
            "Wrong Decoration will happen!"
            pass

    Example:

          @flexible_decorator
          def yourDecorator(decoratedFunction, *posParam, **keyParam):
            "decoratedFunction: function To be decorated with your decorator."
            "posParam: [Optional] positional argument for customizng your decorator behaviour"
            "keyParam: [Optional] keyword argument for customizng your decorator behaviour"

            def inner(*args, **kwargs):
                "args kwargs: arguments of decorated funciton"
                "Use decorative arguments to modify decorator"

                ret = decoratedFunction(*args, **kwargs)
                return ret
            return inner

    Usage:

        yourDecorator
        def someFunction(a=1, b=2):
            pass

        yourDecorator()
        def someFunction(a=1, b=2):
            pass

        yourDecorator(decorationParam)
        def someFunction(a=1, b=2):
            pass

        yourDecorator(decorationParam=5)
        def someFunction(a=1, b=2):
            pass
    """
    def wrapper(*args, **kw):
        if len(args) == 1:
            "If more arguments, then it is not function reference"
            fun1 = args[0]
        else:
            fun1 = None

        if callable(fun1):
            "Decorated without calling () in decoration"
            "No arguments were used during"
            decorWrapped = update_wrapper(decorator, fun1)
            return decorWrapped(fun1)

        def inner(fun2, ):
            ""
            decorWrapped = update_wrapper(decorator, fun2)
            ret = decorWrapped(fun2, *args, **kw)  # (*a2, **kw2)
            return ret

        return inner

    return wrapper


def flexible_decorator_2d(decorator):
    """
    Decorator for decorators made of 2 function levels.
    Decorators wrapped with `Flexible` can be used both with `()` and without `()` operator.
    Child decorator receive function signature, decoration parameters and function arguments.
    Supports both positional and key arguments on any level.

    Args:
        decorator - decorator for wrapping

    Returns:
        your decorated decorator: for decorating other functions.

    Warning:
        Do not pass functions as decoration parameter as FIRST positional argument!

        @decor1(sum)
        def funTest():
            "Wrong Decoration will happen!"
            pass

    Example:

          @flexible_decorator_2d
          def yourDecorator(*posParam, **keyParam):
            "posParam: [Optional] positional argument for customizng your decorator behaviour"
            "keyParam: [Optional] keyword argument for customizng your decorator behaviour"

            def wrapper(decoratedFunction):
                "decoratedFunction: function To be decorated with your decorator."

                def inner(*args, **kwargs):
                    "args kwargs: arguments of decorated funciton"
                    "Use decorative arguments to modify decorator"

                    ret = decoratedFunction(*args, **kwargs)
                    return ret

                return inner

            return wrapper

    Usage:

        yourDecorator
        def someFunction(a=1, b=2):
            pass

        yourDecorator()
        def someFunction(a=1, b=2):
            pass

        yourDecorator(decorationParam)
        def someFunction(a=1, b=2):
            pass

        yourDecorator(decorationParam=5)
        def someFunction(a=1, b=2):
            pass
    """

    def wrapper(*args, **kw):
        if len(args) == 1:
            fun1 = args[0]
        else:
            fun1 = None

        if callable(fun1):
            "Decorated without calling () in decoration"
            "No arguments were used during"
            decorWrapped = update_wrapper(decorator, fun1)
            return decorWrapped()(fun1)

        def inner(fun2, ):
            decorWrapped = update_wrapper(decorator, fun2)
            ret = decorWrapped(*args, **kw)(fun2)

            return ret

        return inner

    return wrapper


__all__ = ['flexible_decorator', 'flexible_decorator_2d']

if __name__ == "__main__":
    print("\n"*1)

    @flexible_decorator_2d
    def decor1(fun, param=5):
        "DEcor1 Docstring your decor"
        def wrapper(asd):
            def inner(*a, **kw):
                print(f"decor1 called, param:{asd}")
                return fun(*a, **kw)
            return inner
        return wrapper

    @decor1()
    def test1(a, b=2, c=3):
        print(f"a:{a}, b:{b}, c:{c}")

    test1(0, 1, 2)
    test1(10)
