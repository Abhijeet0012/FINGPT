# FinanceGPT

FinanceGPT is an AI-powered financial assistant platform designed to help users discover, analyze, and compare financial products such as fixed deposits, mutual funds, insurance, and credit cards. The platform leverages a modern headless architecture and an agentic approach to deliver intelligent, flexible, and scalable financial insights.

## Key Features
- **Conversational AI Assistant:** Natural language chat interface for personalized financial queries and recommendations.
- **Agentic Architecture:** Modular agents (SQL Agent, PDF Agent, Offers Agent) handle specialized tasks such as database querying, document analysis, and promotional offer retrieval.
- **Headless Design:** Decoupled frontend and backend enable seamless integration, scalability, and flexibility for various deployment scenarios.
- **User Authentication:** Secure JWT-based signup, login, and session management.
- **Real-Time Recommendations:** WebSocket-powered streaming for instant, context-aware financial advice.
- **Product Brochure Analysis:** Extracts and synthesizes information from PDF brochures using advanced document processing.
- **Mock Offers API:** Provides promotional offers for demonstration and testing.
- **Comprehensive Logging:** Tracks user queries, responses, and analytics for continuous improvement.

## About the Architecture

### Headless Architecture
FinanceGPT is built with a headless architecture, separating the user interface (frontend) from the business logic and data processing (backend). This allows:
- Independent development and deployment of frontend and backend
- Easy integration with other platforms or channels (web, mobile, chatbots)
- Enhanced scalability and maintainability

### Agentic Approach
The backend employs an agentic approach, where specialized agents are responsible for distinct tasks:
- **SQL Agent:** Converts natural language queries into SQL to fetch data from the financial products database.
- **PDF Agent:** Processes and retrieves information from product brochures in PDF format.
- **Offers Agent:** Supplies promotional offers via a mock API for demonstration purposes.

Agents can be extended or replaced, making the system adaptable to new data sources or business requirements.

## Technology Stack
- **Frontend:** React, TypeScript, Vite, shadcn-ui, Tailwind CSS
- **Backend:** FastAPI, SQLAlchemy, OpenAI API, PostgreSQL, LangChain, ChromaDB
- **Authentication:** JWT (JSON Web Tokens)
- **Document Processing:** LangChain, PyPDF

## Getting Started
- See `financegpt-frontend/README.md` for frontend setup and usage.
- See `financegpt-backend/README.md` for backend setup, environment variables, and API details.

## License
This project is for demonstration and educational purposes. 