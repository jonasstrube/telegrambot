from telegram.ext import Updater
import os
import logging

class community:
  def __init__(self, name, id):
    self.name = name
    self.id = id
    self.members = []
  
  def add_member(self, id):
    self.members.append(id)


#----------initialize database-------------

groceriesneeded = []
communities = []
communities.append(community("examplecommunity", 2353254))

#------------------------------------------

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

def wirbrauchen(update, context):
    # stick words of user input together to one string with spaces
    if len(context.args) != 0:
      groceries_item = ""
      for word in context.args:
        groceries_item = groceries_item + word + " "
      groceries_item = groceries_item[:-1:]

      groceriesneeded.append(groceries_item)
      
      answer_text = "Erfolgreich hinzugefügt"
    else:
      answer_text = "Schreib deine Einkäufe direkt hinter den Befehl"

    context.bot.send_message(chat_id=update.effective_chat.id, text=answer_text)
wirbrauchen_handler = CommandHandler('wirbrauchen', wirbrauchen)
dispatcher.add_handler(wirbrauchen_handler)

def wasbrauchen(update, context):
  for word in groceriesneeded:
    if word != '':
      context.bot.send_message(chat_id=update.effective_chat.id, text=word)

wasbrauchen_handler = CommandHandler('wasbrauchen', wasbrauchen)
dispatcher.add_handler(wasbrauchen_handler)

def leeren(update, context):
  groceriesneeded.clear()

leeren_handler = CommandHandler('leeren', leeren)
dispatcher.add_handler(leeren_handler)

def setcommunity(update, context):
  add_new_community_dialog = False
  # check if given argument is one number
  if len(context.args) == 1 and context.args[0].isdigit():
    id = int(context.args[0])
    community_found = False
    # find community with the id the user gave
    for community in communities:
      if community.id == id and community_found != True:
        community_found = True
        current_user_id = update.message.from_user.id

    if community_found == True:
      # check if user is already in community
      user_already_is_in_community = False
      for user_id in community.members:
        if current_user_id == user_id and user_already_is_in_community != True:
          user_already_is_in_community = True
      
      if not user_already_is_in_community:
        community.add_member(current_user_id)
        answer_text = "Fertig! Herzlich willkommen in der Community " + community.name
      else:  
        answer_text = "Du bist schon Teil der Community " + community.name
    else:
      #TODO add community (ask user for name before)
      add_new_community_dialog = True
      answer_text = "Eine Community mit dieser ID existiert nicht. Willst du eine neue Community erstellen? (J/N)"
    
  else:
    add_new_community_dialog= True
    answer_text = "Du hast keine Community-ID mitgegeben. Willst du eine neue Community erstellen? (J/N)"

  context.bot.send_message(chat_id=update.effective_chat.id, text=answer_text)

  if add_new_community_dialog == True:
    placeholder_var = 0
    # wait for J/N
    # if J:
    #   generate community id
    #   add community to communities
    #   ask for community name
    #   give community chosen name 

setcommunity_handler = CommandHandler('setcommunity', setcommunity)
dispatcher.add_handler(setcommunity_handler)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I don't understand that command man, thats unfair")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)
