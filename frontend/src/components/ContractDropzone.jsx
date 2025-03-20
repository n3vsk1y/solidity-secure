import { useDropzone } from 'react-dropzone'
import { useCallback, useState } from 'react'

import './ContractDropzone.css'

export default function ContractDropzone({ onFilesDropped }) {
	const [file, setFile] = useState(null)

	const onDrop = useCallback(
		async (acceptedFiles) => {
			if (acceptedFiles.length > 0) {
				const selectedFile = acceptedFiles[0]
				setFile(selectedFile)

				try {
					// const response = await processContract(selectedFile);
					const response = 'success'
					console.log('SERVER RESPONSE:', response)

					if (onFilesDropped) {
						onFilesDropped(response)
					}
				} catch (error) {
					console.error('FILE ERROR:', error)
				}
			}
		},
		[onFilesDropped]
	)

	const removeFile = (e) => {
		e.stopPropagation()
		setFile(null)
	}

	const { getRootProps, getInputProps, isDragActive } = useDropzone({
		accept: { 'text/plain': ['.sol'] },
		multiple: false,
		onDrop,
		noClick: !!file,
	})

	return (
		<div
			{...getRootProps()}
			className={`dropzone ${isDragActive ? 'dropzone-active' : ''} ${
				file ? 'dropzone-filled' : ''
			}`}
		>
			<input {...getInputProps()} />
			{file ? (
				<div className="file-info">
					<p>Загружен: {file.name}</p>
					<button className="remove-btn" onClick={removeFile}>
						Удалить
					</button>
				</div>
			) : (
				<>
					<p>
						{isDragActive
							? 'Отпустите файл здесь...'
							: 'Перетащите файл сюда или нажмите для выбора'}
					</p>
					<p className="dropzone-hint">Формат: .sol</p>
				</>
			)}
		</div>
	)
}
