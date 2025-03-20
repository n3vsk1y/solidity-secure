import ContractDropzone from './components/ContractDropzone'
import './App.css'

function App() {
	const handleFileAccepted = (file) => {
		console.log('FILE PROCESS...')
        // handler
	}

	return (
		<div>
			<ContractDropzone onFilesDroped={handleFileAccepted} />
		</div>
	)
}

export default App
