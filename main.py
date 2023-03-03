import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import discord
import os
from dotenv import load_dotenv

load_dotenv()

intent = discord.Intents.default()
intent.members = True
intent.message_content = True
client = discord.Client(intents=intent)

# Replace with your own last.fm username and API key
username = 'insert your username'
api_key = 'insert your last.fm API Key'
# Set the time period to the last month
time_period = "1month"

# Make a request to the last.fm API to get the user's top artists over the last month
response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user={username}&api_key={api_key}&period={time_period}&limit=100&format=json")

# Extract the top artists from the API response
top_artists = response.json()['topartists']['artist']
# Create a new image with a size of 1000x1000 pixels
image = Image.new("RGB", (1000, 1000), (0, 0, 0))
# Creation of the png 
draw = ImageDraw.Draw(image)
font_size = 20
font = ImageFont.truetype('arial.ttf', font_size)
# Loop through the top artists and paste their images onto the image
for i, artist in enumerate(top_artists):
    # Make a request to the last.fm API to get the artist's image
    response = requests.get(artist["image"][-1]["#text"])
    # Open the image using the Pillow library
    artist_image = Image.open(BytesIO(response.content))
    # Resize the image to 100x100 pixels
    artist_image = artist_image.resize((100, 100))
    # Calculate the x and y coordinates for the image based on the current iteration
    x = (i % 10) * 100
    y = (i // 10) * 100
    # Paste the image onto the main image
    image.paste(artist_image, (x, y))

# Save the image to disk
image.save("lastfm_collage.png")

#Work in progress: implement the function in a discord bot
@client.event
async def on_ready():
    print("10x10 Collage bot ready for use")

