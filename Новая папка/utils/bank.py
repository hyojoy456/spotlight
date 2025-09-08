import json
import random
import uuid
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

BANKS_DIR = Path(__file__).resolve().parent.parent / "banks"
BANKS_DIR.mkdir(parents=True, exist_ok=True)

BANK_NAMES = [f"bank{i}" for i in range(1, 9)]


def _bank_path(bank_name: str) -> Path:
    return BANKS_DIR / f"{bank_name}.json"


def ensure_bank_exists(bank_name: str) -> None:
    path = _bank_path(bank_name)
    if not path.exists():
        path.write_text("[]", encoding="utf-8")


def load_bank(bank_name: str) -> List[Dict[str, Any]]:
    ensure_bank_exists(bank_name)
    path = _bank_path(bank_name)
    try:
        data = json.loads(path.read_text(encoding="utf-8") or "[]")
        if isinstance(data, list):
            return data
        return []
    except Exception:
        return []


def save_bank(bank_name: str, questions: List[Dict[str, Any]]) -> None:
    path = _bank_path(bank_name)
    path.write_text(json.dumps(questions, ensure_ascii=False, indent=2), encoding="utf-8")


def add_text_question(bank_name: str, text: str) -> Dict[str, Any]:
    questions = load_bank(bank_name)
    new_q = {"id": str(uuid.uuid4()), "type": "text", "text": text}
    questions.append(new_q)
    save_bank(bank_name, questions)
    return new_q


def add_mcq_question(bank_name: str, text: str, options: List[Dict[str, str]], correct_key: str) -> Dict[str, Any]:
    questions = load_bank(bank_name)
    new_q = {
        "id": str(uuid.uuid4()),
        "type": "mcq",
        "text": text,
        "options": options,
        "correct_key": correct_key,
    }
    questions.append(new_q)
    save_bank(bank_name, questions)
    return new_q


def parse_pasted_mcq(pasted: str) -> Tuple[str, List[Dict[str, str]]]:
    s = pasted.strip()
    s = re.sub(r"^\s*\d+[\.)\-]\s*", "", s)
    s = re.sub(r"\s+", " ", s)
    parts = re.split(r"\s([a-zA-Z])\)\s", s)
    if len(parts) >= 3 and isinstance(parts[1], str) and len(parts[1]) == 1:
        question_text = parts[0].strip()
        options: List[Dict[str, str]] = []
        i = 1
        while i + 1 < len(parts):
            key = parts[i].lower()
            text = parts[i + 1].strip()
            options.append({"key": key, "text": text})
            i += 2
        return question_text, options
    lines = [ln.strip() for ln in pasted.splitlines() if ln.strip()]
    if not lines:
        return pasted.strip(), []
    question_text = lines[0]
    options = []
    for ln in lines[1:]:
        m = re.match(r"^([a-zA-Z])\)\s*(.+)$", ln)
        if m:
            options.append({"key": m.group(1).lower(), "text": m.group(2).strip()})
    return question_text, options


def get_random_questions_from_bank(bank_name: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    questions = load_bank(bank_name)
    random.shuffle(questions)
    if limit is not None:
        return questions[:limit]
    return questions


def get_random_questions_from_multiple(banks: List[str], limit: Optional[int] = None) -> List[Dict[str, Any]]:
    pool: List[Dict[str, Any]] = []
    for b in banks:
        pool.extend(load_bank(b))
    random.shuffle(pool)
    if limit is not None:
        return pool[:limit]
    return pool
