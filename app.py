from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
import os

from routes import auth

load_dotenv()

app = FastAPI(title="API Payment Gateway",debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(auth.router)

@app.get('/', include_in_schema=False)
async def index():
    return {
        "description": "API for payment gateway.",
        "created_by": "Victor Apolinares"
    }
    
if __name__ == "__main__":
    uvicorn.run('app:app', host=os.getenv('HOST_APP'), port=int(os.getenv('PORT_APP')), log_level='info')