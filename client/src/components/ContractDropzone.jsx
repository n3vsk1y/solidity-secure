import { useDropzone } from 'react-dropzone'
import { useCallback, useState } from 'react'

import './ContractDropzone.css'

export default function ContractDropzone({
	onFilesDropped,
	disabled,
	uploadedFile,
}) {
	const [file, setFile] = useState(uploadedFile || null)

	const onDrop = useCallback(
		async (acceptedFiles) => {
			if (disabled) return
			if (acceptedFiles.length > 0) {
				const selectedFile = acceptedFiles[0]
				setFile(selectedFile)
				if (onFilesDropped) onFilesDropped(selectedFile)
			}
		},
		[onFilesDropped, disabled]
	)

	const removeFile = (e) => {
		e.stopPropagation()
		setFile(null)
		if (onFilesDropped) onFilesDropped(null)
	}

	const { getRootProps, getInputProps, isDragActive } = useDropzone({
		accept: { 'text/plain': ['.sol'] },
		multiple: false,
		onDrop,
		noClick: !!file || disabled,
	})

	return (
		<div
			{...getRootProps()}
			className={`dropzone ${isDragActive ? 'dropzone-active' : ''} ${
				file ? 'dropzone-filled' : ''
			} ${disabled ? 'dropzone-disabled' : ''}`}
		>
			<input {...getInputProps()} disabled={disabled} />
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
						{disabled
							? 'Загрузка файлов недоступна при вводе адреса'
							: isDragActive
							? 'Отпустите файл здесь...'
							: 'Перетащите сюда файл с контрактом'}
					</p>
					<p className="dropzone-hint">Формат: .sol</p>
				</>
			)}
		</div>
	)
}
