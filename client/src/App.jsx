import { useState } from 'react';
import ContractDropzone from './components/ContractDropzone';
import AddressInput from './components/AddressInput';
import { sendContractAddress, sendContractFile } from './Api';

import './App.css';

function App() {
    const [contractAddress, setContractAddress] = useState('');
    const [uploadedFile, setUploadedFile] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleFileAccepted = (file) => {
        setUploadedFile(file);
        setContractAddress('');
    };

    const handleAddressChange = (newAddress) => {
        setContractAddress(newAddress);
        if (uploadedFile) setUploadedFile(null);
    };

    const handleAnalyze = async () => {
        if (!contractAddress && !uploadedFile) {
            alert('Выберите файл или введите адрес контракта');
            return;
        }

        setLoading(true);
        try {
            let response;
            if (uploadedFile) {
                response = await sendContractFile(uploadedFile);
            } else if (contractAddress) {
                response = await sendContractAddress(contractAddress);
            }
            console.log('Результат анализа:', response);
        } catch (error) {
            console.error('Ошибка анализа:', error);
            alert('Ошибка анализа. Проверьте данные и попробуйте снова.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <main>
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
            <button className="analyze" onClick={handleAnalyze} disabled={loading}>
                {loading ? 'Анализирую...' : 'Анализировать'}
            </button>
        </main>
    );
}

export default App;