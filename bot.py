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
        # send request to shopify site and parses html content with lxml
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        
        #####
        
        # # if proxies are being used: put proxy between single quotes and remove curly braces.
        


        # proxy = '{INSERT-PROXY-HERE}'.split(":")
        # ip, port, user, passw = proxy[0], proxy[1], proxy[2], proxy[3]
        # proxyinuse = { "http": "http://{}:{}@{}:{}".format(user, passw, ip, port),
        #                "https": "https://{}:{}@{}:{}".format(user, passw, ip, port) }
            
        # # then after url in requests, put proxies=proxy, E.G. -- r = requests.get(url,proxies=proxyinuse)
        
        #####
        
        # keyword filter to find var meta and access the keys inside.
        pattern = re.compile(r"var meta = (.*?);")
        scripts = soup.find("script", text=pattern, attrs=None).string
        search = pattern.search(scripts)
        
        # search for title name
        title = ''
        titlersvp = soup.find('title', attrs=None).string
        
        # search for image url
        img = soup.find('meta', ({ 'property' : 'og:image'}))
        
        # search for price
        price = ''
        priceoneness = ''
        
        # convert to json and finds the tuple "product" with the "variants" key inside
        products = json.loads(search.groups()[0]).get('product')['variants']
        
        if img:
            img = img.get('content')
        else:
            img = ''


        
        if titlersvp:
            title = titlersvp
        else:
            title = soup.find('meta', ({ 'name' : 'og:title' })).get('content')
        
        

        if price:
            price = soup.find('meta',({ 'property' : 'og:price:amount'})).get('content')
        elif price:
            price = soup.find('meta',({ 'property' : 'product:price:amount'})).get('content')
        elif price not in soup: 
            price = (json.loads(search.groups()[0]).get('product')['variants'][0]['price'])/100
            price = str(price) + '0'
        else:
            price = "Can't find"
            
        # loop through all sizes and prints them
        for sizes in products:
            size = sizes['public_title']
            lsize += "\n" + str(size)
            
        value1 ='```' + f"{lsize}" + '```'


        # loop through all variants and prints them
        for variants in products:
            id = variants['id']
            lvar += "\n" + str(id)
                
        value2 ='```' + f"{lvar}" + '```'
        

        embed = discord.Embed(title=title,url=url, color=0xf09719)
        embed.set_thumbnail(url=img)
        embed.add_field(name="Sizes", value=value1, inline=True)
        embed.add_field(name="Variants", value=value2, inline=True)
        embed.add_field(name="Price", value="${}".format(price), inline=False)
        embed.set_footer(icon_url = f"{ctx.guild.icon_url}", text=f"{ctx.message.guild.name} - {ctx.message.author}")
        await ctx.send(embed=embed)
    except Exception as e:
       print("Error fetching variants!")
       embed = discord.Embed(title="Shopify Variants", color=0xf09719)
       embed.add_field(name = '`Variants Not Found`',value = "\u200b", inline=True)
       embed.set_footer(icon_url = f"{ctx.guild.icon_url}", text=f"{ctx.message.guild.name} - {ctx.message.author}")
       await ctx.send(embed=embed)
     
client.run(token)
