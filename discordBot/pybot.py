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
        inp= msg[4:]
        inp= ' '.join(inp)
        await client.send_message(ch, inp)
        
    if msg.startswith('/img'):
        try:
            inp= msg[5:]
            link= 'https://www.flickr.com/search/?advanced=1&dimension_search_mode=min&height=1920&width=1080&text=',inp
            print(''.join(link))
            soup3 = requests.get(''.join(link))
            soup= BeautifulSoup(soup3.content,"html.parser")

            b= str(soup.find('div',{'class' : 'view photo-list-photo-view requiredToShowOnServer awake'}))
            b= b.split("url(//")[1].split(')">')[0]
            b='https://',b
            print(''.join(b))
            em= discord.Embed(title=inp, colour=0x48437)
            emImg= discord.Embed.set_image(em,url=''.join(b))
            await client.send_message(ch, embed=em)
        except:
            
            await client.send_message(ch, "Try another search input.")
        
    #DEFINITION___________
    if msg.startswith("/define"):
        try:
            await client.delete_message(message)
            inp= msg[8:]
            link= 'http://www.dictionary.com/browse/',inp
            print(''.join(link))
            soup3 = requests.get(''.join(link))
            soup= BeautifulSoup(soup3.content,"lxml")

            b= soup.find('span',{'class' : 'dbox-pg'})
            b= ' '.join(b.get_text().split())
            b=b.replace('. ', '.\n')

            a= soup.find('div',{'class' : 'def-content'})
            a= ' '.join(a.get_text().split())
            a=a.replace('. ', '.\n')

            word= inp,b
            em= discord.Embed(title= '- '.join(word) , description=a, colour=0xABCDE)
            await client.send_message(ch, embed=em)
        except:
            await client.send_message(ch, "No definition of {0}".format(inp))

    #ASTRONOMY PICTURE OF THE DAY____________       
    if msg.startswith("/apod"):
        inp= msg[6:]
        if len(inp)<6 or len(inp)>6:
            await client.send_message(ch, "Incorrect format; /apod YYMMDD")
            await client.delete_message(message)
        else:
            if inp.isdigit():
                try:
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
                    
                    do= soup.find_all('p')
                    do2= str(do[2])
                    do2= re.sub('<[^>]+>', '', do2)
                    do2= do2.split()
                    do2= " ".join(do2)
                    do2= do2.replace(". ",".\n\n")
                    do2= do2.replace("? ",".\n\n")
                    do2= do2.replace("! ",".\n\n")
                    do2= do2.replace("Explanation: ","")

                    
                    em= discord.Embed(description=do2, colour=0x48437)
                    emImg= discord.Embed.set_image(em,url=imggoto)                    

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
            soup= BeautifulSoup(req.content,"lxml")

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
    
client.run('MzI4MzExOTgxMTg4ODQxNDgy.DDRtOQ.abeJ3CSJ9k5XoHHxWk6ZkfOjK0U')
