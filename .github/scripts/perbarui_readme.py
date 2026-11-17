"""Perbarui bagian otomatis README profil dari isi repo situs GeoSR.

Bagian yang ditulis ulang ada di antara penanda:
  <!-- KALKULATOR:MULAI --> ... <!-- KALKULATOR:SELESAI -->  kalkulator dan latihan dari konten/alat.json
  <!-- PRAKTIKUM:MULAI -->  ... <!-- PRAKTIKUM:SELESAI -->   alat praktikum per kelompok dari konten/praktikum.json

Alamat situs dibaca dari konten/situs.json di repo situs, jadi ikut berubah bila situs pindah alamat.
Hanya memakai pustaka bawaan Python. Repo sumbernya publik, jadi skrip jalan tanpa token.

Jalankan dari akar repo profil:  python3 .github/scripts/perbarui_readme.py
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

# Repo situs. Ganti di sini bila repo situs pindah pemilik atau nama.
PEMILIK, REPO = "defsayurinda", "defsayurinda.github.io"
MENTAH = f"https://raw.githubusercontent.com/{PEMILIK}/{REPO}/main/"
README = Path(__file__).resolve().parents[2] / "README.md"
STATUS = {"asli": "sumber asli", "sekunder": "sumber sekunder", "belum": "belum terverifikasi"}


def ambil(jalur):
    permintaan = urllib.request.Request(MENTAH + jalur, headers={"User-Agent": "perbarui-readme-profil"})
    with urllib.request.urlopen(permintaan, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def bagian_kalkulator(situs, alat):
    baris = [f"| [{a['judul_pendek']}]({situs}{a['halaman']}) | {a['deskripsi']} | {STATUS.get(a['status'], a['status'])} |"
             for a in alat if a["id"] != "praktikum"]
    return "\n| Alat | Isi | Status rumus |\n|---|---|---|\n" + "\n".join(baris) + "\n"


def bagian_praktikum(situs, praktikum):
    baris = []
    for k in praktikum["kelompok"]:
        tautan = ", ".join(f"[{a['judul']}]({situs}praktikum/{a['id']}/)" for a in k["alat"] if a.get("status") == "tersedia")
        if tautan:
            baris.append(f"- **{k['judul']}:** {tautan}")
    return "\n" + "\n".join(baris) + "\n"


def ganti(teks, nama, isi):
    pola = re.compile(rf"(<!-- {nama}:MULAI -->)(.*?)(<!-- {nama}:SELESAI -->)", re.S)
    if not pola.search(teks):
        sys.exit(f"Penanda {nama} tidak ditemukan di README.md")
    return pola.sub(lambda m: f"{m.group(1)}\n{isi}\n{m.group(3)}", teks)


def main():
    situs = ambil("konten/situs.json")["situs"]
    alat = ambil("konten/alat.json")["alat"]
    praktikum = ambil("konten/praktikum.json")
    lama = README.read_text(encoding="utf-8")
    baru = ganti(lama, "KALKULATOR", bagian_kalkulator(situs, alat))
    baru = ganti(baru, "PRAKTIKUM", bagian_praktikum(situs, praktikum))
    if baru == lama:
        print("README sudah terbaru.")
        return
    README.write_text(baru, encoding="utf-8", newline="\n")
    print("README diperbarui.")


if __name__ == "__main__":
    main()
