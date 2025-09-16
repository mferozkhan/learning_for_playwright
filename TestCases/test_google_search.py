import pytest
import re
from playwright.sync_api import expect
from PageObject.google_home_page import GoogleHomePage


class TestGoogleSearch:
    def test_google_search(self, page):
        google_page = GoogleHomePage(page)

        # Start tracing
        google_page.start_tracing("google_search_test")

        try:
            # Navigate to Google
            google_page.navigate_to_google()

            # Accept cookies if the dialog appears
            try:
                page.get_by_role("button", name="Accept all").click(timeout=5000)
            except:
                pass  # Cookie dialog might not appear

            # Verify we're on Google homepage
            expect(page).to_have_title(re.compile(r"Google", re.IGNORECASE))

            # Perform search
            google_page.search_for("playwright")

            # Verify search results
            expect(page.locator("#search")).to_be_visible()

        finally:
            # Stop tracing and save
            google_page.stop_tracing("google_search_test")

    def test_gmail_navigation(self, page):
        google_page = GoogleHomePage(page)

        # Start tracing
        google_page.start_tracing("gmail_navigation_test")

        try:
            # Navigate to Google
            google_page.navigate_to_google()

            # Accept cookies if the dialog appears
            try:
                page.get_by_role("button", name="Accept all").click(timeout=5000)
            except:
                pass  # Cookie dialog might not appear

            # Click on Gmail link
            page.get_by_role("link", name="Gmail", exact=True).click()

            # Verify we're on the Gmail page
            expect(page).to_have_title(re.compile(r"Gmail", re.IGNORECASE))

        finally:
            # Stop tracing and save
            google_page.stop_tracing("gmail_navigation_test")