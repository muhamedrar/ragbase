from models.db_schema.department import Department
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete , exists



class DepartmentRepository:

    def __init__(self, session:AsyncSession):
        self.session = session


    async def create_department(self,data_department:Department):
        if await self.is_department_exists(data_department.id):
            return None
        else:
            
            self.session.add(data_department)
            await self.session.commit()
            await self.session.refresh(data_department)

            return data_department
    
    
    async def delete_department(self,department_id:int):
        stmt = delete(Department).where(Department.id==department_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount
    
        

    async def is_department_exists(self,id:int):
        stmt = select(
            exists().where(Department.id==id)
        )

        result = await self.session.execute(stmt)
        return result.scalar()
    
    async def get_all_departments_names(self):
        if not await self.any_department_exists():
            return []
        else:
            stmt = select(Department.name)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        
    async def get_department_by_id(self,department_id):
        stmt = select(Department).where(Department.id==department_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    

    async def any_department_exists(self):
        stmt = select(
            exists().where(Department.id!=None)
        )
        result = await self.session.execute(stmt)

        return result.scalar()