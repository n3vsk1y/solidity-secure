// src/App.jsx
import { useState, useEffect } from 'react'
import LoginPage from './components/LoginPage'
import MainApp from './MainApp'

import ProtectedRoute from './components/ProtectedRoute'

function App() {
	const [isAuthenticated, setIsAuthenticated] = useState(false)
	const [loading, setLoading] = useState(true)

	useEffect(() => {
		const url = new URL(window.location.href)
		const accessToken = url.searchParams.get('access_token')
		console.log('access: ', accessToken)

		if (accessToken) {
			localStorage.setItem('access_token', accessToken)
			setIsAuthenticated(true)
			setLoading(false)
			window.history.replaceState({}, document.title, '/')
			return
		}

		const checkAuth = async () => {
			try {
				const response = await fetch(
					'http://localhost/api/auth/check',
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

	return <>{isAuthenticated ? <ProtectedRoute><MainApp /></ProtectedRoute> : <LoginPage />}</>
}

export default App
