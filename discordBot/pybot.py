import discord,asyncio
import random
import urllib.request, time, shutil, os
from bs4 import BeautifulSoup
import bs4
import requests
import re, io
from PIL import Image
import goslate

img=0
h=0
w=0

def translate(inp):
    g= goslate.Goslate()
    inp = str(g.translate(inp,'fr'))
    return inp
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

    if msg.startswith('/wiki'):
        inp=msg[6:]
        print(inp)
        link= ''.join(('https://en.wikipedia.org/wiki/Special:Random'))
        
        soup3 = requests.get(link)
        print(soup3.url)
        soup= BeautifulSoup(soup3.content,"html.parser")
        words= []
        link = soup.find_all('p')
        for a in range(len(link)):
            words.append(link[a].get_text())
        s= soup.find('h1',{'id':'firstHeading'}).text
        d= '\n'.join(words)
        url= soup3.url
        
        em= discord.Embed(title= s ,description=d, colour=0x000DA)
        fm= discord.Embed.set_footer(em,text= url)

        await client.send_message(ch, embed=em)

        await client.delete_message(message)

#___________________________________________________________________________________________________________________________

    if msg.startswith('/vid'):
        inp=msg[5:]

        await client.delete_message(message)
        
        tmp= await client.send_message(ch, "Loading...".format(msg))
        
        link= 'http://www.bing.com/videos/search?q=',inp,'&qs=n&form=QBVLPG&sp=-1&pq=animal&sc=8-5&sk=&cvid=16424F2262AA469C81860655F851BDB5'
        print(link)
        soup3 = requests.get(''.join(link))
        soup= BeautifulSoup(soup3.content,"html.parser")
        words= []

        for a in soup.find_all('a', href=True):
            if a['href'].startswith('http') and not(a['href'].startswith('http://go')):
                
                words.append(a['href'])
        print('\n'.join(words))

        link=words[random.randint(0,len(words)-1)]
        print(link)


        await client.delete_message(tmp)
        await client.send_message(ch, link)






#_____________________________________________________________________________________________________________________________________
    
    if msg.startswith('/help'):
        helplist="/urb 'word'; Defines a word using Urban Dictionary\n/map'number' 'coordinates or a location'. -Displays a satellite image at the specified \tzoom level at the specified location. ex: /map15 New York City\n/sp 'word(s)'. -splits a word up by each letter\n\
/img 'word(s)'. -Displays a random image based on your specified word(s)\n/define 'word'. -Defines a word using Dictionary.com\n/verse 'quran' or 'bible'. -Displays a random verse from the specified religious text\n\
/apod 'YYMMDD'. -Displays the Astronomy Picture of the Day and the associated text of the specified date."
        em= discord.Embed(title="A list of the available commands",description=helplist, colour=0x48437)
    
        await client.send_message(ch, embed=em)
        
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

        images=[]

        for a in range(0,360,36):
            linkst= 'https://maps.googleapis.com/maps/api/streetview?size=650x650&location=',inp,'&heading=',str(a),'&pitch=0&key=AIzaSyAYf5mIyC5RJxY-u3xiRPsLfjn6niJ9O4o'
            linkst= ''.join(linkst)
            
            with urllib.request.urlopen(linkst) as url:
                f = io.BytesIO(url.read())
            im= Image.open(f)
            images.append(im)
            #imageio.mimsave('img.gif', images, duration=10)
        im.save('/home/ubuntu/DiscordPybot/mapImg.jpg', save_all=True, append_images=images, loop=0, subrectangles=True, duration=500)
        print("done")
        em2= discord.Embed(title='', colour=0x000DA)
        emImg= discord.Embed.set_image(em2,url=linkst)
        
        

        await client.delete_message(message)
        await client.send_message(ch, embed= em)
        await client.send_file(ch,'/image.gif')
        

            
        
#S P A C E S_______________________________________________________________________________________________________________________________________________           
    if msg.startswith('/sp'):
        await client.delete_message(message)
        inp= ' '.join(message.content[4:])
        await client.send_message(ch, inp)
        
#Image Search_______________________________________________________________________________________________________________________________________        
    if msg.startswith('/img'):
        x=False
        imgs= []
        msg1=msg[5:]
        dif=msg[6:]
        
        await client.delete_message(message)
        
        tmp= await client.send_message(ch, "Loading...".format(msg))

        if msg.startswith('/imgf'):
            
            link= 'https://www.bing.com/images/search?q=',dif,'&qft=+filterui:photo-animatedgif&FORM=RESTAB'
            soup3 = requests.get(''.join(link))
            soup= BeautifulSoup(soup3.content,"html.parser")
            for a in soup.find_all('a', href=True):
                if a['href'].startswith("http://") and a['href'].endswith('.gif'):
                    imgs.append(a['href'])
            
            if len(imgs)<1:
                await client.send_message(ch, 'No gifs were found...')
            
        else:
            link= 'https://www.bing.com/images/search?q=',msg1,'&FORM=RESTAB'
            soup3 = requests.get(''.join(link))
            soup= BeautifulSoup(soup3.content,"html.parser")
            for a in soup.find_all('a', href=True):
                if a['href'].startswith("http://") and a['href'].endswith('.jpg'):
                    imgs.append(a['href'])

            if len(imgs)<1:
                await client.send_message(ch, 'No images were found...')
                
            if msg.startswith('/imgx'):
                link= imgs[random.randint(0,len(imgs)-1)]
                print(link)

                try:
                    r= requests.get(link)
                    with open('/home/ubuntu/DiscordPybot/mainImg.jpg', 'wb') as outfile:
                        outfile.write(r.content)
                        img= Image.open('/home/ubuntu/DiscordPybot/mainImg.jpg')
                        w= img.size[0]
                        h= img.size[1]
                    
                except Exception as e:
                    print(e)
                    await client.send_message(ch, "An error occured, please try again...")
                    
                
                img1= img.crop((0,0,w/2,h/2))

                img2= img1.transpose(Image.FLIP_LEFT_RIGHT)
                img3= img1.transpose(Image.FLIP_LEFT_RIGHT).rotate(180)
                img4= img1.rotate(-180)


                newim= Image.new('RGB',(w,h))
                newim.paste(img1,(0,0))
                newim.paste(img2,(int(w/2),0))
                newim.paste(img3,(0,int(h/2)))
                newim.paste(img4,(int(w/2),int(h/2)))
                newim.save('/home/ubuntu/DiscordPybot/mainImg.jpg')
                await client.send_file(ch,'/home/ubuntu/DiscordPybot/mainImg.jpg')
                print(newim.size)
                os.remove('/home/ubuntu/DiscordPybot/mainImg.jpg')
                x=True
                await client.delete_message(tmp)
            
        if not(x):
            try:
                link=imgs[random.randint(0,len(imgs)-1)]
                print(link)
                em= discord.Embed(title=msg1, colour=0x48437)
                emImg= discord.Embed.set_image(em,url=link)

                await client.delete_message(tmp)
                await client.send_message(ch, embed=em)
            except Exception as errorMsg:
                print(errorMsg)
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
