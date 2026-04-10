# tests/integration/test_calculation_db.py
"""
Database Integration Tests

These tests verify that the SQLAlchemy models correctly map to the database,
and that records can be successfully inserted, retrieved, and interact with 
the polymorphic factory pattern.
"""

import pytest
from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app.models.user import User
from app.models.calculation import Calculation, Addition

@pytest.fixture(scope="module")
def db_session():
    """
    Fixture that creates the database schema before testing and 
    drops it after testing is complete.
    """
    # Create all tables in the test database
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    # Clean up after tests
    Base.metadata.drop_all(bind=engine)

def test_insert_calculation_record(db_session: Session):
    """
    Integration test to confirm the database stores correct data.
    """
    # 1. Create a dummy user to satisfy the foreign key constraint
    user = User(username="testuser_db", email="test_db@example.com")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # 2. Insert a calculation using the Factory pattern
    calc = Calculation.create(
        calculation_type="addition",
        user_id=user.id,
        a=10.5,
        b=5.0
    )
    db_session.add(calc)
    db_session.commit()
    db_session.refresh(calc)

    # 3. Query the database to confirm it was stored correctly
    saved_calc = db_session.query(Calculation).filter(Calculation.id == calc.id).first()
    
    # Assertions
    assert saved_calc is not None
    assert saved_calc.type == "addition"
    assert saved_calc.a == 10.5
    assert saved_calc.b == 5.0
    
    # Verify Polymorphic behavior persisted after retrieval
    assert isinstance(saved_calc, Addition)
    assert saved_calc.get_result() == 15.5