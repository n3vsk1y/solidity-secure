import axios from 'axios'

const apiClient = axios.create({
	baseURL: 'http://127.0.0.1:8000/api',
	withCredentials: true,
})

export async function processContract(contract) {
	try {
		const response = await apiClient.post('/login', { username, password })
		apiClient.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`
		return response.data
	} catch (error) {
		throw error.response.data
	}
}