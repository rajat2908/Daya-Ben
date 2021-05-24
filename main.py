  
import discord

from discord.ext import commands

import os

from Webhosting import keep_alive

from replit import db

import asyncio

bot = commands.Bot(command_prefix=["daya", "d!"])

newline = '\n'

filterd_words = ['gali', 'dena' , 'buri' 'bat' 'google se yaha daliya dal dena' ]

@bot.event

async def on_message(msg):

  for word in filterd_words:

    if word in msg.content:

      await msg.delete()

      await msg.channel.send(f'ye mana hai {msg.author.mention}')

  

  if ':' == msg.content[0] and ':' == msg.content[-1]:

    emoji_name = msg.content[1 : -1]

    for emoji in msg.guild.emojis:

      if emoji_name == emoji.name:

        await msg.channel.send(str(emoji))

        await msg.delete()

        break

  await bot.process_commands(msg)

@bot.command()

async def whois(ctx, member : discord.Member):

  embed = discord.Embed(title = member.name, discription =member.mention, colour = discord.Colour.orange())

  embed.add_field(name = 'ID' , value = member.id , inline = True)

  embed.set_thumbnail(url = member.avatar_url)

  embed.set_footer(icon_url = ctx.author.avatar_url , text = f'requested by {ctx.author.name}')

  await ctx.send(embed = embed)

  

#creating tag

@bot.command()

async def tagbana(ctx, tag=None,*,value):

  if tag == None:

    await ctx.send(f'Are {ctx.author.name} bhaiya taag ka naam to batao')

  elif tag is not None:

    db[tag] = value

    await ctx.send (f'a halo taag {tag} ban chuka hai')

@bot.command()

async def tag(ctx,tag=None):

  if tag == None:

    await ctx.send(f'Are {ctx.author.name} bhaiya taag ka naam to batao')

  elif tag is not None:

    value = db[tag]

    await ctx.send(value)

    

@bot.command()

async def taghata(ctx, tag=None):

  if tag == None:

    await ctx.send(f'Are {ctx.author.name} bhaiya taag ka naam to batao')

  elif tag is not None:

    del db[tag]

    await ctx.send (f'{tag} taag gaya ab chalo garba karte hai!')

@bot.command(description="Mutes the specified user.")

@commands.has_permissions(manage_messages=True)

async def mute(ctx, member: discord.Member, *, reason=None):

    guild = ctx.guild

    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:

        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:

            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    embed = discord.Embed(title="muted", description=f"{member.mention} chup ho gaya hai ", colour=discord.Colour.light_gray())

    embed.add_field(name="reason:", value=reason, inline=False)

    await ctx.send(embed=embed)

    await member.add_roles(mutedRole, reason=reason)

    await member.send(f" you have been muted from: {guild.name} reason: {reason}")

@bot.command()

@commands.has_permissions(kick_members=True)

async def chilla(ctx,*,msg=None):

  if msg == None:

    await ctx.send(f'Are {ctx.author.name} bhaiya kya chillau mai? ye bata ke likho firse')

  elif msg is not None:

    await ctx.send(f'@everyone sunooo {ctx.author.name} bol raha hai ki "{msg}"')

@bot.command()

async def laatmar(ctx,member:discord.Member,*,kyuki='Pata nahi'):

  await ctx.send(f'{member} ko nikal diya kyuki {kyuki}')

  await member.kick(reason=kyuki)

  

@bot.command(description="Unmutes a specified user.")

@commands.has_permissions(manage_messages=True)

async def unmute(ctx, member: discord.Member):

   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

   await member.remove_roles(mutedRole)

   await member.send(f" you have unmutedd from: - {ctx.guild.name}")

   Embed = discord.Embed(title="unmute", description=f" unmuted-{member.mention}",colour=discord.Colour.light_gray())

   await ctx.send(Embed = Embed)

   

   

   

@bot.event

async def on_ready():

  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Tapu"))

@bot.command()

@commands.has_permissions(ban_members=True)

async def ban(ctx,member : discord.Member, *,reason = None):

  await ctx.send(f'{member} ban ho gaya hai')

  await member.ban(reason = reason)

@bot.command()

async def unban(ctx, *, member):

	banned_users = await ctx.guild.bans()	

	member_name, member_discriminator = member.split('#')

	for ban_entry in banned_users:

		user = ban_entry.user

		

		if (user.name, user.discriminator) == (member_name, member_discriminator):

 			await ctx.guild.unban(user)

 			await ctx.channel.send(f"{user.mention} ko unban kar diya")

 			

 		

@bot.command()

@commands.has_permissions(manage_messages = True)

async def purge(ctx, amount = 2):

    await ctx.channel.purge(limit = amount)

    await ctx.send(f'deleted {amount} messages. ')

keep_alive()

bot.run(os.getenv('token'))