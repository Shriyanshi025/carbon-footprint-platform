# AI-Assisted Development and Prompt Evolution

This document records how AI tools were used during the development of the **Carbon Footprint Awareness Platform**, how their suggestions evolved, and how every important output was manually reviewed, tested, and corrected.

AI tools supported the development process, but they were not treated as an unquestioned source of truth. Generated code was validated through browser testing, API testing, automated tests, production builds, deployment checks, and manual code review.

---

## 1. Project Objective

The development goal was to build a practical full-stack platform that helps users:

* Estimate their carbon footprint
* Understand the contribution of different activity categories
* Visualize their emissions
* Receive personalized reduction recommendations
* Continue using the application even when the external AI service is unavailable

The project was also designed around the following quality parameters:

* Practical usability
* Clean and maintainable code
* Security
* Efficiency
* Testing
* Accessibility
* Reliable deployment
* Clear AI usage documentation

---

## 2. AI Tools Used

| Tool                      | Primary Use                                                                                               |
| ------------------------- | --------------------------------------------------------------------------------------------------------- |
| Gemini in Firebase Studio | Initial project scaffolding and environment setup                                                         |
| Claude                    | Early planning, architecture suggestions, and setup guidance                                              |
| ChatGPT                   | Debugging, validation, testing, accessibility, security hardening, documentation, and deployment guidance |
| Gemini API                | Runtime generation of personalized carbon-reduction tips                                                  |

---

## 3. Initial Project-Scaffolding Prompt

The initial prompt requested a complete full-stack project structure.

```text
I am building a Carbon Footprint Awareness Platform web app.

Create a full-stack project using:

Backend:
- Python FastAPI
- Carbon footprint calculator
- Gemini API integration
- CORS configuration
- requirements.txt

Frontend:
- React with Vite
- Tailwind CSS
- Activity logger
- Carbon score
- Breakdown chart
- Personalized tips
- Mobile-responsive layout

Also create:
- .env.example
- PROMPTS.md
- Clean folder structure
- Proper error handling
```

### Initial Outcome

The generated project included:

* React frontend
* FastAPI backend
* Emission-factor calculations
* Chart.js visualization
* Gemini integration
* Basic documentation files

### Problems Discovered

The initial generated output was not production-ready. Manual review identified:

* Incorrect form-state handling
* Input values being sent as zero
* Development proxy and cloud-preview networking issues
* Missing backend input validation
* Unrestricted CORS configuration
* Gemini quota failures causing HTTP 500 errors
* No user-friendly frontend error handling
* No automated tests
* Incomplete accessibility support
* Environment configuration ordering errors

These issues were fixed through smaller, focused prompts and manual verification.

---

## 4. Environment Configuration Evolution

### Initial Environment Prompt

```text
Configure Firebase Studio dev.nix with:

- Python 3.11
- Node.js 20
- Python and formatting extensions
- Web preview configuration
- Automatic backend and frontend dependency installation
```

### Issue

The first generated configuration failed to build because some Nix packages and workspace hooks were incompatible with the environment.

### Refined Approach

The environment configuration was reduced to a minimal working version first:

```nix
{ pkgs, ... }: {
  channel = "stable-24.05";

  packages = [
    pkgs.python311
    pkgs.nodejs_20
  ];
}
```

After successful environment creation, dependency-installation hooks were added carefully.

### Learning

A minimal configuration was more reliable than introducing multiple packages and hooks before confirming the base environment.

---

## 5. Frontend Form-State Debugging

### Problem

The user interface accepted values, but the calculated score remained `0.00`.

### Diagnostic Prompt

```text
Inspect the React form state and determine why visible input values are not being sent correctly to the FastAPI backend.
```

### Root Cause

The generated inputs used a custom attribute:

```jsx
parent="transport"
```

The event handler attempted to access it as:

```jsx
e.target.parent
```

This produced an `undefined` section in the React state.

### Correction

The custom field was replaced with a valid data attribute:

```jsx
data-section="transport"
```

The handler was updated to use:

```jsx
const section = e.target.dataset.section;
```

