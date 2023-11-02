# Copyright (c) 2022 Xingchen Song (sxc19@tsinghua.org.cn)
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
import sys

from setuptools import setup, find_packages

version = sys.argv[-1].split('=')[1]
sys.argv = sys.argv[0:len(sys.argv) - 1]

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(
    name="WeTextProcessing",
    version=version,
    author="Zhendong Peng, Xingchen Song",
    author_email="pzd17@tsinghua.org.cn, sxc19@tsinghua.org.cn",
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="WeTextProcessing, including TN & ITN",
    url="https://github.com/wenet-e2e/WeTextProcessing",
    packages=find_packages(),
    package_data={
        "tn": ["*.fst"],
        "itn": ["*.fst"],
    },
    install_requires=['pynini', 'importlib_resources'],
    entry_points={
        "console_scripts": [
            "wetn = tn.main:main",
            "weitn = itn.main:main",
        ]
    },
    tests_require=['pytest'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
