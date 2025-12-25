# Product Architecture & Tech Stack

To maintain high standards (SDE-focused) and scalability, we utilize a Multi-tenant Monorepo architecture.

## The 2026 Pro Stack

| Component       | Technology                | Rationale                                                                |
| :-------------- | :------------------------ | :----------------------------------------------------------------------- |
| **Monorepo**    | pnpm Workspaces           | Manages `staff-app`, `customer-pwa`, and `api` in one place.             |
| **Backend**     | FastAPI (Python 3.12+)    | High-concurrency async handling for WhatsApp Webhooks.                   |
| **Database**    | PostgreSQL (Multi-tenant) | Relational data for complex loyalty logic with RLS (Row Level Security). |
| **Cache/Queue** | Redis + TaskIQ            | Low-latency state management and async AI background tasks.              |
| **AI Vision**   | Gemini 1.5 Flash          | Multimodal reasoning for OCR + fraud detection in screenshots.           |
| **Frontend**    | React 19 + Vite           | Ultra-fast PWA with Offline Support (Service Workers + IndexedDB).       |
| **Infra**       | GCP Cloud Run             | Serverless containers that scale to zero (saves credits).                |
