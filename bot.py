#!/usr/bin/env python

import praw,time,os,requests,config,re

def login():
    print("Logging in...")
    r = praw.Reddit(username = config.username,
                   password = config.password,
                   client_id = config.client_id,
                   client_secret = config.client_secret,
                   user_agent = config.user_agent)
    
    print("Logged in...")
    return r



def get_weather(city):
    url = "http://api.openweathermap.org/data/2.5/weather?appid="+config.api_key+"&units=metric&format=json&q="+city
    req = requests.get(url)
    weather = {}
    if req.status_code == 200:
        weather['temp'] = req.json()['main']['temp']
        weather['desc'] = req.json()['weather'][0]['description']
        weather['city'] = req.json()['name']
        weather['country'] = req.json()['sys']['country']
        return weather
    else:
        return 'Unable to get weather data'
    

def conversion(w):
    
    return (w*1.8)+32
    
    
def run_bot(r,comments_store):
    pattern = "((w|W)4|(w|W)eather of)\s([A-z]+)"
    
    for comment in r.subreddit('test').comments(limit=25):
        m = re.search(pattern,comment.body)
        
        if m != None and comment.id not in comments_store and comment.author != r.user.me():
            print("String found!")
            city = m.group(4)
            print("City = "+city)
            weather = get_weather(city)
            comment.reply("**"+str(weather['temp']) + "C/"+ str(round(conversion(weather['temp']),2))+"F "+u"\u2022 "+weather['desc']+" ~** "+weather['city']+", "+weather['country']+". \n ***\n I'm a Bot. Weather provided from [openweather.org](https://openweathermap.org/)")
            print("Reply successfull")
            
            comments_store.append(comment.id)
            
            with open('list_of_ids.txt','a') as f:
                f.write(comment.id + "\n")
                
    
    print("Sleeping for 10sec")
    time.sleep(10)

    

def get_comments():
    if not os.path.isfile('list_of_ids.txt'):
        comments_store = []
    else:
        with open('list_of_ids.txt','r') as f:
            comments_store = f.read()
            comments_store = comments_store.split('\n')
            comments_store = filter(None,comments_store)
    
    return comments_store
    



reddit = login()
comments_store = get_comments()
while True:
    run_bot(reddit,comments_store)
