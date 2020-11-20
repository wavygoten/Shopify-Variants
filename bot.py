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
        try:
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
            except:
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
                titlersvp = soup.find('title', attrs=None)
                
                # search for image url
                img = ''
                
                # search for price
                price = ''
                priceoneness = ''
                
                # convert to json and finds the tuple "product" with the "variants" key inside
                products = json.loads(search.groups()[0]).get('product')['variants']
                
                try:
                    img = soup.find('meta', ({ 'property' : 'og:image'})).get('content')
                except:
                    img = ''


                
                try:
                    title = soup.find('meta', ({ 'property' : 'og:title' })).get('content')
                except:
                    title = str(titlersvp)
                
                

                try:
                    if True:
                        price = soup.find('meta',({ 'property' : 'og:price:amount'})).get('content')
                    else:
                        price = soup.find('meta',({ 'property' : 'product:price:amount'})).get('content')
                except:
                    price = (json.loads(search.groups()[0]).get('product')['variants'][0]['price'])/100
                    price = (price + "{}".format("0"))
                    
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
                
                embed = discord.Embed(title=title,url=args, color=0xf09719)
                embed.set_thumbnail(url=img)
                embed.add_field(name="Sizes", value=value1, inline=True)
                embed.add_field(name="Variants", value=value2, inline=True)
                embed.add_field(name="Price", value="${}".format(price), inline=False)
                embed.set_footer(icon_url = f"{ctx.guild.icon_url}", text=f"{ctx.message.guild.name} - {ctx.message.author}")
                await ctx.send(embed=embed)
        except requests.exceptions.MissingSchema:
            embed = discord.Embed(color=0xf09719)
            embed.description = 'URL is not complete'
            await ctx.send(embed=embed)
        except requests.exceptions.HTTPError as errh:
            embed = discord.Embed(color=0xf09719)
            embed.description = ("HTTP Error: ",errh)
            await ctx.send(embed=embed)
        except requests.exceptions.ConnectionError as errc:
            embed = discord.Embed(color=0xf09719)
            embed.description = ("Error Connecting: ",errc)
            await ctx.send(embed=embed)
        except requests.exceptions.Timeout as errt:
            embed = discord.Embed(color=0xf09719)
            embed.description = ("Timeout Error: ",errt)
            await ctx.send(embed=embed)
        except requests.exceptions.RequestException as err:
            embed = discord.Embed(color=0xf09719)
            embed.description = 'Unknown error retrieving variants'
            await ctx.send(embed=embed)
            
    except:
        r = requests.get(url) 
        embed = discord.Embed(color=0xf09719)
        embed.description = str(r.status_code) + ' error retrieving variants'
        await ctx.send(embed=embed)
     
client.run(token)
