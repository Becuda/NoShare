export const Api = {
    async fetchItems(path = '') {
        const response = await fetch(`/files/items/${path}`);
        if (!response.ok) throw new Error('Не удалось загрузить список файлов');
        return await response.json();
    },

    getDownloadUrl(path) {
        return `/files/download/${path}`;
    },

    async createFolder(targetPath, name) {
        const formData = new FormData();
        formData.append('target_path', targetPath);
        formData.append('folder_name', name);
        const response = await fetch('/files/mkdir',
            {
                method: 'POST',
                body: formData
        });
        if (!response.ok) throw new Error('Не удалось создать папку');
        return await response.json();
    },

    async deleteItem(path) {
        const response = await fetch(`/files/delete/${path}`, {
            method: 'DELETE'
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Ошибка при удалении');
        }
        return await response.json();
    },

    async uploadFile(targetPath, file) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('target_path', targetPath);

        const response = await fetch('/files/upload',
            {
            method: 'POST',
            body: formData
        });
        if (!response.ok) {
            const errorText = await response.text(); 
            console.error('Сервер ответил ошибкой:', errorText);
            throw new Error(`Сервер вернул ${response.status}: ${errorText}`);
        }
        return await response.json();
    }
};