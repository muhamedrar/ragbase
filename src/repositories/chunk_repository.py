from .base_repository import BaseRepository
from models.db_schema import chunk
from sqlalchemy.orm import Session

class ChunkRepository(BaseRepository):

    def __init__(self, db_client:object):
        super().__init__(db_client)
        self.db_client = db_client


    def create_chunk(self,chunk:chunk):
