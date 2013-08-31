

import requests,string,pika,json
import redis

red = redis.Redis()

pagination = 50
ttl = 86400
class storage:
	def __init__(self,couch,database):
		self.couch = couch
		self.database = database
		self.req = requests.Session()
		try:
			credentials = pika.PlainCredentials('guest','guest')
			connection = pika.BlockingConnection(pika.ConnectionParameters(credentials=credentials,host='192.168.1.84'))
			channel = connection.channel()
			channel.basic_qos(prefetch_count=1)
			self.channel = channel
		except:
			print 'no carrot for you'

			
	def info(self):
		r = self.req.get(self.couch+'_all_dbs')
		return r.json()

	def author_list(self,author,page):
		r = self.get_list('author_list',author,page)
		return r 

	def author(self,author,page):
		r = self.get_list('author',author,page)
		return r 
			
	def tag(self,tag,page):
		r = self.get_list('tag',tag,page)
		return r

	def home(self,name,page):
		r = self.get_list('home','',page)
		return r

	def get_doc(self,id):
		if red.exists('id:'+id):
			return json.loads(red.get('id:'+id))
		else:
			r = self.req.get(self.couch+'/'+self.database+'/'+id)
			data = r.json()
			red.set('id:'+id,json.dumps(data))
			red.expire('id:'+id,ttl)
			return data

	def get_attach(self,path):
		if red.exists('att:'+path):
			return red.get('att:'+path)
		else:
			r = self.req.get(self.couch+'/'+self.database+'/'+path)
			data = r.content
			red.set('att:'+path,data)
			red.expire('att:'+path,ttl)
			return data	
		

	def get_list(self,view,value,page):
		key_str = 'list:'+view+':'+value
		if red.exists(key_str):
			d = json.loads(red.get(key_str))
		else:
			if value == '': 
				r = self.req.get(self.couch+'/'+self.database+'/_design/substrate_explorer/_view/'+view)
			else:
				r = self.req.get(self.couch+'/'+self.database+'/_design/substrate_explorer/_view/'+view+'?key="'+value+'"')
			red.set(key_str,r.content)	
			red.expire(key_str,ttl)
			d = r.json()
		ret = {}
		rows = len(d['rows'])
		pages = (rows//pagination)+1
		ret['view'] = view
		ret['value'] = value
		ret['rows'] = rows 
		ret['page'] = page
		ret['pages'] = pages 
		ret['pagination'] = pagination
		# return only 1 page
		ret['data'] = d['rows'][page*pagination:page*pagination+pagination]
		return ret
	
	def send_action(self,action,doc_id):
		" send the action to the spooler"
		self.channel.basic_publish('incoming','incoming',json.dumps({'_id':doc_id}))
		return
