"""
Unit and regression test for the geometry_analysis package.
"""

# Import package, test suite, and other packages as needed
import geometry_analysis
import pytest
import sys

import numpy as np

## Define a "fixture" -- something that you'll call on for multiple tests
@pytest.fixture()
def water_molecule():
    name = "water"
    symbols = ["H", "O", "H"]
    coordinates = np.array([[2, 0, 0], [0, 0, 0], [-2, 0, 0]])

    water = geometry_analysis.Molecule(name, symbols, coordinates)

    return water

def test_create_failure():
    name = 25
    symbols = ["H", "O", "H"]
    coordinates = np.zeros([3, 3])

    ## Intentional fail becaause name isn't string
    with pytest.raises(TypeError):
        water = geometry_analysis.Molecule(name, symbols, coordinates)

def test_molecule_set_coordinates(water_molecule):
    """Test that the bond list is rebuilt when we reset coordinates."""

    ## Practically, we should have a test for this first...
    num_bonds = len(water_molecule.bonds)

    assert num_bonds == 2

    new_coordinates = np.array([[5, 0, 0], [0, 0, 0], [-2, 0, 0]])

    water_molecule.coordinates = new_coordinates

    new_bonds = len(water_molecule.bonds)

    assert new_bonds == 1
    assert np.array_equal(new_coordinates, water_molecule.coordinates)


def test_geometry_analysis_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "geometry_analysis" in sys.modules

def test_calculate_distance():
    """Test the calculate_distance function"""

    r1 = np.array([0, 0, -1])
    r2 = np.array([0, 1, 0])

    expected_distance = np.sqrt(2.) #PASS
    # expected_distance = np.sqrt(23) # FAIL

    calculated_distance = geometry_analysis.calculate_distance(r1, r2)

    assert expected_distance == calculated_distance

## Long form, without decorators
# def test_calculate_angle_90():
#     """Test the calculate_angle function"""
#
#     r1 = np.array([1, 0, 0])
#     r2 = np.array([0, 0, 0])
#     r3 = np.array([0, 1, 0])
#
#     expected_value = 90 #PASS
#     # expected_value = 180 # FAIL
#
#    calculated_value= geometry_analysis.calculate_angle(r1, r2, r3,
#     degrees=True)
#
#     assert expected_value == calculated_value
#
# def test_calculate_angle_180():
#     """Test a second value of the calculate_angle function"""
#
#     r1 = np.array([0, 0, -2])
#     r2 = np.array([0, 0, 0])
#     r3 = np.array([0, 0, 2])
#
#     expected_value = 180 #PASS
#     # expected_value = 90 # FAIL
#
#     calculated_value = geometry_analysis.calculate_angle(r1, r2, r3,
#      degrees=True)
#
#     assert expected_value == calculated_value
#
# def test_calculate_angle_60():
#     """Test another value of the calculate_angle function"""
#
#     r1 = np.array([0, 0, -1])
#     r2 = np.array([0, 1, 0])
#     r3 = np.array([1, 0, 0])
#
#     expected_value = 60 #PASS
#     # expected_value = 90 # FAIL
#
#     calculated_value = geometry_analysis.calculate_angle(r1, r2, r3,
#      degrees=True)
#
#     # Want something to evalue to True if they're close and false if not
#     # Has a default tolerence you can screw with
#     assert np.isclose(expected_value, calculated_value)


## p1 and p2 are variables. Start by designing test cases.
@pytest.mark.parametrize("p1, p2, p3, expected_angle", [
    ## First set of 3 points, making 90 degrees
    (np.array([1, 0, 0]), np.array([0, 0, 0]), np.array([0, 1, 0]), 90),
    (np.array([0, 0, -1]), np.array([0, 1, 0]), np.array([1, 0, 0]), 60),
    (np.array([0, 0, -2]), np.array([0, 0, 0]), np.array([0, 0, 2]), 180),
    ## Let's test intentional FAILS
    # (np.array([1, 0, 0]), np.array([0, 0, 0]), np.array([0, 1, 0]), 180),
    # (np.array([0, 0, -1]), np.array([0, 1, 0]), np.array([1, 0, 0]), 90),
    # (np.array([0, 0, -2]), np.array([0, 0, 0]), np.array([0, 0, 2]), 60),
])

## Create function and pass everything you passed to the decorator
def test_calculate_angle(p1, p2, p3, expected_angle):

    calculated_angle = geometry_analysis.calculate_angle(p1, p2, p3,
     degrees=True)

    assert np.isclose(expected_angle, calculated_angle)


@pytest.mark.parametrize("p1, p2, p3, expected_angle", [
## Let's test intentional FAILS
(np.array([1, 0, 0]), np.array([0, 0, 0]), np.array([0, 1, 0]), 180),
(np.array([0, 0, -1]), np.array([0, 1, 0]), np.array([1, 0, 0]), 90),
(np.array([0, 0, -2]), np.array([0, 0, 0]), np.array([0, 0, 2]), 60),
])
def test_calculate_angle_fail(p1, p2, p3, expected_angle):

    calculated_angle = geometry_analysis.calculate_angle(p1, p2, p3,
     degrees=True)

    ## Test that this failure returns a failure
    if np.isclose(expected_angle, calculated_angle) == True:
        fail = False
    else:
        fail = True
    ## needs to fail, True is a failure
    assert fail == True
