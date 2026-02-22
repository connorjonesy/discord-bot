import discord
from features import Blackjack
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        #await self.tree.sync()  # Sync commands with Discord
        MY_GUILD = discord.Object(id=int(os.getenv('GUILD_ID'))) #error here but still works?
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
        print("Commands synced!")

client = MyClient()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    # Ignore our own messages
    if message.author == client.user:
        return

    if message.content.lower() == ('/berda'):
        await message.channel.send('I am the Berda Bucks bot')
        await message.channel.send('Type /help for commands')

@client.tree.command(name="help", description="Show berda bot commands")
async def help_command(interaction: discord.Interaction):
    await interaction.response.send_message(
            "**Berda Bot Commands:**\n"
            "/21 -- Play a round of Blackjack against me\n"
            "/help -- Show this message"
        )

@client.tree.command(name="21", description="Play blackjack against berda bot")
async def play_blackjack(interaction: discord.Interaction):
    await interaction.response.send_message("Starting blackjack game...")
    newGame = Blackjack(interaction.channel, interaction.user, client)
    await newGame.playgame()

client.run(os.getenv('DISCORD_TOKEN'))
