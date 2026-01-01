# Design Decisions & Architecture Decisions Log (ADR)

## 001. "Context Triangulation" for Verification (V0)

- **Context**: We need to link a customer's WhatsApp screenshot to a specific Cafe Visit without asking the customer to scan a QR code (Zero Friction).
- **Decision**: We use a "Triangulation" logic:
  1.  Staff enters Customer Phone in Staff PWA -> Creates `VerificationRequest`.
  2.  Customer sends Image to WhatsApp Bot.
  3.  Worker looks up `VerificationRequest` by `sender_phone` (Latest pending request).
  4.  Logic assumes the customer sends the photo shortly after the visit.
- **Tradeoff**: Edge case where a user visits two cafes back-to-back and sends a photo for the first one late. Accepted for V0 simplicity.

## 002. Immutable Audit Logs

- **Context**: Compliance requires strict tracking of who did what (Consent, Policy Changes).
- **Decision**: Created a dedicated `audit_logs` table with `JSONB` payload.
- **Logic**: DB-level immutability is not enforced yet, but App-level service provides a "Write Only" interface.

## 003. Rate Limiting & Point Logic (Distinction)

- **Context**: Distinction between "Just Visiting" (Bill Payment) and "Checking In" (Loyalty).
- **Decision**:
  - **Visits/Nudges**: **UNLIMITED**. Every bill payment triggers a visit record and a WhatsApp Nudge.
  - **Check-in Points**: **LIMITED**. (Configurable: 1/cafe/day, 5/global/day).
  - **Review Reward**: **ONE-TIME**. A user can only be "Verified" for a Google Review once per cafe (Lifetime).
  - **Bill Points**: **UNLIMITED**. Always awarded based on spend.

## 004. Stack Choices

- **Backend**: FastAPI (Async) + SQLAlchemy + Postgres (Robustness).
- **Task Queue**: TaskIQ + Redis (Future-proof for high throughput).
- **Frontend**: React + Vite (Standard, Staff PWA focus).
