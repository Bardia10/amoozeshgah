from app.models.user import User 
from app.schemas.user import UserCreate 
from app.repository.common import CommonRepository 
from fastapi import Depends

table_name="users"

class UserRepository(CommonRepository):
    def __init__(self, connection):
        super().__init__(connection, table_name, User)

    async def add_or_update(self, item: UserCreate):
        query = """
            INSERT INTO users (username, password_hash, role, firstname, lastname, bio, contact, ssn, year_born)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            ON CONFLICT (username) 
            DO UPDATE SET 
            firstname = EXCLUDED.firstname,
            lastname = EXCLUDED.lastname,
            contact = EXCLUDED.contact,
            bio = EXCLUDED.bio,
            year_born = EXCLUDED.year_born,
            password_hash = EXCLUDED.password_hash
            RETURNING id
        """
        return await self.connection.fetchrow(
        query,
        item.username,
        item.password_hash,
        item.role,
        item.firstname,
        item.lastname,
        item.bio,
        item.contact,
        item.ssn,
        item.year_born
        )

    async def get_teachers_public(self):
        query = f"SELECT id,firstname, lastname , image FROM {self.table_name} WHERE role = $1"
        return await self.connection.fetch(query, "teacher")


    async def update(self,item_id:int, item: UserCreate):
        query = """
            UPDATE users
            SET 
                username = $1,
                password_hash = $2,
                role = $3,
                firstname = $4,
                lastname = $5,
                bio = $6,
                contact = $7,
                ssn = $8,
                year_born = $9
            WHERE id = $10
            RETURNING id
        """
        return await self.connection.fetchrow(
            query,
            item.username,
            item.password_hash,
            item.role,
            item.firstname,
            item.lastname,
            item.bio,
            item.contact,
            item.ssn,
            item.year_born,
            item_id
        )


    async def add(self, item: UserCreate):
        query = """
            INSERT INTO users (username, password_hash, role, firstname, lastname, bio, contact, ssn, year_born)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            RETURNING id
        """
        return await self.connection.fetchrow(
            query,
            item.username,
            item.password_hash,
            item.role,
            item.firstname,
            item.lastname,
            item.bio,
            item.contact,
            item.ssn,
            item.year_born
        )
