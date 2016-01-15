from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi #common gateway interface, interpret server message

# import CRUD operations
from lean_fridge_setup import Base, Stock, ItemProperty
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# create session and connect to DB
engine = create_engine('sqlite:///lean_fridge_app.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        try:
            if self.path.endswith("/stock/new"):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Add a New Item</h1>"
                output += "<form method = 'POST' enctype = 'multipart/form-data action = '/stock/new'>"
                output += "<input name = 'newItemName' type = 'text' placeholder = 'add new item name here'>"
                output += "<input type = 'submit' value = 'Add'></br>"
                #output += "<input name = 'newItemCount' type = 'text' placeholder = 'add count here'>"
                #output += "<input type = 'submit' value = 'Add'>"
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/update"):
                itemIDPath = self.path.split("/")[2] # e.g. localhost:8080/stock/item_id/update
                myItemQuery = session.query(Stock).filter_by(id = itemIDPath).one()
                if myItemQuery:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>" + myItemQuery.name + "</h1>"
                    #output += myItemQuery.name
                    #output += "</h1>"
                    output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/stock/%s/update'>"%itemIDPath
                    output += "<input name = 'renameitem' type = 'text' placeholder = 'Rename this item'>"
                    output += "<input type = 'submit' value = 'Rename'>"
                    output += "</form>"
                    output += "</html>"
                    self.wfile.write(output)

            if self.path.endswith("/delete"):
                itemIDPath = self.path.split("/")[2]
                myItemQuery = session.query(Stock).filter_by(id = itemIDPath).one()

                #Create a confirmation page upon delete
                if myItemQuery:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    output = ""
                    output = "<html><body>"
                    output += "<h1>Are you sure about deleting %s" % myItemQuery.name + "?"
                    output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/stock/%s/delete'>"%itemIDPath
                    output += "<input type = 'submit' value = 'delete'>"
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    return

            if self.path.endswith("/stock"):
                stock = session.query(Stock).all()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers() 

                output = ""
                output += "<html><body>"
                output += "<h1>Welcome to your fridge!</h1><h2>Now, take a look at what you have in stock.</h2></br></br>"
                output += "<a href = '/stock/new'> Add a New Item Here</a><br><br>"
                
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                
                for item in stock: # list all the items in the stock
                    output += "Item name: " + item.name + " " + "</br>In stock: " + str(item.total)
                    output += "</br>"
                    output += "<a href = '/stock/%s/update'>Update this item</a></br>"% item.id
                    output += "<a href = '/stock/%s/delete'>Delete this item</a></br>"% item.id
                    output += "</br></br>"
                
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
        
        except IOError:
            self.send_error(404, "File Not Found: %s" % self.path)


    def do_POST(self):
        try:
            if myItemQuery:
                session.delete(myItemQuery)
                session.commit()
                self.send_response(301)
                self.send_header("Content-type", "text/html")
                self.send_header("Location", "/stock")
                self.end_headers()

            if self.path.endswith("/stock/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
                if ctype == "multipart/form-data":
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    fieldcontent = fields.get("newItemName")
                    
                    # Add the newItem to the db table
                    
                    newItem = Stock(name = fieldcontent[0])
                    session.add(newItem)
                    session.commit()

                    self.send_response(301)
                    self.send_header("Content-type", "text/html")
                    self.send_header("Location", "/stock")
                    self.end_headers()

            if self.path.endswith("/update"):
                ctype, pdict = cgi.parse_header(self.headers.getheader("Content-type"))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    fieldcontent = fields.get("renameitem")
                    itemIDPath = self.path.split("/")[2]

                    myItemQuery = session.query(Stock).filter_by(id = itemIDPath).one()
                    if myItemQuery:
                        myItemQuery.name = fieldcontent[0]
                        session.add(myItemQuery)
                        session.commit()
                        
                        self.send_response(301)
                        self.send_header("Content-type", "text/html")
                        self.send_header("Location", "/stock")
                        self.end_headers()

        except:
            pass



def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web server running...open localhost:%s/stock in your browser"% port
        server.serve_forever()
    except KeyboardInterrupt:
        print "^C received, shutting down server"
        server.socket.close()

if __name__ == '__main__':
    main()



