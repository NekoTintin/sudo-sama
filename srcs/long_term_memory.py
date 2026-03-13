import chromadb
import os

class LongTermMemory:

	def __init__(self, path="data/long_term/chromadb") -> None:
		os.makedirs("data/long_term/", exist_ok=True)
		self.client = chromadb.PersistentClient(path=path)