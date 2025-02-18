import discord
import asyncio
from discord.ext import commands
from discord.ui import Button, View
import os

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    global leagues_emoji
    leagues_emoji = discord.utils.get(bot.emojis, name="leagues")
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="Managing Roles"))

@bot.command()
async def area_panel(ctx):
    await ctx.message.delete()

    # Construct the embed with the emoji
    embed = discord.Embed(
        title=f"{leagues_emoji} Region Role Assign {leagues_emoji}",
        description="# Select the regions you have unlocked #\n"
                    "## Click again to remove them. ##",
        color=discord.Color.green()
    )
    embed.set_footer(text="Select your regions")

    embed.set_image(url="https://cdn.discordapp.com/attachments/1273094409432469605/1299599252829503508/xejylXb.png?ex=671dc99f&is=671c781f&hm=ddb7ebcf4e96205dc6dca40b3a93f29411990fb26b7afb591c4cca2fbdce14cf&")  # Reference the uploaded image as an attachment


    guild = ctx.guild
    custom_emoji_desert = discord.utils.get(guild.emojis, name="desert")
    custom_emoji_kourend = discord.utils.get(guild.emojis, name="kourend")
    custom_emoji_fremennik = discord.utils.get(guild.emojis, name="fremennik")
    custom_emoji_tirannwn = discord.utils.get(guild.emojis, name="tirannwn")
    custom_emoji_wilderness = discord.utils.get(guild.emojis, name="wilderness")
    custom_emoji_asgarnia = discord.utils.get(guild.emojis, name="asgarnia")
    custom_emoji_morytania = discord.utils.get(guild.emojis, name="morytania")
    custom_emoji_kandarin = discord.utils.get(guild.emojis, name="kandarin")
    custom_emoji_varlamore = discord.utils.get(guild.emojis, name="varlamore")

    button_desert = Button(label="Desert", style=discord.ButtonStyle.secondary, emoji=custom_emoji_desert)
    button_kourend = Button(label="Kourend", style=discord.ButtonStyle.secondary, emoji=custom_emoji_kourend)
    button_fremennik = Button(label="Fremennik", style=discord.ButtonStyle.secondary, emoji=custom_emoji_fremennik)
    button_tirannwn = Button(label="Tirannwn", style=discord.ButtonStyle.secondary, emoji=custom_emoji_tirannwn)
    button_wilderness = Button(label="Wilderness", style=discord.ButtonStyle.secondary, emoji=custom_emoji_wilderness)
    button_asgarnia = Button(label="Asgarnia", style=discord.ButtonStyle.secondary, emoji=custom_emoji_asgarnia)
    button_morytania = Button(label="Morytania", style=discord.ButtonStyle.secondary, emoji=custom_emoji_morytania)
    button_kandarin = Button(label="Kandarin", style=discord.ButtonStyle.secondary, emoji=custom_emoji_kandarin)
    button_varlamore = Button(label="Varlamore", style=discord.ButtonStyle.secondary, emoji=custom_emoji_varlamore)

    view = View(timeout=None)
    view.add_item(button_asgarnia)
    view.add_item(button_kandarin)
    view.add_item(button_desert)
    view.add_item(button_fremennik)
    view.add_item(button_wilderness)
    view.add_item(button_morytania)
    view.add_item(button_kourend)
    view.add_item(button_varlamore)
    view.add_item(button_tirannwn)

    async def button_callback(interaction):
        role_name = interaction.data['custom_id']
        role = discord.utils.get(interaction.guild.roles, name=role_name)

        if role is None:
            await interaction.response.send_message(f"Error: Area {role_name} not found.", ephemeral=True)
            return

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            feedback_message = await interaction.channel.send(f"{interaction.user.mention}, Area {role_name} Removed.")
        else:
            await interaction.user.add_roles(role)
            feedback_message = await interaction.channel.send(f"{interaction.user.mention}, Area {role_name} Added.")

        # Acknowledge the interaction and delete the message after 1 second
        await interaction.response.defer()
        await feedback_message.delete(delay=1)

    buttons = [button_asgarnia, button_kandarin, button_desert, button_fremennik, button_wilderness, button_morytania, button_kourend, button_varlamore, button_tirannwn]
    role_names = ["Asgarnia", "Kandarin", "Desert", "Fremennik", "Wilderness", "Morytania", "Kourend", "Varlamore", "Tirannwn"]

    for button, role_name in zip(buttons, role_names):
        button.custom_id = role_name
        button.callback = button_callback

    await ctx.send(embed=embed, view=view)

bot.run(os.getenv('DISCORD_BOT_TOKEN'))
