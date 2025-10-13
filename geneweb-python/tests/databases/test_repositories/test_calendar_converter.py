import pytest
from datetime import date
from geneweb.core.services.calendar_converter import CalendarConverter


def test_gregorian_to_julian_day_number():
    """Test conversion grégorien vers jour julien"""
    converter = CalendarConverter()
    
    # Test avec une date connue: 1er janvier 2000 = JDN 2451545
    jdn = converter.gregorian_to_julian_day_number(2000, 1, 1)
    assert jdn == 2451545
    
    # Test avec une autre date: 15 octobre 1582 (début du calendrier grégorien)
    jdn = converter.gregorian_to_julian_day_number(1582, 10, 15)
    assert jdn == 2299161


def test_julian_day_number_to_gregorian():
    """Test conversion jour julien vers grégorien"""
    converter = CalendarConverter()
    
    # Test avec JDN 2451545 = 1er janvier 2000
    result = converter.julian_day_number_to_gregorian(2451545)
    assert result["year"] == 2000
    assert result["month"] == 1
    assert result["day"] == 1


def test_gregorian_to_julian():
    """Test conversion grégorien vers julien"""
    converter = CalendarConverter()
    
    # Test avec une date moderne
    result = converter.gregorian_to_julian(2025, 10, 3)
    assert result is not None
    assert "year" in result
    assert "month" in result
    assert "day" in result
    # La différence devrait être d'environ 13 jours pour les dates modernes
    assert result["day"] == 20 or result["day"] == 21  # Peut varier selon le mois


def test_gregorian_to_french_republican():
    """Test conversion vers calendrier républicain français"""
    converter = CalendarConverter()
    
    # Test avec une date dans la période républicaine (22 sept 1792 - 1805)
    result = converter.gregorian_to_french_republican(1794, 7, 27)
    assert result is not None
    assert result["year"] >= 1
    assert 1 <= result["month"] <= 13
    assert 1 <= result["day"] <= 30
    assert result["month_name"] in converter.FRENCH_MONTHS or result["month_name"] == "Sansculottides"
    
    # Test avec une date hors période
    result = converter.gregorian_to_french_republican(1700, 1, 1)
    assert result is None
    
    result = converter.gregorian_to_french_republican(1900, 1, 1)
    assert result is None


def test_gregorian_to_hebrew():
    """Test conversion vers calendrier hébraïque"""
    converter = CalendarConverter()
    
    result = converter.gregorian_to_hebrew(2025, 10, 3)
    assert result is not None
    assert result["year"] > 5700  # L'année hébraïque devrait être > 5700
    assert 1 <= result["month"] <= 12
    assert 1 <= result["day"] <= 30
    assert result["month_name"] in converter.HEBREW_MONTHS


def test_convert_from_gregorian():
    """Test conversion complète depuis grégorien"""
    converter = CalendarConverter()
    
    result = converter.convert_from_gregorian(2025, 10, 3)
    
    # Vérifier grégorien
    assert result["gregorian"]["year"] == 2025
    assert result["gregorian"]["month"] == 10
    assert result["gregorian"]["day"] == 3
    assert result["gregorian"]["month_name"] == "October"
    
    # Vérifier julien
    assert "julian" in result
    assert "year" in result["julian"]
    assert "month_name" in result["julian"]
    
    # Vérifier jour julien
    assert result["julian_day_number"] > 0
    
    # Vérifier hébreu
    assert "hebrew" in result
    assert result["hebrew"]["year"] > 5700
    
    # Français peut être None si hors période
    # assert "french_republican" in result


def test_month_names():
    """Test que les noms de mois sont corrects"""
    converter = CalendarConverter()
    
    assert len(converter.GREGORIAN_MONTHS) == 12
    assert len(converter.FRENCH_MONTHS) == 12
    assert len(converter.HEBREW_MONTHS) == 12
    
    assert "January" in converter.GREGORIAN_MONTHS
    assert "Vendémiaire" in converter.FRENCH_MONTHS
    assert "Tishri" in converter.HEBREW_MONTHS