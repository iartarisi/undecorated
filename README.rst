undecorated
-----------

This library provides an easy way to strip a function of its decorators.

Tested on python 2.6 up to 3.6: |travis|


.. |travis| image:: https://travis-ci.org/mapleoin/undecorated.svg?branch=master
    :target: https://travis-ci.org/mapleoin/undecorated


Quickstart
``````````

Install:

.. code:: bash

    $ pip install undecorated

Try it on one of your functions:

.. code:: python

   >>> from undecorated import undecorated
   >>> undecorated(my_decorated_function)
   <function my_decorated_function at 0x7fbdd6e95938>

`undecorated` has returned your original function clean of any decorators.


It also works with class decorators!


Example
```````

.. code:: python

    >>> from functools import wraps
    >>> from undecorated import undecorated
    >>>
    >>> def decorate_with(*decorations):
    ...     def decorator(f):
    ...         @wraps(f)
    ...         def wrapper(*args, **kwargs):
    ...             print decorations
    ...             return f(*args, **kwargs)
    ...         return wrapper
    ...     return decorator
    ... 
    >>> @decorate_with('yellow_bauble')
    ... @decorate_with('red_bauble')
    ... @decorate_with('tinsel')
    ... def tree():
    ...     print 'tree'
    ... 
    >>> tree()
    ('yellow_bauble',)
    ('red_bauble',)
    ('tinsel',)
    tree
    >>> undecorated(tree)()
    tree


Project
```````

This project uses `Semantic Versioning <http://semver.org>`.


License
```````

Copyright 2016 Ionuț Arțăriși <ionut@artarisi.eu>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
