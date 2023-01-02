import telebot
import time
import requests
from bs4 import BeautifulSoup
import re
import gspread
import time

##############################################################
# Connect with Google Sheet
##############################################################

credentials ={
  ####################################
  ####### SECRET   CREDENTIALS #######
  ####################################
}
sa = gspread.service_account_from_dict(credentials)

sh = sa.open("""DATABASE NAME""")

wks = sh.worksheet("""WORK SHEET NAME""")

##############################################################
# INFO OF BOT
##############################################################

API_TOKEN= ### SECRET telegram API KEY ###

bot = telebot.TeleBot(API_TOKEN, parse_mode=None) 

##############################################################
# VARIABLES & FUNCTION DECLERATION
##############################################################

url ="https://www.aiet.edu.eg/pages/FTerm_ResultDetails_PDF_main.asp?STCode=20-0-0037&ClassYear=03&Dept=01"

Dept = ["01","02","03","04","05"]
classYear = ["00","01","02","03","04"]

telegramIDs= []
telegramIDs_handles = {}
eduids= []

CHANNEL_ID =  ### SECRET  CHANNEL_ID ###
GROUP_ID =    ### SECRET    GROUP_ID ###
GROUP_ID2 =   ### SECRET    GROUP_ID ###
PROBLEMC_ID = ### SECRET PROBLEMC_ID ###

def get_name_from_gs (telegram_id):
    for ids in wks.get_all_records():
        if (ids["telegram_id"]==telegram_id):
            return (ids["name"])

##############################################################
# WELCOME COMMAND
##############################################################

@bot.message_handler(commands=['start','refresh'])
def start(message):
    try :
        if  (message.chat.type=="private"):
            for ids in wks.get_all_records():
                    telegramIDs.append(ids["telegram_id"])
            if (message.from_user.id in telegramIDs):
                telegramIDs.clear()
            
                bot.send_message(chat_id=message.chat.id,text="**Welcome , "+get_name_from_gs(message.from_user.id).split(" ")[0]+" 👋**",parse_mode="MarkdownV2")   
                user_info="Name : "+str(message.from_user.first_name)+" "+str(message.from_user.last_name)+"\n\n@"+str(message.from_user.username)+"\n"+str(message.from_user.id)
                bot.send_message("""SECRET Telegram ID""",user_info)
            else:
                telegramIDs.clear()

                welcome_msg ="""This bot for controlling your login in ICPC AIET community.

Please follow the instructions :

1️⃣ Click on  /login  to log in to the bot .

2️⃣ If the message is not answered, choose /refresh from the menu.

- - -

This bot built with ❤️ by @M0xYasser"""
                bot.reply_to(message,welcome_msg)
                user_info="Name : "+str(message.from_user.first_name)+" "+str(message.from_user.last_name)+"\n\n@"+str(message.from_user.username)+"\n"+str(message.from_user.id)
                bot.send_message("""SECRET Telegram ID""",user_info)
        else : 
            x=bot.reply_to(message, "❌ This command for the BOT only")
            time.sleep(5)
            bot.delete_message(x.chat.id,x.message_id)
            bot.delete_message(x.chat.id,x.reply_to_message.id)
    except :
        err="""
❌ حدث خطأ غير متوقع 

🐞 اذا واجهتك اي مشكلة او تريد الابلاغ عن مشكلة فيمكنك التواصل معي عن طريق المعرف   ⬅️ @M0xYasser
        """
        bot.reply_to(message, err)   

##############################################################
# LOGIN COMMAND 
##############################################################

@bot.message_handler(commands=['login'])
def login(message):
    try :
        if  (message.chat.type=="private"):
            for ids in wks.get_all_records():
                telegramIDs.append(ids["telegram_id"])
            if (message.from_user.id in telegramIDs):
                telegramIDs.clear()
                # print(get_name_from_gs(message.from_user.id))
                bot.send_message(chat_id=message.chat.id,text="**You are already logged in 😊**",parse_mode="MarkdownV2")   
            else:
                telegramIDs.clear()
                msg = bot.reply_to(message,"Enter EDU_Mail :")
                bot.register_next_step_handler(msg, process_id_step)
        else : 
            x=bot.reply_to(message, "❌ This command for the BOT only")
            time.sleep(5)
            bot.delete_message(x.chat.id,x.message_id)
            bot.delete_message(x.chat.id,x.reply_to_message.id)
    except :
        err="""
❌ حدث خطأ غير متوقع 

🐞 اذا واجهتك اي مشكلة او تريد الابلاغ عن مشكلة فيمكنك التواصل معي عن طريق المعرف   ⬅️ @M0xYasser
        """
        bot.reply_to(message, err)

