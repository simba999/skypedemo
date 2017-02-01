import json
import sys
from datetime import datetime, timezone
from skpy import Skype, SkypeAuthException, SkypeEventLoop, SkypeNewMessageEvent

class SkypeMessageProcessor(SkypeEventLoop):

    def onEvent(self, event):
        try:
            if isinstance(event, SkypeNewMessageEvent) \
              and not event.msg.userId == self.userId:
                # event.msg.chat.sendMsg("Pong!")
                # print("Message: " + event.msg.content)
                print(json.dumps({
                    "event": "NewMessage",
                    "source": u"skype",
                    "author": event.msg.userId,
                    "contentType": event.msg.type,
                    "content": event.msg.content,
                    "time": event.msg.time
                }, separators=(',',':')))
        except Exception as ex:
            print ("EVNEnT EXCEPTION")
            sys.stderr.write(json.dumps({
                    "event": "Error",
                    "source": u"skype_message_processor",
                    "type": ex.__class__.__name__,
                    "time": datetime.now(timezone.utc),
                    "content": str(ex)
                }, separators=(',',':')))

    def logIntoSkype(self, username, password, token):
        try:
            self.conn.tokenFile = token
            try:
                self.conn.readToken()
            except (SkypeAuthException, IOError):
                print ("**********READ TOkEN**********")
                # newsk = Skype(username, password)
                # print ("@@@@CNNN: ", newsk)
                if (not username or not password == ""):
                    print (username)
                    print (password)

                    # sys.stderr.write(json.dumps({
                    #     "event": "Error",
                    #     "source": u"skype_message_processor",
                    #     "type": "Internal",
                    #     "time": datetime.now(timezone.utc),
                    #     "content": "Token is invalid and username or password was not specified"
                    # }, separators=(',',':')))
                    # sys.exit(-1)
                # Prompt the user for their credentials.
                print ("!!!!!!!!!!!!!!ERROR!!!!!!!!!!!!")
                self.conn.setUserPwd(username, password)
                self.conn.getSkypeToken()
                # getSkypeTokens writes token file automatically if specified
            # try:
            #     self.conn.readToken()
            # except:
            #     self.conn.getSkypeToken()
        except Exception as ex:
            print ("@@@@@@@@@@@@@@@@@TakenFileException!@@@@@@@@@@")
            sys.stderr.write(json.dumps({
                "event": "Error",
                "source": u"skype_message_processor",
                "type": ex.__class__.__name__,
                "time": datetime.now(timezone.utc),
                "content": str(ex)
            }, separators=(',',':')))
            sys.exit(-1)