#!/usr/bin/python
import web
import requests,string

couch = 'http://192.168.1.84:5984/'
database = 'zignig'

urls = (
	'/','home',
    '/slides/(.*)','slides',
	'/config','config',
    '/thing/(.*)','thing',
	'/(.*)', 'hello'
)

inserts = web.template.render('templates/')

def get_menu():
	data = [['test','blah']]
	menu = inserts.menu(data)
	return menu

def nav_bar():
	data = ''
	nav = inserts.nav_bar(data)
	return nav

app = web.application(urls, globals())

render = web.template.render('templates/',base='base',globals={'menu':get_menu,'nav_bar':nav_bar})

class home:
	def GET(self):
		return render.index()

class config:
	def GET(self):
		return render.config()

class thing:
	def GET(self,name):
		print name
		doc_id = string.split(name,'/')[-1]
		r = requests.get(couch+'/'+database+'/'+doc_id)
		return render.thing(r.json())

class hello:        
    def GET(self, name):
		return render.three()

class slides:
	def GET(self,name):
		r = requests.get(couch+'/'+database+'/_design/robot/_view/mime_types?key=%22image/jpeg%22&reduce=false&limit=20')
		j = r.json()
		print j
		j['couch'] = couch
		j['database'] = database
		return render.slides(j)

if __name__ == "__main__":
    app.run()
