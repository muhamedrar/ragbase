from models.db_schema.department import Department
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete , exists
import logging

logger = logging.getLogger("uvicorn.error")

class DepartmentRepository:

    def __init__(self, session:AsyncSession):
        self.session = session


    async def create_department(self,data_department:dict):
        if await self.is_department_exists(data_department["name"]):
            logger.warning(f"Department with name {data_department['name']} already exists")
            return None
        else:
            new_department = Department(**data_department)
            
            await self.session.add(new_department)
            await self.session.commit()
            await self.session.refresh(new_department)

            return new_department
    
    
    async def delete_department(self,department_id:int):
        stmt = delete(Department).where(Department.id==department_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount
    
        

    async def is_department_exists(self,name:str):
        stmt = select(
            exists().where(Department.name==name)
        )

        result = await self.session.execute(stmt)
        return result.scalar()

   