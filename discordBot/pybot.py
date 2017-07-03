import discord,asyncio
import random, re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import urllib.request, time, shutil, os

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


client= discord.Client()
#ANY TIME A USER SENDS A MESSAGE------------------------------------------------------------------------------------
@client.event #THIS LINE AND ASYNC ON THE NEXT LINE ARE REQUIRE FOR FUNCTIONS
async def on_message(message):
    
    msg= (message.content).lower()
    user= message.author.name
    
    #Translate function------------------------------------------------------------------------
    if msg.startswith("/verse"):
        inp= msg[7:]
        if inp.lower() == "bible":
            
            await client.delete_message(message)
            tmp= await client.send_message(message.channel, "Loading Holy Text...")
        
            browser= webdriver.Firefox()
            browser.get("https://dailyverses.net/random-bible-verse")
            verse= browser.find_element_by_css_selector(".bibleVerse")
            splita= str(verse.text)

            a= splita.split('.')[0]
            b= splita.split('.')[1]
            g= b.split(' | ')[0]
            
            await client.delete_message(tmp)
            em= discord.Embed(title= a , description=g, colour=0x23456)
            await client.send_message(message.channel, embed=em)
            
            #await client.send_message(message.channel, g)
            browser.quit()
        elif inp.lower() == 'quran':
            await client.delete_message(message)
            tmp= await client.send_message(message.channel, "Loading Holy Text...")
            browser= webdriver.Firefox()

            browser.get("http://ayatalquran.com/random")
            j= browser.find_element_by_id("aya_text").text
            f= browser.find_element_by_id("aya_footnote").text

            em= discord.Embed(title= j , description=f, colour=0xBAD69)
            await client.send_message(message.channel, embed=em)
            browser.quit()
            
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


#REQUIRED TO START BOT --------------------------------------------------
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
client.run('MzI4MzExOTgxMTg4ODQxNDgy.DDRtOQ.abeJ3CSJ9k5XoHHxWk6ZkfOjK0U')
#------------------------------------------------------------------------


#PROFANITY FILTER; UNDER CONSTRUCTION
'''
    for a in range(21):
        if words[a] in msg:
            em= discord.Embed(title= user, description=phrases[random.randint(0,3)], colour=0xFE34A)
            await client.send_message(message.channel, embed=em)
            userCuss(user)
            break
'''
#PROFANITY POINTS; UNDER CONSTRUCTION; UNUSED
'''                                  
def userCuss(user):
    users= {}
    
    cussAmt = 1
    if user in users:
        #users.update({user:})
        print(users)
    else:
        users.update({user:cussAmt})
        print(users)
#http://www.nocussing.com/becomeafreemember/beamember.html
'''    
#REFERENCE FOR SENDING MESSAGES; UNUSED
'''
counter = 0
tmp = await client.send_message(message.channel, 'Calculating messages...')
async for log in client.logs_from(message.channel, limit=100):
if log.author == message.author:
counter += 1
await client.edit_message(tmp, 'You have {} messages.'.format(counter))
elif message.content.startswith('!sleep'):
await asyncio.sleep(5)
await client.send_message(message.channel, 'Done sleeping')
'''
