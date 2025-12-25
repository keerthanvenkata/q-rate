# System Architecture

## Overview

Q-Rate is a multi-tenant loyalty and review platform built on a staff-driven interaction model.

## Components

### 1. Backend (FastAPI)

- **Role**: Central Orchestrator.
- **Responsibilities**:
  - API for Frontends (Staff, Customer, Admin).
  - WhatsApp Webhook handling.
  - Task Orchestration (TaskIQ + Redis).
  - AI Verification (Gemini).

### 2. Frontend - Staff PWA (React)

- **Role**: The "Input Terminal".
- **Users**: Waiters, Cashiers.
- **Key Features**:
  - Visit Entry (Phone, Bill ID, Amount).
  - Verbal Consent Check.
  - Offline-first capabilities (PWA).

### 3. Frontend - Admin Portal (React) -- _Planned_

- **Role**: Configuration & Analytics.
- **Users**: Cafe Owners/Managers.
- **Key Features**:
  - **Loyalty Config**: Set points ratio (e.g., $1 = 1 Point).
  - **Rewards**: Configure Freebies/Coupons.
  - **Analytics**: View staff performance and customer retention.

### 4. Frontend - Customer PWA (React)

- **Role**: Digital Wallet/Stamp Card.
- **Users**: End Customers.
- **Access**: Via WhatsApp Link (Magic Link).

## Data Flow (Verification Loop)

1. Staff Input (Staff PWA) -> Backend (Create `VerificationRequest`).
2. Backend -> WhatsApp API (Send Template Message).
3. Customer -> WhatsApp (Upload Screenshot).
4. WhatsApp Webhook -> Backend (TaskIQ Worker).
5. Worker -> Gemini (Verify Image).
6. Worker -> Backend (Generate Coupon).
7. Backend -> WhatsApp API (Reply with Code).
