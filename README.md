# Carbon Footprint Awareness Platform

A full-stack web application that helps individuals understand, calculate, and reduce their carbon footprint through activity tracking, visual breakdowns, input validation, and personalized sustainability recommendations.

## Problem Statement

Many people want to live more sustainably but do not clearly understand how their daily choices contribute to carbon emissions.

This platform simplifies carbon-footprint awareness by allowing users to enter common activities such as transportation, food consumption, electricity usage, and shopping. It then calculates an estimated carbon footprint and provides practical actions to reduce environmental impact.

## Key Features

* Carbon-footprint calculation across four everyday categories
* Activity-wise emissions breakdown
* Interactive bar-chart visualization
* Personalized carbon-reduction recommendations
* Gemini-powered tips with a reliable rule-based fallback
* Empty-field and negative-value validation
* Accessible labels, keyboard-friendly controls, and user-readable error messages
* Responsive interface for desktop and mobile devices
* Automated backend tests
* Secure environment-variable handling

## Technology Stack

### Frontend

* React
* Vite
* Tailwind CSS
* Axios
* Chart.js
* React Chart.js 2

### Backend

* Python
* FastAPI
* Pydantic
* Google Gen AI SDK
* Uvicorn

### Testing and Development

* Pytest
* FastAPI TestClient
* Firebase Studio
* Git and GitHub

## Project Structure

```text
carbon-footprint-platform/
├── .idx/
│   └── dev.nix
├── backend/
│   ├── tests/
│   │   ├── conftest.py
│   │   └── test_main.py
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── .env.example
├── PROMPTS.md
├── LICENSE
└── README.md
```

## How It Works

1. The user enters activity data.
2. The frontend validates the entered values.
3. The FastAPI backend validates the request using Pydantic models.
4. Category-specific emission factors are used to estimate emissions.
5. The application returns:

   * Total carbon footprint
   * Category-wise breakdown
   * Personalized reduction recommendations
6. If the Gemini API is temporarily unavailable, the application automatically uses its built-in sustainability recommendation engine.

## Carbon Categories

| Category    | Example Inputs                      |
| ----------- | ----------------------------------- |
| Transport   | Distance travelled and vehicle type |
| Food        | Food type and consumption           |
| Electricity | Electricity consumption in kWh      |
| Shopping    | Amount spent and shopping category  |

> The current emission factors are simplified estimates designed for awareness and educational use. They should not be treated as an official environmental audit.

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Shriyanshi025/carbon-footprint-platform.git
cd carbon-footprint-platform
```

### 2. Configure the backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

For Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### 3. Configure environment variables

Create a file named `.env` inside the `backend` directory:

```env
GEMINI_API_KEY=your_actual_gemini_api_key
```

Never commit the real `.env` file or API key.

### 4. Start the backend

```bash
python -m uvicorn main:app --reload --port 8000
```

Backend URL:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

### 5. Start the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

## Running Tests

From the backend directory:

```bash
source venv/bin/activate
python -m pytest -v
```

Current automated test coverage includes:

* Transport calculation
* Food calculation
* Electricity calculation
* Shopping calculation
* Root API endpoint
* Valid calculation request
* Negative-value rejection
* Invalid category rejection

Current result:

```text
8 passed
```

## Validation and Reliability

The platform applies validation at multiple levels:

1. HTML input constraints
2. React frontend validation
3. Pydantic backend validation

Invalid requests receive proper validation responses instead of being processed silently.

The AI recommendation feature also uses graceful degradation. When Gemini is unavailable because of quota or network limitations, the application continues working through rule-based sustainability recommendations.

## Security Practices

* API keys are stored using environment variables
* Actual `.env` files are excluded through `.gitignore`
* `.env.example` contains placeholders only
* Backend request payloads are validated
* Dependencies and generated folders are excluded from version control
* No secret keys are stored in frontend code

## Accessibility

* Explicit labels for form controls
* Keyboard-accessible input flow
* Accessible error messages using `role="alert"`
* `aria-live` support for validation feedback
* Clear input descriptions and measurement units
* Responsive single-column layout on smaller screens

## AI-Assisted Development

AI tools were used to support project planning, debugging, code improvement, and documentation. Prompt iterations and important development decisions are recorded in `PROMPTS.md`.

All generated suggestions were reviewed, tested, corrected, and integrated manually.

## Current Limitations

* Emission factors are simplified awareness estimates
* User history is not yet persisted
* Gemini availability depends on API quota
* Currency and regional electricity factors are not yet location-specific

## Future Improvements

* Country-specific emission factors
* User accounts and activity history
* Weekly and monthly progress tracking
* Carbon-reduction goals and achievements
* Downloadable sustainability reports
* Community challenges and leaderboards
* Localization and multi-language support

## License

This project is licensed under the MIT License.

## Author

**Shriyanshi Sinha**

GitHub: [Shriyanshi025](https://github.com/Shriyanshi025)
