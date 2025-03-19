import { useDropzone } from 'react-dropzone'
import { useCallback } from 'react'
import './ContractUploader.css'

export default function ContractDropzone({ onFilesUploaded }) {
	const onDrop = useCallback(
		(acceptedFiles) => {
			console.log('Загруженные файлы:', acceptedFiles)
			if (onFilesUploaded) onFilesUploaded(acceptedFiles)
		},
		[onFilesUploaded]
	)

	const { getRootProps, getInputProps, isDragActive } = useDropzone({
		accept: {
			'text/plain': ['.txt'],
			'application/json': ['.json'],
		},
		multiple: false,
		onDrop,
	})

	return (
		<div
			{...getRootProps()}
			className={`dropzone ${isDragActive ? 'dropzone-active' : ''}`}
		>
			<input {...getInputProps()} />
			<p>
				{isDragActive
					? 'Отпустите файл здесь...'
					: 'Перетащите файл сюда или нажмите для выбора'}
			</p>
			<p className="dropzone-hint">Формат: .txt или .json</p>
		</div>
	)
}
