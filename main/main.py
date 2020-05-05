import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import uuid


# an array that will contain a list of all users currentlt in the broadcast
global_users=[]
class mainhandler(tornado.web.RequestHandler):
    def get(self):
        # create the form for clients to input their usernames
        self.write(
            '<html style="padding:0">'
            '<body style="margin:0;padding:0;width:100%;text-align:center;">'
            '<form style="padding:0;width:auto;padding:40px" action="/" method="POST">'
            '<h1 style="font-size:32px">Please enter a username to join</h1>'
            '<input style="margin-top:30px;margin-bottom:30px;padding-left:10px;height: 50px;line-height: 45px;width:300px"type="text" placeholder="username"name="username">'
            '<br><input style="font-size:16px;width:300px;height:45px;background-color: black;color: white;border: none;" type="submit" value="submit">'
            '</form>'
            '</body>'
            '</html>'
            )
    # when users submit their usernames get it
    def post(self):
        # check if the user is in the database
        current_username=self.get_body_argument('username')

        if current_username in global_users:
            # if user exists display user exists and a button for going back
            self.write('<h2>user exists<h2><a href="%s"><button style="width:200px;height:40px;background-color: #fd3333;color: white;border: none;">try another</button></a>' % 
                self.reverse_url("home"))
        else:
            #  add the user to the user list
            global_users.append(current_username)
            
            # get the position of the username in the array
            user_position=global_users.index(current_username)
            # redirect the user to  ../user/<position of user in the array>
            self.write('<h2>you have been verified</h2><a href="%s"><button style="width:200px;height:40px;background-color: rgb(0, 161, 5);color: white;border: none;">go to chat</button></a>' %
                   self.reverse_url("user", user_position))
            
class userhandler(tornado.web.RequestHandler):
    def initialize(self, db):
        # If a dictionary is passed as the third element of the URLSpec, 
        # it supplies the initialization arguments which will be passed to 
        # RequestHandler.initialize
        self.db = db

    def get(self, user_id):
        # get the name of current user based on the index received at the header
        # username=nameofU
        # now render index.html where the chatrooom is and display the cached messages
        self.render("index.html", messages=ChatSocketHandler.cache,userid=user_id)


class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    cache = []
    cache_size = 200
    usrloc=''
    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}
    # if the user logs in
    def open(self):
        ChatSocketHandler.waiters.add(self)
        logging.info(str(len(ChatSocketHandler.waiters))+" connected")
    # if the user logs out  
    def on_close(self):
        ChatSocketHandler.waiters.remove(self)
        logging.info(str(len(ChatSocketHandler.waiters))+" connected")
    @classmethod
    def update_cache(cls, chat):
        # append the cache with the message
        cls.cache.append(chat)
        # and if the current cache size is bigger than the original cache size reduce it
        # so that we can store more messages
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size :]

    @classmethod
    def send_updates(cls, chat):
        # logging.info("sending message to %d waiters", len(cls.waiters))
        # send updates to the connected waiters
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                # print an error when theres an error sending the message
                logging.error("Error sending message", exc_info=True)

    def on_message(self, message):
        # to send a message to the clients in the server we write
        logging.info("the message here")

        # decode the message because it is in html tags
        parsed = tornado.escape.json_decode(message)
        
        # get the name of user from the array
        try:
            nameofU=global_users[int(parsed['bdy'])]
        
        
        # check if the client has requested for a list of the users
        
            if parsed['body']=='USERS \\n':
                for b in global_users:
                    # get the parsed arguments from the chat.js which fetches them from index.html
                   
                    # uuid -> universally unique identifiers
                    # uuid4 creates a random uuid. uuid1 creates a uuid from a  
                    # clients computer network hence not safe
                    # print(users)
                    chat = {"id": str(uuid.uuid4()), "body": b+',', "un": nameofU}
                    chat["html"] = tornado.escape.to_basestring(
                        self.render_string("message.html", message=chat)
                    )
                    file_object = open('chatlogs.log', 'a')

                    # Append username: message to a new line at the end of file
                    file_object.write(b+','+'\n')
            
                    # Close the file
                    file_object.close()
                    # add the message to messages cache
                    ChatSocketHandler.update_cache(chat)
                    ChatSocketHandler.send_updates(chat)
                    
            else:
                # get the parsed arguments from the chat.js which fetches them from index.html

                # uuid -> universally unique identifiers
                # uuid4 creates a random uuid. uuid1 creates a uuid from a  
                # clients computer network hence not safe
                chat = {"id": str(uuid.uuid4()), "body": parsed["body"], "un": nameofU}
                chat["html"] = tornado.escape.to_basestring(
                    self.render_string("message.html", message=chat)
                )
                file_object = open('chatlogs.log', 'a')

                # Append username: message to a new line at the end of file
                file_object.write(nameofU+':'+parsed["body"]+'\n')
                
                # Close the file
                file_object.close()
                # add the message to messages
                ChatSocketHandler.update_cache(chat)
                ChatSocketHandler.send_updates(chat)
        except:
            # print an error if someone tries to send a message without a username
            logging.error("No user currently restered", exc_info=True)
            

def makeApp():
    url=tornado.web.URLSpec
        #crerate a dictionary that will contain the total number of users
    db=dict()
    # populate this dictionary with dummy data until the total number of users is arrrived at
    for g in range(30):
        db.update({g: g})
    return tornado.web.Application ([
        # entry point of the app. This is where the client states their username
    url(r'/',mainhandler,name='home'),
    # after the user has stated their name, navigate to a page after they are verified
    # here the user will select whether they want to chat or leave
    # the users can be a maximum of 30
    url(r"/user/([0-30]+)", userhandler, dict(db=db), name="user"),
    (r"/chatsocket", ChatSocketHandler),
    
    ],
    # generate a random value as the cookie
    cookie_secret="hUmAnsArEwEIrdInmArblE3",
    # set the template path to where the html folder is
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    # ser the template path to where the css folder is
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    # allow cookies
    xsrf_cookies=False,
    # run in debug mode
    debug=True,
    )


def main():
    # in order to see some output on the terminal/commandline
    tornado.options.parse_command_line()
    # pass in your application object
    app = makeApp()
    # listen to the port
    app.listen(8158)
    # start the websocket
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()