# 🚗 Pricing Module - Assignment (Vcriate)

A Django-based configurable pricing engine that simulates ride pricing logic similar to Uber/Ola. The system supports dynamic pricing rules for distance, time, waiting charges, and specific day-based configurations — all manageable via Django Admin.

---

## 📌 Features

- ✅ **Distance Base Price (DBP)**: Flat rate up to certain kilometers
- ✅ **Distance Additional Price (DAP)**: Per-kilometer rate beyond base distance
- ✅ **Time Multiplier Factor (TMF)**: Tiered multipliers based on ride time
- ✅ **Waiting Charges (WC)**: Cost after initial grace waiting time
- ✅ **Configurable per day-of-week**
- ✅ **Multiple configurations supported**, toggleable via `is_active`
- ✅ **Django Admin UI** for business team to update pricing easily
- ✅ **REST API** to calculate final ride price based on inputs

---

## 🛠 Tech Stack

- Python 3.10+
- Django 5.2+
- SQLite3 (default DB)
- Django Admin
- Postman for API testing

---

## 🚀 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/deadheaven07/Assignment-vcriate.git
cd Assignment-vcriate
