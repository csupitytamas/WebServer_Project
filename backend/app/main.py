from fastapi import FastAPI
from app.middleware.jwt_auth_middleware import JWTAuthMiddleware
from app.routes import user
from app.config.settings import SECRET_KEY, ALGORITHM


app = FastAPI()

app.add_middleware(JWTAuthMiddleware) # minden /api endpointet védett

app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "API elérhető"}