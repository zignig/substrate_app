
import requests,string
pagination = 20
class storage:
	def __init__(self,couch,database):
		self.couch = couch
		self.database = database
		self.req = requests.Session()
		
	def author(self,author,page):
		r = self.get_list('author',author,page)
		return r 
			
	def tag(self,tag,page):
		r = self.get_list('tag',tag,page)
		return r

	def get_doc(self,id):
		r = self.req.get(self.couch+'/'+self.database+'/'+id)
		return r.json()

	def get_attach(self,path):
		r = self.req.get(self.couch+'/'+self.database+'/'+path)
		return r.content

	def get_list(self,view,value,page):
		r = self.req.get(self.couch+'/'+self.database+'/_design/substrate_explorer/_view/'+view+'?key="'+value+'"')
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
