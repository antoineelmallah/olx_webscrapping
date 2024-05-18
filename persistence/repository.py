from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from model import Base

connection_string = 'mariadb+mariadbconnector://admin:698400@127.0.0.1:3306/olx'

engine = create_engine(connection_string, echo=True)

Base.metadata.create_all(engine)

def persist(models):
    with Session(engine) as session:
        session.add_all(models)
        session.commit()

def find_domain_or_new(description, model_class: Base):
    with Session(engine) as session:
        stmt = select(model_class).where(model_class.description == description)
        result = session.scalar(stmt)
        return model_class(description=description) if not result else result
