from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi #common gateway interface, interpret server message

# import CRUD operations
from lean_fridge_setup import Base, Stock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# create session and connect to DB
engine = create_engine('sqlite:///lean_fridge_app.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


class WebServerHandler(BaseHTTPRequestHandler):

    def get_item_names(self):
        stock = session.query(Stock).all()
        item_names = set()
        for item in stock:
            item_names.add(item.name)
        return item_names 


    def do_GET(self):
        try:
            if self.path.endswith("/stock/new"):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Add a New Item & its Count</h1>"
                output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/stock/new'>"
                output += "<input name = 'newItemName' type = 'text' placeholder = 'add new item name here'>"
                output += "<input name = 'newItemCount' type = 'text' placeholder = 'add new item count here'></br>"
                output += "<input type = 'submit' value = 'Add the new item & count'>"
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/update"):
                itemIDPath = self.path.split("/")[2] # e.g. localhost:8080/stock/item_id/update
                ItemQuery = session.query(Stock).filter_by(id = itemIDPath).one()
                if ItemQuery:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>" + ItemQuery.name + "</h1>"
                    output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/stock/%s/update'>"%itemIDPath
                    output += "<input name = 'renameitem' type = 'text' placeholder = 'Rename this item'></br>"
                    output += "<input name = 'updatecount' type = 'text' placeholder = '%s is already in stock'>" % ItemQuery.total
                    output += "<input type = 'submit' value = 'Add'>"
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(output)

            if self.path.endswith("/delete"):
                itemIDPath = self.path.split("/")[2]
                ItemQuery = session.query(Stock).filter_by(id = itemIDPath).one()

                #Create a confirmation page upon delete
                if ItemQuery:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    output = ""
                    output = "<html><body>"
                    output += "<h1>Are you sure about deleting %s" % ItemQuery.name + "?"
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
                output += "<a href = '/stock/new'> Not on the stock list? Add the new item here!</a><br><br>"
                
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
        output = ""
        try:
            if self.path.endswith("/delete"):
                itemIDPath = self.path.split("/")[2]
                ItemQuery = session.query(Stock).filter_by(id=itemIDPath).one()

                if ItemQuery != []:
                    session.delete(ItemQuery)
                    print ItemQuery
                    session.commit()
                    print "deleting %s" % ItemQuery.name
                    self.send_response(301)
                    self.send_header("Content-type", "text/html")
                    self.send_header("Location", "/stock")
                    self.end_headers()

            if self.path.endswith("/stock/new"):
                
                ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))

                if ctype == "multipart/form-data":
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_item_name = fields.get("newItemName")[0]
                    new_count = int(fields.get("newItemCount")[0])
                    print new_count
                    item_names = self.get_item_names()
                    name_was_found = new_item_name in item_names

                    if name_was_found:
                        output += "<html><body><p>This item already exists in stock! You can find that item and update its count <a href = '/stock'>here</a></p></html></body>"
                        
                    else:
                    #Add the newItem to the db table
                        newItem = Stock(name = new_item_name, total = new_count)
                        print newItem
                        session.add(newItem)
                        print "new item added"
                        #session.add(newCount)
                        print "new count added"
                        session.commit()
                        print "committing"
                        output += "<html><body><p>New item is added successfully!</p>"
                        output += "<p>Go <a href = '/stock'>Back</a></p></body></html>"

                self.send_response(201)
                self.send_header("Content-type", "text/html")
                self.send_header("Location", "/stock")
                self.end_headers()

                self.wfile.write(output)
                        

            if self.path.endswith("/update"):
                ctype, pdict = cgi.parse_header(self.headers.getheader("Content-type"))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    rename_item = fields.get("renameitem")
                    update_count = fields.get("updatecount")
                    itemIDPath = self.path.split("/")[2]

                    ItemQuery = session.query(Stock).filter_by(id = itemIDPath).one()
                    if ItemQuery != []:
                        ItemQuery.name = rename_item[0]
                        ItemQuery.total = update_count[0]
                        if ItemQuery.name and ItemQuery.total:

                            session.add(ItemQuery)
                            session.commit()
                            output += "<html><body><p>This item is updated successfully! Go <a href = '/stock'>back</a></p></body><html>"
                            self.wfile.write(output)
                        else:
                            output += "<html><body><p>Did you forget to fill one of the fields? Go <a href = '/stock/%s/update'>back</a><p><body><html>" % itemIDPath
                            self.wfile.write(output)

                        self.send_response(201)
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



