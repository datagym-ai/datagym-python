import sys
from typing import Iterable


def progressbar(it: Iterable, prefix: str = "", size: int = 60):
    count = len(it)

    def show(j: int):
        x = int(size*j/count)
        print("\r%s[%s%s] %i/%i" % (prefix, "#"*x, "."*(size-x), j, count), end='')
        sys.stdout.flush()

    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print("\n")
    sys.stdout.flush()
