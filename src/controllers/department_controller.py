import os
from pathlib import Path


class DepartmentController:

    
    async def get_or_create_department_path(self,department_name:int):
        
        work_dir_src = Path(os.getcwd())
        department_path = os.path.join(work_dir_src,'assets',department_name)
        if os.path.exists(department_path):
            return department_path
        os.mkdir(department_path)
        return department_path
    
    async def remove_department_dir(self,department_name:int):

        path = await self.get_or_create_department_path(department_name)
        if path == None:
            return False
        os.rmdir(path)
        return True
    