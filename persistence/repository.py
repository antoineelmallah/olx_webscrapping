from sqlalchemy import create_engine, select, or_
from sqlalchemy.orm import Session, joinedload, contains_eager
from datetime import datetime
import os
if __name__ == '__main__':
    from model import Base, Advertisement, Category, VehicleType, Model, Brand, Fuel, Gear, Steering, Color, Accessory, Vehicle
else:
    from persistence.model import Base, Advertisement, Category, VehicleType, Model, Brand, Fuel, Gear, Steering, Color, Accessory, Vehicle

connection_string = os.environ['WEBSCRAPING_DB_CONNECTION_STRING']

engine = create_engine(connection_string, echo=False)

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
            .options(joinedload(Advertisement.vehicle).joinedload(Vehicle.accessories))\
            .where(Advertisement.code == code)
        return session.scalar(stmt)
    
def find_advertisements_without_geocode():
    with Session(engine) as session:
        stmt = select(Advertisement)\
            .where(or_(Advertisement.lat == None, Advertisement.lon == None))
        return [ row[0] for row in session.execute(stmt) ]
       
def find_advertisements_without_prices():
    with Session(engine) as session:
        return session.query(Advertisement)\
            .join(Advertisement.vehicle)\
            .options(contains_eager(Advertisement.vehicle))\
            .filter(or_(Vehicle.average_price == None, Vehicle.fipe_price == None))\
            .all()

def persist_advertisement(adv: Advertisement, before_persist):

    with Session(engine) as session:
    
        adv_from_db = find_advertisement_by_code(adv.code)
        
        if adv_from_db:
            adv_from_db.last_update_date = datetime.now()
            if adv.states and adv.states[0] not in adv_from_db.states:
                adv_from_db.states.append(adv.states[0])
            adv = adv_from_db
        else:
            vehicle = adv.vehicle
            vehicle.category = find_domain_or_new(vehicle.category.description, Category) if vehicle.category else None
            vehicle.vehicle_type = find_domain_or_new(vehicle.vehicle_type.description, VehicleType) if vehicle.vehicle_type else None
            vehicle.model = find_domain_or_new(vehicle.model.description, Model) if vehicle.model else None
            vehicle.brand = find_domain_or_new(vehicle.brand.description, Brand) if vehicle.brand else None
            vehicle.fuel = find_domain_or_new(vehicle.fuel.description, Fuel) if vehicle.fuel else None
            vehicle.gear = find_domain_or_new(vehicle.gear.description, Gear) if vehicle.gear else None
            vehicle.steering = find_domain_or_new(vehicle.steering.description, Steering) if vehicle.steering else None
            vehicle.color = find_domain_or_new(vehicle.color.description, Color) if vehicle.color else None
            vehicle.accessories = [ find_domain_or_new(a.description, Accessory) for a in vehicle.accessories ]
        
        before_persist(adv)
        
        persist(adv)

                

if __name__ == '__main__':
    Base.metadata.create_all(engine)
