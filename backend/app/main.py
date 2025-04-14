from fastapi import FastAPI
from app.middleware.jwt_auth_middleware import JWTAuthMiddleware

app = FastAPI()

app.add_middleware(JWTAuthMiddleware) # minden /api endpointet védett

@app.get("/xyz")
async def public_route():
    return {"message": "This is a public route"}

@app.get("/api/xyz")
async def protected_route():
    return {"message": "This is a protected route"}
