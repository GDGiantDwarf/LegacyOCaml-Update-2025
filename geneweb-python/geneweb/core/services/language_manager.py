import json
import pathlib
from typing import Dict, List


class LanguageManager:
    def __init__(
        self,
        base_dir: pathlib.Path,
        default_lang: str = "en",
    ) -> None:
        locales_folder = (
            pathlib.Path(__file__).parent.parent / "locales"
        )
        self.default_lang = default_lang
        self.locales_path = locales_folder / "base.json"
        self.translations_json: Dict[
            str, Dict[str, str]
        ] = self._load_translations()

    def _load_translations(
        self,
    ) -> Dict[str, Dict[str, str]]:
        with open(
            self.locales_path, "r", encoding="utf-8"
        ) as f:
            return json.load(f)

    def get_text(self, key: str, lang: str) -> str:
        if key not in self.translations_json:
            return key

        entry = self.translations_json[key]
        if lang in entry:
            return entry[lang]
        if "en" in entry:
            return entry["en"]
        if entry:
            return next(iter(entry.values()))
        return key

    def get_translations_for_lang(
        self, lang: str
    ) -> Dict[str, str]:
        """Return all keys translated for a given language.

        Fallback chain: requested lang -> English ->
        any available translation -> key name.
        """
        result: Dict[str, str] = {}
        for key, entry in self.translations_json.items():
            if lang in entry:
                result[key] = entry[lang]
            elif "en" in entry:
                result[key] = entry["en"]
            elif entry:
                first_value: str = next(iter(entry.values()))
                result[key] = first_value
            else:
                result[key] = key
        return result

    def available_languages(self) -> List[str]:
        langs: set[str] = set()
        for translations in self.translations_json.values():
            langs.update(translations.keys())
        return list(langs)
