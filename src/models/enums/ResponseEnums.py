from enum import Enum

class ResponseEnums(Enum):
    DEPARTMENT_ALREADY_EXIST = "department is already exist"
    DEPARTMENT_CREATED_SUCCESSFULLY = "department created successfully"
    DEPARTMENT_IS_NOT_EXIST = "department is not exist for deletion"
    DEPARTMENT_DELETED_SUCCESSFULLY = "department deleted successfully"

    DEPARTMENT_NOT_FOUND = "DEPARTMENT_NOT_FOUND please add DEPARTMENT first"

    DOCUMENT_UPLOADED_SUCCESSFULLY = "DOCUMENT_UPLOADED_SUCCESSFULLY"
    DOCUMENT_ALREADY_EXIST = "document is already exist"
    DOCUMENT_LARGER_THAN_ALLOWED = "DOCUMENT_LARGER_THAN_ALLOWED"
    DOCUMENT_DELETED_SUCCESSFULLY = "department deleted successfully"

