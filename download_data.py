"""Скачивание файлов HI-Small из датасета IBM Transactions for AML (Kaggle) в папку data/."""

import shutil
import sys
from pathlib import Path

import kagglehub

DATASET = "ealtman2019/ibm-transactions-for-anti-money-laundering-aml"
FILES = {
    "HI-Small_Patterns.txt": 323_844,
    "HI-Small_accounts.csv": 34_053_187,
    "HI-Small_Trans.csv": 475_664_283,
}
DATA_DIR = Path(__file__).resolve().parent / "data"


def find_file(root: Path, name: str) -> Path | None:
    if root.is_file():
        return root if root.name == name else None
    matches = list(root.rglob(name))
    return matches[0] if matches else None


def main() -> int:
    DATA_DIR.mkdir(exist_ok=True)
    failed = []
    for name, size in FILES.items():
        target = DATA_DIR / name
        if target.exists() and target.stat().st_size == size:
            print(f"{name}: уже есть, {size:,} байт", flush=True)
            continue
        print(f"{name}: скачивание, {size / 1e6:.1f} МБ", flush=True)
        result = Path(kagglehub.dataset_download(DATASET, path=name, output_dir=str(DATA_DIR)))
        found = find_file(result, name)
        if found is None:
            print(f"{name}: файл не найден после скачивания ({result})", flush=True)
            failed.append(name)
            continue
        if found != target:
            shutil.move(str(found), target)
        got = target.stat().st_size
        status = "OK" if got == size else f"размер не совпал, ожидалось {size:,}"
        print(f"{name}: {got:,} байт, {status}", flush=True)
        if got != size:
            failed.append(name)
    print("Готово" if not failed else f"Ошибки: {', '.join(failed)}", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
