from fastapi import FastAPI
from routes.users import user
from routes.movies import movie
from fastapi.openapi.utils import get_openapi
import uvicorn
from pyngrok import ngrok
from config.security import PORT
app = FastAPI()
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="VeeMind",
        version="1.0.0",
        description="NetIX Community",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter the JWT token in the format: Bearer <token>"
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema
app.openapi = custom_openapi
app.include_router(user)
app.include_router(movie)
if __name__ == "__main__":
    public_url = ngrok.connect(int(PORT))
    print(f"🔗 Public URL: {public_url}")
    uvicorn.run("app:app", host="0.0.0.0", port=int(PORT), reload=True)