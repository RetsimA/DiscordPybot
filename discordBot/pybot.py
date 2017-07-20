import discord,asyncio
import random
import urllib.request, time, shutil, os
from bs4 import BeautifulSoup
import bs4
import requests
import re
from PIL import Image


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
    
    if msg.startswith('/help'):
        helplist="/urb 'word'; Defines a word using Urban Dictionary\n/map'number' 'coordinates or a location'. -Displays a satellite image at the specified \tzoom level at the specified location. ex: /map15 New York City\n/sp 'word(s)'. -splits a word up by each letter\n\
/img 'word(s)'. -Displays a random image based on your specified word(s)\n/define 'word'. -Defines a word using Dictionary.com\n/verse 'quran' or 'bible'. -Displays a random verse from the specified religious text\n\
/apod 'YYMMDD'. -Displays the Astronomy Picture of the Day and the associated text of the specified date."
        em= discord.Embed(title="A list of the available commands",description=helplist, colour=0x48437)
    
        await client.send_message(ch, embed=em)
#____________________________________________________________________________________________________________________________________________________________________


    if msg.startswith('/punch'):
        await client.delete_message(message)
        
        em= discord.Embed(title="You need to chill out my dude...", colour=0x48437)
        emImg= discord.Embed.set_image(em,url='https://cdn.discordapp.com/attachments/288910294661726219/337451209776431106/eYlX8jHWjNGy48nQAAAABJRU5ErkJggg.png')
        await client.send_message(ch, embed=em)
        
#____________________________________________________________________________________________________________________________________________________________________
        
    if msg.startswith('/flip'):
        try:
            urllib.request.urlretrieve(message.content[6:], "Z:/Py/mainImg.jpg")

            img= Image.open('Z:/Py/mainImg.jpg')
            w= img.size[0]
            h= img.size[1]

            img1= img.crop((0,0,w/2,h))

            img2= img1.transpose(Image.FLIP_LEFT_RIGHT)


            newim= Image.new('RGB',(w,h))
            newim.paste(img1,(0,0))
            newim.paste(img2,(int(w/2),0))

            newim.save("Z:/Py/mainImg.jpg")
            em= discord.Embed(title="!@#", colour=0x48437)
            emImg= discord.Embed.set_image(em,url=newim)

            await client.send_file(ch, 'Z:/Py/mainImg.jpg')
            await client.delete_message(message)
        except Exception as e:
            print(e)
            await client.send_message(ch, 'Sorry an error occurred...')
#Urban Dictionary Search_____________________________________________________________________________________________________________________________________________
    if msg.startswith('/urb'):
        inp=msg[5:]
        await client.delete_message(message)
        tmp= await client.send_message(ch, "Loading urban definition of {0}...".format(msg[5:]))
        try:
            link= 'http://www.urbandictionary.com/define.php?term=','+'.join(inp.split())
            soup3 = requests.get(''.join(link))
            soup= BeautifulSoup(soup3.content,"html.parser")

            text= soup.find('div',{'class':'meaning'}).text.replace('&apos;',''),'\n\n',soup.find('div',{'class':'example'}).text.replace('&apos;','')
            em= discord.Embed(title=msg[5:],description=''.join(text), colour=0x48437)

            await client.delete_message(tmp)
            await client.send_message(ch, embed=em)
        except:
            await client.delete_message(tmp)
            await client.send_message(ch, '{0} is not a word in the Urban Dictionary.\nTry looking up "Ignoramous"...'.format(inp))
