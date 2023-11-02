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

import argparse

# TODO(pzd17): multi-language support
from tn.chinese.normalizer import Normalizer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--text', help='input string')
    parser.add_argument('--file', help='input file path')
    parser.add_argument('--cache_dir', type=str,
                        default=None,
                        help='cache dir containing *.fst')
    parser.add_argument('--overwrite_cache', action='store_true',
                        help='rebuild *.fst')
    args = parser.parse_args()

    normalizer = Normalizer(cache_dir=args.cache_dir,
                            overwrite_cache=args.overwrite_cache)

    if args.text:
        print(normalizer.tag(args.text))
        print(normalizer.normalize(args.text))
    elif args.file:
        with open(args.file) as fin:
            for line in fin:
                print(normalizer.tag(line.strip()))
                print(normalizer.normalize(line.strip()))


if __name__ == '__main__':
    main()
