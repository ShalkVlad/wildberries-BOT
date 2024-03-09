from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class RequestHistory(Base):
    __tablename__ = 'request_history'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    request_time = Column(DateTime, default=datetime.now(timezone.utc))
    article = Column(String)


engine = create_engine('postgresql://postgres:2705@db:5432/Art')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def get_data():
    print("Fetching data from the database...")
    data = session.query(RequestHistory).order_by(RequestHistory.request_time.desc()).limit(5).all()
    print("Data from the database:", data)
    return [f"User ID: {entry.user_id}, Time: {entry.request_time}, Article: {entry.article}" for entry in data]


session.commit()

print("Request history saved successfully!")