Numeric inputs were also converted safely while preserving empty values:

```jsx
[name]:
  type === 'number'
    ? value === ''
      ? ''
      : Number(value)
    : value
```

### Verification

The following input produced the expected result:

```text
Transport: 10 km by car
Food: 1 kg vegan
Electricity: 5 kWh
Shopping: 10 in other category
```

Expected and verified result:

```text
7.58 kg CO2e
```

---

## 6. Runtime Gemini Prompt

The `/tips` endpoint sends footprint information to Gemini using a focused prompt.

```text
Based on this carbon footprint information:

{footprint_data}

Give exactly 3 practical and personalized carbon-reduction tips.

Requirements:
- Keep each tip short
- Make each recommendation specific
- Focus on actions the user can realistically follow
```

### Example Input

```json
{
  "total_footprint": 7.575,
  "breakdown": {
    "transport": 1.7,
    "food": 0.5,
    "electricity": 2.375,
    "shopping": 3.0
  }
}
```

### Expected Output Characteristics

* Exactly three tips
* Clear and actionable language
* Recommendations linked to the user's largest emission categories
* No unnecessary long explanation

---

## 7. Gemini Quota Failure and Graceful Fallback

### Problem

The Gemini API returned:

```text
429 RESOURCE_EXHAUSTED
```

The initial implementation allowed this external API failure to become a backend HTTP 500 error.

### Reliability Prompt

```text
Update the personalized-tips endpoint so that an unavailable Gemini API does not break the application.

Requirements:
- Catch external API errors
- Identify the user's highest-emission category
- Return three meaningful rule-based recommendations
- Return the source as either "gemini" or "fallback"
- Keep the calculation feature fully operational
```

### Final Behaviour

When Gemini is available:

```json
{
  "tips": "AI-generated recommendations",
  "source": "gemini"
}
```

When Gemini is unavailable:

```json
{
  "tips": "Rule-based sustainability recommendations",
  "source": "fallback"
}
```

The frontend displays either:

* `Gemini AI`
* `Smart Fallback`

This prevents an external service outage or quota limitation from breaking the primary user experience.

---

## 8. Backend Validation Prompt

```text
Replace unstructured dictionary request bodies with typed Pydantic models.

Validate:
- Non-negative numeric values
- Reasonable maximum limits
- Allowed transport types
- Allowed food types
- Allowed shopping categories

Invalid data must return a proper validation response.
```

### Improvements Added

* `BaseModel` request schemas
* `Field` constraints
* `Literal` category restrictions
* Automatic `422 Unprocessable Entity` responses
* Rounded and structured API output

### Validation Layers

The final platform validates input at three levels:

1. HTML input constraints
2. React frontend checks
3. Pydantic backend validation

---

## 9. Frontend Error-Handling Prompt

```text
Improve the calculation workflow so users receive clear feedback for:

- Empty fields
- Negative values
- Backend validation errors
- Network failures
- Slow or unavailable services

Also:
- Disable the button while calculating
- Prevent repeated submissions
- Remove stale score, chart, and tips after invalid input
- Add a request timeout
```

### Final User-Facing Messages

```text
Please fill in all activity fields before calculating.
```

```text
Values cannot be negative. Please enter zero or a positive number.
```

```text
Some entered values are invalid or outside the allowed range.
```

```text
Unable to calculate your footprint right now. Please try again.
```

Axios requests also use a timeout so the interface does not remain indefinitely stuck on `Calculating...`.

---

## 10. Accessibility Improvement Prompt

```text
Improve the React form for accessibility.

Add:
- Explicit labels
- Matching htmlFor and id values
- Keyboard-friendly controls
- Accessible validation feedback
- role="alert"
- aria-live
- Measurement units
- Clear example placeholders
```

### Accessibility Improvements

* Every input has an explicit label
* Form controls have unique IDs
* Error messages use `role="alert"`
* Validation feedback uses `aria-live="polite"`
* Inputs follow a logical keyboard tab order
* Fields clearly communicate measurement units
* The layout becomes single-column on smaller screens

