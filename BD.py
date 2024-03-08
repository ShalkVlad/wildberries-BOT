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


# Инициализируйте базу данных
engine = create_engine('postgresql://postgres:2705@localhost:5432/Art')
Base.metadata.create_all(engine)

# Создайте сессию
Session = sessionmaker(bind=engine)
session = Session()


def get_data():
    print("Fetching data from the database...")  # Отладочное сообщение
    data = session.query(RequestHistory).order_by(RequestHistory.request_time.desc()).limit(5).all()
    print("Data from the database:", data)  # Отладочное сообщение
    return [f"User ID: {entry.user_id}, Time: {entry.request_time}, Article: {entry.article}" for entry in data]


# Коммитим изменения (сохраняем запрос в базу данных)
session.commit()

print("Request history saved successfully!")
