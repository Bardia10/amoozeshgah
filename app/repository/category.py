from app.models.category import Category as Item
from app.repository.common import CommonRepository 
from fastapi import Depends

table_name="categories"

class CategoryRepository(CommonRepository):
    def __init__(self, connection):
        super().__init__(connection, table_name, Item)

