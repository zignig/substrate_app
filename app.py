#!/usr/bin/python
import web
import requests,string

import storage

couch = 'http://192.168.1.84:5984/'
database = 'incoming'
stor = storage.storage(couch,database)

urls = (
	'/','slides',
    '/author/(.*)','author',
    '/tags/(.*)','tags',
    '/slides/','slides',
	'/config','config',
    '/thing/(.*)','thing',
    '/attachment/(.*)','attachment',
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

def actions():
	data = ['process','render','clean','strip','print']
	actions = inserts.actions(data)
	return actions

app = web.application(urls, globals())

render = web.template.render('templates/',base='base',globals={'actions': actions ,'menu':get_menu,'nav_bar':nav_bar})
#session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'count': 0})

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
		r = stor.get_doc(doc_id)
		return render.thing(r)

class author:
	def GET(self,name):
		page = web.input(page=0)
		l = stor.author(name,int(page['page']))
		return render.item_list(l)

class tags:
	def GET(self,name):
		page = web.input(page=0)
		l = stor.tag(name,int(page['page']))
		return render.item_list(l)

class attachment:
	def GET(self,name):
		r = stor.get_attach(name)
		return r

class hello:        
    def GET(self, name):
		return render.three()

class slides:
	def GET(self):
		r = requests.get(couch+'/'+database+'/_design/robot/_view/mime_types?key=%22image/jpeg%22&reduce=false&limit=20')
		j = r.json()
		print j
		j['couch'] = couch
		j['database'] = database
		return render.slides(j)

if __name__ == "__main__":
    app.run()
