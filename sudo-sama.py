import discord
import asyncio
from discord.ext import commands
import os
import builtins

from srcs.short_term_memory import ShortTermMemory
from srcs.utils import setup_i18n, error_management

# Stop VScode warnings
if not hasattr(builtins, "_"):
	_ = lambda s: s

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
					print(_("cog_load_error"))
					print(f"{file}: {e}")
					return
	
	async def on_ready(self):
		print(_("ready_msg") + str(self.user) + " " + f"(ID: {self.user.id})")
		await self.change_presence(activity=discord.CustomActivity(name=_("discord_activity")))

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
	setup_i18n()
	error_management()
	os.makedirs("data/", exist_ok=True)
	try:
		asyncio.run(start())
	except KeyboardInterrupt:
		pass