import datetime
import os
import atexit

from sqlalchemy import DateTime, String, create_engine, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, relationship

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "Tdutybq2020")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "flask_hw")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

PG_DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)

atexit.register(engine.dispose)


class Base(DeclarativeBase):
    pass

# класс для информации о пользователях
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    second_name: Mapped[str] = mapped_column(String(100), nullable=False)
    mail: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    registration_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    ad = relationship("Ad", backref="users")

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "second_name": self.second_name,
            "mail": self.mail,
            "registration_time": self.registration_time.isoformat(),
        }


Base.metadata.create_all(bind=engine)

# класс для объявлений

class Ad(Base):
    __tablename__ = "advertisement"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    registration_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "user_id": self.user_id,
            "registration_time": self.registration_time.isoformat(),
        }


Base.metadata.create_all(bind=engine)
