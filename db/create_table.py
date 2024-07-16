from sqlalchemy import create_engine, Column, String, Enum, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from config import host, user, password, db_name, port
import uuid

Base = declarative_base()

class App(Base):
    __tablename__ = 'apps'
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    kind = Column(String(32), nullable=False)
    name = Column(String(128), nullable=False)
    version = Column(String(), nullable=False)  # TODO: regex
    description = Column(Text(4096), nullable=True)
    state = Column(Enum('NEW', 'INSTALLING', 'RUNNING', name='state_enum'), default='NEW', nullable=False)
    json_data = Column(JSON, nullable=False)

if __name__ == "__main__":
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
    Base.metadata.create_all(engine)
