import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import ast
from evalSpice import evalSpice

# Path to the test data folder - end with / 

# Things to be tested
# - Invalid filename: correct message with FileNotFoundError
# - Invalid circuit elements: TypeError with message "Unknown element type"

testparams = [("test_2.ckt", "test_2.exp"), ("test_1.ckt", "test_1.exp"), ("test_1R.ckt", "test_1R.exp")]

def checkdiff(Vout, Iout, expFile):
    """expected outputs are in `expFile`.  Read and compare."""
    with open(expFile) as f:
        data = f.read()
    (Vexp, Iexp) = ast.literal_eval(data)
    s = 0
    for i in Vexp.keys():
        # print(f"Vexp[{i}] = {Vexp[i]}")
        s += abs(Vexp[i] - Vout[i])
    for i in Iexp.keys():
        # print(f"Iexp[{i}][{j}] = {Iexp[i][j]}")
        s += abs(Iexp[i] - Iout[i])
    return s

@pytest.mark.parametrize("inFile, expFile", testparams)
def test_spice(inFile, expFile):
    """Test with various input combinations."""
    (Vout, Iout) = evalSpice(inFile)
    assert checkdiff(Vout, Iout, expFile) <= 0.001
