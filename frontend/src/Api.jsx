import axios from 'axios';

const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:8000/api',
    withCredentials: true,
});

export async function sendContractFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await apiClient.post('/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    } catch (error) {
        console.error('Ошибка при отправке файла:', error);
        throw error;
    }
}

export async function sendContractAddress(address) {
    try {
        const response = await apiClient.post('/analyze-address', { address });
        return response.data;
    } catch (error) {
        console.error('Ошибка при отправке адреса:', error);
        throw error;
    }
}