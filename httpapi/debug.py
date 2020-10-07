import uvicorn
from service.config import DEBUG_API_PORT
from service.api import app


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=DEBUG_API_PORT)
