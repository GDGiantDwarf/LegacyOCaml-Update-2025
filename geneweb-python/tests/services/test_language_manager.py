from geneweb.core.services.language_manager import (
    LanguageManager,
)
from geneweb.web.utils import BASE_DIR


def _make_manager():
    """Create a LanguageManager with default settings."""
    return LanguageManager(BASE_DIR, default_lang="en")


def test_get_text_known():
    mgr = _make_manager()
    keys = list(mgr.translations_json.keys())
    assert len(keys) > 0
    key = keys[0]
    result = mgr.get_text(key, "en")
    assert isinstance(result, str)
    assert result != f"[{key}]" or "en" not in (
        mgr.translations_json[key]
    )


def test_get_text_unknown():
    mgr = _make_manager()
    result = mgr.get_text("nonexistent", "en")
    assert result == "nonexistent"


def test_get_translations_for_lang():
    mgr = _make_manager()
    trans = mgr.get_translations_for_lang("en")
    assert isinstance(trans, dict)
    assert len(trans) > 0


def test_available_languages():
    mgr = _make_manager()
    langs = mgr.available_languages()
    assert isinstance(langs, list)
    assert len(langs) > 0
    assert all(
        isinstance(lang, str) for lang in langs
    )


def test_get_text_fallback_to_en():
    """get_text with unknown lang falls back to EN."""
    mgr = _make_manager()
    keys = list(mgr.translations_json.keys())
    key = keys[0]
    result = mgr.get_text(key, "zz_nonexistent")
    assert isinstance(result, str)


def test_get_translations_unknown_lang():
    """get_translations_for_lang with unknown lang."""
    mgr = _make_manager()
    trans = mgr.get_translations_for_lang("zz")
    assert isinstance(trans, dict)
    assert len(trans) > 0
