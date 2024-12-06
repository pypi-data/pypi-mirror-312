import psutil
import os
from .utils import mebibyte
process = psutil.Process(os.getpid())

DEFAULTTHRESHOLD = 100 * 1024 ** 2 #not using mebibyte() so it is a literal

MINTHRESHOLD = int(process.memory_info().rss) + mebibyte(1)