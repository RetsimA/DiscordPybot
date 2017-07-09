import discord,asyncio
import random
import urllib.request, time, shutil, os
from bs4 import BeautifulSoup
import bs4
import requests
import re


client= discord.Client()
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event #THIS LINE AND ASYNC ON THE NEXT LINE ARE REQUIRE FOR FUNCTIONS
#ANY TIME A USER SENDS A MESSAGE
async def on_message(message):
    
    msg= (message.content).lower()
    user= message.author.name
    ch= message.channel

    if msg.startswith('/sp'):
        await client.delete_message(message)
        inp= ' '.join(message.content[4:])
        await client.send_message(ch, inp)
        
    if msg.startswith('/img'):
        imgs= []

        try:
            await client.delete_message(message)
            tmp= await client.send_message(ch, "Loading image of {0}...".format(msg[5:]))
            
            link= 'http://www.bing.com/images/search?q=',msg[5:],'&FORM=RESTAB'
            soup3 = requests.get(''.join(link))
            soup= BeautifulSoup(soup3.content,"html.parser")

            for a in soup.find_all('a', href=True):
                if a['href'].startswith("http://"):
                    if a['href'].endswith(".jpg"):
                        imgs.append(a['href'])
            
            em= discord.Embed(title=msg[5:], colour=0x48437)
            emImg= discord.Embed.set_image(em,url=imgs[random.randint(0,len(imgs))])

            await client.delete_message(tmp)
            await client.send_message(ch, embed=em)
        except Exception as errorMsg:
            print(errorMsg)

            await client.delete_message(tmp)
            await client.send_message(ch, "An error occured, please try again...")
        
        
    #DEFINITION___________
    if msg.startswith("/define"):
        try:
            inp= msg[8:]
            await client.delete_message(message)
            tmp= await client.send_message(ch, "Defining {0}...".format(inp))
            
            soup3 = requests.get(''.join(('http://www.dictionary.com/browse/',inp)))
            soup= BeautifulSoup(soup3.content,"html.parser")

            b= soup.find('span',{'class' : 'dbox-pg'})
            b= (' '.join(b.get_text().split())).replace('. ', '.\n')


            a= soup.find('div',{'class' : 'def-content'})
            a= (' '.join(a.get_text().split())).replace('. ', '.\n')

            em= discord.Embed(title= '- '.join((inp,b)) , description=a, colour=0xABCDE)
            
            await client.delete_message(tmp)
            await client.send_message(ch, embed=em)

        except:
            await client.delete_message(tmp)
            await client.send_message(ch, "No definition of {0}.".format(inp))

    #ASTRONOMY PICTURE OF THE DAY____________       
    if msg.startswith("/apod"):
        inp= msg[6:]
        
        if len(inp)<6 or len(inp)>6:
            await client.send_message(ch, "Incorrect format; /apod YYMMDD")
            await client.delete_message(message)
            
        else:
            if inp.isdigit():
                try:
                    date= [inp[i:i+2] for i in range(0, len(inp), 2)]
                    tmp= await client.send_message(ch, "Loading Astronomy Picture of the Day from {0}.".format('/'.join(date)))
                    
                    link= ''.join(('https://apod.nasa.gov/apod/ap',inp,'.html'))

                    soup3 = requests.get(link)
                    soup= BeautifulSoup(soup3.content,"html.parser")
                    
                    imgLink= ''.join(('https://apod.nasa.gov/',str((soup.find_all("a", href=True))[1]).split('="')[1].split('">')[0]))
                    
                    text= " ".join((re.sub('<[^>]+>', '', str((soup.find_all('p'))[2]))).split())
                    text= text.split("Tomorrow's picture:")[0].split("digg")[0]
                    text= text.replace("Explanation: ","").replace(". ",".\n\n").replace("? ","?\n\n").replace("! ","!\n\n")

                    em= discord.Embed(title= '/'.join(date), description=text, colour=0x48437)
                    emImg= discord.Embed.set_image(em,url=imgLink)                    

                    await client.delete_message(tmp)
                    await client.send_message(ch, embed=em)
                    
                except IndexError:
                    
                    client.send_message(ch, 'Incorrect format; /apod YYMMDD')
                    await client.delete_message(message)
                    
            elif not inp.isdigit():
                
                await client.send_message(ch, "Incorrect format; /apod YYMMDD")
                await client.delete_message(message)
                
    #RELIGIOUS TEXT___________________              
    if msg.startswith("/verse"):
        inp= msg[7:]

        #BIBLE______________
        if inp.lower() == "bible":
            
            await client.delete_message(message)
            req= requests.get('https://dailyverses.net/random-bible-verse')
            soup= BeautifulSoup(req.content,"html.parser")

            verse= str(soup.select('.bibleVerse'))
            verse= verse.split('[<div class="bibleVerse">')[1].split('<div class')[0]
            verse= verse.replace("<br/>"," ")

            verse2= str(soup.select('.bibleChapter'))
            verse2= re.sub('<[^>]+>', '', verse2)
            verse2= verse2.split('[')[1].split('|')[0]
            
            em= discord.Embed(title= verse , description= verse2, colour=0x48437)
            await client.send_message(ch, embed=em)
            
        #QURAN____________    
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
            await client.send_message(ch, embed=em)
    
client.run('MzI4MzExOTgxMTg4ODQxNDgy.DERF0w.OXEv3Ee4aIFfVrDKAxxzjevXt88')
