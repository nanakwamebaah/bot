from urllib import response
import discord
import  os
import nltk
from dotenv import load_dotenv
import requests
import json

from neuralintents import GenericAssistant



chatbot = GenericAssistant('intents.json')
chatbot.train_model()
chatbot.save_model()

print("Bot running...")
client = discord.Client()

load_dotenv()
TOKEN = os.getenv('TOKEN')

def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def get_bible_quote(verse):
  response = requests.get('https://bible-api.com/' + verse)
  json_data = json.loads(response.text)
  return(json_data['text'])

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$aibot'):
        response = chatbot.request(message.content[7:])
        await message.channel.send(response)
    
    msg = message.content
    if msg.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if msg.startswith('$bible'):
        verse = msg.split("$bible ",1)[1]
        bible = get_bible_quote(verse)
        await message.channel.send(bible)    


client.run(TOKEN)