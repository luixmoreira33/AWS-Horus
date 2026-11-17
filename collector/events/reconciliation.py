"""
Reconciliação periódica (full scan) para corrigir drift.
Deve ser agendada via EventBridge Scheduler (ex.: a cada 6h).
"""
from collector.runner import run_full_scan
import os

def run_reconciliation():
    external_id = os.environ["EXTERNAL_ID"]
    mode = os.getenv("DEPLOY_MODE", "lite")
    dsn = os.getenv("DATABASE_URL")
    result = run_full_scan(external_id=external_id, mode=mode, dsn=dsn)
    return result
