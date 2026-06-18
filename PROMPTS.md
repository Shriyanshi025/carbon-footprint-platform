# AI Prompt Documentation

This document outlines the prompts used for interacting with the Gemini AI model in the Carbon Footprint Awareness Platform.

## Personalized Tips Prompt

**Endpoint:** `/tips`

**Method:** POST

**Prompt:**

```
Based on the following carbon footprint data, provide personalized tips to reduce environmental impact.
The data is in the format: {footprint_data}.
Provide 3 actionable and specific tips.
```

**Example `footprint_data`:**

```json
{
  "total_footprint": 150.75,
  "breakdown": {
    "transport": 51,
    "food": 81,
    "electricity": 18.75
  }
}
```
