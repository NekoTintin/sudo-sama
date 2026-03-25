from discord.ext import commands
import ollama
import time
import os
import asyncio
import builtins

# Stop VScode warnings
if not hasattr(builtins, "_"):
	builtins._ = lambda s: s

class AI(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.short_mem = bot.short_mem
		self.model_name = os.getenv("MODEL")

	@commands.Cog.listener()
	async def on_message(self, msg):
		if (msg.author.bot):
			return
		
		self.short_mem.add_message(
			msg.channel.id,
			"user",
			msg.author.name,
			msg.content,
			time.time()
		)

		if self.bot.user.mentioned_in(msg):
			async with msg.channel.typing():
				ctx = self.short_mem.normalize_message_for_ai(msg.channel.id)

				#last_msg = ctx[-1]['content']
				#ctx[-1]['content'] = self.bot.check_sudo(last_msg)

				#print(f"\n--- [ ENTRÉE IA POUR {msg.channel.id} ] ---")
				#for m in ctx:
				#	role_icon = "👤" if m['role'] == 'user' else "🤖"
				#	print(f"{role_icon} {m['role'].upper()}: {m['content']}")
				#print("-------------------------------------------\n")

				try:
					resp = await asyncio.to_thread(
						ollama.chat,
						model=self.model_name,
						messages=ctx
					)
					answer = resp['message']['content']
					self.bot.short_mem.add_message(
						msg.channel.id,
						"assistant",
						self.bot.user.name,
						answer,
						time.time()
					)
					await msg.reply(answer)
				except Exception as e:
					print(_("generating_error") + f"{e}")
					await msg.reply(_("generating_error_resp"))


async def setup(bot):
	await bot.add_cog(AI(bot))