# q-rate

q-rate is a loyalty and verification system featuring:

- **Backend**: FastAPI (Python) with PostgreSQL.
- **Frontend**: Two PWA applications (Customer & Staff) built with React + Vite.
- **Database**: PostgreSQL (managed via Docker).
- **Integrations**: WhatsApp Business API (Meta/Twilio) for notifications and interactions.

## Project Structure

- `/backend`: FastAPI application.
- `/frontend-customer`: Customer-facing PWA.
- `/frontend-staff`: Staff-facing PWA.
- `/docs`: Project documentation.
- `docker-compose.yml`: Local development services (DB, Adminer).

## Getting Started

1.  **Backend**:

    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows
    pip install -r requirements.txt
    docker-compose up -d
    uvicorn app.main:app --reload
    ```

2.  **Frontend**:
    ```bash
    cd frontend-customer  # or frontend-staff
    npm install
    npm run dev
    ```
