import discord,asyncio
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import urllib.request, time, shutil, os
from bs4 import BeautifulSoup
import bs4
import requests
from lxml import html
import re


client= discord.Client()

#ANY TIME A USER SENDS A MESSAGE------------------------------------------------------------------------------------
@client.event #THIS LINE AND ASYNC ON THE NEXT LINE ARE REQUIRE FOR FUNCTIONS
async def on_message(message):
    
    msg= (message.content).lower()
    user= message.author.name

    if msg.startswith("/apod"):
            inp= msg[6:]

            
            link= 'https://apod.nasa.gov/apod/ap',inp,'.html'
            print(''.join(link))
            soup3 = requests.get(''.join(link))
            soup= BeautifulSoup(soup3.content,"lxml")
            img= str(soup.findAll('a',{"href":True}))
            imglink= img.split('src="')[1].split('"/>')[0]
            imggoto= "https://apod.nasa.gov/apod/",imglink
            imggoto= "".join(imggoto)
            imggoto= imggoto.replace(" ", "")
            
            imggoto= imggoto.replace('"style="max-width:100%', "")
            print(imggoto)
            await client.send_message(message.channel, imggoto)
            
    if msg.startswith("/verse"):
        inp= msg[7:]
        if inp.lower() == "bible":
            
            await client.delete_message(message)
            req= requests.get('https://dailyverses.net/random-bible-verse')
            soup= BeautifulSoup(req.content,"lxml")

            verse= str(soup.select('.bibleVerse'))
            verse= verse.split('[<div class="bibleVerse">')[1].split('<div class')[0]
            verse= verse.replace("<br/>"," ")
            verse= verse.replace("God", user)
            verse= verse.replace("Jesus", user)
            verse= verse.replace("Lord", user)
            verse= verse.replace("lord", user)
            verse= verse.replace("jesus", user)

            verse2= str(soup.select('.bibleChapter'))
            verse2= re.sub('<[^>]+>', '', verse2)
            verse2= verse2.split('[')[1].split('|')[0]
            em= discord.Embed(title= verse , description= verse2, colour=0x48437)
            await client.send_message(message.channel, embed=em)
            
        elif inp.lower() == 'quran':
            
            await client.delete_message(message)
            req= requests.get('http://ayatalquran.com/random')
            soup= BeautifulSoup(req.content,"html.parser")
            verse= str(soup.select('#aya_text'))
            verse= verse.split('[<h2 id="aya_text">')[1].split('</h2>]')[0]

            book1= str(soup.select('#sura_id'))
            book1= book1.split('[<span id="sura_id">')[1].split('</span>]')[0]
            book2= str(soup.select('#verse_id'))
            book2= book2.split('[<span id="verse_id">')[1].split('</span>]')[0]

            book= "The Holy Quran ",book1,":",book2
            em= discord.Embed(title= verse , description="".join(book), colour=0x48437)
            await client.send_message(message.channel, embed=em)
            
            
words= ['cock','pussy','fuck','shit','damn','hell','cunt','bitch','ass', 'nazi','nigger','nigga','jap','gook','zipperface','wigger','skinhead','fag','twat','dammit','nig ']
phrases= ["this is a friendly progressive channel, please don't use that kind of deprecated language.",
          "please dont speak like that, we are a Christian channel",
          "don't use that kind of language, please.",
          "do I need to bring out the soap?"]
languages= ["arabic","hebrew","haitian creole","greek","german",
            "french","finnish","estonian","dutch","danish",
            "czech","catalan","bulgarian","hindi",
            "urdu","ukranian","turksih","thai","swedish",
            "spanish","slovenian","slovak","russian","romanian",
            "portuguese","polish","persian","norwegian",
            "maltese","malay","lithuanian","latvian","korean",
            "klingon","japanese","italian","indonesian","hungarian"]
            
users= []
#languages= open("languages.txt","r")

#REQUIRED TO START BOT --------------------------------------------------
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
client.run('MzI4MzExOTgxMTg4ODQxNDgy.DDRtOQ.abeJ3CSJ9k5XoHHxWk6ZkfOjK0U')
#------------------------------------------------------------------------

#Translate function------------------------------------------------------------------------        
'''
if msg.startswith("/tr"):
    
    if msg.startswith("/trlist"):
        await client.send_message(message.channel, "\n".join(languages))
        
    else:
        inp= msg[4:] #REMOVES THE FIRST 4 CHARACTERS OF THE STRING; ie. REMOVES /tr FROM USER INPUT
        
        if ";" not in inp:
            await client.send_message(message.channel, 'Incorrect Format. Correct format: \n/tr "language" ; "text to be translated"')

        #REMINDER! ADD CHECK FOR MULTIPLE SEMICOLONS    
        else:
            #THESE TWO LINES SEPERATE THE INPUT INTO A STRING ARRAY WITH THE SEMICOLON AS THE IDENTIFIER OF WHERE TO SPLIT
            #0 AND 1 DESCRIBE THE LEFT AND RIGHT SIDE OF THE SEMICOLON
            inpLang= inp.split(';')[0]
            inpText= inp.split(';')[1]

            #THIS IF CHECKS IF THE USER INPUT IS EMPTY OR IF IT IS EMPTY SPACES
            if inpText.isspace() or not inpText:
                await client.send_message(message.channel, 'Text to translate cannot be blank.')
                
            else:    
                for a in range(38):
                    if languages[a] in inpLang:
                        print(inpText,languages[a],sep= ' : ')
                        await client.delete_message(message)
                        
                        await translate(user, languages[a], inpText, message.channel) #CALLS THE TRANSLATE FUNCTION WHICH ACITVATES SELENIUM
                        break
                    
                    #IF THE FOR LOOP REACHES THE END, THE INPUT LANGUAGE WAS NOT FOUND
                    if a == 37:
                        await client.send_message(message.channel, "{0} is not an available language.\nType /trhelp to see a list of available languages.".format(inpLang))
                        
async def translate(user,language,text,channel):
    
    tmp= await client.send_message(channel, "Loading translation of '{0}'".format(text))
    
    url= "http://translate.reference.com/english/",language.strip(),"/",text
    browser= webdriver.Firefox()
    browser.get("".join(url))
    
    translated= browser.find_element_by_id("clipboard-text").text
    await client.edit_message(tmp, "Translated!")

    string= user,",",'"',text,'"'," in ", language, " is..."
    em= discord.Embed(title= " ".join(string) , description=translated, colour=0xFE34A)
    await client.send_message(channel, embed=em)
    browser.quit()
    
    return str(translated)#RETURNS THE TRANSLATED TEXT
'''
#PROFANITY FILTER; UNDER CONSTRUCTION
'''
    for a in range(21):
        if words[a] in msg:
            em= discord.Embed(title= user, description=phrases[random.randint(0,3)], colour=0xFE34A)
            await client.send_message(message.channel, embed=em)
            userCuss(user)
            break
'''
