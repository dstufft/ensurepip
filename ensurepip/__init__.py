# Copyright 2013 Donald Stufft
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
import contextlib
import os.path
import sys

SETUPTOOLS_WHEEL = "setuptools-1.1.6-py2.py3-none-any.whl"

PIP_WHEEL = "pip-1.5.dev1-py2.py3-none-any.whl"


@contextlib.contextmanager
def _mount_wheel(wheel, modules=None):
    if modules is None:
        modules = []

    # Construct the full path to the wheel file
    wheel_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        wheel,
    )

    try:
        # Append the Wheel to the system path
        sys.path.append(wheel_path)

        # Yield to the body of the context manager
        yield
    finally:
        # Remove the wheel from the sys.path
        sys.path = [p for p in sys.path if p != wheel_path]

        # Remove modules that could have been imported
        for module in modules:
            if module in sys.modules:
                del sys.modules[module]


def version():
    """
    Returns a string specifying the bundled version of pip.
    """
    with _mount_wheel(SETUPTOOLS_WHEEL, ["setuptools", "pkg_resources"]):
        with _mount_wheel(PIP_WHEEL, ["pip"]):
            import pip
            return pip.__version__


def bootstrap(root=None, upgrade=False, user=False, verbosity=0):
    """
    Bootstrap pip into the current Python installation (or the given root
    directory).
    """
