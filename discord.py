from discord.ext import commands
import aiohttp
import asyncio
import discord

prefix = '!'
intents = discord.Intents().all()
bot = commands.Bot(command_prefix=prefix, case_insensitive=True, intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('!check (txid)'))
    print('Bot is Online')

@bot.command()
async def check(ctx, transaction_hash):
    print(f'{ctx.author} | {ctx.author.id} -> #check {transaction_hash}')
    if ctx.channel.type != discord.ChannelType.private:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://api.blockcypher.com/v1/ltc/main/txs/{transaction_hash}') as r:
                    r = await r.json()

                    confirmations = r['confirmations']
                    
            if confirmations >= 1:
                embed = discord.Embed(title="Transaction Confirmed", description="This transaction has already reached 1 confirmation.", color=0x01fe00)
                embed.add_field(name="Transaction ID", value=f"[{transaction_hash}](https://live.blockcypher.com/ltc/tx/{transaction_hash})") # you can change the crypto type by changing the ticker symbol (supported coins: btc, eth, ltc, doge, dash)
                await ctx.send(embed=embed)
            elif confirmations == 0:
                embed = discord.Embed(title="Checking Transaction", color=0xD3D3D3, description='When this transaction reaches 1 confirmation, you will be pinged.')
                embed.add_field(name="Transaction ID", value=f"[{transaction_hash}](https://live.blockcypher.com/ltc/tx/{transaction_hash})") # you can change the crypto type by changing the ticker symbol (supported coins: btc, eth, ltc, doge, dash)
                message = await ctx.send(embed=embed)

                async def check_confirmations():
                    while True:
                        async with aiohttp.ClientSession() as session:
                            async with session.get(f'https://api.blockcypher.com/v1/ltc/main/txs/{transaction_hash}') as r: # you can change the crypto type by changing the ticker symbol (supported coins: btc, eth, ltc, doge, dash)
                                r = await r.json()
                                confirmations = r['confirmations']
                                if confirmations >= 1:
                                    embed = discord.Embed(title="Transaction Confirmed", description="This transaction has reached 1 confirmation.", color=0x01fe00)
                                    embed.add_field(name="Transaction ID", value=f"[{transaction_hash}](https://live.blockcypher.com/ltc/tx/{transaction_hash})") # you can change the crypto type by changing the ticker symbol (supported coins: btc, eth, ltc, doge, dash)
                                    await ctx.send(f'{ctx.author.mention}', embed=embed)
                                    break
                        await asyncio.sleep(60)

                asyncio.create_task(check_confirmations())
        except:
            await ctx.send("Invalid transaction ID, please make sure it's correct.")

bot.run("YOUR BOT TOKEN")




# Made by TellMe#0001 (caniloveyou)