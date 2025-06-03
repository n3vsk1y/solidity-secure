import subprocess
import tempfile
import os
import json
import logging
from typing import List
from schemas import AnalysisResult, Severity

logger = logging.getLogger(__name__)

class SolidityAnalyzer:
    @staticmethod
    def analyze(code: str) -> List[AnalysisResult]:
        results = []
        with tempfile.NamedTemporaryFile(delete=False, suffix=".sol", mode="w", encoding="utf-8") as temp_sol:
            temp_sol.write(code)
            temp_sol_path = temp_sol.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_json:
            temp_json_path = temp_json.name

        if os.path.exists(temp_json_path):
            os.unlink(temp_json_path)

        try:
            proc = subprocess.run(
                ["slither", temp_sol_path, "--json", temp_json_path],
                capture_output=True, text=True
            )

            if proc.stderr:
                logger.warning(f"SLITHER STDERR: {proc.stderr.strip()}")
            with open(temp_sol_path, "r", encoding="utf-8") as f:
                sol_content = f.read()
                if not sol_content.strip():
                    logger.warning("ВНИМАНИЕ: temp_sol пустой!")

            if not os.path.exists(temp_json_path):
                logger.error("Slither не создал JSON файл.")
                return results

            if os.path.getsize(temp_json_path) == 0:
                logger.warning("Slither JSON файл пустой.")
                return results

            with open(temp_json_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    logger.error("Slither вывел некорректный JSON.")
                    return results

            detectors = data.get("results", {}).get("detectors", [])
            if not detectors:
                logger.info("Slither не нашёл уязвимостей или не смог проанализировать контракт.")

            for issue in detectors:
                impact = issue.get("impact", "").upper()
                try:
                    severity = Severity(impact)
                except ValueError:
                    severity = Severity.LOW

                results.append(
                    AnalysisResult(
                        contract=issue.get("contract", ""),
                        severity=severity,
                        title=issue.get("check", ""),
                        description=issue.get("description", "").strip(),
                        impact=issue.get("impact", ""),
                        confidence=issue.get("confidence", "")
                    )
                )
        finally:
            os.unlink(temp_sol_path)
            if os.path.exists(temp_json_path):
                os.unlink(temp_json_path)
        return results