# System Flows & Architecture

## 1. The V0 "Review Hook" Flow (Sequence Diagram)

This diagram illustrates how we link the **Staff's Entry** to the **Customer's WhatsApp Message** via the Phone Number.

```mermaid
sequenceDiagram
    autonumber
    actor Staff
    participant PWA as Staff PWA
    participant BE as Backend API
    participant DB as Database
    participant WA as WhatsApp API
    actor Customer
    participant Worker as TaskIQ Worker
    participant AI as Gemini AI

    Note over Staff, Customer: In the Cafe

    Staff->>PWA: Enters Phone (123), Bill ($50), Consent
    PWA->>BE: POST /visits (phone=123, cafe=A)
    BE->>DB: INSERT VerificationRequest(phone=123, cafe=A, status=PENDING)
    BE->>WA: Send Template ("Rate us for Free Cookie")
    WA->>Customer: Delivers WhatsApp Message

    Note over Customer: Verification Loop

    Customer->>WA: Sends Screenshot (Image)
    WA->>BE: Webhook (from=123, type=image)
    BE->>Worker: Enqueue Task (process_webhook)

    Note over Worker: Context Triangulation

    Worker->>DB: SELECT * FROM VerificationRequest WHERE phone=123 ORDER BY date DESC LIMIT 1
    DB-->>Worker: Returns {id: 101, cafe_id: A, status: PENDING}

    Worker->>AI: Verify(Image, context_cafe="Cafe A")
    AI-->>Worker: {valid: true, stars: 5}

    Worker->>DB: UPDATE VerificationRequest SET verified=true
    Worker->>DB: INSERT Coupon(user=123, cafe=A, type=REVIEW_REWARD)

    Worker->>WA: Reply ("Here is your Coupon: FREE-123")
    WA->>Customer: Delivers Coupon
```

## 2. Object State: Verification Request

The life-cycle of a "Visit" record.

```mermaid
stateDiagram-v2
    [*] --> Created : Staff Submits Form
    Created --> PWA_Opened : Customer Clicks Link (Optional)
    Created --> Review_Posted : (Inferred)

    Review_Posted --> Screenshot_Received : Webhook
    Screenshot_Received --> Searching_Context : Worker Lookup(Phone)

    Searching_Context --> Context_Found : Visit Record Exists
    Searching_Context --> Context_Missing : No Visitor Record (Error)

    Context_Found --> Verifying_AI : Gemini Check

    Verifying_AI --> Verified : 4-5 Stars & Matching Name
    Verifying_AI --> Rejected : Blurry/Wrong Cafe

    Verified --> Coupon_Generated : Reward Issued
    Coupon_Generated --> [*]
```

## 3. Data Model Relationships (UML)

How the entities link together to support this flow.

```mermaid
classDiagram
    direction LR

    class Cafe {
        id: int
        name: string
        loyalty_config: json
    }

    class Staff {
        id: string
        cafe_id: int
    }

    class VerificationRequest {
        id: int
        phone_number: string
        bill_id: string
        bill_amount: float
        verbal_consent: bool
        --
        cafe_id: FK
        is_verified: bool
    }

    class User {
        id: int
        phone_number: string
        loyalty_points: int
    }

    class Coupon {
        id: int
        code: string
        type: enum
        is_redeemed: bool
        --
        cafe_id: FK
        user_id: FK
    }

    Cafe "1" -- "many" VerificationRequest : originates_from
    Cafe "1" -- "many" Coupon : issues
    User "1" -- "many" Coupon : owns
    User "1" -- "many" VerificationRequest : associated_with
    VerificationRequest ..> Coupon : triggers_generation_of
```
