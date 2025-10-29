import json
import pathlib
from typing import Dict


class LanguageManager:
    def __init__(self, base_dir: pathlib.Path, default_lang: str = "en"):
        BASES_FOLDER = pathlib.Path(__file__).parent.parent / "locales"
        self.default_lang = default_lang
        self.locales_path = BASES_FOLDER / "base.json"
        self.translations_json: Dict[
            str, Dict[str, str]
        ] = self._load_translations()

    def _load_translations(self) -> Dict[str, Dict[str, str]]:
        with open(self.locales_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_text(self, key: str, lang: str) -> str:
        if key not in self.translations_json:
            return f"[{key}]"

        entry = self.translations_json[key]
        if lang in entry:
            return entry[lang]
        else:
            return f"[{entry['en']}]"

    def available_languages(self):
        langs = set()
        for translations in self.translations_json.values():
            langs.update(translations.keys())
        return list(langs)
