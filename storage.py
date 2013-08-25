
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
		ret['rows'] = rows 
		ret['pages'] = (rows//pagination)+1 
		ret['data'] = d['rows']
		return ret
