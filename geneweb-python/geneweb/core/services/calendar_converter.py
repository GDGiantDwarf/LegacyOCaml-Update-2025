from datetime import date, timedelta
from typing import Dict, Optional


class CalendarConverter:
    """Service pour convertir entre différents systèmes de calendrier"""
    
    GREGORIAN_MONTHS = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    
    JULIAN_MONTHS = GREGORIAN_MONTHS  # Même noms
    
    FRENCH_MONTHS = [
        "Vendémiaire", "Brumaire", "Frimaire", "Nivôse", "Pluviôse", "Ventôse",
        "Germinal", "Floréal", "Prairial", "Messidor", "Thermidor", "Fructidor"
    ]
    
    HEBREW_MONTHS = [
        "Tishri", "Heshvan", "Kislev", "Tevet", "Shevat", "Adar",
        "Nisan", "Iyar", "Sivan", "Tammuz", "Av", "Elul"
    ]

    @staticmethod
    def gregorian_to_julian_day_number(year: int, month: int, day: int) -> int:
        """Convertit une date grégorienne en numéro de jour julien"""
        a = (14 - month) // 12
        y = year + 4800 - a
        m = month + 12 * a - 3
        
        jdn = day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
        return jdn

    @staticmethod
    def julian_day_number_to_gregorian(jdn: int) -> Dict[str, int]:
        """Convertit un numéro de jour julien en date grégorienne"""
        a = jdn + 32044
        b = (4 * a + 3) // 146097
        c = a - (146097 * b) // 4
        d = (4 * c + 3) // 1461
        e = c - (1461 * d) // 4
        m = (5 * e + 2) // 153
        
        day = e - (153 * m + 2) // 5 + 1
        month = m + 3 - 12 * (m // 10)
        year = 100 * b + d - 4800 + m // 10
        
        return {"year": year, "month": month, "day": day}

    @staticmethod
    def gregorian_to_julian(year: int, month: int, day: int) -> Dict[str, int]:
        """Convertit une date grégorienne en date julienne"""
        jdn = CalendarConverter.gregorian_to_julian_day_number(year, month, day)
        
        # Calcul approximatif (différence de 13 jours pour dates modernes)
        b = jdn + 1524
        c = (b - 122.1) // 365.25
        d = int(365.25 * c)
        e = int((b - d) / 30.6001)
        
        julian_day = int(b - d - int(30.6001 * e))
        julian_month = int(e - 1 if e < 14 else e - 13)
        julian_year = int(c - 4716 if julian_month > 2 else c - 4715)
        
        return {"year": julian_year, "month": julian_month, "day": julian_day}

    @staticmethod
    def gregorian_to_french_republican(year: int, month: int, day: int) -> Optional[Dict]:
        """Convertit une date grégorienne en calendrier républicain français"""
        # Le calendrier républicain a été en vigueur du 22 septembre 1792 au 31 décembre 1805
        epoch = date(1792, 9, 22)
        end_date = date(1805, 12, 31)  # Dernier jour du calendrier républicain
        target = date(year, month, day)
        
        # Vérifier si la date est dans la période du calendrier républicain (1792-1805)
        if target < epoch or target > end_date:
            return None
        
        delta = (target - epoch).days
        french_year = (delta // 365) + 1
        day_in_year = delta % 365
        french_month = (day_in_year // 30) + 1
        french_day = (day_in_year % 30) + 1
        
        if french_month > 12:
            french_month = 12
            french_day = 30
        
        return {
            "year": french_year,
            "month": french_month,
            "month_name": CalendarConverter.FRENCH_MONTHS[french_month - 1] if french_month <= 12 else "Sansculottides",
            "day": french_day
        }

    @staticmethod
    def gregorian_to_hebrew(year: int, month: int, day: int) -> Dict:
        """Convertit une date grégorienne en calendrier hébraïque (approximatif)"""
        # Formule simplifiée - pour une conversion exacte, utiliser une bibliothèque spécialisée
        jdn = CalendarConverter.gregorian_to_julian_day_number(year, month, day)
        
        # L'époque hébraïque commence le 7 octobre -3761 (calendrier julien proleptique)
        hebrew_epoch = 347995.5
        
        # Calcul approximatif
        days_since_epoch = jdn - hebrew_epoch
        hebrew_year = int(days_since_epoch / 365.25) + 1
        day_in_year = int(days_since_epoch % 365.25)
        hebrew_month = (day_in_year // 30) + 1
        hebrew_day = (day_in_year % 30) + 1
        
        if hebrew_month > 12:
            hebrew_month = 12
        
        return {
            "year": hebrew_year,
            "month": hebrew_month,
            "month_name": CalendarConverter.HEBREW_MONTHS[hebrew_month - 1],
            "day": hebrew_day
        }

    @staticmethod
    def convert_from_gregorian(year: int, month: int, day: int) -> Dict:
        """Convertit une date grégorienne vers tous les calendriers"""
        jdn = CalendarConverter.gregorian_to_julian_day_number(year, month, day)
        julian = CalendarConverter.gregorian_to_julian(year, month, day)
        french = CalendarConverter.gregorian_to_french_republican(year, month, day)
        hebrew = CalendarConverter.gregorian_to_hebrew(year, month, day)
        
        return {
            "gregorian": {
                "year": year,
                "month": month,
                "month_name": CalendarConverter.GREGORIAN_MONTHS[month - 1],
                "day": day
            },
            "julian": {
                **julian,
                "month_name": CalendarConverter.JULIAN_MONTHS[julian["month"] - 1]
            },
            "julian_day_number": jdn,
            "french_republican": french,
            "hebrew": hebrew
        }