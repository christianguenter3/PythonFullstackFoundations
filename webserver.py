from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import re
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

class Model:
	def __init__(self):
		self.session = self.getSession()

	def getSession(self):
		engine = create_engine('sqlite:///restaurantmenu.db')

		Base.metadata.bind = engine
	
		DBSession = sessionmaker(bind = engine) 
		session = DBSession()
		return session

	def getAllRestaurants(self):		
		return self.session.query(Restaurant)

	def createNewRestaurant(self,name):
		id = random.randint(0,999999)
		newRestaurant = Restaurant(id=id,name=name)
		self.session.add(newRestaurant)
		self.session.commit()		
		return

	def getUniqueRestaurant(self,id):
		return self.session.query(Restaurant).filter_by(id = id).one()

	def delete(self,id):	
		restaurant = self.getUniqueRestaurant(session,id)
		self.session.delete(restaurant)
		self.session.commit()
		return

	def update(self,id,name):
		restaurant = self.getUniqueRestaurant(session,id)
		restaurant.name = name
		self.session.add(restaurant)
		self.session.commit()
		return

class webserverHandler(BaseHTTPRequestHandler):
	def sayHello(self):
		self.handler("Hello")

	def sayHola(self):
		self.handler("Hola")


	def handler(self,text):
				
		output = ""
		output += "<html><body>%s" %text
		output += self.getForm()
		output += "</body></html>"
		self.wfile.write(output)
		print output

	def getForm(self):
		return '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''


	def getNewForm(self):
		output = "<html><body>"
		output += '''<form method='POST' enctype='multipart/form-data' action='/new'>Name<input name="name" type="text"><input type="submit" value="Submit"></form>'''
		output += "</body></html>"
		return output

	def showAllRestaurants(self):
		model = Model()
		
		restaurants = model.getAllRestaurants()
		
		output = "<html><body>"

		
		for restaurant in restaurants:
			output += restaurant.name + "  "
			output += self.addEditLink(restaurant.id) + " "
			output += self.addDeleteLink(restaurant.id)
			output += "<br/><br/>" 

		output += "</body></html>" 		
		self.wfile.write(output)
		print output
		return

	def addEditLink(self, id):
		return "<a href='/edit?id=" + str(id) + "'>edit</a>"
	
	def addDeleteLink(self, id):
		return "<a href='/delete?id=" + str(id) + "'>delete</a>"

	def getIdFromPath(self):
		m = re.match(r'.*id=(\d+)',self.path)
		return m.group(1)


	def delete(self):
		model = Model()
		id = self.getIdFromPath()
		model.delete(id)
		
		output = "<html><body>Restaurant: %s wurde geloescht</body></html>" %id
		self.wfile.write(output)	
		print(output)
		return

	def edit(self):
		self.notYetImplemented()
		return

	def new(self):
		output = self.getNewForm()
		self.wfile.write(output)
		print(output)
		return

	def notYetImplemented(self):
		output = "<html><body>Function is not yet implemented</body></html>"
		self.wfile.write(output)	
		print(output)
		return

	def pathMatches(self,path):
		return re.match(path,self.path)
	def do_GET(self):
		try:
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()

			if self.pathMatches(r'/hello'): #self.path.endswith("/hello"):
				self.sayHello()
				return
			
			if self.pathMatches(r'/hola'): #self.path.endswith("/hola"):
				self.sayHola()

			if self.pathMatches(r'/restaurants'): #self.path.endswith("/restaurants"):
				self.showAllRestaurants()

			if self.pathMatches(r'/delete'): # self.path.endswith("/delete"):
				self.delete()

			if self.pathMatches(r'/edit'): #self.path.endswith("/edit"):
				self.edit()

			if self.pathMatches(r'/new'):
				self.new()
			
		except IOError:
			self.send_error(404,"File Not Found %s" %self.path)


	def do_POST(self):
		try:
			if self.pathMatches(r'/new'):
				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				ctype, pdict = cgi.parse_header( self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					name = fields.get('name')[0]
					print(name)
					model = Model()
					model.createNewRestaurant(name)
					output = "<html><body>Restaurant %s angelegt<body></html>" %name
					print(output)
					self.wfile.write(output)
					return

			else:
				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				ctype, pdict = cgi.parse_header( self.headers.getheader('content-type'))
				
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('message')

				output = ""
				output += "<html><body>"
				output += " <h2> Okay, how about this: </h2>"
				output += "<h1> %s </h1>" % messagecontent[0]
				output += self.getForm() 
				output += "</body></html>"

				self.wfile.write(output)

				print output
		except:
			pass


def main():
	try:
		port = 8080 
		server = HTTPServer(('',port), webserverHandler)
		print "web server running on port %s" % port
		server.serve_forever()
	except KeyboardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()

if __name__ ==  '__main__':
	main()
