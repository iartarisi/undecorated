# -*- coding: utf-8 -*-
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

"""Return a function with any decorators removed """


def undecorated(f):
    try:
        f.func_closure
    except AttributeError:
        return

    if f.func_closure:
        for cell in f.func_closure:
            # avoid infinite recursion
            if cell.cell_contents is f:
                continue

            undecd = undecorated(cell.cell_contents)
            if undecd:
                return undecd
    else:
        return f
