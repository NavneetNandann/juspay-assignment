import os
from pathlib import Path

import pytest
from playwright.sync_api import expect, sync_playwright


BASE_URL = os.getenv("BASE_URL", "https://rarewolf.online").rstrip("/")


@pytest.fixture
def credentials():
    email = os.getenv("TEST_EMAIL")
    password = os.getenv("TEST_PASSWORD")
    if not email or not password:
        pytest.skip("Set TEST_EMAIL and TEST_PASSWORD before running this test")
    return email, password


def test_rarewolf_reaches_upi_verification(credentials):
    email, password = credentials
    Path("artifacts").mkdir(exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(
            ignore_https_errors=True,
            viewport={"width": 1365, "height": 900},
        )
        page = context.new_page()

        try:
            page.goto(f"{BASE_URL}/login", wait_until="domcontentloaded")
            page.get_by_role(
                "textbox", name="Email or phone number"
            ).fill(email)
            page.get_by_role("textbox", name="Password").fill(password)
            page.get_by_role("button", name="Log in").click()

            cart = page.get_by_role("link", name="Cart")
            expect(cart).to_be_visible(timeout=20_000)

            # The homepage has product cards; skip the unrelated deal-carousel
            # clicks from codegen that caused the collection-time timeout.
            add_product = page.get_by_role(
                "button", name="Add Wholegrain Breakfast Oats 1kg to cart"
            )
            expect(add_product).to_be_visible(timeout=20_000)
            add_product.click()
            cart.click()
            page.get_by_role("link", name="Continue to checkout").click()

            page.get_by_role(
                "radio", name="Pay online with Razorpay UPI"
            ).check()
            page.get_by_role(
                "button", name="Pay securely with Razorpay"
            ).click()

            checkout = page.locator("iframe").content_frame
            checkout.get_by_test_id("upi").click()
            checkout.get_by_role(
                "radio", name="UPI 4 Offers googlepay"
            ).check()
            checkout.get_by_role("button", name="UPI QR Code").click()

            # Reach the verification stage, then stop without scanning or paying.
            expect(checkout.get_by_text("Scan the QR", exact=False)).to_be_visible(
                timeout=20_000
            )
        except Exception:
            page.screenshot(path="artifacts/rarewolf-failure.png", full_page=True)
            raise
        finally:
            context.close()
            browser.close()
