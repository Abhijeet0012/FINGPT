# FinanceGPT Frontend

FinanceGPT is an AI-powered financial assistant platform that helps users discover, analyze, and compare financial products such as fixed deposits, mutual funds, insurance, and credit cards. The frontend is built with React, TypeScript, Vite, shadcn-ui, and Tailwind CSS, providing a modern and responsive user interface.

## Features
- Chat interface for interacting with the AI assistant
- User authentication (signup, login, logout)
- Real-time recommendations and product analysis
- Responsive design with shadcn-ui and Tailwind CSS

## Getting Started

### Prerequisites
- Node.js (v18 or later recommended)
- npm (v9 or later)

### Installation

```sh
# Clone the repository
 git clone https://github.com/Abhijeet0012/FINGPT.git
 cd financegpt-frontend

# Install dependencies
 npm install

# Start the development server
 npm run dev
```

The app will be available at [http://localhost:8080](http://localhost:8080) by default.

### Environment Variables
- The frontend expects the backend API to be available at `http://localhost:8000` by default. You can override this by setting the `VITE_API_URL` environment variable.

### Build for Production
```sh
npm run build
```
The production build will be in the `dist/` folder.

### Linting
```sh
npm run lint
```

## Technologies Used
- React
- TypeScript
- Vite
- shadcn-ui
- Tailwind CSS

## Project Structure
- `src/` - Main source code (components, pages, hooks, config)
- `public/` - Static assets

## License
This project is for demonstration and educational purposes.
