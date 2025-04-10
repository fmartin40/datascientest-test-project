from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def safe_parse_iso_date(date_str: str):
    """
    Parse une date ISO 8601 de façon robuste.
    Gère les formats avec ou sans 'Z' (UTC).
    Retourne un datetime ou None si parsing impossible.
    """
    if not date_str:
        return None

    try:
        # Exemple : '2025-03-25T21:41:06.000Z' → '2025-03-25T21:41:06.000+00:00'
        if date_str.endswith("Z"):
            date_str = date_str.replace("Z", "+00:00")

        return datetime.fromisoformat(date_str)

    except Exception as e:
        logger.warning(f"Impossible de parser la date ISO : {date_str} → {e}")
        return None
