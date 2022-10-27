import os
from nextcord.ext import commands
import json
import random
import asyncio
from nextcord import File, ButtonStyle, Embed, Color, SelectOption, Intents, Interaction, SlashOption, Member
from nextcord.ui import Button, View, Select
import nextcord
from nextcord.ext.commands import has_permissions, CommandNotFound, MissingPermissions


intents = nextcord.Intents.default()
intents.message_content = True
helpGuide = json.load(open("help.json"))
colour = 0xfcba03

def createHelpEmbed(pageNum=0, inline=False):
    pageNum = (pageNum) % len(list(helpGuide))
    pageTitle = list(helpGuide)[pageNum]
    embed = Embed(color=0xfcba03, title=pageTitle)
    for key, val in helpGuide[pageTitle].items():
        embed.add_field(name=bot.command_prefix+key, value=val, inline=inline)
        embed.set_footer(text=f"Página: {pageNum+1}/{len(list(helpGuide))}")
    return embed


activity = nextcord.Activity(type=nextcord.ActivityType.listening, name="Nani! | /help")
bot = commands.Bot(command_prefix='c-', intents=intents, activity=activity)
bot.remove_command("help")

@bot.event
async def on_ready():
	print(f"Iniciado no Bot: {bot.user.name}")

# Commands #


@bot.command(name="help")
async def Help(ctx):
    currentPage = 0

    async def next_callback(interaction):
        nonlocal currentPage, sent_msg
        currentPage += 1
        await sent_msg.edit(embed=createHelpEmbed(pageNum=currentPage), view=myview)

    async def previous_callback(interaction):
        nonlocal currentPage, sent_msg
        currentPage -= 1
        await sent_msg.edit(embed=createHelpEmbed(pageNum=currentPage), view=myview)

    # add buttons to embed

    previousButton = Button(label="◀️", style=ButtonStyle.blurple)
    nextButton = Button(label="▶️", style=ButtonStyle.blurple)
    previousButton.callback = previous_callback
    nextButton.callback = next_callback

    myview = View(timeout=200)
    myview.add_item(previousButton)
    myview.add_item(nextButton)

    sent_msg = await ctx.send(embed=createHelpEmbed(currentPage), view=myview)




@bot.command(name="invite")
async def Invite(ctx):
	invEmbed = Embed(title="Me Convide!!",description="Seu servidor vai ficar mais bonito com esse bot do discord, mais seguro e mais ativo!", color=0xfc9403)
	linkButton1 = Button(label="Convidar", url="https://discord.com/api/oauth2/authorize?client_id=972322804148097065&permissions=1636315954423&scope=bot", emoji="💌")

	myview = View(timeout=200)
	myview.add_item(linkButton1)

	await ctx.send(embed=invEmbed, view=myview)
	
@bot.command(name="clear")
@has_permissions(manage_messages=True)
async def clear(ctx, amount=0):
    if amount == 0 or None:
        await ctx.send(":x: | Diga um valor de 1 a 200")
        await ctx.message.delete()
    elif amount > 200:
        await ctx.send(":x: | O Máximo é: 200")
        await ctx.message.delete()
    else:
        await ctx.channel.purge(limit=amount)
        await ctx.message.delete()
	await ctx.send(f":tada: | Sucesso! Limpei {amount} mensagens!")


@bot.command(name="kick")
@has_permissions(kick_members=True)
async def kick(ctx, use : nextcord.User=None, *, reason=None):
    if use == None:
        await ctx.send(":x: | Por-favor, mencione um usuário")
        await ctx.message.delete()
    elif reason == None:
        await ctx.send(":X: | Por-favor, diga uma razão")
        await ctx.message.delete()
    else:
        await ctx.send(f":tada: | {use.name} Foi expulso com sucesso! Razão: {reason}")
        await qyce.kick(reason=reason)
        await ctx.message.delete()

# Slash Commands #
@bot.slash_command(description="Veja os Comandos do Bot!")
async def help(interaction: Interaction):
    currentPage = 0

    async def next_callback(interaction):
        nonlocal currentPage, sent_msg
        currentPage += 1
        await sent_msg.edit(embed=createHelpEmbed(pageNum=currentPage), view=myview)

    async def previous_callback(interaction):
        nonlocal currentPage, sent_msg
        currentPage -= 1
        await sent_msg.edit(embed=createHelpEmbed(pageNum=currentPage), view=myview)

    # add buttons to embed

    previousButton = Button(label="◀️", style=ButtonStyle.blurple)
    nextButton = Button(label="▶️", style=ButtonStyle.blurple)
    previousButton.callback = previous_callback
    nextButton.callback = next_callback

    myview = View(timeout=200)
    myview.add_item(previousButton)
    myview.add_item(nextButton)

    sent_msg = await interaction.response.send_message(embed=createHelpEmbed(currentPage), view=myview)


if __name__ == '__main__':
	bot.run(os.environ["DISCORD_TOKEN"])

