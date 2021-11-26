# import sys
from flask import Flask, render_template, request
# import numpy as np
import requests
from random import randint
import time
# from db.mongo import Person

sender = randint(1000, 10000)
app = Flask(__name__)


def restart_session():
    global sender
    sender = randint(10000, 100000)
    print("\n\n\n")
    print(f"Sender id reset to {sender}")
    print("\n\n\n")
    return "Success"


@app.route("/")
def home():
    return render_template("index.html")


name = "Irfan__123__467"
phone = 123467890


@app.route("/get")
def get_bot_response():
    user_text = request.args.get('msg')

    print(f"{__file__} : User :: {user_text}")
    try:
        print(f"\nCurrent sender id {sender}")
        r = requests.post("http://localhost:5005/webhooks/myio/webhook", json={"message": user_text, "sender": sender, "name": name, "phone": phone})
        text = r.json()
        print("\n *************** Response from RASA !!!!", text)
        final_text = ""
        for t in text:
            final_text += t['text'] + "\n"
        
        if final_text == "":
            final_text = "Sorry, Seems like my connection lost!! Please come back later 🙏"

        return_this = '<p class="botText"><span>' + final_text + '</span></p>'
        return_this = return_this.replace("\n", "<br>")
        # print(return_this)
        if len(r.json()) > 0:
            for each in r.json():
                print("each:::", each)
                if 'buttons' in each.keys():
                    buttons = each['buttons']
                    # for i in each:
                    #     buttons.extend(i['buttons'])
                    print("Buttons")
                    print(buttons)

                    for button in buttons:
                        print(button)
                        return_this += '<button class="botButtons" mapto="' + button['payload'] +\
                            '" onclick="BotButtonClicked(this);">' + button['title']+'</button>'

    except Exception as e:
        print(f"Exception while getting response {e}")
    
        final_text = "Sorry, Seems like my connection lost!! Please come back later 🙏"

        return_this = '<p class="botText"><span>' + final_text + '</span></p>'

    print(f"\n{__file__} : Bot :: {final_text}")
    return return_this
    

@app.route("/welcome_messages")
def welcome_messages():
    number = request.args.get('number')
    type_ = request.args.get('type')
    number = int(number)
    print(f"\n{number}*-*-*-*-*-*-*-*- TYPE : {type_} ")

    if type_ == "configure":
        m1 = f"Hello! {name}! Mr.Gupta has diagnosed you with MRI. Your Diginurse will be with you through out the treatment period overseeing your recovery."
    
        m2 = "During your treatment period I'll assist you with keep track of your medications, logging your vitals and symptoms and provide you with recommendations on your diet and lifestyle"
    
        m3 = "Are you ready to setup your personalized nursing plan? It’ll only take few minutes."
        if number == 1:
            print("returning " + m1)
            time.sleep(1)
            return m1
        elif number == 2:
            print("returning " + m2)
            time.sleep(1)
            return m2
        elif number == 3:
            print("returning " + m3)
            time.sleep(1)
            return m3
    elif type_ == "new_treatment":
        m1 = f"Dear {name}! during visit to Hospital, Dr.Gupta has diagnosed with MRI"
        m2 = "\nDuring your treatment period I will help you to get recovered. I will assist you in keeping track of your medication, logging your vitals and symptoms and provide you with recommendations on your diet and lifestyle"
        m3 = "\nHere is the routine and lifestyle you have shared with me last time"

        m3 += "<br><strong class=\"imp\"> Wake Up   : 6:00 - 7:00 </strong>"
        m3 += "<br><strong class=\"imp\"> BreakFast : 8:00 - 9:00 </strong>"
        m3 += "<br><strong class=\"imp\"> Lunch     : 11:00 - 12:00 </strong>"
        m3 += "<br><strong class=\"imp\"> Workout   : 13:00 - 14:00 </strong>"
        m3 += "<br><strong class=\"imp\"> Dinner    : 18:00 - 19:00 </strong>"
        m3 += "<br><strong class=\"imp\"> Bed Time  : 23:00 - 00:00 </strong>"
        m3 += "<br><strong class=\"imp\"> Smoke     : Regular </strong>"
        m3 += "<br><strong class=\"imp\"> Alcohol   : Daily </strong>"
        m3 += "\nHave you changed anything in your routine or lifestyle from last time?"
        if number == 1:
            print("returning " + m1)
            time.sleep(1)
            return m1
        elif number == 2:
            print("returning " + m2)
            time.sleep(2)
            return m2
        elif number == 3:
            print("returning " + m3)
            time.sleep(3)
            return m3
    elif type_ == "nursing_round":
        m1 = f"Good Morning {name}! How are you feeling today ?"
        print("returning " + m1)
        return m1
    return "Hello, Welcome to the Chatbot"


@app.route("/restart")
def restart():
    return restart_session()
    

if __name__ == "__main__":
    app.run(debug=True)
