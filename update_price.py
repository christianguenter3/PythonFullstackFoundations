from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

def getSession():
	engine = create_engine('sqlite:///restaurantmenu.db')

	Base.metadata.bind = engine
	
	DBSession = sessionmaker(bind = engine) 
	session = DBSession()
	return session

def printItem(item):
	print item.id, item.name, item.price, item.restaurant.name

def allVeggieBurgers(session):
	veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')

	print "\n"

	for item in veggieBurgers:
		printItem(item)

def setPriceForVeggieBurger():
	session = getSession()

	allVeggieBurgers(session)

	UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 2).one()
	UrbanVeggieBurger.price = '$5.55'
	
	session.add(UrbanVeggieBurger)
	session.commit()

	allVeggieBurgers(session)

def printAllMenuItems():
	session = getSession()
	
	items = getAllMenuItems(session)

	for item in items:
		printItem(item)

def getAllMenuItems(session):
	return session.query(MenuItem)

def deleteSpinachIceCream():
	session = getSession()

	spinachIceCream = getSpinachIceCream(session)
	session.delete(spinachIceCream)
	session.commit()

def getSpinachIceCream(session):
	return session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()

#setPriceForVeggieBurger()

deleteSpinachIceCream()
printAllMenuItems()
