from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from fastapi.openapi.utils import get_openapi
from app.middleware.jwt_auth_middleware import JWTAuthMiddleware
from app.utils.jwt_helper import decode_jwt
from app.routes import auth, user_routes
from app.db.connection import get_connection
from fastapi.middleware.cors import CORSMiddleware

security = HTTPBearer()

app = FastAPI()
app.add_middleware(JWTAuthMiddleware)

# API útvonalak regisztrálása
app.include_router(auth.router)
app.include_router(user_routes.router)

@app.get("/")
def root():
    return {"message": "API elérhető"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # vagy ["*"] a bármely domain engedélyezéséhez
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/test_oracle")
def test_oracle():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 'Kapcsolat sikeres!' FROM dual")
            eredmeny = cur.fetchone()[0]
    return {"uzenet": eredmeny}

@app.get("/api/protected", dependencies=[Depends(security)])
def protected_route(payload: dict = Depends(decode_jwt)):
    return {"message": "Ez egy védett végpont", "user": payload["sub"]}


# Swagger security konfiguráció
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="WebServer Projekt API",
        version="1.0.0",
        description="JWT alapú hitelesítéssel védett API",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


