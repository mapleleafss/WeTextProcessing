# Copyright (c) 2022 Zhendong Peng (pzd17@tsinghua.org.cn)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from tn.chinese.rules.fraction import Fraction
from tn.chinese.test.utils import parse_test_case


class TestFraction:

    fraction = Fraction()
    fraction_cases = parse_test_case('data/fraction.txt')

    @pytest.mark.parametrize("written, spoken", fraction_cases)
    def test_fraction(self, written, spoken):
        assert self.fraction.normalize(written) == spoken
