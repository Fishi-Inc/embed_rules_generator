from dataclasses import field
from pydoc import describe
from discord_webhook import DiscordWebhook, DiscordEmbed
import json
from PIL import Image
import requests
from io import BytesIO


with open('rules.json') as json_file:
    data = json.load(json_file)

with open('config.json') as json_file:
    config = json.load(json_file)

print('Sending webhook...')
    

webhook = DiscordWebhook(url=config['webhook_url'])

if 'http' in str(config['banner_url']):
    #send a picture to the webhook
    response = requests.get(config['banner_url'])
    img = Image.open(BytesIO(response.content))
    img.save('banner.png')
    embed = DiscordEmbed(color='2F3136')
    embed.set_image(url=config['banner_url'])
    webhook.add_embed(embed)

for rule in data:
    embed = DiscordEmbed(title=rule['title'], description=rule['desc'], color=rule['color'])
    embed.set_footer(text=rule['punishment'])
    webhook.add_embed(embed)
    webhook.avatar_url = config['webhook_avatar']
    webhook.username = config['webhook_name']
    webhook.execute()

print('Successfully sent webhook!\n')
input('Press enter to exit...')