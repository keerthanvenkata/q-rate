# Core Scenarios & Interaction Flows

## Scenario 1: The First-Visit "Review Hook"

**Design Goal:** Low Customer Friction (Staff does the work).

1.  **Staff Input:** Staff asks for number and enters it in the Staff Terminal (PWA).
2.  **WhatsApp Nudge:** Customer immediately receives a WhatsApp message.
    - _Message:_ "Hi! Tap to verify your review for a free cookie at [Cafe Name]: [Link]"
3.  **Review Loop:** Customer clicks $\rightarrow$ Google Maps $\rightarrow$ Post Review $\rightarrow$ Take Screenshot.
4.  **Verification:** Customer sends the photo back to WhatsApp.
5.  **AI Success:** Gemini verifies $\rightarrow$ "Verification Successful! Show this code: CAFE123."

## Scenario 2: The Returning Regular

1.  **Check-in:** Staff enters number (or scans Q-Rate QR from the customer's phone).
2.  **Recognition:** Backend detects an existing user.
3.  **Nudge:** WhatsApp: "Welcome back to [Cafe Name]! You're 2 visits away from a free Brew. [View Progress]"
4.  **Identity:** The link opens the Customer PWA, showing their stamp card.

## WhatsApp Flow & Identity

- **WhatsApp as OS:** We use WhatsApp for the heavy lifting (notifications, image upload).
- **Identity:** Phone number is the key.
- **Digital Wallet:** "Add to Apple/Google Wallet" available in Customer PWA for geofencing.
