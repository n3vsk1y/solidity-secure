import axios from 'axios'

const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:8000/api',
    withCredentials: true,
})

export async function processContract(file) {
    const formData = new FormData()
    formData.append('file', file)

    try {
        const response = await axios.post('/api/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        })
        return response.data
    } catch (error) {
        console.error('Ошибка при отправке файла:', error)
        throw error
    }
}
