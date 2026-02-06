# Elite Bank - Advanced Banking Management System

A full-stack banking application built with **Django (Python)** and **MySQL** that simulates real-world financial operations, including atomic transactions, dynamic credit scoring, and role-based access control.

## Key Features
* **Dynamic Credit Score Engine:** Automatically increases user credit score by 10 points for every successful transfer.
* **"Anti-Error" Transaction Safety:** Uses `transaction.atomic()` to ensure money is never lost during system failures.
* **VIP Lounge Access:** Automatically awards a Gold Badge to users with a balance > ₹50,000.
* **Liquidity Checks:** Prevents the Bank Admin from approving loans if the bank's internal "Vault" has insufficient funds.
* **Master Admin Panel:** Dedicated superuser interface to audit ledgers, delete accounts, and manage loan requests.

## Tech Stack
* **Backend:** Python 3.10+, Django 5.0
* **Database:** MySQL (using `mysql-connector-python`)
* **Frontend:** HTML5, Bootstrap 5, Jinja2 Templates

## How to Run Locally

### 1. Prerequisites
Ensure you have Python and a MySQL Server (like XAMPP or Workbench) installed.

### 2. Installation
```bash
# Clone the repository
git clone [https://github.com/your-username/Analyst_Portfolio.git](https://github.com/your-username/Analyst_Portfolio.git)

# Navigate to the project folder
cd Analyst_Portfolio/Banking_Project

# Install dependencies
pip install -r requirements.txt
