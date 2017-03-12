# -*- coding: utf-8 -*-
# Copyright 2016-2017 Ionuț Arțăriși <ionut@artarisi.eu>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from functools import wraps

from undecorated import undecorated


# this marker will be appended to the return value of functions using
# the `decorate` decorator
DECORATE_MARKER = (object(), )


def decorate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # 'd' is a marker to make it easy to assert that the wrapper was
        # run
        return f(*args, **kwargs) + DECORATE_MARKER
    return wrapper


def decorate_with_params(*d_args, **d_kwargs):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs) + d_args + tuple(d_kwargs.items())
        return wrapper
    return decorator


def f(a, b=2):
    return ('original', )


def test_simple_undecorate():
    # given our original function f, decorated with a simple decorator
    decorated = decorate(f)

    # which appends a marker to the return value of our original function
    assert decorated(None) == f(None) + DECORATE_MARKER
    assert decorated(None, 3) == f(None, 3) + DECORATE_MARKER

    # when calling udnecorated on the decorated function
    # then the returned function will be and behave like the original
    # function f
    assert undecorated(decorated) is f
    assert undecorated(decorated)(None) == f(None)


def test_with_params():
    # given a sample function `f` decorated with some arbitrary params
    test_args = 'a'
    test_kwargs = {'kwarg1': 'b'}
    decorated = decorate_with_params(*test_args, **test_kwargs)(f)

    # which will change its return value (appending our arbitrary params)
    assert (
        decorated(1, 2) ==
        f(1, 2) + (test_args, ) + tuple(test_kwargs.items()))

    # when we undecorate the function

    # then the returned function will be and behave like the original
    # function f
    assert undecorated(decorated) is f
    assert undecorated(decorated)(None) == f(None)


def test_thrice_decorated():
    # given a sample function f, decorated thrice:
    # with an decorator which takes 1 as a parameter
    decorated = decorate_with_params(1)(f)
    # with our normal test decorator
    decorated = decorate(decorated)
    # and with another decorator which takes 1 as a parameter
    decorated = decorate_with_params(2)(decorated)

    # this will append one element to the return value of f for each of
    # the decorators called
    assert decorated(0, 0) == f(0, 0) + (1, ) + DECORATE_MARKER + (2, )

    # when we undecorate the function

    # then the returned function will be and behave like the original
    # function f
    assert undecorated(decorated) is f
    assert undecorated(decorated)(None) == f(None)


def test_params_to_decorator_are_functions():
    # given a sample function f, decorated with a decorator which
    # accepts functions as parameter
    def foo():
        pass

    decorate_params = (foo, foo)
    decorated = decorate_with_params(*decorate_params)(f)

    # and which causes the decorated function to append the parameters
    # to the decorator to the return value of the decorated function
    assert decorated(0) == f(0) + (foo, foo)

    # when we undecorate the function
    # then the returned function will be and behave like the original
    # function f
    assert undecorated(decorated) is f
    assert undecorated(decorated)(None) == f(None)


def test_decorator_without_wraps():
    # given a sample function f, decorated with a decorator which does
    # not use the functools.wraps function
    def lame_decorator(f):
        def decorator(*args, **kwargs):
            return f(*args, **kwargs) + DECORATE_MARKER
        return decorator

    decorated = lame_decorator(f)

    # and which appends a marker to the return value of its decorated
    # function
    assert decorated(0) == f(0) + DECORATE_MARKER

    # when we undecorate the function
    # then the returned function will be and behave like the original
    # function f
    assert undecorated(decorated) is f
    assert undecorated(decorated)(None) == f(None)


def test_infinite_recursion():
    def recursive_decorator(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            decorator.foo()
            return f(*args, **kwargs)

        decorator.foo = lambda: None

        return decorator

    decorated = recursive_decorator(f)

    assert decorated(None) == ('original', )
    assert undecorated(decorated) is f
    assert undecorated(decorated)(None) == ('original', )


def test_simple_method():
    # given a sample class method A.foo
    class A(object):
        def foo(self, a, b):
            return a, b

    # which is decorated with our test decorator
    decorated = decorate(A.foo)

    # and which appends the parameters to the return value of its
    # decorated function
    assert decorated(A(), 1, 2) == A().foo(1, 2) + DECORATE_MARKER

    # when we undecorate the method
    # then the returned method will be the same and behave like the
    # original method
    assert undecorated(decorated) == A.foo
    assert undecorated(decorated)(A(), 1, 2) == (1, 2)


def test_not_decorated():
    # given a function which is not decorated
    def foo(self, a, b):
        return a, b

    # when calling undecorated on it
    # then the result will be the original function f
    assert undecorated(foo) is foo


def test_class_decorator():
    # given a sample class
    class A(object):
        decorated = False

    # and a class decorator
    def decorate(cls):
        def dec():
            ins = cls()
            ins.decorated = True
            return ins
        return dec

    decorated = decorate(A)

    # which changes the class's `decorated` class variable to True
    assert decorated().decorated is True

    # when calling undecorated on the decorated class
    # then the returned class will be and behave like the original class A
    assert undecorated(decorated) is A
    assert undecorated(decorated)().decorated is False
