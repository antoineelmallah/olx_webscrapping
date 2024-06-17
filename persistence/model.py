from typing import List, Optional
from datetime import datetime
from sqlalchemy import ForeignKey, String, DateTime, Float, Boolean, Integer, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class InstantState(Base):

    __tablename__ = 'instant_state'

    id: Mapped[int] = mapped_column(primary_key=True)
    datetime: Mapped[DateTime] = mapped_column(DateTime(timezone=False), default=datetime.now())
    price: Mapped[Float] = mapped_column(Float())

    advertisement_id: Mapped[int] = mapped_column(ForeignKey('advertisement.id'))

    def __eq__(self, value: object) -> bool:
        if not value:
            return False
        if type(value) != type(self):
            return False
        if self.price != value.price:
            return False
        return True

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

vehicle_accessory = Table(
    'vehicle_accessory',
    Base.metadata,
    Column('vehicle_id', ForeignKey('vehicle.id')),
    Column('accessory_id', ForeignKey('accessory.id'))
)

class Vehicle(Base):

    __tablename__ = 'vehicle'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(100))
    hp: Mapped[Float] = mapped_column(Float(), nullable=True)
    gnv: Mapped[Boolean] = mapped_column(Boolean(), default=False)
    year: Mapped[int] = mapped_column(Integer())
    mileage: Mapped[Float] = mapped_column(Float())
    doors: Mapped[int] = mapped_column(Integer(), nullable=True)
    average_price: Mapped[int] = mapped_column(Integer(), nullable=True)
    fipe_price: Mapped[int] = mapped_column(Integer(), nullable=True)

    advertisement_id: Mapped[int] = mapped_column(ForeignKey("advertisement.id"))
    advertisement: Mapped['Advertisement'] = relationship(back_populates="vehicle")

    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("category.id"))
    category: Mapped[Optional['Category']] = relationship(cascade='all')

    model_id: Mapped[Optional[int]] = mapped_column(ForeignKey("model.id"))
    model: Mapped[Optional['Model']] = relationship(cascade='all')

    brand_id: Mapped[Optional[int]] = mapped_column(ForeignKey("brand.id"))
    brand: Mapped[Optional['Brand']] = relationship(cascade='all')

    vehicle_type_id: Mapped[Optional[int]] = mapped_column(ForeignKey("vehicle_type.id"))
    vehicle_type: Mapped[Optional['VehicleType']] = relationship(cascade='all')

    fuel_id: Mapped[Optional[int]] = mapped_column(ForeignKey("fuel.id"))
    fuel: Mapped[Optional['Fuel']] = relationship(cascade='all')

    gear_id: Mapped[Optional[int]] = mapped_column(ForeignKey("gear.id"))
    gear: Mapped[Optional['Gear']] = relationship(cascade='all')

    color_id: Mapped[Optional[int]] = mapped_column(ForeignKey("color.id"))
    color: Mapped[Optional['Color']] = relationship(cascade='all')

    steering_id: Mapped[Optional[int]] = mapped_column(ForeignKey("steering.id"))
    steering: Mapped[Optional['Steering']] = relationship(cascade='all')

    accessories: Mapped[List['Accessory']] = relationship(secondary=vehicle_accessory, cascade='all')

class Accessory(Base):

    __tablename__ = 'accessory'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(100))

    def __eq__(self, value: object) -> bool:
        if not value:
            return False
        if type(value) != type(self):
            return False
        return self.description == value.description


class Advertisement(Base):

    __tablename__ = 'advertisement'

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(15))
    creation_date: Mapped[DateTime] = mapped_column(DateTime(timezone=False), default=datetime.now())
    last_update_date: Mapped[DateTime] = mapped_column(DateTime(timezone=False), default=datetime.now())
    close_date: Mapped[DateTime] = mapped_column(DateTime(timezone=False), nullable=True)
    url: Mapped[str] = mapped_column(String(200))
    zipcode: Mapped[str] = mapped_column(String(8))
    city: Mapped[str] = mapped_column(String(50))
    neighborhood: Mapped[str] = mapped_column(String(50))
    lat: Mapped[Float] = mapped_column(Float(), nullable=True)
    lon: Mapped[Float] = mapped_column(Float(), nullable=True)

    vehicle: Mapped['Vehicle'] = relationship(back_populates='advertisement', cascade='all')

    states: Mapped[List['InstantState']] = relationship(cascade='all, delete-orphan')

    def current_state(self):
        if not self.states:
            return None
        dates = [ it.datetime for it in self.states if it.datetime ]
        if not dates:
            return None
        return list(filter(lambda it : it.datetime == max(dates), self.states))[0]
