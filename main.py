
import discord
import os
import re
import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
options = Options()
options.headless = True
client=discord.Client()
token =open("token.txt",'r').read()
file=open('blacklist.txt','r')
temp=file.readlines()
file.close()
blacklist=[] 
up=	u"\U0001F44D"
down=u"\U0001F44E"
for i in temp:
  blacklist.append(i.replace("\n",""))
def get_data(urls):
  for url in urls:
    driver=webdriver.Chrome('./chromedriver',options=options)
    driver.get(url)
    time.sleep(5)
    pg=driver.page_source 
    soup=BeautifulSoup(pg,'html.parser')
    temp=soup.get_text()
    text=temp.split()
    print(text)
    for tx in text:
      res = [tx[i: j] for i in range(len(tx))
          for j in range(i + 1, len(tx) + 1)]
      for t in res:
        print(t)
        if t.lower() in blacklist:
          print(t)
          driver.close()
          return t
    driver.close()
    return False
@client.event
async def on_ready():
  print('IN {0.user}'.format(client))
@client.event
async def on_message(message):
  def check(reaction,user):
    if (str(reaction)==up):
      return True
    elif (str(reaction)==down):
      return False
  if message.channel.id==891926109485146122:#test channel ie channel which it will detect messages from
    if message.author==client.user or "core" in [y.name.lower() for y in message.author.roles]:
      return
    urls= re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',message.content.lower())
    t=get_data(urls)
    if(t):
      await message.delete()
      mention=message.author.mention
      response=f"{mention} Please wait for the mods to approve your message"
      await message.author.send(response)
      channel=client.get_channel(891929859595571241)#report channel ie channel which the bot reports content to 
      msg=await channel.send(f"{mention} sent the link\n"+message.content+"\nFound the word: "+t+"\nVerify the link & react with"+ up+"to re-send the message or with" +down+"to delete the message")
      await msg.add_reaction(up)
      await msg.add_reaction(down)
      try:
        await client.wait_for('reaction_add',timeout=15.0, check=check)
        await message.channel.send(f"{mention} sent:\n"+message.content)
      except:
        await msg.delete()
        await msg.channel.send(f"Archive \n {mention} sent:\n"+message.content)
client.run(token)