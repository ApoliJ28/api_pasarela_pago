from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
import os
from database.db import engine
from models import user, order

load_dotenv()

app = FastAPI(debug=True)

user.Base.metadata.create_all(bind=engine)
order.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get('/', include_in_schema=False)
async def index():
    return {
        "description": "API for payment gateway.",
        "created_by": "Victor Apolinares"
    }
    
if __name__ == "__main__":
    uvicorn.run('app:app', host=os.getenv('HOST_APP'), port=int(os.getenv('PORT_APP')), log_level='info')