# Internal Wallet Service API

A lightweight, beginner-friendly internal wallet service built with [FastAPI](https://fastapi.tiangolo.com/ "FastAPI official documentation"). This API allows users to create multi-currency wallet accounts, deposit and withdraw funds, transfer money between accounts, and audit immutable transaction logs under strict business rules.

---

## Key Features & Business Rules

* **Account Creation**: Users can open a wallet with a unique `account_number` (or username), `owner_name`, supported `currency` (`USD`, `NGN`, `GHS`, `KES`), and a secret 4-digit `PIN`.
  * *Initial Balance*: Every new account starts with a balance of `0.00`.
  * *PIN Security*: The 4-digit PIN is stored securely in the database and is **never** exposed in any public response schema.
* **Immutable Transactions Ledger**: Every deposit, withdrawal, and transfer automatically generates a permanent record in the `transactions` table containing the transaction ID, account number/ID, transaction type, amount, and timestamp.
* **Zero Overdraft Rule**: Withdrawals and outgoing transfers immediately fail with a `400 Bad Request` if the sender's balance is less than the requested amount.
* **Currency Match Enforcement**: Transfers between two wallets must share the exact same currency (e.g., `GHS` to `GHS`). Cross-currency transfers are rejected with a `400 Bad Request`.
* **Account Freeze Gatekeeper**: When an account is frozen, the owner can still check their balance and view transaction history, but all outgoing movements (withdrawals and transfers out) are blocked.

---

## Tech Stack

* **Framework**: [FastAPI](https://fastapi.tiangolo.com/ "FastAPI official website")
* **Validation & Schemas**: Pydantic
* **Database & ORM**: SQLite / PostgreSQL with SQLAlchemy (or your chosen ORM)
* **Server**: Uvicorn

---

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com
cd internal-wallet-api
```

### 2. Create & Activate a Virtual Environment
```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install "fastapi[standard]" sqlalchemy
```

### 4. Run the Development Server
```bash
fastapi dev main.py
```
Once running, open your browser to access the automatic interactive API docs:
* **Swagger UI**: `http://127.0.0.1:8000/docs`
* **ReDoc**: `http://127.0.0`

---

## API Endpoints Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/wallets/` | Create a new wallet account (starts at `0` balance). |
| `GET` | `/wallets/{account_number}` | Retrieve wallet details and current balance (excludes PIN). |
| `POST` | `/wallets/{account_number}/deposit` | Deposit funds into a wallet and log the transaction. |
| `POST` | `/wallets/{account_number}/withdraw` | Withdraw funds (enforces PIN, Freeze Gatekeeper, and Zero Overdraft). |
| `POST` | `/wallets/transfer` | Transfer funds between two wallets of the same currency. |
| `PATCH` | `/wallets/{account_number}/freeze` | Freeze or unfreeze a wallet account. |
| `GET` | `/wallets/{account_number}/transactions` | View immutable transaction history for an account. |

---

## Example Requests

### Create a Wallet (`POST /wallets/`)
**Request Body:**
```json
{
  "account_number": "kwame_01",
  "owner_name": "Kwame Mensah",
  "currency": "GHS",
  "pin": "1234"
}
```

**Response (`201 Created`):**
```json
{
  "account_number": "kwame_01",
  "owner_name": "Kwame Mensah",
  "currency": "GHS",
  "balance": 0.0,
  "is_frozen": false
}
```
*(Notice the `pin` is omitted from the response.)*

### Transfer Funds (`POST /wallets/transfer`)
**Request Body:**
```json
{
  "sender_account": "kwame_01",
  "receiver_account": "ama_02",
  "amount": 150.00,
  "pin": "1234"
}
```

---

## Error Handling

| HTTP Status | Condition |
| :--- | :--- |
| `400 Bad Request` | Insufficient balance (Zero Overdraft Rule), mismatched currencies on transfer, or invalid amount (`<= 0`). |
| `401 Unauthorized` | Incorrect 4-digit PIN provided for withdrawal or transfer. |
| `403 Forbidden` | Account is frozen and cannot process withdrawals or outgoing transfers. |
| `404 Not Found` | Sender or receiver wallet account does not exist. |

---

## Project Structure

```text
digital-wallet-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization and route registration
│   ├── config.py            # App settings and environment configurations
│   ├── database.py          # SQLAlchemy engine, SessionLocal, and Base
│   ├── models.py            # SQLAlchemy database models (Wallet, Transaction)
│   ├── schemas.py           # Pydantic schemas for request & response validation
│   ├── crud.py              # Database queries and business logic operations
│   ├── security.py          # PIN hashing and verification utilities
│   └── routers/             # API endpoint routes
│       ├── __init__.py
│       └── wallets.py       # Wallet & transaction endpoints
│
├── tests/
│   ├── __init__.py
│   └── test_wallets.py      # Automated tests for wallet features and business rules
│
├── pyproject.toml           # Project dependencies and configurations
└── README.md                # Project documentation and guide
```

