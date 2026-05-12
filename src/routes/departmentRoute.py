from fastapi import APIRouter, Depends,status, Request
import os
from pathlib import Path
from fastapi.responses import JSONResponse
from models.enums.ResponseEnums import ResponseEnums
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_db_session
from models.request_schema.RequestSchema import DepartmentCreate
from repositories.department_repository import  DepartmentRepository
from models.db_schema.department import Department
from controllers.department_controller import DepartmentController


router = APIRouter(
    prefix="/department",
    tags=["department"]
)


@router.post("/create")
async def create_department(
    department: DepartmentCreate,
    session: AsyncSession = Depends(get_db_session),
    
):
    department_repo = DepartmentRepository(session=session)
    department_controller = DepartmentController()

    
    department_path = await department_controller.get_department_path(department.name)

    

    department = Department(name=department.name)
    if department_repo.is_department_exists(id=department.id):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
        content={"message": ResponseEnums.DEPARTMENT_ALREADY_EXIST.value},
        )
    
    await department_repo.create_department(
        data_department=department
    )


    return JSONResponse(
        content={"message": ResponseEnums.DEPARTMENT_CREATED_SUCCESSFULLY.value},
    )


@router.get("/list")
async def list_departments(
    session: AsyncSession = Depends(get_db_session)
):
    department_repo = DepartmentRepository(session=session)

    department_list = await department_repo.get_all_departments_names()

    return JSONResponse(
        content={
            "message": department_list
        }
    )


@router.delete("/delete/{{department_id}}")
async def delete_department(
    department_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    department_repo = DepartmentRepository(session=session)
    department_controller = DepartmentController()

    department = await department_repo.get_department_by_id(department_id=department_id)

    if department == None :

        return JSONResponse(
        content={
            "message": ResponseEnums.DEPARTMENT_IS_NOT_EXIST.value
            }
        )

 
    _ = await department_controller.remove_department_dir(department_name=department.name)

    _ = await department_repo.delete_department(department_id=department_id)
    return JSONResponse(
        content={
            "message": ResponseEnums.DEPARTMENT_DELETED_SUCCESSFULLY.value
        }
    )
