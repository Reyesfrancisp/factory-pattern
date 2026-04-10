# tests/integration/test_calculation.py
"""
Integration Tests for Polymorphic Calculation Models

These tests verify the polymorphic behavior of the Calculation model hierarchy.
Polymorphism in SQLAlchemy means that different calculation types (Addition,
Subtraction, etc.) can be treated uniformly while maintaining type-specific
behavior.

What Makes These Tests Polymorphic:
1. Factory Pattern: Calculation.create() returns different subclasses
2. Type Resolution: isinstance() checks verify correct subclass instantiation
3. Polymorphic Behavior: Each subclass implements get_result() differently
4. Common Interface: All calculations share the same methods/attributes

These tests demonstrate key OOP principles:
- Inheritance: Subclasses inherit from Calculation
- Polymorphism: Same interface, different implementations
- Encapsulation: Each class encapsulates its calculation logic
"""

import pytest
import uuid

from app.models.calculation import (
    Calculation,
    Addition,
    Subtraction,
    Multiplication,
    Division,
)


# Helper function to create a dummy user_id for testing.
def dummy_user_id():
    """
    Generate a random UUID for testing purposes.
    
    In real tests with a database, you would create an actual user
    and use their ID. This helper is sufficient for unit-level testing
    of the calculation logic without database dependencies.
    """
    return uuid.uuid4()


# ============================================================================
# Tests for Individual Calculation Types
# ============================================================================

def test_addition_get_result():
    """
    Test that Addition.get_result returns the correct sum.
    
    This verifies that the Addition class correctly implements the
    polymorphic get_result() method for its specific operation.
    """
    a, b = 10.5, 5.0
    addition = Addition(user_id=dummy_user_id(), a=a, b=b)
    result = addition.get_result()
    assert result == 15.5, f"Expected 15.5, got {result}"


def test_subtraction_get_result():
    """
    Test that Subtraction.get_result returns the correct difference.
    
    Subtraction performs a - b.
    """
    a, b = 20.0, 5.0
    subtraction = Subtraction(user_id=dummy_user_id(), a=a, b=b)
    result = subtraction.get_result()
    assert result == 15.0, f"Expected 15.0, got {result}"


def test_multiplication_get_result():
    """
    Test that Multiplication.get_result returns the correct product.
    
    Multiplication multiplies a and b.
    """
    a, b = 2.0, 3.0
    multiplication = Multiplication(user_id=dummy_user_id(), a=a, b=b)
    result = multiplication.get_result()
    assert result == 6.0, f"Expected 6.0, got {result}"


def test_division_get_result():
    """
    Test that Division.get_result returns the correct quotient.
    
    Division performs a / b.
    """
    a, b = 100.0, 5.0
    division = Division(user_id=dummy_user_id(), a=a, b=b)
    result = division.get_result()
    assert result == 20.0, f"Expected 20.0, got {result}"


def test_division_by_zero():
    """
    Test that Division.get_result raises ValueError when dividing by zero.
    
    This demonstrates EAFP (Easier to Ask for Forgiveness than Permission):
    We attempt the operation and catch the exception rather than checking
    beforehand.
    """
    a, b = 50.0, 0.0
    division = Division(user_id=dummy_user_id(), a=a, b=b)
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        division.get_result()


# ============================================================================
# Tests for Polymorphic Factory Pattern
# ============================================================================

def test_calculation_factory_addition():
    """
    Test the Calculation.create factory method for addition.
    
    This demonstrates polymorphism: The factory method returns a specific
    subclass (Addition) that can be used through the common Calculation
    interface.
    """
    a, b = 10.0, 5.0
    calc = Calculation.create(
        calculation_type='addition',
        user_id=dummy_user_id(),
        a=a,
        b=b,
    )
    # Verify polymorphism: factory returned the correct subclass
    assert isinstance(calc, Addition), \
        "Factory did not return an Addition instance."
    assert isinstance(calc, Calculation), \
        "Addition should also be an instance of Calculation."
    # Verify behavior: subclass implements get_result() correctly
    assert calc.get_result() == 15.0, "Incorrect addition result."


