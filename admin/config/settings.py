from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

include(
    'components/database.py',
    'components/logging.py',
    'components/validators.py',
    'components/middlewares.py',
    'components/templates.py',
    'components/apps.py',
    'components/other.py',
)
