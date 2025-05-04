import React from 'react'
import './LoginPage.css'

function LoginPage({ onLogin }) {
	const handleGoogleLogin = async () => {
		try {
			const response = await fetch('http://localhost/api/auth/login', {
				method: 'GET',
				credentials: 'include',
			})
		} catch (error) {
			console.error('Ошибка при авторизации:', error)
		}
	}

	return (
		<div className="login-container">
			<h1>Анализ смарт-контрактов</h1>
			<p>Для продолжения войдите через Google</p>
			<button onClick={handleGoogleLogin} className="google-login-btn">
				<img
					src="https://upload.wikimedia.org/wikipedia/commons/2/2d/Logo_Google_blanco.png"
					alt="Google logo"
				/>
				Войти через Google
			</button>
		</div>
	)
}

export default LoginPage
