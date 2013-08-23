#!/usr/bin/python
import web
        
render = web.template.render('templates/',base='base')

urls = (
	'/(.*)', 'hello'
)

app = web.application(urls, globals())

class hello:        
    def GET(self, name):
        if not name: 
            name = 'World'
        return 'Hello, ' + name + '!'

if __name__ == "__main__":
    app.run()
