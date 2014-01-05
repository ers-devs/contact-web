import argparse
import json
import tornado.ioloop
import tornado.web
import tornado.template
from View import View
from Controller import Controller
from Model import Model

_model = Model()
_view = View(_model)
_controller = Controller(_view, _model)

class MainHandler(tornado.web.RequestHandler):
    def get(self):        
        # Load the template
        loader = tornado.template.Loader("./")
        self.write(loader.load("ui.html").generate(contacts=["test1", "test2"], triples=[{"p": "foaf:homepage", "o": "www.example.org"}]))

class CommandHandler(tornado.web.RequestHandler):
    # def __init__(self):
    #     super(CommandHandler,self).__init__()
    
    def get(self, url = '/'):
        print "get"
        self.handleRequest()
        
    def post(self, url = '/'):
        print 'post'
        self.handleRequest()
        
    def handleRequest(self):        
        # is op to decide what kind of command is being sent
        op = self.get_argument('op', None)
        data = self.get_argument('data', None)
        print "request handler"

        # received a "checkup" operation command from the browser:
        if op == "checkup":
            # make a dictionary
            status = {"server": True, "mostRecentSerial": mostRecentLine }
            # turn it to JSON and send it to the browser
            self.write( json.dumps(status) )
        elif op == "update_contacts":
            contacts = _controller._update_contacts_cb()
            self.write( json.dumps(contacts) )
        elif op == "contact_selected":
            entity_descriptions = _controller._contact_selected_cb(data)
            self.write( json.dumps(entity_descriptions) )
        elif op == "new_prop_clicked":
            entity_descriptions = _controller._new_prop_clicked_cb( json.loads(data) )
            self.write( json.dumps(entity_descriptions) )
        elif op == "delete_prop_clicked":
            entity_descriptions = _controller._delete_prop_clicked_cb( json.loads(data) )
            self.write( json.dumps(entity_descriptions) )
        elif op == "keep_clicked":
            _controller._keep_clicked_cb()

        # operation was not one of the ones that we know how to handle
        else:
            print op
            print self.request
            raise tornado.web.HTTPError(404, "Missing argument 'op' or not recognized")

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/(com.*)", CommandHandler)
], debug = True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="Web app port", type=int, default=8888)
    args = parser.parse_args()
    
    application.listen(args.port)
    tornado.ioloop.IOLoop.instance().start()