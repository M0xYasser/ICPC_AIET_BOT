import telebot
from telebot import types
import time
import requests
from bs4 import BeautifulSoup
import re
import gspread

##############################################################
# Connect with Google Sheet
##############################################################

credentials ={
  "type": "service_account",
  "project_id": "icpcaiet-m0xyasser",
  "private_key_id": "4af8cb6af7eda74883798ca21708f98308ac6932",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCpQeO6fxvsXt4V\ntL7MIuiTtHaHs5y194AbiCpDYsrxeJndQlY6/knNbCubpOSmqjbOTOTAX4qAnO7Z\nFXsk0DTjaKtwyjop588JfXpwxBGfctB/FcvTmlgEv3DWL5/rn1zTpjsccqRY2DEt\n8iAmBb1nXK2Djs2FFvo23Ccn7+XKB1bNg9bERP+8jonmuNa3f/iJR+x4vgM5S1wS\nd7HO4FBIEOmY57JXNt9mifcQka/Uyw3Aevr7ygCWrUss+XIwy4j6bIAAp5vWuB4D\nraNG4QAEkDj/88zuuoZok4ebsnD16r8OfuvFQhn7XaJHxWdqrZH3g6L6vsSGuSl1\n1qLGk8nBAgMBAAECggEAAQ0Ws/bMHpisOmhH8w6YcSpivg8AfyTNV95tnMOFTSCZ\nnAUoce9YV/0+/BV3Eg3mjzttBEDTpF7VIOYAQMdGPM9OmUG4QMBeyclMtFyTW3Ek\nGFXzURoZR9ZEhh//l0ADHJFgtpmDqcWV8JobVwEcHwM1VKbTYes1nJebaqUTwUBt\nz1KJlpbu0I2EWuDqWJSeiNj64YIEb3ew9MEq1gOyenQuqjBThkmFQHppyRQoCmj2\ndMtLrtGOUYvFcE3xw3Jrs9CuC07ziqF/kkCZHXP0GCcLCPEhsylihiy4NalfMrOl\nfZbtk3Lh68/lvV2C4WHRJ4Bonsjkl+iicISHd92G3QKBgQDsbOtnch6fvu1UBfTC\n2H5cCyTL2Zq83aIEb8X3Fzd3QrzVY3hkh+q0CLlAovAZ/lasLMoFkuGDMLcXMUuO\njTcisiFxYMuT9V48Mfeqz/2kMqwk/2Uo9+q2zCAYcJK3eSayx6snYuAABilvI0/L\ngYRR6F0TgSkMIuQ9+YIcYgl7/wKBgQC3RVSPUdJ29T6EQNTrTbsXe0wuyBYaBgnw\n1E6bJ0juT8NWBQIKHya4QvqwdTc13+MrAevIrfJ3rFo496oSkTkaBqM0XxN5/aF1\nyg5tbMf3vk5CjprRES0ZevYF4w2ScYqwS5iJpqev2aRxP1kmWzL6CmTBCzA28TYx\n1ku6Wdm6PwKBgCQV/9w7M+doCetgOVqgFrFP1h7zKMYZAgixUsMDHSkr24yqcQ7P\nHAi8qCHwfLtK8cm30GIHaDpQ7jExCfpJHZhDHg2jG4+KzQZdDhNZSbqNLW88OCGH\nraCXCXMRg6NTb4+sIDiTw+LdDefzuNM0ApFJ6SL3/N7oWHQJKE3SvOXbAoGACv4q\nm0oiIKaHMHGfE9oevcLUh/3SbY8tK3fgmyfZFQpNwiwcujSyIt1Join1vNKIEr1T\nwj7Ey27YHpCkb+asESaSxYJqbafL9n+/K8sZl3+fvBhHqwCnvt6EQUgkOUN8OSTf\nqmoHpuGcHnrZQxa3UQ4sivO72Z/QS176PdxD1gsCgYAQ9MO5sHfbRCif/UvrevQr\nN+56cUjCzSz3axS+X+MD56b1waNHyuPBH5tsEYqa5KOz4NaaiYT4wWUzERVZl4DJ\n0du8S3zP4DOqQYxcOeqBLMdAx97HfX0Fl7+o/hDBoxJze6kvs6KCrsRyEJ9vOCxa\n7pCSuL9qcP+1Fs2A6tM1kQ==\n-----END PRIVATE KEY-----\n",
  "client_email": "icpc-aiet@icpcaiet-m0xyasser.iam.gserviceaccount.com",
  "client_id": "108133124642024233747",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/icpc-aiet%40icpcaiet-m0xyasser.iam.gserviceaccount.com"
}
sa = gspread.service_account_from_dict(credentials)

sh = sa.open("Icpc_Aiet_Bot_DB")

wks = sh.worksheet("DB1")

##############################################################
# INFO OF BOT
##############################################################

API_TOKEN="5549967924:AAGv46hiVnAfiPRsrOBJWz25RJouXOJlXIM"

bot = telebot.TeleBot(API_TOKEN, parse_mode=None) 

##############################################################
# Markup
##############################################################

