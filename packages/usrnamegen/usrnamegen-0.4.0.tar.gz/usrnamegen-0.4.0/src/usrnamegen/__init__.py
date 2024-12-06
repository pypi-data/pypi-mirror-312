import random
from pathlib import Path


_ROOT = Path(__file__).parent


def generate_username(
    min_len: int | None = None,
    max_len: int | None = None
) -> str:
    noun_list = (_ROOT / 'words/nouns.txt').read_text().strip().split('\n')
    adjective_list = (_ROOT / 'words/adjectives.txt').read_text().strip().split('\n')
    censored = (_ROOT / 'words/blacklist.txt').read_text().strip().split('\n')

    for _ in range(1_000_000):
        adjective = random.choice(adjective_list)
        noun = random.choice(noun_list)

        if adjective in censored or noun in censored:
            continue

        if _chance(0.50):
            adjective = adjective.title()

        if _chance(0.50):
            noun = noun.title()

        sep = '_' if _chance(0.50) else ''

        username = f'{adjective}{sep}{noun}{random.randint(1, 999_999)}'

        if min_len is not None and len(username) < min_len:
            continue

        if max_len is not None and len(username) > max_len:
            continue

        return username

    raise RuntimeError("Can't generate username. Change params.")


def _chance(
    value: float
) -> bool:
    assert 0 < value < 1
    return random.random() < value
