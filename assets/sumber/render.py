"""Render banner (terang dan gelap) dan foto profil dari assets/sumber/banner.html ke PNG.

Butuh Playwright:  pip install playwright  lalu  python -m playwright install chromium
Jalankan dari akar repo profil:  python3 assets/sumber/render.py
"""
from pathlib import Path

from playwright.sync_api import sync_playwright

SUMBER = Path(__file__).resolve().parent
ASET = SUMBER.parent
DAFTAR = (("banner", "terang", 1280, 320, "banner-terang.png"),
          ("banner", "gelap", 1280, 320, "banner-gelap.png"),
          ("foto", "gelap", 460, 460, "foto-profil.png"))


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for jenis, tema, lebar, tinggi, nama in DAFTAR:
            hal = browser.new_page(viewport={"width": lebar, "height": tinggi}, device_scale_factor=2)
            hal.goto(f"{(SUMBER / 'banner.html').as_uri()}?jenis={jenis}&tema={tema}")
            hal.evaluate("document.fonts.ready")
            hal.wait_for_timeout(300)
            hal.screenshot(path=str(ASET / nama))
            hal.close()
            print("ditulis", nama)
        browser.close()


if __name__ == "__main__":
    main()