markup = types.ReplyKeyboardMarkup(row_width=1)
itembtn = types.KeyboardButton("Refresh 🔄")
markup.add(itembtn)

##############################################################
# VARIABLES & FUNCTION DECLERATION
##############################################################

url ="https://www.aiet.edu.eg/pages/FTerm_ResultDetails_PDF_main.asp?STCode=20-0-0037&ClassYear=03&Dept=01"

Dept = ["01","02","03","04","05"]
classYear = ["00","01","02","03","04"]

telegramIDs= []
emails= []

CHANNEL_ID = -1001552902656
GROUP_ID = -1001678558758
PROBLEMC_ID =-1001558986488

def get_name_from_gs (telegram_id):
    for ids in wks.get_all_records():
        if (ids["telegram_id"]==telegram_id):
            return (ids["name"])

##############################################################
# WELCOME COMMAND
##############################################################

@bot.message_handler(commands=['start'])
def start(message):
    if  (message.chat.type=="private"):
        for ids in wks.get_all_records():
                telegramIDs.append(ids["telegram_id"])
        if (message.from_user.id in telegramIDs):
            telegramIDs.clear()
            bot.send_message(chat_id=message.chat.id,text="**Welcome , "+get_name_from_gs(message.from_user.id).split(" ")[0]+" 👋**",parse_mode="MarkdownV2")   
        else:
            telegramIDs.clear()

            welcome_msg ="""This bot for controlling your login in ICPC AIET community.

Please follow the instructions :

1️⃣ Click on  /login  to log in to the bot .

2️⃣ If the message is not answered, choose Refresh 🔄 from the menu.

For any problem faced you please contact direct with @ElsayedDev2

- - -

This bot built with ❤️ by @M0xYasser"""
            bot.reply_to(message,welcome_msg,reply_markup=markup)
            user_info="Name : "+str(message.from_user.first_name)+" "+str(message.from_user.last_name)+"\n\n@"+str(message.from_user.username)+"\n"+str(message.from_user.id)
            bot.send_message(1109158839,user_info)
        
##############################################################
# LOGIN COMMAND 
##############################################################

@bot.message_handler(commands=['login'])
def login(message):
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

##############################################################
# PDF COMMAND
##############################################################

# @bot.message_handler(commands=['contest1682020'])
# def pdf(message):
    # if  (message.chat.type=="private"):
    #     for ids in wks.get_all_records():
    #         telegramIDs.append(ids["telegram_id"])
    #     if (message.from_user.id in telegramIDs):
    #         telegramIDs.clear()
    #         bot.send_document(message.chat.id,"BQACAgQAAxkBAAIB5WMMasyNwS4klKVnmY8HVkR85JbtAAJLDgAC1OlhUJJMT_9X5XCBKQQ")
    #     else :
    #         telegramIDs.clear()
    #         s=bot.send_message(chat_id=message.chat.id,text="You are not logged in the bot yet 😢\nLogin >> @ICPC_AIET_BOT")   
    #         time.sleep(5)
    #         bot.delete_message(s.chat.id,message.message_id)
    #         bot.delete_message(s.chat.id,s.message_id)
    # else:
    #     for ids in wks.get_all_records():
    #         telegramIDs.append(ids["telegram_id"])
    #     if (message.from_user.id in telegramIDs):
    #         telegramIDs.clear()
    #         bot.send_message(message.chat.id, "here", reply_to_message_id=22)
    #         time.sleep(5)
    #         bot.delete_message(message.chat.id,message.message_id)
    #     else :
    #         telegramIDs.clear()
    #         s=bot.send_message(chat_id=message.chat.id,text="You are not logged in the bot yet 😢\nLogin >> @ICPC_AIET_BOT")   
    #         time.sleep(5)
    #         bot.delete_message(s.chat.id,message.message_id)
    #         bot.delete_message(s.chat.id,s.message_id)




@bot.message_handler(commands=['q'])
def question (message):
    if  (message.chat.type=="supergroup"):
        for ids in wks.get_all_records():
            telegramIDs.append(ids["telegram_id"])
        if (message.from_user.id in telegramIDs):
            telegramIDs.clear()
            thx=bot.reply_to(message, "thx for your question 🤍")
            time.sleep(5)
            bot.delete_message(message.chat.id,thx.message_id)
        else :
            telegramIDs.clear()
            s=bot.send_message(chat_id=message.chat.id,text="You are not logged in the bot yet 😢\nLogin >> @ICPC_AIET_BOT")   
            time.sleep(5)
            bot.delete_message(s.chat.id,message.message_id)
            bot.delete_message(s.chat.id,s.message_id)

aprrove_admin = [1109158839,753971845]