def test_calculation_factory_subtraction():
    """
    Test the Calculation.create factory method for subtraction.
    """
    a, b = 10.0, 4.0
    calc = Calculation.create(
        calculation_type='subtraction',
        user_id=dummy_user_id(),
        a=a,
        b=b,
    )
    assert isinstance(calc, Subtraction), \
        "Factory did not return a Subtraction instance."
    assert calc.get_result() == 6.0, "Incorrect subtraction result."


def test_calculation_factory_multiplication():
    """
    Test the Calculation.create factory method for multiplication.
    """
    a, b = 3.0, 4.0
    calc = Calculation.create(
        calculation_type='multiplication',
        user_id=dummy_user_id(),
        a=a,
        b=b,
    )
    assert isinstance(calc, Multiplication), \
        "Factory did not return a Multiplication instance."
    assert calc.get_result() == 12.0, "Incorrect multiplication result."


def test_calculation_factory_division():
    """
    Test the Calculation.create factory method for division.
    """
    a, b = 100.0, 5.0
    calc = Calculation.create(
        calculation_type='division',
        user_id=dummy_user_id(),
        a=a,
        b=b,
    )
    assert isinstance(calc, Division), \
        "Factory did not return a Division instance."
    assert calc.get_result() == 20.0, "Incorrect division result."


def test_calculation_factory_invalid_type():
    """
    Test that Calculation.create raises a ValueError for unsupported types.
    """
    with pytest.raises(ValueError, match="Unsupported calculation type"):
        Calculation.create(
            calculation_type='modulus',  # unsupported type
            user_id=dummy_user_id(),
            a=10.0,
            b=3.0,
        )


def test_calculation_factory_case_insensitive():
    """
    Test that the factory is case-insensitive.
    """
    a, b = 5.0, 3.0
    
    # Test various cases
    for calc_type in ['addition', 'Addition', 'ADDITION', 'AdDiTiOn']:
        calc = Calculation.create(
            calculation_type=calc_type,
            user_id=dummy_user_id(),
            a=a,
            b=b,
        )
        assert isinstance(calc, Addition), \
            f"Factory failed for case: {calc_type}"
        assert calc.get_result() == 8.0


# ============================================================================
# Tests Demonstrating Polymorphic Behavior
# ============================================================================

def test_polymorphic_list_of_calculations():
    """
    Test that different calculation types can be stored in the same list.
    
    This demonstrates polymorphism: A list of Calculation objects can contain
    different subclasses, and each maintains its type-specific behavior.
    """
    user_id = dummy_user_id()
    
    # Create a list of different calculation types
    calculations = [
        Calculation.create('addition', user_id, 10.0, 5.0),
        Calculation.create('subtraction', user_id, 10.0, 5.0),
        Calculation.create('multiplication', user_id, 10.0, 5.0),
        Calculation.create('division', user_id, 10.0, 5.0),
    ]
    
    # Each calculation maintains its specific type
    assert isinstance(calculations[0], Addition)
    assert isinstance(calculations[1], Subtraction)
    assert isinstance(calculations[2], Multiplication)
    assert isinstance(calculations[3], Division)
    
    # All calculations share the same interface
    results = [calc.get_result() for calc in calculations]
    
    # Each produces its type-specific result
    assert results == [15.0, 5.0, 50.0, 2.0]


def test_polymorphic_method_calling():
    """
    Test that polymorphic methods work correctly.
    """
    user_id = dummy_user_id()
    a, b = 10.0, 2.0
    
    # Create calculations dynamically based on type string
    calc_types = ['addition', 'subtraction', 'multiplication', 'division']
    expected_results = [12.0, 8.0, 20.0, 5.0]
    
    for calc_type, expected in zip(calc_types, expected_results):
        calc = Calculation.create(calc_type, user_id, a, b)
        # Polymorphic method call: same method name, different behavior
        result = calc.get_result()
        assert result == expected, \
            f"{calc_type} failed: expected {expected}, got {result}"