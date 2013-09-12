#!/usr/bin/python
import web
import requests,string
import markdown

import storage
import rediswebpy
import json

global configd
configd = json.loads(open('config.json').read())
stor = storage.storage(configd['couch'],configd['database'])

#web.config.debug = False

urls = (
	'/','home',
    '/author/(.*)','author',
    '/tags/(.*)','tags',
    '/slides/','slides',
	'/config','config',
    '/thing/(.*)','thing',
    '/attachment/(.*)','attachment',
	'/action/(.+)/(.+)','do_action',
	'/graph/(.*)','d3graph',
	'/slides','slides',
	'/stl/(.+)/(.+)','stl_view',
	'/image/(.+)/(.+)','image_view',
	'/cube/','cube'
)

inserts = web.template.render('templates/inserts/')

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

def file_block(data,doc_id):
	block = inserts.file_block(data,doc_id)
	return block 

app = web.application(urls, globals())

session = web.session.Session(app, rediswebpy.RedisStore(), initializer={'authors': {}})

t_globals = {
	'actions': actions ,
	'menu':get_menu,
	'nav_bar':nav_bar,
	'markdown': markdown.markdown,
	'context': session,
	'file_block' : file_block
}

render = web.template.render('templates/',base='base',globals=t_globals)

class home:
	def GET(self):
		#l = stor.author(configd['author'],0)
		l = stor.tag('new',0)
		my_stuff = inserts.thumblist(l)
		return render.index(my_stuff)

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
		if 'author' not in session:
			session.author = {}
		session.author[name] = 'viewed'
		l = stor.author(name,int(page['page']))
		return render.item_list(l)

class do_action:
	def GET(self,action,doc_id):
		print action,doc_id
		stor.send_action(action,doc_id)
		return 'woot'

class tags:
	def GET(self,name=''):
		page = web.input(page=0)
		if 'tags' not in session:
			session.tags = {}
		session.tags[name] = 'viewed'
		l = stor.tag(name,int(page['page']))
		return render.item_list(l)

class attachment:
	def GET(self,name):
		ct,r = stor.get_attach(name)
		web.header('Content-Type',ct)
		return r

class d3graph:
	def GET(self,name):
		name = '/static/models/test.js'
		return render.graph(name)

class hello:        
	def GET(self, name):
		return render.three()

class cube:
	def GET(self):
		return render.cube('','')

class stl_view:
	def GET(self,id,attachment):
		return render.three(id,attachment)

class image_view:
	def GET(self,id,attachment):
		return render.image(id,attachment)

class slides:
	def GET(self):
		page = web.input(page=0)
		l = stor.home('',int(page['page']))
		return render.slides(l)

if __name__ == "__main__":
    app.run()
