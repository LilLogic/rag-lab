from pathlib import Path


def find_project_root(marker="requirements.txt"):
    current = Path(__file__).resolve()

    while current != current.parent:
        if (current / marker).exists():
            return current
        current = current.parent

    raise RuntimeError(f"{marker} not found")


ROOT_DIR = find_project_root()
