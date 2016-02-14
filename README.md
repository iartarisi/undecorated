# undecorated

This library provides an easy way to strip a function of its decorators.


## Installation

```
$ pip install undecorated
```


## Example

```python
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
```

## License

# Copyright 2016 Ionuț Arțăriși <ionut@artarisi.eu>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
