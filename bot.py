import discord
from discord.ext import commands
from config import token

intents = discord.Intents.default()
intents.members = True 
intents.message_content = True

client = discord.Client(intents=intents)

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.command()
async def start(ctx):
    await ctx.send("Hi! I'm a chat manager bot!")

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None):
    if member:
        if ctx.author.top_role <= member.top_role:
            await ctx.send("It is not possible to ban a user with equal or higher rank!")
        else:
            await ctx.guild.ban(member)
            await ctx.send(f"User {member.name} was banned.")
    else:
        await ctx.send("This command should point to the user you want to ban. For example: `!ban @user`")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have sufficient permissions to execute this command.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("User not found.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "https://":
        await message.author.ban(reason="Posting links is not allowed.")
        await message.delete()
    await client.process_commands(message)


client.run(token)