# Carbon Footprint Awareness Platform

A full-stack web application that helps individuals understand, calculate, and reduce their carbon footprint through activity tracking, visual breakdowns, input validation, and personalized sustainability recommendations.

## Problem Statement

Many people want to live more sustainably but do not clearly understand how their daily choices contribute to carbon emissions.

This platform simplifies carbon-footprint awareness by allowing users to enter common activities such as transportation, food consumption, electricity usage, and shopping. It then calculates an estimated carbon footprint and provides practical actions to reduce environmental impact.

## Chosen Challenge Vertical

**Challenge 3: Carbon Footprint Awareness Platform**

The platform is designed to help individuals understand, track, and reduce the environmental impact of their everyday activities through contextual calculations, visual insights, measurable reduction goals, and personalized recommendations.

## Target Persona

The primary user is an everyday individual who wants to live more sustainably but does not have technical knowledge of carbon accounting.

The platform helps this user:

* Identify which daily activity contributes the most emissions
* Understand their overall impact level
* Receive a realistic reduction target
* Discover practical actions that can be followed immediately
* Continue receiving useful guidance when the external AI service is unavailable

## Approach and Decision Logic

The platform combines deterministic carbon calculations with contextual decision-making and AI-generated recommendations.

1. The user enters transport, food, electricity, and shopping activity data.
2. Frontend and backend validation protect the calculation flow.
3. Category-specific emission factors calculate the footprint breakdown.
4. The insight engine identifies the dominant emissions category.
5. The platform classifies the result as low, moderate, or high impact.
6. A dynamic reduction target of 5%, 10%, or 15% is generated.
7. Gemini creates personalized recommendations using the calculated context.
8. If Gemini is unavailable, a deterministic sustainability engine provides reliable category-specific advice.
9. Successful Gemini responses are temporarily cached to reduce duplicate AI requests and improve response time.

## Assumptions

* Emission factors are simplified estimates for awareness and educational use.
* User inputs represent activity within the period selected by the user.
* Shopping emissions use a simplified spend-based estimation approach.
* Impact levels and reduction targets are guidance rather than certified environmental standards.
* Results are not intended to replace a professional environmental audit.
* Gemini availability depends on the configured API project and quota.

## Key Features

* Carbon-footprint calculation across four everyday activity categories
* Category-wise emissions breakdown with an interactive bar chart
* Smart identification of the user's dominant emissions source
* Low, moderate, and high contextual impact classification
* Dynamic 5%, 10%, or 15% carbon-reduction targets
* Estimated carbon savings and target-footprint calculation
* Gemini-powered personalized sustainability recommendations
* Built-in category-aware Eco Coach when Gemini is unavailable
* Temporary caching of repeated Gemini requests for improved efficiency
* Automatic backend warm-up to reduce production cold-start delay
* Controlled API retries for temporary network and server failures
* Multi-layer frontend and backend input validation
* Validated request and response schemas through Pydantic
* Accessible semantic forms, field groups, status updates, and error feedback
* Responsive interface for desktop and mobile devices
* 25 automated backend tests covering calculations, validation, insights, fallback logic, and caching
* Secure environment-variable and restricted CORS configuration


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
│   │   ├── test_insights.py
│   │   ├── test_main.py
│   │   └── test_tips_service.py
│   ├── calculations.py
│   ├── insights.py
│   ├── main.py
│   ├── models.py
│   ├── tips_service.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ActivityForm.jsx
│   │   │   └── ResultsPanel.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── .env.example
├── .gitignore
├── PROMPTS.md
├── LICENSE
└── README.md
```

## How It Works

1. The user enters activity information for transport, food, electricity, and shopping.
2. The semantic React form validates empty and negative values.
3. The FastAPI backend validates all values and categories through Pydantic schemas.
4. The calculation engine applies category-specific emission factors.
5. The backend returns:
   * Total carbon footprint
   * Category-wise emissions breakdown
   * Dominant emissions category
   * Contextual impact level
   * Personalized reduction percentage
   * Potential carbon saving
   * Target carbon footprint
6. The frontend displays the score, insight cards, reduction target, and chart.
7. The recommendation service requests three contextual actions from Gemini.
8. Successful Gemini results are cached temporarily for equivalent requests.
9. When Gemini is unavailable, the category-aware built-in Eco Coach returns deterministic recommendations.

## Carbon Categories

| Category    | Example Inputs                      |
| ----------- | ----------------------------------- |
| Transport   | Distance travelled and vehicle type |
| Food        | Food type and consumption           |
| Electricity | Electricity consumption in kWh      |
| Shopping    | Amount spent and shopping category  |

> The current emission factors are simplified estimates designed for awareness and educational use. They should not be treated as an official environmental audit.

## Live Demo

- Frontend: https://carbon-footprint-platform-azure.vercel.app
- Backend API: https://carbon-footprint-platform-s6r4.onrender.com
- API Documentation: https://carbon-footprint-platform-s6r4.onrender.com/docs

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
GEMINI_MODEL=gemini-2.0-flash
FRONTEND_URL=http://localhost:5173
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

Current automated test coverage includes:

* Individual transport, food, electricity, and shopping calculations
* Root and calculation API endpoints
* Valid and invalid request payloads
* Negative-value and unsupported-category rejection
* Impact-level boundary conditions
* Dominant-category identification
* Zero-footprint handling
* Rounded contribution percentages
* Context-aware fallback recommendations
* Missing Gemini-key resilience
* Recommendation API fallback behavior
* Stable cache-key generation
* Cache expiry and safe response copying
* Prevention of repeated Gemini calls for equivalent requests
* Validated API response structures

Current result:

```text
25 passed
```

```md
## Validation, Reliability, and Efficiency

