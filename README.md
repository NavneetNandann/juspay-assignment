# RareWolf — Python Playwright Automation

This project uses Python and Playwright to practice browser automation on RareWolf. The test covers signing in, opening a product, adding it to the cart, and reaching checkout. It stops before submitting a payment or entering an OTP.

Use only an account and environment you’re authorized to test.

## Requirements

- Python 3.10+
- Chromium installed through Playwright
- An authorized RareWolf test account



## Setup

Run these commands from the project directory:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install playwright pytest
python -m playwright install chromium

Open `https://rarewolf.online/` . Demo login: `navneetnandan422@gmail.com` / `12345678`.

## Project structure

```text
payment-automation-challenge/
├── app.py
├── requirements.txt
├── README.md
├── tests/
│   └── test_payment.py
└── artifacts/       # created when tests run
```

## GitHub submission

```bash
git init
git add app.py tests requirements.txt README.md
git commit -m "Add Playwright payment automation demo"
git branch -M main
git remote add origin https://github.com/NavneetNandann/payment-automation-challenge.git
git push -u origin main
```


