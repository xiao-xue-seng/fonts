from __future__ import annotations

import json
import warnings
from pathlib import Path

from sync_amec_from_fonts import sync_amec_by_id


ROOT = Path(__file__).resolve().parent.parent
FONTS_PATH = ROOT / 'api' / 'fonts.json'
AMEC_PATH = ROOT / 'api' / 'amec.json'


def test_sync_amec_by_id_sorts_and_warns_for_missing_ids() -> None:
    fonts = [
        {'id': 'zeta', 'name': 'Zeta'},
        {'id': 'alpha', 'name': 'Alpha'},
    ]
    amec = [
        {'id': 'zeta', 'name': 'Zeta'},
        {'id': 'missing-id', 'name': 'Ghost'},
        {'id': 'alpha', 'name': 'Alpha'},
    ]

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        synced = sync_amec_by_id(fonts, amec)

    assert [item['id'] for item in synced] == ['alpha', 'zeta']
    assert any('missing-id' in str(w.message) for w in caught)


def main() -> None:
    fonts = json.loads(FONTS_PATH.read_text(encoding='utf-8'))
    amec = json.loads(AMEC_PATH.read_text(encoding='utf-8'))

    synced = sync_amec_by_id(fonts, amec)
    by_id = {item['id']: item for item in synced}

    for item in amec:
        if item['id'] not in by_id:
            raise AssertionError(f"Stale id should be removed: {item['id']}")
        expected = next(font for font in fonts if font['id'] == item['id'])
        if by_id[item['id']] != expected:
            raise AssertionError(f"Mismatch for id={item['id']}")


if __name__ == '__main__':
    main()
