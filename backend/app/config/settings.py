"""
A FastAPI alkalmazásunk konfigurációs fájlja.
Itt definiáljuk a globális beállításokat, mint például a titkos kulcsot és az algoritmust, amelyet a JWT tokenek generálásához használunk.
"""

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
