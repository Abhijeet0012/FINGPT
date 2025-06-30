# FinanceGPT Backend

> **Note:** All required environment variables have been added for seamless integration.

FinanceGPT is an AI-powered financial assistant platform that enables users to discover, analyze, and compare financial products such as fixed deposits, mutual funds, insurance, and credit cards. The backend is built with FastAPI and integrates with OpenAI, a PostgreSQL database, and document (PDF) analysis for comprehensive financial insights.

## Features
- RESTful API and WebSocket endpoints for chat and recommendations
- User authentication (JWT-based signup, login, logout)
- AI-powered SQL agent for natural language queries on financial products
- PDF agent for extracting information from product brochures
- Promotional offers API
- Logging and analytics of user queries

## Getting Started

### Prerequisites
- Python 3.10
- PostgreSQL database

### Installation

1. **Clone the repository**
```sh
git clone <YOUR_GIT_URL>
cd financegpt-backend
```

2. **Install dependencies**
```sh
pip install -r requirements.txt
```

3. **Set up environment variables**
Create a `.env` file in the backend directory with the following variables:
```
DATABASE_URL=postgresql+psycopg2://<user>:<password>@<host>:<port>/<db>
OPENAI_API_KEY=your-openai-api-key
SECRET_KEY=your-secret-key
# Optional: You can add more variables as needed for your deployment
```

- `DATABASE_URL`: PostgreSQL connection string (required)
- `OPENAI_API_KEY`: Your OpenAI API key for LLM features (required)
- `SECRET_KEY`: Secret key for JWT authentication (required)

4. **Run database migrations**
Ensure your PostgreSQL database is running and the schema is set up (see `data/db_setup.sql` if needed).

5. **Start the server**
```sh
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at [http://localhost:8000](http://localhost:8000).

## API Overview

### Authentication
- `POST /auth/signup` — Register a new user
- `POST /auth/login` — Login and receive JWT token
- `POST /auth/logout` — Logout (client-side token deletion)

### Query
- `POST /query` — Submit a financial query (natural language)
- `GET /offers` — Get current promotional offers
- `WebSocket /ws/stream` — Real-time chat and recommendations

### Agents
- **SQL Agent**: Converts natural language to SQL and queries the `financial_products` table
- **PDF Agent**: Extracts information from PDF brochures in the `brochures/` directory

## Project Structure
- `main.py` — FastAPI app entry point
- `routes/` — API route definitions
- `agents/` — AI agent logic (SQL, PDF)
- `models/` — SQLAlchemy models
- `prompts/` — LLM prompt templates
- `data/` — Database setup scripts

## License
This project is for demonstration and educational purposes.