#Google Image Search___________________________________________________________________________________________________________________________________________________
            
    if msg.startswith('/map'):
        inp= msg[4:]
        inpNum= inp[0:2]

        
        inp= inp[2:]
        
        inp=inp.replace(' ','')
        link= 'https://maps.googleapis.com/maps/api/staticmap?center=',inp,'&zoom=',inpNum.replace(' ',''),'&size=1000x1000&scale=2&maptype=satellite&key=AIzaSyAYf5mIyC5RJxY-u3xiRPsLfjn6niJ9O4o'
        linkst= 'https://maps.googleapis.com/maps/api/streetview?size=600x300&location=',inp,'&heading=151.78&pitch=-0.76&key=AIzaSyAYf5mIyC5RJxY-u3xiRPsLfjn6niJ9O4o'

        link= ''.join(link)
        linkst= ''.join(linkst)
        

        inp= inp.replace('_',' ')
        em= discord.Embed(title=' '.join(('Zoom level',inpNum,'of',inp)), colour=0x48437)
        emImg= discord.Embed.set_image(em,url=link)
        em2= discord.Embed(title='', colour=0x000DA)
        emImg= discord.Embed.set_image(em2,url=linkst)
        
        

        await client.delete_message(message)
        await client.send_message(ch, embed= em)
        tmp= await client.send_message(ch, embed= em2)


            
        
#S P A C E S_______________________________________________________________________________________________________________________________________________           
    if msg.startswith('/sp'):
        await client.delete_message(message)
        inp= ' '.join(message.content[4:])
        await client.send_message(ch, inp)
        
#Image Search_______________________________________________________________________________________________________________________________________        
    if msg.startswith('/img'):
        flip= False
        if msg[4:].startswith('flip'):
            flip=True
            msg= msg[9:]
        else:
            msg= msg[5:]
        imgs= []

        try:
            await client.delete_message(message)
            tmp= await client.send_message(ch, "Loading image of {0}...".format(msg))
            
            link= 'http://www.bing.com/images/search?q=',msg,'&FORM=RESTAB'
            soup3 = requests.get(''.join(link))
            soup= BeautifulSoup(soup3.content,"html.parser")

            for a in soup.find_all('a', href=True):
                if a['href'].startswith("http://"):
                    if a['href'].endswith(".jpg"):
                        imgs.append(a['href'])
            
            em= discord.Embed(title=msg, colour=0x48437)
            
            emImg= discord.Embed.set_image(em,url=imgs[random.randint(0,len(imgs)-1)])

            if flip==True:
                try:
                    urllib.request.urlretrieve(imgs[random.randint(0,len(imgs)-1)], "Z:/Py/mainImg.jpg")

                    img= Image.open('Z:/Py/mainImg.jpg')
                    w= img.size[0]
                    h= img.size[1]
                    newim= Image.new('RGB',(w,h))
                    img1= img.crop((0,0,w/2,h/2))

                    img2= img1.transpose(Image.FLIP_LEFT_RIGHT)
                    img3= img1.transpose(Image.FLIP_LEFT_RIGHT).rotate(180)
                    img4= img1.rotate(-180)


                    newim= Image.new('RGB',(w,h))
                    newim.paste(img1,(0,0))
                    newim.paste(img2,(int(w/2),0))
                    newim.paste(img3,(0,int(h/2)))
                    newim.paste(img4,(int(w/2),int(h/2)))

                    newim.save("Z:/Py/mainImg.jpg")
                    em= discord.Embed(title="!@#", colour=0x48437)
                    emImg= discord.Embed.set_image(em,url=newim)

                    await client.send_message(ch, msg)
                    await client.send_file(ch, 'Z:/Py/mainImg.jpg')
                    await client.delete_message(tmp)
                    flip= False
                except Exception as e:
                    print(e)
                    await client.send_message(ch, 'Sorry an error occurred...')
                    flip= False
            else:    
                await client.delete_message(tmp)
                await client.send_message(ch, embed=em)
        except Exception as errorMsg:
            print(errorMsg)

            await client.delete_message(tmp)
            await client.send_message(ch, "An error occured, please try again...")
        

#DEFINITION______________________________________________________________________________________________________________________________________
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

#ASTRONOMY PICTURE OF THE DAY______________________________________________________________________________________________________________________      
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
                
#RELIGIOUS TEXT_____________________________________________________________________________________________________________________________________              
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
