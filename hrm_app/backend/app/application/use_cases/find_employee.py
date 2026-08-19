"""
Use case: search employees by a free-text query — name substring(s) or an id
fragment (e.g. "17" -> E100017, "jashim" -> MD JASHIM UDDIN). Filters the in-DB
list; no new repository method needed.
"""
from __future__ import annotations

import re
from difflib import SequenceMatcher

from ...domain.entities import Employee
from ...domain.repositories import EmployeeRepository


def _token_score(tok: str, name_tokens: list[str]) -> float:
    """1.0 on a substring hit, else best fuzzy ratio (so 'joshm'≈'jashim')."""
    best = 0.0
    for nt in name_tokens:
        if tok == nt or tok in nt or nt in tok:
            return 1.0
        best = max(best, SequenceMatcher(None, tok, nt).ratio())
    return best if best >= 0.72 else 0.0

_STOP = {
    "find", "search", "lookup", "look", "up", "employee", "employees", "emp",
    "staff", "worker", "id", "ids", "name", "the", "is", "was", "last", "first",
    "digit", "digits", "whose", "ends", "ending", "end", "with", "of", "for",
    "show", "me", "please", "who", "which", "a", "an", "and",
}


class FindEmployee:
    def __init__(self, employees: EmployeeRepository) -> None:
        self._e = employees

    def execute(self, query: str) -> list[Employee]:
        q = (query or "").strip().lower()
        if not q:
            return []
        digits = re.sub(r"\D", "", q)
        tokens = [t for t in re.findall(r"[a-z]+", q)
                  if t not in _STOP and len(t) >= 2]

        # Score each employee (fuzzy). Noise words score ~0, so the best-matching
        # name still wins even from a messy, misspelled sentence.
        scored: list[tuple[float, Employee]] = []
        for e in self._e.list_all():
            num = e.id.lower().lstrip("e")
            name_tokens = re.findall(r"[a-z]+", e.name.lower())
            score = 0.0
            if digits and (num.endswith(digits) or digits in num):
                score += 3.0
            for t in tokens:
                score += _token_score(t, name_tokens)
            if score > 0:
                scored.append((score, e))
        if not scored:
            return []
        best = max(s for s, _ in scored)
        return [e for s, e in sorted(scored, key=lambda x: (-x[0], len(x[1].name), x[1].id))
                if s >= best - 0.01]
