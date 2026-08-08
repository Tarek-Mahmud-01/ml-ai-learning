"""
BioTime SQL reader — infrastructure adapter (I/O + parsing only, no business math).

Reads a ZKTeco "BioTime" MariaDB dump and yields raw punches from the
`bio_time_raw_attendance_data` INSERT. The dump stores all rows as one huge
multi-row INSERT, so we scan the text with a regex anchored on the constant
`'Department'` column that sits between the employee name and the punch time:

    (id, emp, 'emp_code', 'employee_name', 'Department', 'YYYY-MM-DD HH:MM:SS', ...)
                 ^group1        ^group2                     ^group3

Rows that don't match (e.g. a name containing a quote) are simply skipped; the
importer reports how many punches were read so nothing is hidden.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterator

# 'emp_code','employee_name','Department','punch_time'
_ROW = re.compile(
    r"'([^']+)','([^']*)','Department','"
    r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'"
)


@dataclass(frozen=True)
class Punch:
    emp_code: str
    name: str
    ts: datetime


class BioTimeSqlReader:
    """Turns a BioTime SQL dump into a stream of Punch records."""

    def parse(self, text: str) -> Iterator[Punch]:
        for m in _ROW.finditer(text):
            code, name, ts = m.group(1), m.group(2), m.group(3)
            yield Punch(
                emp_code=code.strip(),
                name=name.strip(),
                ts=datetime.strptime(ts, "%Y-%m-%d %H:%M:%S"),
            )

    def read_punches(self, path: str | Path) -> Iterator[Punch]:
        text = Path(path).read_text(encoding="utf-8", errors="ignore")
        yield from self.parse(text)