---

## 11. Automated Testing Prompt

```text
Create backend automated tests for:

- Transport calculation
- Food calculation
- Electricity calculation
- Shopping calculation
- Root API endpoint
- Valid calculation request
- Negative-value rejection
- Invalid vehicle-type rejection
```

### Testing Corrections

The initial transport test compared floating-point numbers directly:

```python
assert result == 1.7
```

Python returned:

```text
1.7000000000000002
```

The test was corrected using:

```python
pytest.approx(1.7)
```

### Verified Result

```text
27 passed
```

The tests verify both calculation accuracy and backend validation behaviour.

---

## 12. Security Hardening Prompt

```text
Review the project for basic secret-management and API-security issues.

Requirements:
- Never commit the Gemini API key
- Keep real .env files ignored
- Use placeholders in .env.example
- Restrict production CORS
- Validate all backend requests
- Do not expose secrets in frontend code
```

### Security Decisions

* The actual Gemini key is stored only as an environment variable
* `.env.example` contains a placeholder
* `.env` files are ignored
* Git staged content was searched for API-key patterns before commit
* Production CORS uses the deployed frontend URL
* Backend payloads are validated before processing
* The browser only receives the public backend URL

---

## 13. Deployment Preparation Prompt

```text
Prepare the monorepo for production deployment.

Frontend:
- Vercel
- Root directory: frontend
- Build command: npm run build
- Output directory: dist
- Environment-based API URL

Backend:
- Render
- Root directory: backend
- Build command: pip install -r requirements.txt
- Start command using Render's PORT variable
- Secure environment variables
- Health-check endpoint
```

### Deployment Architecture

```text
User Browser
     |
     v
Vercel React Frontend
     |
     v
Render FastAPI Backend
     |
     v
Gemini API or Smart Fallback Engine
```

### Production Services

* Frontend: `https://carbon-footprint-platform-azure.vercel.app`
* Backend: `https://carbon-footprint-platform-s6r4.onrender.com`
* API documentation: `https://carbon-footprint-platform-s6r4.onrender.com/docs`

---

## 14. Manual Verification Performed

The following checks were performed manually:

* Valid carbon calculation
* Empty-field rejection
* Negative-value rejection
* Invalid-category backend rejection
* Chart rendering
* Gemini failure fallback
* Loading-state behaviour
* API request timeout
* Local frontend-backend communication
* Production frontend-backend communication
* CORS configuration
* FastAPI root endpoint
* Swagger API documentation
* Production frontend build
* Git secret-pattern inspection
* Clean Git working tree
* Single active submission branch

---

## 15. Human Review and Corrections

AI-generated output was not copied blindly.

Manual intervention was required to:

* Correct malformed Nix configuration
* Fix Python import and initialization order
* Remove duplicate application configuration
* Repair invalid JSX structure
* Restore incorrect dropdown options
* Fix React form-state updates
* Diagnose cloud-preview networking behaviour
* Add API fallback handling
* Improve validation
* Add accessible labels and alerts
* Correct floating-point testing
* Configure secure environment variables
* Verify production CORS
* Test deployed endpoints directly with `curl`

---

## 16. Prompt-Engineering Principles Used

The prompts evolved according to these principles:

1. **Start broad, then narrow the task**
2. **Provide exact error logs**
3. **Request minimal changes to working code**
4. **Verify one layer at a time**
5. **Test generated output immediately**
6. **Never expose secrets in prompts or repositories**
7. **Prefer graceful degradation over total failure**
8. **Document errors as well as successful outputs**
9. **Use human review before committing generated code**
10. **Validate locally and again after deployment**

---

## 17. Final Reflection

AI significantly accelerated project scaffolding, debugging, and documentation. However, several generated suggestions contained incorrect assumptions or incomplete implementation details.

The strongest results came from combining:

* Clear prompts
* Small implementation steps
* Exact error logs
* Manual code review
* Automated testing
* Security checks
* Real production verification

The final application therefore represents an **AI-assisted but human-validated engineering workflow**.