##############################################################
# PROCESS EDU EMAIL
##############################################################

def process_id_step(message):
    if (message.text=="/refresh"):
        start(message)
        return
    elif (message.text=="/start"):
        start(message)
        return
    elif (message.text=="/login"):
        login(message)
        return
    elif (message.text=="/handle"):
        handle(message)
        return
    elif (message.text=="/old"):
        old(message)
        return
    elif (message.text=="/tech_summit"):
        booking(message)
        return
    telegramId=message.from_user.id
    userName=message.from_user.username
    flag=0
    c=0

    for eduid in wks.get_all_records():
        eduids.append(eduid["edu_id"])

    try:
        match = re.match(r"([a-z.]+)([0-9]+)", message.text , re.I)
        if match:
            user = match.groups()

        id=user[1][0:2]+"-"+user[1][2]+"-"+user[1][3:]
        eduEmail = user[0]+user[1]+"@aiet.edu.eg"
        
        if (id in eduids):
            eduids.clear()
            m=bot.reply_to(message, "This email has already been used ..")

        else :
            eduids.clear()
            m=bot.reply_to(message, "Waitting ...")
            for dep in Dept:
                for cy in classYear:
                    c=c+1
                    URL = "https://www.aiet.edu.eg/pages/FTerm_ResultDetails_PDF_main.asp?STCode="+id+"&ClassYear="+cy+"&Dept="+dep
                    page = requests.get(URL,verify=False)
                    soup = BeautifulSoup(page.content, "html.parser")
                    results = soup.find(class_="new88")

                    if (c in [1,2,3]) : prog="█▒▒▒▒▒▒▒▒▒ "+str(10+c-1)+"%"
                    elif (c in [4,5]) : prog="██▒▒▒▒▒▒▒▒ "+str(20+c-4)+"%"
                    elif (c in [6,7,8]) : prog="███▒▒▒▒▒▒▒ "+str(30+c-6)+"%"
                    elif (c in [9,10]) : prog="████▒▒▒▒▒▒ "+str(40+c-9)+"%"
                    elif (c in [11,12,13]) : prog="█████▒▒▒▒▒ "+str(50+c-11)+"%"
                    elif (c in [14,15]) : prog="██████▒▒▒▒ "+str(60+c-14)+"%"
                    elif (c in [16,17,18]) : prog="███████▒▒▒ "+str(70+c-16)+"%"
                    elif (c in [19,20]) : prog="████████▒▒ "+str(80+c-19)+"%"
                    elif (c in [21,22,23,24]) : prog="█████████▒ "+str(90+c-15)+"%"
                    else : prog="██████████ 100%"

                    bot.edit_message_text(chat_id=message.chat.id,text=prog,message_id=m.message_id)

                    try :
                        nameStudent = results.find_all("h1")[0].text
                        bot.edit_message_text(chat_id=message.chat.id,text="██████████ 100%",message_id=m.message_id)  
                        bot.edit_message_text(chat_id=message.chat.id,text="**Welcome , "+nameStudent.split(" ")[0]+" "+nameStudent.split(" ")[1]+" 👋**",parse_mode="MarkdownV2",message_id=m.message_id)
                        wks.insert_row([telegramId,userName,eduEmail,id,nameStudent,0,0],2)
                        pollq="""In what year did you participate in the competition?
If in 2021 send number 1
If in 2022 send number 2
If you participated in the two years, send number 3
If you haven't participated before, send number 4
And if you were a volunteer before, send number 5
"""
                        msg = bot.send_message(chat_id=message.chat.id,text=pollq)
                        bot.register_next_step_handler(msg, poll)
                        flag=1
                        
                    except : 
                        continue
                    if (flag) : break
                if (flag) : break
            if (not flag) : make_err = 1/0
    except :
        err="""
❌ حدث خطأ غير متوقع 

        ⬅️  برجاء التأكد من كتابة ايميل AIET بالشكل الصحيح ✅

🐞 اذا واجهتك اي مشكلة او تريد الابلاغ عن مشكلة فيمكنك التواصل معي عن طريق المعرف   ⬅️ @M0xYasser
        """
        bot.reply_to(message, err)

