import os
import sys


def test_show_import_path():
    print("\nCurrent working directory:")
    print(os.getcwd())

    print("\nPython executable:")
    print(sys.executable)

    print("\nPython import path:")
    for path in sys.path:
        print(repr(path))