The platform applies safeguards at multiple levels:

1. HTML input constraints
2. Controlled React form state
3. Frontend empty and negative-value validation
4. Pydantic request validation
5. Validated FastAPI response models

Production reliability measures include:

* Background backend warm-up on application load
* One controlled retry for temporary network, timeout, or server failures
* Non-blocking recommendation loading after the footprint result is available
* Deterministic recommendations when Gemini is unavailable
* A bounded in-memory cache with a 10-minute expiry
* A maximum of 50 cached recommendation entries
* Caching only successful Gemini results so temporary failures do not become stale responses

## Security Practices

* API keys are stored only through environment variables
* Real `.env` files are excluded through `.gitignore`
* `.env.example` contains configuration placeholders only
* No API key or secret is exposed in frontend code
* Backend request payloads are restricted through typed Pydantic schemas
* Backend responses are validated through explicit response models
* CORS access is restricted to configured development and production origins
* Only required HTTP methods and headers are allowed
* Dependency folders and generated files are excluded from version control
* Invalid values and unsupported categories are rejected before processing

## Accessibility

* Explicit labels connected to every form control
* Semantic `<form>`, `<fieldset>`, and `<legend>` elements
* Keyboard submission through the Enter key
* Visible focus styling for interactive controls
* Disabled-state feedback during calculations
* Accessible validation feedback using `role="alert"`
* Assertive announcements for form errors
* `aria-live` updates for recommendation results
* `aria-busy` feedback while the Eco Action Plan is loading
* Clear measurement units, descriptions, and status labels
* Responsive single-column layout on smaller screens

## AI-Assisted Development

AI tools were used to support project planning, debugging, code improvement, and documentation. Prompt iterations and important development decisions are recorded in `PROMPTS.md`.

All generated suggestions were reviewed, tested, corrected, and integrated manually.

## Current Limitations

* Emission factors are simplified awareness estimates
* User history is not persisted between sessions
* Impact thresholds are general guidance rather than region-specific standards
* Gemini availability depends on API quota and service availability
* Electricity factors and shopping estimates are not location-specific
* The in-memory recommendation cache resets when the backend restarts

## Future Improvements

* Country and region-specific emission factors
* User accounts and secure activity history
* Weekly and monthly footprint comparisons
* Achievement tracking for completed reduction goals
* Downloadable sustainability reports
* Localization and multi-language support
* Optional persistent caching for larger production deployments
* Community sustainability challenges

## License

This project is licensed under the MIT License.

## Author

**Shriyanshi Sinha**

GitHub: [Shriyanshi025](https://github.com/Shriyanshi025)
