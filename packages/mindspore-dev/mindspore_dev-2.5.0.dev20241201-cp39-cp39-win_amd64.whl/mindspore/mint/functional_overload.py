# Copyright 2024 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Holding mint APIs"""
from mindspore._c_expression import ClampFunctional_
from mindspore._c_expression import DivFunctional_
from mindspore._c_expression import FmodFunctional_
from mindspore._c_expression import RemainderFunctional_
from mindspore._c_expression import RepeatInterleaveFunctional_
from mindspore._c_expression import SplitFunctional_

_clamp = ClampFunctional_()
_clip = ClampFunctional_()
_div = DivFunctional_()
_divide = DivFunctional_()
_fmod = FmodFunctional_()
_remainder = RemainderFunctional_()
_repeat_interleave = RepeatInterleaveFunctional_()
_split = SplitFunctional_()


def clamp(*args, **kwargs):
    return _clamp(*args, **kwargs)


def clip(*args, **kwargs):
    return _clip(*args, **kwargs)


def div(*args, **kwargs):
    return _div(*args, **kwargs)


def divide(*args, **kwargs):
    return _divide(*args, **kwargs)


def fmod(*args, **kwargs):
    return _fmod(*args, **kwargs)


def remainder(*args, **kwargs):
    return _remainder(*args, **kwargs)


def repeat_interleave(*args, **kwargs):
    return _repeat_interleave(*args, **kwargs)


def split(*args, **kwargs):
    return _split(*args, **kwargs)

__all__ = [
    "clamp",
    "clip",
    "div",
    "divide",
    "fmod",
    "remainder",
    "repeat_interleave",
    "split",
]
