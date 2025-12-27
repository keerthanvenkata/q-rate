# Staff PWA Design Proposal

## Overview

The **Staff PWA** is a mobile-first web application designed for speed and simplicity. Staff members use it to:

1.  **Initiate Visits** (The Hook).
2.  **Redeem Coupons** (The Reward).

## Architecture

- **Framework**: React + Vite (Typescript).
- **Styling**: Vanilla CSS (with CSS Variables for theming) or Tailwind (per user preference - assuming Vanilla based on system instructions unless specified).
- **State Management**: React Query (Server State), Context API (Auth/Session).
- **Routing**: React Router DOM.

## Sitemap & Flow

### 1. Home / Dashboard (`/`)

- **Goal**: Quick access to primary actions.
- **Components**:
  - **Greeting**: "Hello, [Staff Name]"
  - **Action Cards**:
    - [CTA Button] **"New Visit"** (Primary) -> Goes to `/visit`
    - [Secondary Button] **"Redeem Coupon"** -> Goes to `/redeem`
  - **Recent Activity**: List of last 3-5 actions (e.g., "Checked in 9876543210").

### 2. New Visit Form (`/visit`)

- **Goal**: Capture customer data in < 10 seconds.
- **Fields**:
  - **Phone Number** (Tel input, auto-format).
  - **Bill Amount** (Number, Currency).
  - **Bill ID** (Text).
  - **Guest Count** (Number stepper, Default: 1).
  - **Consent Checkbox** (Required): "I have explained the review process."
  - _(Optional)_ Customer Name.
- **Action**: "Send Magic Link" (POST `/api/visits`).

### 3. Redemption & Lookup (`/redeem`)

- **Goal**: Verify coupons or burn loyalty points.
- **Modes**:
  - **Scan QR**: (Future V1 feature using camera).
  - **Enter Code**: Text input for "LATTE-492".
- **Result**:
  - Success: "✅ Valid Coupon: Free Cookie".
  - Error: "❌ Invalid or Expired".

## UI/UX Principles

- **Big Buttons**: easy to tap on mobile.
- **High Contrast**: readable in varying cafe lighting.
- **Speed**: Optimistic UI updates.

## Discussion Points

1.  **Styling**: Shall we stick to **Vanilla CSS** (as per global rules) or use **Tailwind** for speed?
2.  **Auth**: For V0, will we use a simple shared "Access Pin" or full Login?
3.  **Review Logic**: Confirming this PWA does _not_ show the Google Review URL. (It only triggers the WhatsApp message).
