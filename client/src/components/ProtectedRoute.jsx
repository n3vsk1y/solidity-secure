import LoginPage from './LoginPage'

const ProtectedRoute = ({ children }) => {
	const token = localStorage.getItem('access_token')

	if (!token) {
		console.log('%c' + 'INVALID ACCESS\nPLEASE LOGIN', 'color: red')
		return <LoginPage />
	}
	return children
}

export default ProtectedRoute