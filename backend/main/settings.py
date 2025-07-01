import os

from dotenv import load_dotenv
from backend.main.config import Environments, get_configurations

BASE_DIR = os.path.dirname((os.path.dirname(__file__)))
APPS_DIR = os.path.join(BASE_DIR, 'apps')
MAIN_DIR = os.path.join(BASE_DIR, 'main')

################################################################################################
# READ VARIABLES FROM ENV
################################################################################################
dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)

current_env = os.getenv("ENVIRONMENT", "local").strip()
print("ENVIRONMENT: ", current_env)

valid_envs = [
    Environments.PROD.value,
    Environments.DEV.value,
    Environments.LOCAL.value
]

if current_env not in valid_envs:
    print(current_env)
    print("Invalid ENVIRONMENT in config %s" % current_env)
    print("VALID_ENVIRONMENTS ", valid_envs)
    exit(-1)
################################################################################################

################################################################################################
# LOAD CONFIGURATIONS
################################################################################################
configurations = get_configurations(current_env)
################################################################################################

################################################################################################
# LLM DETAILS
################################################################################################
OPEN_API_KEY = os.getenv("OPEN_API_KEY", None).strip()
if not OPEN_API_KEY:
    print('Please add API key for GPT in .env. Refer README.md for more info')
    exit()

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
