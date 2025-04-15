from app.models.instrument import Instrument as Item
from app.repository.common import CommonRepository 
from fastapi import Depends

table_name="instruments"

class InstrumentRepository(CommonRepository):
    def __init__(self, connection):
        super().__init__(connection, table_name, Item)

