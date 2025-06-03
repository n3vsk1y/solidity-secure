from pydantic import BaseModel
from enum import Enum

class Severity(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class AnalysisResult(BaseModel):
    contract: str
    severity: Severity
    title: str
    description: str
    impact: str | None = None
    confidence: str | None = None 
