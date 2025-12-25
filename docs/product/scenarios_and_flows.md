# Core Scenarios & Interaction Flows

## Scenario 1: The First-Visit "Review Hook"

**Design Goal:** Low Customer Friction (Staff does the work).

17. **Staff Input:** Staff asks for number and enters it in the Staff Terminal (PWA).
    - **Data Entry:**
      - **Phone Number** (Mandatory, ID).
      - **Bill ID / Receipt Number** (Mandatory).
      - **Bill Amount** (Mandatory, determines points).
      - **Customer Name** (Optional).
      - **"Verbal Consent" Checkbox** (Mandatory): Confirm staff explained the freebie/review process.
      - _Metadata Recorded:_ Timestamp, Staff Name/ID.
18. **WhatsApp Nudge:** Customer immediately receives a WhatsApp message.
    - _Message:_ "Hi [Name]! Tap to verify your review for a **free [Reward]** at [Cafe Name]: [Link]"
19. **Review Loop:** Customer clicks $\rightarrow$ Google Maps $\rightarrow$ Post Review $\rightarrow$ Take Screenshot.
20. **Verification:** Customer sends the photo back to WhatsApp.
21. **AI Success:** Gemini verifies $\rightarrow$ "Verification Successful! Here is your **Coupon Code: KOALA88**. Show this to the staff to claim your freebie!"

> [!NOTE] > **Configurable Loyalty:** Owners configure the "Points Ratio" (e.g., 1 point per $10), "Redeemables", and specific "Freebies" via an Admin Panel (Future).
> **V0 Logic:** Coupon generation is the immediate reward.

## Scenario 2: The Returning Regular

1.  **Check-in:** Staff enters number (or scans Q-Rate QR from the customer's phone).
2.  **Recognition:** Backend detects an existing user.
3.  **Nudge:** WhatsApp: "Welcome back to [Cafe Name]! You're 2 visits away from a free Brew. [View Progress]"
4.  **Identity:** The link opens the Customer PWA, showing their stamp card.

## Scenario 3: Loyalty Redemption

1.  **Redeem:** Customer clicks "Redeem 500 Points" in PWA -> "Generate Coupon".
2.  **Display:** PWA shows a QR Code/Alphanumeric Code (e.g., "BREW500").
3.  **Burn:** Staff scans code or enters it in Staff PWA.
4.  **Backend:** Validates points balance -> Deducts Points -> Marks Code Used -> Success Message.

## Scenario 4: The Social Bonus (Referrals)

1.  **Staff Input:** During check-in, Staff checks "**Guest count**" (e.g., +2 friends).
2.  **Logic:** Backend checks "Referral Bonus" config (e.g., +10 points per guest).
3.  **Reward:** Customer receives extra points notification. "Thanks for bringing friends! You earned +20 bonus points."

## WhatsApp Flow & Identity

- **WhatsApp as OS:** We use WhatsApp for the heavy lifting (notifications, image upload).
- **Identity:** Phone number is the key.
- **Digital Wallet:** "Add to Apple/Google Wallet" available in Customer PWA for geofencing.
