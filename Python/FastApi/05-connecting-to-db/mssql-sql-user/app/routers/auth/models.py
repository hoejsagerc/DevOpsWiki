# Importing Standard python modules and open import from top-level package
import sys
sys.path.append("...")

# Importing SQLAlchemy Modules
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Importing the Database config
from database import Base # Direct inmport since i have appended top level path

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    username = Column(String(50), unique=True)
    role = Column(String(50))
    hashed_password = Column(String(200))