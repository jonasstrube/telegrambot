from telegram.ext import Updater
import os
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()
logger.info("Ich bin gestartet!")
updater = Updater(token=os.environ['TELEGRAM_BOTAPI_TOKEN'], use_context=True)
dispatcher = updater.dispatcher
import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger()
def start(update, context):
    logger.info("start aufgerufen Vier")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hallo Welt!")

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I don't understand that command man, thats unfair")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

# -----------------------------------------------
# Basic WebServer for handling Http-Requests
# Goal: when the bot is asleep on azure (after 30 minutes of inactivity): wake the bot up with a http request to the exposed azure-domain

from http.server import BaseHTTPRequestHandler, HTTPServer  
import os  
  
#Create custom HTTPRequestHandler class  
class MyHTTPRequestHandler(BaseHTTPRequestHandler):  

  #handle GET command  
  def do_GET(self): 
    #send code 200 response  
    self.send_response(200)  

    #send header first  
    self.send_header('Content-type','text-html')  
    self.end_headers() 
    return  

def run():  
  print('http server is starting...')  
  
  #ip and port of server  
  #by default http server port is 80  
  server_address = ('', 8000)  
  httpd = HTTPServer(server_address, MyHTTPRequestHandler)  
  print('http server is running...')  
  httpd.serve_forever()  

if __name__ == '__main__':  
  run()  