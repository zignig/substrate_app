#!/usr/bin/python
import web
import requests,string
import markdown

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
	'/action/(.+)/(.+)','do_action',
	'/graph/(.*)','d3graph',
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

def actions(id):
	data = ['process','render','clean','strip','print']
	actions = inserts.actions(data,id)
	return actions

app = web.application(urls, globals())

t_globals = {
	'actions': actions ,
	'menu':get_menu,
	'nav_bar':nav_bar,
	'markdown': markdown.markdown
}

render = web.template.render('templates/',base='base',globals=t_globals)
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

class do_action:
	def GET(self,action,doc_id):
		print action,doc_id
		stor.send_action(action,doc_id)
		return 'woot'

class tags:
	def GET(self,name):
		page = web.input(page=0)
		l = stor.tag(name,int(page['page']))
		return render.item_list(l)

class attachment:
	def GET(self,name):
		r = stor.get_attach(name)
		return r

class d3graph:
	def GET(self,name):
		name = '/static/models/test.js'
		return render.graph(name)

class hello:        
    def GET(self, name):
		return render.three()

class slides:
	def GET(self):
		page = web.input(page=0)
		l = stor.home('',int(page['page']))
		return render.item_list(l)

if __name__ == "__main__":
    app.run()
