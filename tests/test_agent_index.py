from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from check_agent_index import validate  # noqa: E402


class AgentIndexTests(unittest.TestCase):
    def test_machine_readable_index_is_current(self) -> None:
        self.assertEqual(validate(), [])


if __name__ == '__main__':
    unittest.main()
