import os
import nextcord
from nextcord.ext import commands
import aiohttp
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv("secrets.env"))
WeatherAPI = os.getenv("WEATHER_KEY")
token = os.getenv("SECRET_KEY")

bot = commands.Bot(command_prefix="!", intents=nextcord.Intents.all())

@bot.event
async def on_ready():
    print ("The Bot is live on Discord now!")

@bot.command()
async def weather(ctx:commands.Context, *, city):
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": WeatherAPI,
        "q": city,
    }
    async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as res:
                data = await res.json()

                if "error" in data:
                    return await ctx.send(f"An error occured: {data['error']['message']}")

                location = data["location"]["name"]
                temp_c = data["current"]["temp_c"]
                temp_f = data["current"]["temp_f"]
                humidity = data["current"]["humidity"]
                wind_kph = data["current"]["wind_kph"]
                wind_mph = data["current"]["wind_mph"]
                wind_dir = data["current"]["wind_dir"]
                condition = data["current"]["condition"]["text"]
                icon = "http:"+data["current"]["condition"]["icon"]

                embed = nextcord.Embed(title=f"Weather in {location}",description=f"The condition in `{location}` is currently `{condition}`")
                embed.add_field(name="Temperature", value=f"{temp_c}°C | {temp_f}°F")
                embed.add_field(name="Humidity", value=f"{humidity}%")
                embed.add_field(name="Wind Speed", value=f"{wind_kph}kph | {wind_mph}mph")
                embed.add_field(name="Wind Direction", value=f"{wind_dir}")
                embed.set_thumbnail(url=icon)
                await ctx.send(embed=embed)

bot.run(token)