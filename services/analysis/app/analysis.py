import os
import tempfile

from fastapi import APIRouter, UploadFile, File, HTTPException
from analyzer import SolidityAnalyzer
from etherscan import EtherscanClient
from schemas import AnalysisResult

analysis = APIRouter(tags=["Analyze"])

@analysis.post("/file", response_model=list[AnalysisResult])
async def analyze_file(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".sol") as temp:
            content = await file.read()
            temp.write(content)
            temp_path = temp.name
            try:
                code_str = content.decode("utf-8")
                results = SolidityAnalyzer.analyze(code_str)
                return results
            finally:
                os.unlink(temp_path)
            
    except Exception as e:
        raise HTTPException(400, detail=f"File analysis error: {str(e)}")

@analysis.post("/address", response_model=list[AnalysisResult])
async def analyze_address(address: str):
    try:
        code = EtherscanClient.get_contract_code(address)
        return SolidityAnalyzer.analyze(code)
    except Exception as e:
        raise HTTPException(400, detail=f"Address analysis error: {str(e)}")