##############################################################
# POLL
##############################################################
 
def poll (message):
    global y2021,y2022,v
    try :
        if (message.text == '1' or message.text == '١'):
            y2021=1
            y2022=v=0
        elif (message.text == '2' or message.text == '٢'):
            y2022=1
            y2021=v=0
        elif (message.text == '3' or message.text == '٣'):
            y2021=y2022=1
            v=0
        elif (message.text == '4' or message.text == '٤'):
            y2021=y2022=v=0
        elif (message.text == '5' or message.text == '٥'):
            v=1
            y2021=y2022=0
        else :
            errr=x/0
        for ids in wks.get_all_records():
            telegramIDs.append(ids["telegram_id"])
        x = telegramIDs.index(message.from_user.id)+2
        telegramIDs.clear()
        wks.update('F'+str(x),y2021)
        wks.update('G'+str(x),y2022)
        wks.update('L'+str(x),v)
        links = """Congratulations! 🎉👏

Your login has been accepted by the admin.

We have 3 way for communications.

1- Main channel: 
https://t.me/icpcaiet

2- Community group:
https://t.me/+hrrAxNNNkyUyMGI0
< Please request to join >

3- Questions & Problems channel:
https://t.me/+mGFOCOMix1cyYzA0

- - -

Thanks 🙏"""
        bot.send_message(chat_id=message.chat.id,text=links)
        user_info="Name : "+str(message.from_user.first_name)+" "+str(message.from_user.last_name)+"\n"+get_name_from_gs(message.from_user.id)+"\n2021 >> "+str(y2021)+" & 2022 >> "+str(y2022)+" & volunteer >>"+str(v)+"\n@"+str(message.from_user.username)
        bot.send_message("""SECRET Telegram ID""",user_info)
    except :
        err="""
❌ حدث خطأ غير متوقع 

        ⬅️  برجاء التاكد من ادخال القيم بالشكل الصحيح  ✅

🐞 اذا واجهتك اي مشكلة او تريد الابلاغ عن مشكلة فيمكنك التواصل معي عن طريق المعرف   ⬅️ @M0xYasser
        """
        bot.reply_to(message, err)
        pollq="""In what year did you participate in the competition?
If in 2021 send number 1
If in 2022 send number 2
If you participated in the two years, send number 3
And if you haven't participated before, send number 4"""
        msg = bot.send_message(chat_id=message.chat.id,text=pollq)
        bot.register_next_step_handler(msg, poll)

##############################################################
# Question COMMAND
##############################################################

@bot.message_handler(commands=['q'])
def question (message):
    try : 
        if  (message.chat.type=="supergroup"):
            for ids in wks.get_all_records():
                telegramIDs.append(ids["telegram_id"])
            if (message.from_user.id in telegramIDs):
                telegramIDs.clear()
                bot.send_message(GROUP_ID2,message.reply_to_message.text+"\n\n__________\n\nBY : "+get_name_from_gs(message.reply_to_message.from_user.id).split(" ")[0]+" "+get_name_from_gs(message.reply_to_message.from_user.id).split(" ")[1])
                thx=bot.reply_to(message.reply_to_message, "thx for your question 🤍")
                time.sleep(3)
                bot.delete_message(message.chat.id,message.reply_to_message.message_id)
                bot.delete_message(message.chat.id,message.message_id)
                bot.delete_message(message.chat.id,thx.message_id)
            else :
                telegramIDs.clear()
                s=bot.reply_to(message,text="You are not logged in the bot yet 😢\nLogin >> @ICPCAIET_bot")   
                time.sleep(5)
                bot.delete_message(s.chat.id,message.message_id)
                bot.delete_message(s.chat.id,s.message_id)
    except :
        x=bot.reply_to(message, "❌ Please reply to message")
        time.sleep(5)
        bot.delete_message(x.chat.id,x.message_id)
        bot.delete_message(x.chat.id,x.reply_to_message.id)

##############################################################
# APPROVE COMMAND
##############################################################

