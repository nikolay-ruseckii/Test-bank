import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
SRC_MAIN = PROJECT_ROOT / "src" / "main"

sys.path.insert(0, str(SRC_MAIN))

from src.main.api.fixtures.api_fixture import *
from src.main.api.fixtures.object_fixture import *
from src.main.api.fixtures.db_fixture import *
from src.main.api.fixtures.deposit_fixture import *
from src.main.api.fixtures.account_fixture import *
from src.main.api.fixtures.credit_fixture import *
from src.main.api.fixtures.user_fixture import *
from src.main.api.fixtures.transfer_fixture import *