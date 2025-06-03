import requests
from config import settings

class EtherscanClient:
    @staticmethod
    def get_contract_code(address: str) -> str:
        params = {
            "module": "contract",
            "action": "getsourcecode",
            "address": address,
            "apikey": settings.etherscan_api_key
        }
        response = requests.get(
            "https://api.etherscan.io/api",
            params=params,
            timeout=settings.analysis_timeout
        )
        data = response.json()
        return data["result"][0]["SourceCode"]