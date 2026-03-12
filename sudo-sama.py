import discord
import asyncio
from discord.ext import commands
import os
from dotenv import load_dotenv
from srcs.short_term_memory import ShortTermMemory

class SudoSama(commands.Bot):

	def __init__(self):
		self._intents = discord.Intents.all()
		super().__init__(command_prefix="!", intents=self._intents)
		self.short_mem = ShortTermMemory()
		self.short_mem.load_all()

	async def setup_hook(self):
		for file in os.listdir("cogs"):
			if file.endswith(".py"):
				try:
					await self.load_extension(f"cogs.{file[:-3]}")
				except Exception as e:
					print(f"Failed to load {file}: {e}")
					return
	
	async def on_ready(self):
		print(f"Logged in as {self.user} (ID: {self.user.id})")
		await self.change_presence(activity=discord.CustomActivity(name="Gardienne du Kernel"))

async def start():
	bot = SudoSama()
	try:
		async with bot:
			await bot.start(os.getenv("CLIENT_TOKEN"))
	except asyncio.CancelledError:
		pass
	finally:
		bot.short_mem.save_all()

if __name__ == "__main__":
	load_dotenv()
	os.makedirs("data/", exist_ok=True)
	try:
		asyncio.run(start())
	except KeyboardInterrupt:
		pass