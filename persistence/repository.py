from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, joinedload
from persistence.model import Base, Advertisement, Category, VehicleType, Model, Brand, Fuel, Gear, Steering, Color

connection_string = 'mariadb+mariadbconnector://admin:698400@127.0.0.1:3306/olx'

engine = create_engine(connection_string, echo=True)

def persist(model):
    with Session(engine) as session:
        session.add(model)
        session.commit()

def find_domain_or_new(description, model_class: Base):
    with Session(engine) as session:
        stmt = select(model_class).where(model_class.description == description)
        result = session.scalar(stmt)
        return model_class(description=description) if not result else result

def find_advertisement_by_code(code: str) -> Advertisement:
    with Session(engine) as session:
        stmt = select(Advertisement)\
            .options(joinedload(Advertisement.states))\
            .where(Advertisement.code == code)
        return session.scalar(stmt)
    
def persist_advertisement(adv: Advertisement):
    with Session(engine) as session:
        adv_from_db = find_advertisement_by_code(adv.code)
        if adv_from_db:
            if adv.states and adv.states[0] not in adv_from_db.states:
                adv_from_db.states.append(adv.states[0])
                persist(adv_from_db)
        else:
            vehicle = adv.vehicle
            vehicle.category = find_domain_or_new(vehicle.category.description, Category)
            vehicle.vehicle_type = find_domain_or_new(vehicle.vehicle_type.description, VehicleType)
            vehicle.model = find_domain_or_new(vehicle.model.description, Model)
            vehicle.brand = find_domain_or_new(vehicle.brand.description, Brand)
            vehicle.fuel = find_domain_or_new(vehicle.fuel.description, Fuel)
            vehicle.gear = find_domain_or_new(vehicle.gear.description, Gear)
            vehicle.steering = find_domain_or_new(vehicle.steering.description, Steering)
            vehicle.color = find_domain_or_new(vehicle.color.description, Color)
            persist(adv)
                

if __name__ == '__main__':
    Base.metadata.create_all(engine)
