from fastapi import routing, Depends, Form, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException 
from pathlib import Path
from schemas.file_dto import FileDTO
import logging
from services.file_manager import FileManager

router = routing.APIRouter(prefix="/files", tags=["files"])

SHARED_FOLDER_PATH = Path.cwd().parent / "shared_folder"
def get_file_manager():
    return FileManager(base_path=SHARED_FOLDER_PATH)

def sum_a_b(a: int, b: int) -> int:
    return a + b


@router.get("/items/{items_path:path}", response_model=list[FileDTO])
async def list_items(items_path: str="", manager: FileManager = Depends(get_file_manager)):
    logging.info(f'recived commad to list items({items_path})')
    user_dto=manager.item_list(items_path)
    return user_dto

@router.get("/download/{item_path:path}", response_class=FileResponse)
async def download_file(item_path: str,  manager: FileManager = Depends(get_file_manager)):
    logging.info(f'recived commad to download file({item_path})')
    try:
        file_path=manager.download_item(item_path)

        return FileResponse(
            path= file_path,
            filename= file_path.name,
            media_type='application/octet-stream')
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/upload", response_model=FileDTO)
async def upload_file(file: UploadFile = File(...), target_path: str = Form(""), manager: FileManager = Depends(get_file_manager)):
    try: 
        user_dto=manager.upload_item(file.filename,file.file, target_path)
        return user_dto
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mkdir", response_model=FileDTO)
async def create_folder(folder_name: str=Form(...), target_path: str = Form(""),manager: FileManager = Depends(get_file_manager)):
    logging.info(f'recived commad to create folder({folder_name}:{target_path})')
    try:
        user_dto=manager.create_folder(folder_name,target_path)
        return user_dto
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{item_path:path}", response_model=FileDTO)
async def delete_item(item_path: str, manager: FileManager = Depends(get_file_manager)):
    logging.info(f'recived commad to delete file original {item_path})')
    try:
        user_dto=manager.delete_item(item_path)
        return user_dto
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/rename/{item_path:path}", response_model=FileDTO)
async def rename_item(old_name: str, new_name: str, manager: FileManager = Depends(get_file_manager)):
    try:
        user_dto=manager.rename_item(old_name, new_name)
        return user_dto
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
