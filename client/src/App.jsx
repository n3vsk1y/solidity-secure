// src/App.jsx
import { useState, useEffect } from 'react'
import LoginPage from './components/LoginPage'
import MainApp from './MainApp'

function App() {
	const [isAuthenticated, setIsAuthenticated] = useState(false)
	const [loading, setLoading] = useState(true)

	useEffect(() => {
		const checkAuth = async () => {
			try {
				const response = await fetch(
					'http://your-fastapi-server/auth/check',
					{
						credentials: 'include',
					}
				)

				if (response.ok) {
					setIsAuthenticated(true)
				}
			} catch (error) {
				console.error('Auth check failed:', error)
			} finally {
				setLoading(false)
			}
		}

		checkAuth()
	}, [])

	if (loading) {
		return <div>Проверка аутентификации...</div>
	}

	return <>{isAuthenticated ? <MainApp /> : <LoginPage />}</>
}

export default App
