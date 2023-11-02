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

import os


def parse_test_case(file_name):
    file = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + file_name

    delimiter = '=>'
    with open(file) as fin:
        for line in fin:
            assert delimiter in line
            arr = line.strip().split(delimiter)
            assert 0 < len(arr) <= 2

            written = arr[0].strip()
            spoken = ''
            if len(arr) > 1:
                spoken = arr[1].strip()
            yield (written, spoken)
