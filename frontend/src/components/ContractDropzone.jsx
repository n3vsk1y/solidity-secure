import { useDropzone } from 'react-dropzone'
import { useCallback } from 'react'

import { processContract } from '../Api.jsx'
import './ContractDropzone.css'

export default function ContractDropzone({ onFilesUploaded }) {
    const onDrop = useCallback(
        async (acceptedFiles) => {
            console.log('Загруженные файлы:', acceptedFiles)

            if (acceptedFiles.length > 0) {
                const file = acceptedFiles[0]
                try {
                    const response = await processContract(file)
                    console.log('Ответ от сервера:', response)

                    if (onFilesUploaded) onFilesUploaded(response)
                } catch (error) {
                    console.error('Ошибка загрузки файла:', error)
                }
            }
        },
        [onFilesUploaded]
    )

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        accept: { 'text/plain': ['.sol'] },
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
            <p className="dropzone-hint">Формат: .sol</p>
        </div>
    )
}
