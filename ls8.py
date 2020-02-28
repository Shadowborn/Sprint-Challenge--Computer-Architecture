import sys
from cpu import *

cpu = myCPU()

cpu.load('sctest.ls8')
cpu.run()