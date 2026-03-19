import os
import ssl
import certifi
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
from hello_ai.crew import HelloAi

# Fix SSL Certificate Error on macOS
os.environ['SSL_CERT_FILE'] = certifi.where()

# Load environment variables
load_dotenv()

# Discord Configuration
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER_ID = os.getenv('DISCORD_SERVER_ID')
CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')

# Convert IDs to integers if they exist
SERVER_ID = int(SERVER_ID) if SERVER_ID else None
CHANNEL_ID = int(CHANNEL_ID) if CHANNEL_ID else None

# Define Intents
intents = discord.Intents.default()
intents.message_content = True  # Required to read message content

# Initialize Bot
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    if SERVER_ID:
        print(f'Target Server ID: {SERVER_ID}')
    if CHANNEL_ID:
        print(f'Target Channel ID: {CHANNEL_ID}')
    print('------')

@bot.check
async def globally_restrict_to_channel(ctx):
    """
    Globally restrict all bot commands to a specific server and channel if configured.
    """
    # Allow DMs if no restriction is set
    if isinstance(ctx.channel, discord.DMChannel):
        return True
    
    # Check Server ID
    if SERVER_ID and ctx.guild.id != SERVER_ID:
        return False
        
    # Check Channel ID
    if CHANNEL_ID and ctx.channel.id != CHANNEL_ID:
        return False
        
    return True

@bot.command(name='chat')
async def chat(ctx, *, message: str):
    """
    Chat with the AI assistant.
    Usage: !chat สวัสดีครับ
    """
    async with ctx.typing():
        # Prepare inputs for the crew
        inputs = {
            'topic': message,
            'current_year': str(datetime.now().year)
        }

        try:
            # Run the crew in a thread to not block the bot
            import asyncio
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, lambda: HelloAi().crew().kickoff(inputs=inputs))
            
            output_str = str(result.raw)
            
            # Send the response (handle Discord's 2000 character limit)
            if len(output_str) > 1900:
                parts = [output_str[i:i+1900] for i in range(0, len(output_str), 1900)]
                for part in parts:
                    await ctx.send(part)
            else:
                await ctx.send(output_str)

        except Exception as e:
            await ctx.send(f"❌ เกิดข้อผิดพลาด: {str(e)}")

# Keep !research for compatibility but it will use the new Thai chat logic
@bot.command(name='research')
async def research(ctx, *, topic: str):
    await chat(ctx, message=topic)

@bot.event
async def on_message(message):
    # Don't let the bot reply to itself
    if message.author == bot.user:
        return

    # Check Server/Channel Restrictions for non-DM channels
    if not isinstance(message.channel, discord.DMChannel):
        if SERVER_ID and message.guild.id != SERVER_ID:
            return
        if CHANNEL_ID and message.channel.id != CHANNEL_ID:
            return

    # Process commands first
    await bot.process_commands(message)
    
    # Handle direct messages or mentions
    is_dm = isinstance(message.channel, discord.DMChannel)
    is_mention = bot.user.mentioned_in(message)

    if (is_dm or is_mention) and not message.content.startswith('!'):
        # Clean the message content
        topic = message.content
        if is_mention:
            topic = topic.replace(f'<@!{bot.user.id}>', '').replace(f'<@{bot.user.id}>', '').strip()
        
        if topic:
            # Create a context and call the chat command
            ctx = await bot.get_context(message)
            await chat(ctx, message=topic)

def start_bot():
    if not TOKEN:
        print("Error: DISCORD_TOKEN not found in .env file.")
        return
    bot.run(TOKEN)

if __name__ == "__main__":
    start_bot()
