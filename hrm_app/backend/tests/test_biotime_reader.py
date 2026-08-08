"""Infra test: the BioTime SQL reader extracts punches from a dump fragment."""
from datetime import datetime

from app.infrastructure.io.biotime_reader import BioTimeSqlReader

# A tiny slice shaped exactly like the real dump's raw-attendance INSERT.
SAMPLE = (
    "INSERT INTO `bio_time_raw_attendance_data` VALUES "
    "(262,13,'12','MDMILON','Department','2024-08-22 06:57:58','255',15,'0',NULL,"
    "'three-arrows','CQUG233760513',0.00,255,'SpeedFace-V5L','2024-08-22 11:48:06',0),"
    "(263,13,'12','MDMILON','Department','2024-08-22 06:58:00','255',15,'0',NULL,"
    "'three-arrows','CQUG233760513',0.00,255,'SpeedFace-V5L','2024-08-22 11:48:06',0),"
    "(105343,15,'100017','MD JASHIM UDDIN','Department','2026-07-27 08:44:18','255',1,'0',"
    "NULL,'three-arrows','CQUG233760513',0.00,255,'SpeedFace-VL5','2026-07-27 08:44:19',1);"
)


def test_reader_extracts_code_name_and_time():
    punches = list(BioTimeSqlReader().parse(SAMPLE))
    assert len(punches) == 3

    first = punches[0]
    assert first.emp_code == "12"
    assert first.name == "MDMILON"
    assert first.ts == datetime(2024, 8, 22, 6, 57, 58)

    last = punches[-1]
    assert last.emp_code == "100017"
    assert last.name == "MD JASHIM UDDIN"
    assert last.ts == datetime(2026, 7, 27, 8, 44, 18)