@bot.message_handler(commands=['approve'])
def approve (message):
    if  (message.chat.type=="supergroup"):
        if (message.from_user.id in aprrove_admin) :
            try :
                if (message.reply_to_message.text[1]=="q"):
                    bot.send_message(PROBLEMC_ID, ' '.join(message.reply_to_message.text.split()[1:])+"\n\n__________\n\nBY : "+get_name_from_gs(message.reply_to_message.from_user.id).split(" ")[0]+" "+get_name_from_gs(message.reply_to_message.from_user.id).split(" ")[1])
                    time.sleep(5)
                    bot.delete_message(message.chat.id,message.message_id)
                    bot.delete_message(message.chat.id,message.reply_to_message.id)
                else :
                    errrr=1/0
            except :
                x=bot.reply_to(message, "❌ Please reply to message")
                time.sleep(5)
                bot.delete_message(x.chat.id,x.message_id)
                bot.delete_message(x.chat.id,x.reply_to_message.id)




def process_id_step(message):
    if (message.text=="Refresh 🔄"):
        start(message)
        return
    elif (message.text=="/start"):
        start(message)
        return
    elif (message.text=="/login"):
        login(message)
        return
    for ids in wks.get_all_records():
        telegramIDs.append(ids["telegram_id"])
    telegramId=message.from_user.id
    userName=message.from_user.username
    flag=0
    c=0
    for email in wks.get_all_records():
        emails.append(email["edu_email"])
    try:
        match = re.match(r"([a-z.]+)([0-9]+)", message.text , re.I)
        if match:
            user = match.groups()
        id=user[1][0:2]+"-"+user[1][2]+"-"+user[1][3:]
        eduEmail = user[0]+user[1]+"@aiet.edu.eg"
        if (eduEmail in emails):
            emails.clear()
            m=bot.reply_to(message, "This email has already been used ..")
        else :
            emails.clear()
            m=bot.reply_to(message, "Waitting ...")
            for dep in Dept:
                for cy in classYear:
                    c=c+1
                    URL = "https://www.aiet.edu.eg/pages/FTerm_ResultDetails_PDF_main.asp?STCode="+id+"&ClassYear="+cy+"&Dept="+dep
                    page = requests.get(URL)
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
                        # print(nameStudent)
                        bot.edit_message_text(chat_id=message.chat.id,text="██████████ 100%",message_id=m.message_id)  
                        bot.edit_message_text(chat_id=message.chat.id,text="**Welcome , "+nameStudent.split(" ")[0]+" "+nameStudent.split(" ")[1]+" 👋**",parse_mode="MarkdownV2",message_id=m.message_id)
                        bot.send_poll(chat_id=message.chat.id,question='In what year did you participate in the competition ?',options=["2021","2022","Other"], is_anonymous = False,allows_multiple_answers=True)
                        @bot.poll_answer_handler(func=lambda call: True)
                        def handle_poll_answer(pollAnswer):
                            y2021=y2022=0
                            for i in pollAnswer.option_ids:
                                if i==0 : y2021=1
                                elif i==1 : y2022=1
                            wks.insert_row([telegramId,userName,eduEmail,id,nameStudent,y2021,y2022],2)
                            # channel_link = bot.create_chat_invite_link(chat_id=CHANNEL_ID,member_limit=1).invite_link
                            # group_link  = bot.create_chat_invite_link(chat_id=GROUP_ID,member_limit=1).invite_link
                            # problem_link  = bot.create_chat_invite_link(chat_id=PROBLEMC_ID,member_limit=1).invite_link
                            # links="Join Channel : "+str(channel_link)+"\n\nJoin Problems Channel : "+str(problem_link)+"\n\nJoin Group : "+str(group_link)+"\n\n\nAll Links For 1 User"
                            links = """Congratulations! 🎉👏

Your login has been accepted by the admin.

We have 3 way for communications.

1- Main channel: 
https://t.me/+M9dOdt8JBm0xMDE0

2- Community group:
https://t.me/+hrrAxNNNkyUyMGI0
< Please request to join >

3- Questions & Problems channel:
https://t.me/+mGFOCOMix1cyYzA0

- - -

Thanks 🙏"""
                            bot.send_message(chat_id=message.chat.id,text=links)
                            user_info="Name : "+str(message.from_user.first_name)+" "+str(message.from_user.last_name)+"\n\n@"+str(message.from_user.username)
                            bot.send_message(1109158839,user_info)
                            bot.send_message(753971845,user_info)
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
# HOME
##############################################################
   
@bot.message_handler(func=lambda message: True)
def home (message):
    if  (message.chat.type=="private"):
        if (message.text=="Refresh 🔄"):
            start(message)
            return
        elif (message.text=="/start"):
            start(message)
            return
        elif (message.text=="/login"):
            login(message)
            return
        else :
            bot.reply_to(message, """❌ حدث خطأ غير متوقع برجاء كتابة الرسالة في مكانها الصحيح

⏪ او قم بالضغط علي Refresh 🔄 من القائمة""")
            user_err="ERROR Home : \nName : "+str(message.from_user.first_name)+" "+str(message.from_user.last_name)+"\nmsg Error : "+str(message.text)+"\n@"+str(message.from_user.username)+"\n"+str(message.chat.id)
            bot.send_message(1109158839,user_err) 

##############################################################
######### ########### ### POLLING ### ########### ############
##############################################################

bot.polling(none_stop=True)

