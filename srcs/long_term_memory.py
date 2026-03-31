import chromadb
import ollama
import os
import uuid
import asyncio
import time

class LongTermMemory:

	def __init__(self, path="data/long_term/chromadb") -> None:
		os.makedirs(os.path.dirname(path), exist_ok=True)
		self.client = chromadb.PersistentClient(path=path)
		self.collections = self.client.get_or_create_collection(name="discord_mem")

	async def process_memory(self, user_id: int, message_content: str) -> bool:
		loop = asyncio.get_event_loop()
		resp = await loop.run_in_executor(None, lambda: ollama.generate(
			model="memmod:latest",
			prompt=message_content
		))

		fact = resp["response"].strip()

		# len > 4 to avoid basic responses (...., rien, etc)
		if fact.upper() != "RIEN" and len(fact) > 4:
			existing_fact = self.collections.query(
				query_texts=[fact],
				n_results=1,
				where={"user_id": str(user_id)})

			if existing_fact["documents"] and \
				len(existing_fact["documents"][0]) > 0 and \
				existing_fact["distances"][0][0] < 0.15:
				print(_("fact_already_exists") + fact)
				return False

			print(_("insert_in_chromadb") + fact)

			self.collections.add(
				documents=[fact],
				metadatas=[{
					"user_id": str(user_id),
					"source": "discord",
					"timestamp": time.time()}],
				ids=[str(uuid.uuid4())])
			return True
		return False

	def query_memory(self, user_id: int, query: str, lim: int = 5) -> str:
		res = self.collections.query(
			query_texts=[query],
			n_results=lim,
			where={"user_id": str(user_id)})
		
		if not res["documents"] or not res["documents"][0]:
			return ""
		
		context = "\n".join([f"- {fact}" for fact in res["documents"][0]])
		return f"INFORMATION SUR L'UTILISATEUR:\n{context}\n"