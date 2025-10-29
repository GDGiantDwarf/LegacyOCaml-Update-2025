from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from jinja2 import pass_context
from .language_manager import LanguageManager


class ExtendedJinja2Templates(Jinja2Templates):
    def __init__(self, directory: str, lang_manager: LanguageManager):
        super().__init__(directory=directory)
        self.lang_manager = lang_manager

    def get_context(self, request: Request):
        lang = getattr(request.state, "lang", self.lang_manager.default_lang)

        # t(key) renvoie directement la traduction selon la langue active
        def t(key):
            return self.lang_manager.get_text(key, lang)

        return {"request": request, "t": t, "lang": lang}
