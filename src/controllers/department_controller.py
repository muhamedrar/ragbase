import os
from pathlib import Path


class DepartmentController:
    
    @classmethod
    def make_department_path(self,department_name:int):
        work_dir_src = Path(os.getcwd())
        department_path = os.path.join(work_dir_src,'assets',department_name)
        return department_path
    
    def get_department_path(self,department_name:int):
        department_path = self.make_department_path(department_name=department_name)
        if not os.path.exists(department_path):
            return None
        return department_path

    def create_department_path(self,department_name:int):
        department_path = self.make_department_path(department_name=department_name)
        if self.get_department_path(department_name=department_name) == None:
            os.mkdir(department_path)
            return department_path
        return department_path
    
    def remove_department_dir(self,department_name:int):

        path = self.get_department_path(department_name)
        if path == None:
            return False
        os.rmdir(path)
        return True
    