import sys
sys.path.append("../Basic Functions")
from LoadData import LoadDataAndLabel
import numpy
from Tree import *

if __name__ == '__main__':
    dataArray, resultList = LoadDataAndLabel("Dataset2.txt")