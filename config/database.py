from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# File DB:
DATABASE_URL = "sqlite:///../data/pbo.db"
# In-memory DB:
# DATABASE_URL = "sqlite:///:memory:"

# create engine (use check_same_thread=False if you will share across threads, e.g. FastAPI background tasks)
engine = create_engine(
    DATABASE_URL,
    echo=True,  # log SQL for debugging, set False in production
    connect_args={"check_same_thread": False},  # only needed for some multithreaded use-cases
    future=True,  # use SQLAlchemy 2.0 style features
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

# example model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)

session = SessionLocal

# create tables
def init_db():
    Base.metadata.create_all(bind=engine)
