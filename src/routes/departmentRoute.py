from fastapi import APIRouter, Depends,status
import os
from pathlib import Path
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/department",
    tags=["department"]
)


@router.post("/create")
async def create_department(department_name: str):
 
    work_dir_src = Path(os.getcwd())
    department_path = os.path.join(work_dir_src,'assets',department_name)

    if os.path.exists(department_path):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
        content={"message": f"department {department_name} is already exist"},
        )

    else:
        os.mkdir(path=department_path)

        return JSONResponse(
            content={"message": f"department {department_name} created successfally"},
        )