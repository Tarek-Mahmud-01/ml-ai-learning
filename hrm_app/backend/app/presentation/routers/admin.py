"""Admin endpoints — seed demo data, import real biometric data, and train."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from ...application.use_cases.import_bio_time import ImportBioTime
from ...application.use_cases.seed_month import SeedMonth
from ...application.use_cases.train_model import TrainModel
from ...infrastructure.config import settings
from ..deps import import_uc, seed_uc, train_uc
from ..schemas import (
    ImportRequest,
    ImportResult,
    SeedRequest,
    SeedResult,
    TrainResult,
)

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/seed", response_model=SeedResult)
def seed(body: SeedRequest, uc: SeedMonth = Depends(seed_uc)) -> SeedResult:
    year, mon = int(body.month[:4]), int(body.month[5:7])
    return SeedResult(**uc.execute(year, mon))


@router.post("/import", response_model=ImportResult)
def import_bio(
    body: ImportRequest, uc: ImportBioTime = Depends(import_uc)
) -> ImportResult:
    path = body.path or settings.import_sql_path
    return ImportResult(**uc.execute(
        path, replace=body.replace, merge_seconds=body.merge_seconds))


@router.post("/train", response_model=TrainResult)
def train(uc: TrainModel = Depends(train_uc)) -> TrainResult:
    return TrainResult(samples_trained=uc.execute().samples)
