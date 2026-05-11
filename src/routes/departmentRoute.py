from fastapi import APIRouter, Depends,status, Request
import os
from pathlib import Path
from fastapi.responses import JSONResponse
from models.enums.ResponseEnums import ResponseEnums
from repositories.department_repository import  DepartmentRepository
from app.db.dependencies import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from models.db_schema.department import Department


router = APIRouter(
    prefix="/department",
    tags=["department"]
)


@router.post("/create")
async def create_department(
    department_name: str,
    session: AsyncSession = Depends(get_db_session),
    
):
    department_repo = DepartmentRepository(session=session)

    work_dir_src = Path(os.getcwd())
    department_path = os.path.join(work_dir_src,'assets',department_name)

    if os.path.exists(department_path):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
        content={"message": ResponseEnums.DEPARTMENT_ALREADY_EXIST.value},
        )

    else:
        department = Department(name=department_name)
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