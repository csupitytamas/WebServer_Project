from fastapi import FastAPI
from app.routes import user
from app.config.settings import SECRET_KEY, ALGORITHM
from app.middleware.jwt_auth_middleware import JWTAuthMiddleware


"""
A FastAPI alkalmazásunk inicializálása.
A FastAPI alkalmazásunk inicializálása során beállítjuk a middleware-t, amely lehetővé teszi a JWT tokenek kezelését.
A middleware egy olyan köztes réteg, amely lehetővé teszi a kérések és válaszok feldolgozását, mielőtt azok elérnék az alkalmazásunk logikáját 
és segítségével ellenőrizhetjük a JWT tokeneket, és biztosíthatjuk, hogy csak a megfelelő jogosultságokkal rendelkező felhasználók férjenek hozzá 
az API végpontokhoz.



"""
app = FastAPI()

# app.add_middleware(JWTAuthMiddleware) # minden /api endpointet védett

app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "API elérhető"}
