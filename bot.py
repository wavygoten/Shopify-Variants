import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests, json, re, lxml
client = commands.Bot(command_prefix='-')
token = '{INSERT-BOT-TOKEN-HERE}'
@client.event
async def on_ready():
    print('Bot is ready.')

@client.command()
async def variants(ctx, args):
    url = args
    lsize = str()
    lvar = str()

    try:
        # send request to shopify site
        url += "/products.json"
        r = requests.get(url).json()
        getproduct = r.get('product')['variants']
        
        for variants in getproduct:
            id = variants['id']
            lvar += "\n" + str(id)
        
        
        for sizes in getproduct:
            size = sizes['title']
            lsize += "\n" + str(size)
        
            
        price = (str(getproduct[0]['price']))
        
        title = (str(r.get('product')['title']))
        
        try:
            img = (str(r.get('product')['images'][0]['src']))
        except:
            img = ''
        
        value1 ='```' + f"{lsize}" + '```'
        value2 ='```' + f"{lvar}" + '```'
    

        embed = discord.Embed(title=title,url=args, color=0xf09719)
        embed.set_thumbnail(url=img)
        embed.add_field(name="Sizes", value=value1, inline=True)
        embed.add_field(name="Variants", value=value2, inline=True)
        embed.add_field(name="Price", value="${}".format(price), inline=False)
        embed.set_footer(icon_url = f"{ctx.guild.icon_url}", text=f"{ctx.message.guild.name} - {ctx.message.author}")
        await ctx.send(embed=embed)
    except Exception as e:
        print("Error fetching variants! {} {}".format(e, r.status_code))
        embed = discord.Embed(title="Shopify Variants", color=0xf09719)
        embed.add_field(name = '`Variants Not Found`',value = "\u200b", inline=True)
        embed.set_footer(icon_url = f"{ctx.guild.icon_url}", text=f"{ctx.message.guild.name} - {ctx.message.author}")
        await ctx.send(embed=embed)
     
client.run(token)
