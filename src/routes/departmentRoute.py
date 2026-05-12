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

    work_dir_src = Path(os.getcwd())
    department_path = os.path.join(work_dir_src,'assets',department.name)

    if os.path.exists(department_path):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
        content={"message": ResponseEnums.DEPARTMENT_ALREADY_EXIST.value},
        )

    department = Department(name=department.name)
    await department_repo.create_department(
        data_department=department
    )

    os.mkdir(path=department_path)

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
    department = await department_repo.get_department_by_id(department_id=department_id)

    if department == None :

        return JSONResponse(
        content={
            "message": ResponseEnums.DEPARTMENT_IS_NOT_EXIST.value
            }
        )

    work_dir_src = Path(os.getcwd())
    department_path = os.path.join(work_dir_src,'assets',department.name)
    os.rmdir(department_path)
    _ = await department_repo.delete_department(department_id=department_id)
    return JSONResponse(
        content={
            "message": ResponseEnums.DEPARTMENT_DELETED_SUCCESSFULLY.value
        }
    )
