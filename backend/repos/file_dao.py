import shutil
import logging
from pydantic import BaseModel
from pathlib import Path


class ItemInfo(BaseModel):
    name: str
    extension: str
    size: int
    is_dir: bool
    timestamp: float

class FileDAO:

    def __init__(self, base_path: str):
        self.base_path = Path(base_path).resolve()    

    def safe_path(self, relative_path: str) -> Path:
        target_path = (self.base_path / relative_path).resolve()
        if not str(target_path).startswith(str(self.base_path)):
            raise ValueError("Access denied")
        return target_path
    
    #FOLDER OPERATIONS 

    def create_folder(self, folder_name: str, relative_path: str = ""):
        target_path = self.safe_path(relative_path) / folder_name
        logging.info(f'DAO safe path to create path: {target_path}')
        try:
            target_path.mkdir(parents=True, exist_ok=True)
            return target_path
        except Exception as e:
            raise ValueError(str(e))


    def rename_folder(self, old_name: str, new_name: str, relative_path: str = ""):
        old_path = self.safe_path(relative_path) / old_name
        new_path = self.safe_path(relative_path) / new_name
        if not old_path.is_dir():
            raise ValueError("Path is not a directory")
        old_path.rename(new_path)
        
    def delete_folder(self, folder_name: str, relative_path: str = ""):
        target_path = self.safe_path(relative_path) / folder_name
        if not target_path.is_dir():
            raise ValueError("Path is not a directory")
        shutil.rmtree(target_path)
    
    #FILE OPERATIONS
    
    def get_file_for_download(self, file_name: str, relative_path: str = ""):
        target_path = self.safe_path(relative_path) / file_name
        if not target_path.is_file():
            raise ValueError("Path is not a file")
        with open(target_path, "r") as f:
            return target_path

    def create_file(self, file_name: str, file_obj, relative_path: str = "") -> Path:   
        target_path = self.safe_path(relative_path) / file_name
        logging.info(f'DAO safe path to create path: {target_path}')
        try:
            with open(target_path, "wb") as buffer:
                shutil.copyfileobj(file_obj, buffer)
            return target_path
        
        except Exception as e:
            raise ValueError(str(e))

    def delete_file(self, file_name: str, relative_path: str = ""):
        target_path = self.safe_path(relative_path) / file_name
        
        if not target_path.is_file():
            raise ValueError("Path is not a file")
        target_path.unlink()

    def rename_file(self, old_name: str, new_name: str, relative_path: str = ""):
        old_path = self.safe_path(relative_path) / old_name
        new_path = self.safe_path(relative_path) / new_name
        
        if not old_path.is_file():
            raise ValueError("Path is not a file")
        old_path.rename(new_path)

    #GENERAL OPERATIONS
    def item_info(self, item_name: str="", relative_path: str = "") -> ItemInfo:
        target_path = self.safe_path(relative_path) / item_name
        if not target_path.exists():
            raise ValueError("Path not found")
        stats = target_path.stat()
        return ItemInfo(
            name=target_path.name,
            extension=target_path.suffix,
            size=stats.st_size,
            is_dir=target_path.is_dir(),
            timestamp=stats.st_mtime
        )
    def folder_items(self,relative_path="") -> list[ItemInfo]:
        logging.info(f'DAO get path {relative_path}')
        target_path = self.safe_path(relative_path)
        logging.info(f'DAO make save path {target_path}')
        if not target_path.exists():
            raise ValueError("Path not found")
        if not target_path.is_dir:
            raise ValueError("Path is not a directory")
        
        items=[]
        for item in target_path.iterdir():
            stats=item.stat()
            item= ItemInfo(
                name=item.name,
                extension=item.suffix,
                size=stats.st_size,
                is_dir=item.is_dir(),
                timestamp=stats.st_mtime
            )
            items.append(item)
        return items


                