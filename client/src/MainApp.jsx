import { useState, useEffect } from 'react'

import ContractDropzone from './components/ContractDropzone'
import AddressInput from './components/AddressInput'

import { sendContractAddress, sendContractFile } from './Api'

import './MainApp.css'

function MainApp() {
	const [userData, setUserData] = useState(null)
    const [contractAddress, setContractAddress] = useState('')
    const [uploadedFile, setUploadedFile] = useState(null)
    const [loading, setLoading] = useState(false)

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const response = await fetch('http://localhost/api/auth/check')
                const data = await response.json()
                setUserData(data)
            } catch (error) {
                console.error('Ошибка загрузки данных пользователя:', error)
            }
        }
        fetchUserData()
    }, [])

	const handleFileAccepted = (file) => {
		setUploadedFile(file)
		setContractAddress('')
	}

	const handleAddressChange = (newAddress) => {
		setContractAddress(newAddress)
		if (uploadedFile) setUploadedFile(null)
	}

	const handleAnalyze = async () => {
		if (!contractAddress && !uploadedFile) {
			alert('Выберите файл или введите адрес контракта')
			return
		}

		setLoading(true)
		try {
			let response
			if (uploadedFile) {
				response = await sendContractFile(uploadedFile)
			} else if (contractAddress) {
				response = await sendContractAddress(contractAddress)
			}
			console.log('Результат анализа:', response)
		} catch (error) {
			console.error('Ошибка анализа:', error)
			alert('Ошибка анализа. Проверьте данные и попробуйте снова.')
		} finally {
			setLoading(false)
		}
	}

	const handleLogout = async () => {
        try {
            localStorage.removeItem("access_token")
            setUserData(null)
            location.reload()
        } catch (error) {
            console.error('Logout failed:', error)
        }
    }

	return (
		<main>
			{userData && (
                <header>
                    <div className="user-info">
                        <img 
                            src={userData.picture} 
                            alt="User avatar" 
                            className="user-avatar"
                        />
                        <span className="user-name">{userData.name}</span>
                        <span className="user-email">({userData.email})</span>
                    </div>
                    <button onClick={handleLogout} className="logout-btn">
                        Выйти
                    </button>
                </header>
            )}
			<div className="zone">
				<ContractDropzone
					onFilesDropped={handleFileAccepted}
					disabled={!!contractAddress}
				/>
			</div>
			<span className="or">или</span>
			<div className="address">
				<AddressInput
					value={contractAddress}
					onChange={handleAddressChange}
					disabled={!!uploadedFile}
				/>
			</div>
			<button
				className="analyze"
				onClick={handleAnalyze}
				disabled={loading}
			>
				{loading ? 'Анализирую...' : 'Анализировать'}
			</button>
		</main>
	)
}

export default MainApp