@bot.message_handler(commands=['approve'])
def approve (message):
    if  (message.chat.id==GROUP_ID2):
        try :
            bot.send_message(PROBLEMC_ID,(message.reply_to_message.text))
            bot.delete_message(message.chat.id,message.message_id)
            bot.delete_message(message.chat.id,message.reply_to_message.id)
        except :
            x=bot.reply_to(message, "❌ Please reply to message")
            time.sleep(5)
            bot.delete_message(x.chat.id,x.message_id)
            bot.delete_message(x.chat.id,x.reply_to_message.id)
    else:
        x=bot.reply_to(message, "❌ This command for ADMINS only")
        time.sleep(5)
        bot.delete_message(x.chat.id,x.message_id)
        bot.delete_message(x.chat.id,x.reply_to_message.id)

##############################################################
# old COMMAND 
##############################################################
@bot.message_handler(commands=['old'])
def old(message):
    oldMsg="""Traning old group:
https://t.me/+l8MCwhWfr5MyNmQ0
< Please request to join >
"""
    suc="""You have been registered successfully ✅
Your information will be reviewed and accepted ✔️"""
    try :
        if  (message.chat.type=="private" ):
            for ids in wks.get_all_records():
                telegramIDs.append(ids["telegram_id"])
            x = telegramIDs.index(message.from_user.id)+2
            wks.update('I'+str(x),1)
            bot.reply_to(message, oldMsg)
            bot.send_message(chat_id=message.chat.id,text=suc)
            user_info="Name : "+str(message.from_user.first_name)+" "+str(message.from_user.last_name)+"\n"+get_name_from_gs(message.from_user.id)+"\n@"+str(message.from_user.username)
            #print(user_info)
            # Put your telegram Id to get notification when user login
            bot.send_message("""Your Telegram ID""",user_info)
        else : 
            x=bot.reply_to(message, "❌ This command for the BOT only")
            time.sleep(5)
            bot.delete_message(x.chat.id,x.message_id)
            bot.delete_message(x.chat.id,x.reply_to_message.id)
    except :
        err="""
❌ حدث خطأ غير متوقع 

🐞 اذا واجهتك اي مشكلة او تريد الابلاغ عن مشكلة فيمكنك التواصل معي عن طريق المعرف   ⬅️ @M0xYasser
        """
        bot.reply_to(message, err) 


##############################################################
# Tech Summit COMMAND
##############################################################

@bot.message_handler(commands=['tech_summit'])
def booking (message):
    try : 
        if  (message.chat.type=="private"):
            for ids in wks.get_all_records():
                telegramIDs.append(ids["telegram_id"])
            if (message.from_user.id in telegramIDs):
                x = telegramIDs.index(message.from_user.id)+2
                telegramIDs.clear()
                if (wks.cell(x,11).value is None):
                    bot.reply_to(message ,"Now you can book a Tech Summit's ticket 🤍")
                    phone=bot.send_message(chat_id=message.chat.id,text="Please Enter Your Phone Number (Whatsapp) :")
                    bot.register_next_step_handler(phone, setPhone)
                else:
                    bot.reply_to(message,"You have already booked 🙃")
                
            else :
                telegramIDs.clear()
                bot.reply_to(message,text="You are not logged in the bot yet 😢\nLogin >> @ICPCAIET_bot")   
        else : 
            x=bot.reply_to(message, "❌ This command for the BOT only")
            time.sleep(5)
            bot.delete_message(x.chat.id,x.message_id)
            bot.delete_message(x.chat.id,x.reply_to_message.id)
    except :
        err="""
❌ حدث خطأ غير متوقع 

🐞 اذا واجهتك اي مشكلة او تريد الابلاغ عن مشكلة فيمكنك التواصل معي عن طريق المعرف   ⬅️ @M0xYasser
        """
        bot.reply_to(message, err)
##############################################################
#  SET PHONE 
##############################################################
def setPhone (message):
    if (message.text=="/refresh"):
        start(message)
        return
    elif (message.text=="/start"):
        start(message)
        return
    elif (message.text=="/login"):
        login(message)
        return
    elif (message.text=="/handle"):
        handle(message)
        return
    elif (message.text=="/old"):
        old(message)
        return
    elif (message.text=="/tech_summit"):
        booking(message)
        return
    for ids in wks.get_all_records():
        telegramIDs.append(ids["telegram_id"])
    x = telegramIDs.index(message.from_user.id)+2
    telegramIDs.clear()
    wks.update('k'+str(x),str(message.text))
    bot.reply_to(message,"""Your seat on the waiting list has been reserved ✅
We will confirm your reservation as soon as possible 🙏""")

