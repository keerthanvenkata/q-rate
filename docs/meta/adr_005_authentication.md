# ADR 005: Authentication & Authorization Strategy

## Context

- **Multi-tenancy**: We serve multiple cafes. Data _must_ be isolated.
- **Staff**: High turnover, shared devices (iPad at POS). Fast login needed.
- **Owners**: Secure remote access (Admin Portal).
- **Customers**: Zero friction point accumulation.

## Decisions

### 1. Staff Authentication (Device Binding + PIN)

- **Concept**: The "Tablet" is bound to the Cafe, the "Session" is bound to the Staff member.
- **Phase 1: Device Setup (One Time)**
  - Manager opens `staff.q-rate.app` on the tablet.
  - Enters **Cafe Code** (e.g., `CAFE-123`) OR scans a Setup QR.
  - System validates code and stores `cafe_id` in **LocalStorage** (Permanent).
  - _Answer to "How does it work?"_: The ID is stored in the browser. The URL _can_ pre-fill it (`/setup?code=123`), but it persists after that.
- **Phase 2: Daily Login (Shift)**
  - Tablet shows "Welcome to [Cafe Name]".
  - Staff selects their **Name** from a list.
  - Enters **4-Digit PIN**.
  - Authenticates and gets a `session_token`.
- **Management**:
  - Owner creates Staff profiles and sets PINs in Admin Portal.

### 2. Owner Authentication (Admin Portal)

- **Method**: Email/Password (V0).
- **Scope**: JWT scoped to `cafe_ids` user owns.

### 3. Customer Authentication

- **Method**: Phone -> WhatsApp Magic Link -> Session.

## Schema Implications

- **Staff Table**: `id`, `name`, `pin_hash`, `cafe_id`, `role`.
- **Cafe Table**: `code` (Unique String for setup).
