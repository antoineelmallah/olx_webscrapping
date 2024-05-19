from typing import List, Optional
from datetime import datetime
from sqlalchemy import ForeignKey, String, DateTime, Float, Boolean, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class InstantState(Base):

    __tablename__ = 'instant_state'

    id: Mapped[int] = mapped_column(primary_key=True)
    datetime: Mapped[DateTime] = mapped_column(DateTime(timezone=False), default=datetime.now())
    price: Mapped[Float] = mapped_column(Float())
    average_price: Mapped[Float] = mapped_column(Float())
    fipe_price: Mapped[Float] = mapped_column(Float())

    advertisement_id: Mapped[int] = mapped_column(ForeignKey('advertisement.id'))

class Category(Base):

    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(100))

class VehicleType(Base):

    __tablename__ = 'vehicle_type'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(100))

class Model(Base):

    __tablename__ = 'model'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(100))

class Brand(Base):

    __tablename__ = 'brand'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(100))

class Fuel(Base):

    __tablename__ = 'fuel'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(100))

class Gear(Base):

    __tablename__ = 'gear'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(100))

class Steering(Base):

    __tablename__ = 'steering'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(100))

class Color(Base):

    __tablename__ = 'color'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(100))

class Vehicle(Brand):

    __tablename__ = 'vehicle'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(100))
    hp: Mapped[Float] = mapped_column(Float())
    gnv: Mapped[Boolean] = mapped_column(Boolean())
    year: Mapped[int] = mapped_column(Integer())
    mileage: Mapped[Float] = mapped_column(Float())
    doors: Mapped[int] = mapped_column(Integer())

    advertisement_id: Mapped[int] = mapped_column(ForeignKey("advertisement.id"))
    advertisement: Mapped['Advertisement'] = relationship(back_populates="vehicle")

    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("category.id"))
    category: Mapped[Optional['Category']] = relationship(cascade='all')

    model_id: Mapped[Optional[int]] = mapped_column(ForeignKey("model.id"))
    model: Mapped[Optional['Model']] = relationship(cascade='all')

    brand_id: Mapped[Optional[int]] = mapped_column(ForeignKey("brand.id"))
    brand: Mapped[Optional['Brand']] = relationship(cascade='all')

    fuel_id: Mapped[Optional[int]] = mapped_column(ForeignKey("fuel.id"))
    fuel: Mapped[Optional['Fuel']] = relationship(cascade='all')

    gear_id: Mapped[Optional[int]] = mapped_column(ForeignKey("gear.id"))
    gear: Mapped[Optional['Gear']] = relationship(cascade='all')

    color_id: Mapped[Optional[int]] = mapped_column(ForeignKey("color.id"))
    color: Mapped[Optional['Color']] = relationship(cascade='all')

    steering_id: Mapped[Optional[int]] = mapped_column(ForeignKey("steering.id"))
    steering: Mapped[Optional['Steering']] = relationship(cascade='all')

class Advertisement(Base):

    __tablename__ = 'advertisement'

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[int] = mapped_column(Integer())
    creation_date: Mapped[DateTime] = mapped_column(DateTime(timezone=False), default=datetime.now())
    close_date: Mapped[DateTime] = mapped_column(DateTime(timezone=False), nullable=True)
    url: Mapped[str] = mapped_column(String(200))
    zipcode: Mapped[str] = mapped_column(String(8))
    city: Mapped[str] = mapped_column(String(50))
    neighborhood: Mapped[str] = mapped_column(String(50))

    vehicle: Mapped['Vehicle'] = relationship(back_populates='advertisement', cascade='all')

    states: Mapped[List['InstantState']] = relationship(cascade='all, delete-orphan')
