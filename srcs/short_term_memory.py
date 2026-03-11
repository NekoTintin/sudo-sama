from collections import deque
import json
import os

MAX_MEM_SIZE = 10

class ShortTermMemory():

	def __init__(self, dir="./data/short_mem/") -> None:
		self.dir = dir
		self.short_mem = {}
		os.makedirs(self.dir, exist_ok=True)

	def load_all(self) -> None:
		try:
			for file in os.listdir(self.dir):
				if (file.endswith(".json")):
					with open(os.path.join(self.dir, file), "r") as f:
						self.short_mem[int(file[:-5])] = deque(json.load(f), maxlen=MAX_MEM_SIZE)
		except json.JSONDecodeError as e:
			print(f"Error loading short term memory: {e}")

	def save_all(self) -> None:
		for channel_id, msg in self.short_mem.items():
			with open(os.path.join(self.dir, f"{channel_id}.json"), "w") as f:
				json.dump(list(msg), f, indent=4)

	def add_message(self, channel_id: int, role: str, user: str, msg: str, timestamp: float) -> None:
		if channel_id not in self.short_mem:
			self.short_mem[channel_id] = deque(maxlen=MAX_MEM_SIZE)

		self.short_mem[channel_id].append({
			"role": role,
			"username": user,
			"message": msg,
			"timestamp": timestamp
		})