import pytest
import numpy as np
import typing as typ
from cdfcProject import __discretization, __getPermutation, __formatForSciKit, __flattenTrainingData

# TODO add test case for __transform()
# TODO add test case for __mapToInstance()
# TODO add test case for __dealToBuckets()
# TODO add test case for __buildAccuracyFrame()
# TODO add test case for __accuracyFrameToLatex()


def test_discretization() -> None:
    # * This test checks that the discrete function we are using has the expected outcomes
    # the values should become           -1   -1   1   1    0     0   0  1  -1
    actual = __discretization(np.array((-10, -5.7, 2, 9.5, 0.5, -0.5, 0, 1, -1)))
    expected = np.array((-1, -1, 1, 1, 0, 0, 0, 1, -1))
    assert np.array_equal(actual, expected)


# * These tests will check that the permutation that happens in __getPermutation() doesn't change based on the
# * data type of the array of arrays. The __getPermutation function takes an array of instances, which will all
# * be in the same class, and reorders them (randomly in production, but using seed 498 during testing). This
# * random ordering will then be looped over sequentially in order to fill (or "deal") to our buckets.
# * Essentially this is the function that introduces randomness into our K-Fold Validation.
# * Notes:
# * > we are using seed 498. This will create a default_rng that when given a list of 3 items, it will move the
# *   1st item to the last position. So:
# *   [[1, 2, 3], [4, 5, 6], [7, 8, 9]]  ---becomes-->  [[4, 5, 6], [7, 8, 9], [1, 2, 3]]
# *   [[a, b, c], [d, e, f], [g, h, i]]  ---becomes-->  [[d, e, f], [g, h, i], [a, b, c]]

# ******************************* Testing Data for getPermutation() ******************************* #
discreteOriginal = [[1, 1, 0], [0, -1, 1], [0, 0, -1]]
discretePermutation = [[0, -1, 1], [0, 0, -1], [1, 1, 0]]

intOriginal = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
intPermute = [[4, 5, 6], [7, 8, 9], [1, 2, 3]]

floatOriginal = [[1.5, 2.6, 3.1], [4.001, 5.778, 6.345], [7.001, 8.123, 9.912]]
floatPermute = [[4.001, 5.778, 6.345], [7.001, 8.123, 9.912], [1.5, 2.6, 3.1]]

negIntOriginal = [[-1, -2, -3], [-4, -5, -6], [-7, -8, -9]]
negIntPermutation = [[-4, -5, -6], [-7, -8, -9], [-1, -2, -3]]

negFloatOriginal = [[-1.5, -2.6, -3.1], [-4.001, -5.778, -6.345], [-7.001, -8.123, -9.912]]
negFloatPermutation = [[-4.001, -5.778, -6.345], [-7.001, -8.123, -9.912], [-1.5, -2.6, -3.1]]

mixedPosNegIntOriginal = [[1, 2, 3], [-4, 5, -6], [-7, -8, -9]]
mixedPosNegIntPermutation = [[-4, 5, -6], [-7, -8, -9], [1, 2, 3]]

mixedAllOriginal = [[-1.5, 2.6, -3.1], [4.001, 5, 6], [-7.001, -8, -9.912]]
mixedAllPermutation = [[4.001, 5, 6], [-7.001, -8, -9.912], [-1.5, 2.6, -3.1]]

permuteType = typ.Union[typ.List[typ.List[int]], typ.List[typ.List[float]]]
# ***************************** End Testing Data for getPermutation() ***************************** #


@pytest.mark.parametrize("originalValue, permutation", [
    (discreteOriginal, discretePermutation),              # discrete test
    (intOriginal, intPermute),                            # int test
    (floatOriginal, floatPermute),                        # float test
    (negIntOriginal, negIntPermutation),                  # negative int test
    (negFloatOriginal, negFloatPermutation),              # negative float test
    (mixedPosNegIntOriginal, mixedPosNegIntPermutation),  # positive & negative int test
    (mixedAllOriginal, mixedAllPermutation),                 # positive, negative, int, & float test
])
def test_getPermutation(originalValue: permuteType, permutation: permuteType) -> None:
    actualValue = __getPermutation(originalValue, 498)
    assert np.array_equal(actualValue, permutation)


# * Setup Data Used to Test formatForSciKit() * #
# use strings for clarity. The data type inside shouldn't matter
data = np.array([['class1', 'feature1', 'feature2', 'feature3'],   # instance 1
                 ['class2', 'feature1', 'feature2', 'feature3'],   # instance 2
                 ['class3', 'feature1', 'feature2', 'feature3']])  # instance 3


def test__formatForSciKitLabels() -> None:
    exLabels = np.array(['class1', 'class2', 'class3'])  # setup expected data
    ftrs, labels = __formatForSciKit(data)               # make the function call
    assert np.array_equal(labels, exLabels)


def test_formatForSciKitFeatures() -> None:
    # setup expected data values
    exFeatures = np.array([['feature1', 'feature2', 'feature3'],   # instance 1
                           ['feature1', 'feature2', 'feature3'],   # instance 2
                           ['feature1', 'feature2', 'feature3']])  # instance 3
    ftrs, labels = __formatForSciKit(data)
    assert np.array_equal(ftrs, exFeatures)


def test_flattenTrainingData() -> None:
    # setup expected data values
    trainIn = [[np.array('instance1'), np.array('instance2'), np.array('instance3')],  # This should be a list of buckets
               [np.array('instance4'), np.array('instance5'), np.array('instance6')],  # with the instances inside
               [np.array('instance7'), np.array('instance8'), np.array('instance9'), np.array('instance10')]]

    trainExp = np.array(['instance1', 'instance2', 'instance3',                 # This should be the list
                         'instance4', 'instance5', 'instance6',                 # of instances with the
                         'instance7', 'instance8', 'instance9', 'instance10'])  # buckets removed
    trainOut = __flattenTrainingData(trainIn)
    assert np.array_equal(trainOut, trainExp)

