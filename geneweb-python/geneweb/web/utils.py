import pathlib
from starlette.templating import Jinja2Templates
from geneweb.core.services.language_manager import LanguageManager
from geneweb.core.services.template_config import ExtendedJinja2Templates

BASE_DIR = pathlib.Path(__file__).resolve().parent

lang_manager = LanguageManager(BASE_DIR)
templates = ExtendedJinja2Templates(directory=str(BASE_DIR / "templates"), lang_manager=lang_manager)