import motor.motor_asyncio
from config import Config

class Database:
    def __init__(self): self.collection = None
    async def connect(self):
        if Config.DATABASE_URL:
            client = motor.motor_asyncio.AsyncIOMotorClient(Config.DATABASE_URL)
            self.collection = client["GhostStream"]["links"]
            print("✅ DB Connected")
    async def save_link(self, uid, mid):
        if self.collection is not None: await self.collection.insert_one({'_id': uid, 'msg_id': mid})
    async def get_link(self, uid):
        if self.collection is not None:
            doc = await self.collection.find_one({'_id': uid})
            return doc['msg_id'] if doc else None
db = Database()
