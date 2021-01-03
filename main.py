from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Handler, CommandHandler, ConversationHandler, MessageHandler, Filters, Updater, CallbackContext
import os
import logging
import random

# -------------set up logging--------------------------------------------
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
# ----------------------------------------------------------------------------

# -------------declare classes----------------------------------
class community:
  def __init__(self, name: str, id: int):
    self.name = name
    self.id = id
    self.members = []
  
  def add_member(self, id: int):
    self.members.append(id)
# ---------------------------------------------------------------


# ----------initialize database-------------
groceriesneeded = []
communities = []
communities.append(community("examplecommunity", 2353254))
# ------------------------------------------

# ----------set global variables--------

SETCOMMUNITY_ASKNAME, SETCOMMUNITY_ADDCOMMUNITY = range(2)
# --------------------------------------

logger.debug("initialization is finished!")

def start(update: Update, context: CallbackContext):
    logger.info("start aufgerufen Vier")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hallo Welt!")

def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def wirbrauchen(update: Update, context: CallbackContext):
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

def wasbrauchen(update: Update, context: CallbackContext):
  for word in groceriesneeded:
    if word != '':
      context.bot.send_message(chat_id=update.effective_chat.id, text=word)

def leeren(update: Update, context: CallbackContext):
  groceriesneeded.clear()

def setcommunity(update: Update, context: CallbackContext) -> int:
  add_new_community_dialog = False
  current_user_id = update.message.from_user.id

  # check if user is already in community
  user_already_is_in_community = False
  for community in communities:
    for user_id in community.members:
      if current_user_id == user_id and user_already_is_in_community != True:
        user_already_is_in_community = True

  if user_already_is_in_community:
    answer_text = "Du bist schon Teil der Community " + community.name
  else:
    # check if given argument is one number
    if not len(context.args) == 1 or not context.args[0].isdigit():
      add_new_community_dialog= True
      answer_text = "Du hast keine Community-ID mitgegeben.\n\nWillst du eine neue Community erstellen?"
    else:
      id = int(context.args[0])
      # find community with the id the user gave
      community_found = False
      for community in communities:
        if community.id == id and community_found != True:
          community_found = True

      if community_found == False:
        add_new_community_dialog = True
        answer_text = "Eine Community mit dieser ID habe ich nicht gefunden.\n\nWillst du eine neue Community erstellen?" 
      else:
        community.add_member(current_user_id)
        answer_text = "Fertig! Herzlich willkommen in der Community " + community.name

  if add_new_community_dialog == True:
    reply_keyboard = [['Ja', 'Nein']]
    update.message.reply_text(answer_text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return SETCOMMUNITY_ASKNAME
  else:
    update.message.reply_text(answer_text)
    return ConversationHandler.END

def setcommunity_askname(update: Update, context: CallbackContext) -> int:
  update.message.reply_text(
    'Okay. Wie soll deine Community heißen?', reply_markup=ReplyKeyboardRemove()
  )

  return SETCOMMUNITY_ADDCOMMUNITY

def setcommunity_addcommunity(update: Update, context: CallbackContext) -> int:

  #   generate community id
  id_base = random.randint(10000, 99999)
  id_control = round(id_base / 10000) - 1
  id = id_base * 10 + id_control

  new_community = community(update.message.text, id)
  new_community.members.append(update.message.from_user.id)
  
  #   add community to communities
  communities.append(new_community)
  
  update.message.reply_text(
    'Fertig! Herzlich Willkommen in deiner neuen Community:\n\n' + new_community.name
  )
  return ConversationHandler.END

def setcommunity_cancel(update: Update, context: CallbackContext) -> int:
  update.message.reply_text(
      "Okay. Wenn du hinter /setcommunity direkt die Community-ID schreibst, kannst du dich zu einer Community hinzufügen. Beispiel:\n\n/setcommunity 123456", reply_markup=ReplyKeyboardRemove()
  )

  return ConversationHandler.END

def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I don't understand that command man, thats unfair")

def main() -> None:
  updater = Updater(token=os.environ['TELEGRAM_BOTAPI_TOKEN'], use_context=True)
  dispatcher = updater.dispatcher

  dispatcher.add_handler(CommandHandler('start', start))
  dispatcher.add_handler(CommandHandler('wirbrauchen', wirbrauchen))
  dispatcher.add_handler(CommandHandler('wasbrauchen', wasbrauchen))
  dispatcher.add_handler(CommandHandler('leeren', leeren))

  conv_handler_setcommunity = ConversationHandler(
        entry_points = [CommandHandler('setcommunity', setcommunity)],
        states = { 
          SETCOMMUNITY_ASKNAME: [MessageHandler(Filters.regex('^(Ja)$'), setcommunity_askname)], 
          SETCOMMUNITY_ADDCOMMUNITY: [MessageHandler(Filters.text & ~Filters.command, setcommunity_addcommunity)]
        },
        fallbacks = [MessageHandler(Filters.regex('^(Nein)$'), setcommunity_cancel)]
    )
  dispatcher.add_handler(conv_handler_setcommunity)

  # must be last handlers: handlers for unknown commands and messages
  dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))
  dispatcher.add_handler(MessageHandler(Filters.command, unknown))

  # ------- start the bot ------------------------
  updater.start_polling()

  # Run the bot until you press Ctrl-C or the process receives SIGINT,
  # SIGTERM or SIGABRT. This should be used most of the time, since
  # start_polling() is non-blocking and will stop the bot gracefully.
  updater.idle()

if __name__ == '__main__':
    main()