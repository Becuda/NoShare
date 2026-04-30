import shutil

import logging
from pathlib import Path
from schemas.file_dto import FileDTO, OperationType,OperationStatus
from repos.file_dao import FileDAO
from datetime import datetime

class FileManager:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path).resolve()
        self.file_dao = FileDAO(base_path)

    def item_to_DTO(self, item: FileDTO, operation_type: OperationType=None, operation_status: OperationStatus=None):
        return FileDTO(
            name=item.name,
            extension=item.extension,
            size=item.size,
            is_dir=item.is_dir,
            timestamp=datetime.fromtimestamp(item.timestamp).isoformat(),
            operation_type=operation_type,
            operation_status=operation_status
            )
    
    def create_folder(self, folder_name: str, relative_path: str = ""):
        logging.info(f'File manager create folder {folder_name}')
        folder_path=self.file_dao.create_folder(folder_name, relative_path)
        item=self.file_dao.item_info(folder_name, relative_path)
        return self.item_to_DTO(item, OperationType.CREATE, OperationStatus.SUCCESS)

    def download_item(self, item_name: str, relative_path: str = "") -> Path:
        target_path: Path = self.file_dao.safe_path(relative_path)/item_name
        logging.info(f'target_path {target_path.is_dir()}')
        logging.info(f'target_path type {target_path.__class__}')
        if target_path.is_dir():
            raise ValueError("Path is not a file")
        return target_path
    
    def upload_item(self, file_name: str, file_obj, relative_path: str = ""):
        logging.info(f'File manager upload file {file_name}')
        self.file_dao.create_file(file_name, file_obj, relative_path)
        item=self.file_dao.item_info(file_name, relative_path)
        logging.info(item)
        return self.item_to_DTO(item, OperationType.UPLOAD, OperationStatus.SUCCESS)

    def item_info(self, item_name: str="", relative_path: str = "") -> FileDTO:
        item = self.file_dao.item_info(item_name, relative_path)
        return self.item_to_DTO(item, OperationType.INFO, OperationStatus.SUCCESS)
    
    def item_list(self,relative_path: str="") -> list[FileDTO]:
        logging.info(f'File manager get path {relative_path}')
        raw_items= self.file_dao.folder_items(relative_path)
        # yep, its look like duplicated code...
        items: list[FileDTO] = [] 

        for item in raw_items:
            items.append(self.item_to_DTO(item, OperationType.INFO, OperationStatus.SUCCESS))
        
        items=sorted(items, key=lambda item: (not item.is_dir, item.name.lower()))
        return items
    
    def delete_item(self, name: str, relative_path: str = ""):
        item=self.file_dao.item_info(name, relative_path)
        if item.is_dir:
            self.file_dao.delete_folder(name, relative_path)
        else:
            self.file_dao.delete_file(name, relative_path)   

        dto = self.item_to_DTO(item,OperationType.DELETE, OperationStatus.SUCCESS)
        return dto
    
    def rename_item(self, old_name: str, new_name: str, relative_path: str = ""):
        target_path = self.file_dao.safe_path(relative_path) / old_name
        

        if target_path.is_dir():
            self.file_dao.rename_folder(old_name, new_name, relative_path)
        elif target_path.is_file():
            self.file_dao.rename_file(old_name, new_name, relative_path)
        else:
            raise ValueError("Item not found")
        
        item=self.file_dao.item_info(new_name, relative_path)
        dto = self.item_to_DTO(item,OperationType.RENAME, OperationStatus.SUCCESS)
        return dto
