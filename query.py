from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine) 
session = DBSession()

#result = session.query(Restaurant).all()

#for item in result:
#	print item.name

items = session.query(MenuItem).all()

for item in items:
	print item.name
	print item.price

