#  TASK MANAGER API

 A mini client side TASK managing system build with FastAPI.This application handle user registration,authentication,task add,view task.
 
## Prerequisites
 - Python 3.8+
 - Virtual environment(recommended)

## Installation
```
# Clone and navigate to project
git clone <repository-url>
cd task_manager_api

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt 
```
## Environment Setup
Create .env file on your root directory
```commandline
# Database Configuration
DATABASE_URL=sqlite:///./trading_crm.db

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

```
## Run the application
Start the client application
```commandline
cd ./app
uvicorn app.main:app --reload --port 8000
```
The Application will available at:
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
---