import { Api } from './api.js';
import { Renderer } from './renderer.js';

const App = {
    state: {
        currentPath: '',
        items: []
    },

    async init() {
        console.log("App initialized");
        this.setupEventListeners();
        await this.loadPath('');
    },

    async loadPath(newPath) {
        try {
            this.state.currentPath = newPath;
            const items = await Api.fetchItems(newPath);
            this.state.items = items;
            
            this.render();
        } catch (error) {
            console.error(error);
            alert("Ошибка загрузки: " + error.message);
        }
    },

    render() {
        const container = document.getElementById('file-list-container');
        container.innerHTML = '';

        Renderer.renderBreadcrumbs(this.state.currentPath, (path) => this.loadPath(path));

        if (this.state.items.length === 0) {
            container.innerHTML = '<div class="text-center p-5 text-muted">Папка пуста</div>';
            return;
        }

        this.state.items.forEach(item => {
            const row = Renderer.createItemRow(item, {
                onNavigate: (name) => {
                    const nextPath = this.state.currentPath ? `${this.state.currentPath}/${name}` : name;
                    this.loadPath(nextPath);
                },
                onDownload: (name) => {
                    const fullPath = this.state.currentPath ? `${this.state.currentPath}/${name}` : name;
                    window.location.href = Api.getDownloadUrl(fullPath);
                },
                onDelete: async (name) => {
                    const fullPath = this.state.currentPath ? `${this.state.currentPath}/${name}` : name;
                    await Api.deleteItem(fullPath);
                    await this.loadPath(this.state.currentPath); // Обновляем список
                }
            });
            container.appendChild(row);
        });
    },

    setupEventListeners() {
        const dropZone = document.getElementById('main-drop-zone');
        const fileInput = document.createElement('input'); 
        fileInput.type = 'file';
        fileInput.multiple = true;

        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
            }, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.add('drag-over');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.remove('drag-over');
            }, false);
        });

        dropZone.addEventListener('drop', async (e) => {
            const files = e.dataTransfer.files;
            
            if (files.length > 0) {
                for (const file of files) {
                    try {
                        await Api.uploadFile(this.state.currentPath, file);
                    } catch (error) {
                        console.error("Ошибка при дропе файла:", error);
                    }
                }
                await this.loadPath(this.state.currentPath); 
            }
        });

        dropZone.onclick = () => fileInput.click();

        fileInput.onchange = async () => {
            for (const file of fileInput.files) {
                await Api.uploadFile(this.state.currentPath, file);
            }
            await this.loadPath(this.state.currentPath);
        };

        const confirmFolderBtn = document.getElementById('confirmCreateFolderBtn');
        const folderInput = document.getElementById('newFolderName');
        const openModalBtn = document.getElementById('create-folder-btn');

        if (confirmFolderBtn) {
            confirmFolderBtn.onclick = async () => {
                const name = folderInput.value.trim();
                if (!name) return;

                try {
                    await Api.createFolder(this.state.currentPath, name);
                    
                    const modalEl = document.getElementById('createFolderModal');
                    const modal = bootstrap.Modal.getInstance(modalEl);
                    if (modal) modal.hide();
                    
                    folderInput.value = ''; 
                    await this.loadPath(this.state.currentPath);
                } catch (e) {
                    alert(e.message);
                }
            };
        }


        if (openModalBtn) {
            openModalBtn.onclick = () => {
                const modal = new bootstrap.Modal(document.getElementById('createFolderModal'));
                modal.show();
            };
        }


        const uploadInput = document.getElementById('file-upload-input');
        if (uploadInput) {
            uploadInput.onchange = async (e) => {
                const file = e.target.files[0];
                if (!file) return;
                
                try {
                    await Api.uploadFile(this.state.currentPath, file);
                    uploadInput.value = '';
                    await this.loadPath(this.state.currentPath);
                } catch (error) {
                    alert("Ошибка загрузки: " + error.message);
                }
            };
        }
    }
};

document.addEventListener('DOMContentLoaded', () => App.init());