##############################################################
# handel COMMAND 
##############################################################
@bot.message_handler(commands=['handle'])
def handle(message):
    try :
        if  (message.chat.type=="private"):
            for ids in wks.get_all_records():
                telegramIDs_handles[ids["telegram_id"]]=ids["handle_cf"]

            if (telegramIDs_handles[message.from_user.id]):
                telegramIDs_handles.clear()
                bot.send_message(chat_id=message.chat.id,text="**You are already entered handle 😊**",parse_mode="MarkdownV2")   
            else:
                telegramIDs_handles.clear()
                msg=bot.reply_to(message,"Please enter your handle in CodeForces without @ :")
                bot.register_next_step_handler(msg, handle_process)

        else : 
            x=bot.reply_to(message, "❌ This command for the BOT only")
            time.sleep(5)
            bot.delete_message(x.chat.id,x.message_id)
            bot.delete_message(x.chat.id,x.reply_to_message.id)
    except :
        err="""
❌ حدث خطأ غير متوقع 

🐞 اذا واجهتك اي مشكلة او تريد الابلاغ عن مشكلة فيمكنك التواصل معي عن طريق المعرف   ⬅️ @M0xYasser
        """
        bot.reply_to(message, err) 

##############################################################
# handle process
##############################################################
def handle_process (message) :
    if (message.text=="/refresh"):
        start(message)
        return
    elif (message.text=="/start"):
        start(message)
        return
    elif (message.text=="/login"):
        login(message)
        return
    elif (message.text=="/handle"):
        handle(message)
        return
    elif (message.text=="/old"):
        old(message)
        return
    elif (message.text=="/tech_summit"):
        booking(message)
        return
    try :
        for ids in wks.get_all_records():
            telegramIDs.append(ids["telegram_id"])
        x = telegramIDs.index(message.from_user.id)+2
        telegramIDs.clear()
        url = "https://codeforces.com/api/user.info?handles="+message.text    
        response = requests.get(url)
        status = response.json()["status"]
        if (status =="OK"):
            wks.update('H'+str(x),message.text)
            bot.reply_to(message, "Added successfully ✅")
        else :
            err="""
    ❌ حدث خطأ غير متوقع 

            ⬅️  برجاء التاكد من ادخال الهاندل الخاص بك بالشكل الصحيح  ✅

    🐞 اذا واجهتك اي مشكلة او تريد الابلاغ عن مشكلة فيمكنك التواصل معي عن طريق المعرف   ⬅️ @M0xYasser
            """
            bot.reply_to(message, err)
            msg = bot.send_message(chat_id=message.chat.id,text="Please enter your handle in CodeForces without @ :")
            bot.register_next_step_handler(msg, handle_process)
    except:
        err="""
❌ حدث خطأ غير متوقع 

🐞 اذا واجهتك اي مشكلة او تريد الابلاغ عن مشكلة فيمكنك التواصل معي عن طريق المعرف   ⬅️ @M0xYasser
        """
        bot.reply_to(message, err) 


##############################################################
# HOME
##############################################################
   
@bot.message_handler(func=lambda message: True)
def home (message):

    if  (message.chat.type=="private"):
        if (message.text=="/refresh"):
            start(message)
            return
        elif (message.text=="/start"):
            start(message)
            return
        elif (message.text=="/login"):
            login(message)
            return
        elif (message.text=="/handle"):
            handle(message)
            return
        elif (message.text=="/old"):
            old(message)
            return
        elif (message.text=="/tech_summit"):
            booking(message)
            return
        else :
            bot.reply_to(message, """❌ حدث خطأ غير متوقع برجاء كتابة الرسالة في مكانها الصحيح

⏪ قم بالضغط علي /refresh من القائمة""")
            user_err="ERROR Home : \nName : "+str(message.from_user.first_name)+" "+str(message.from_user.last_name)+"\nmsg Error : "+str(message.text)+"\n@"+str(message.from_user.username)+"\n"+str(message.chat.id)
            bot.send_message("""SECRET Telegram ID""",user_err)


##############################################################
######### ########### ### POLLING ### ########### ############
##############################################################

def runBot():
	bot.polling(none_stop=True)

runBot()

