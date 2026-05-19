# Lead Middleware API

This service receives lead data from different sources, cleans and standardizes it, and forwards it to the MIS API.

---

## Purpose

- Accept data from bots (e.g., WATI)
- Normalize fields (especially phone numbers)
- Apply source-specific transformations
- Send clean data to MIS

---

## Endpoint

POST /api/leads

---

## Data Transformation

This API does not forward incoming data as-is.

It transforms incoming request data into the format required by the MIS API.

### Incoming Format (Example)

```json
{
  "source": "sm_general_bot",
  "data": {
    "name": "Test User",
    "phone": "9446649206",
    "email": "testuser@gmail.com",
    "service": "Study Abroad Guidance",
    "branch": "Kochi",
    "comments": "Interested"
  }
}
```

### Transformed Output (Sent to MIS)

```json
{
  "name": "Test User",
  "Email": "testuser@gmail.com",
  "Phone": "9446649206",
  "DesiredCourse": "",
  "NearestBranch": "Kochi",
  "Remarks": "Service: Study Abroad Guidance | Comments: Interested | CountryCode: +91",
  "label": "14920"
}
```

---

## What the API does

- Validates `source`
- Cleans input fields
- Normalizes phone number into:
  - Phone (national number)
  - CountryCode (with +)
- Builds final payload
- Sends data to MIS API

---

## Running the Service

1. Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Start server

```bash
python run.py
```
4. Access Locally

http://127.0.0.1:8000/docs

---

## Testing

Use Postman or Swagger UI:

POST http://127.0.0.1:8000/api/leads

---

## Adding a New Source

1. Add a new transformer in `transformers.py`
2. Register it in `get_transformer()`

Example:

```python
if source == "new_source":
    return transform_new_source
```
---

## Updating the Service

Update the code on the server using:

```bash
git pull
sudo systemctl restart lead-middleware
```

---
## Notes

- Do not edit code directly on the server
- Always update locally and push via Git
- Phone numbers are normalized before sending to MIS

---
## License

This project is proprietary software developed for
Santamonica Study Abroad Pvt. Ltd.
Unauthorized use or distribution is not permitted.

---