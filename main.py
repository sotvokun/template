import dotenv
from fastapi import FastAPI

from app.autoload import Autoloader


dotenv.load_dotenv()

app = FastAPI()
autoloader = Autoloader(app, main_subapp="site")
