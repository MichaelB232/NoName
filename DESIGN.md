# Design System & UI/UX Specification
**Inspiration:** Harvey AI (harvey.ai) & Modern Institutional Legal-Tech  
**Philosophy:** "Understated Authority, Editorial Precision, Zero AI Gimmicks"  
**Domain:** Enterprise FinTech & Regulatory Compliance (OJK, BI, UU PDP)

---

## 1. Design Philosophy & Aesthetic Pillars

Harvey AI is trusted by firms like Allen & Overy, PwC, and elite legal departments not because it looks "futuristic", but because it looks **serious, reliable, and institutional**.

### The 4 Core Tenets:
1. **Editorial Gravitas (Buku Besar Hukum Modern):**
   * Perpaduan tipografi **Serif Editorial** untuk judul/dokumen resmi dan **Clean Geometric Sans** untuk data grid & navigation.
   * Tidak ada ilustrasi kartun, tidak ada maskot robot, tidak ada ikon "magic wand" (tongkat sihir) yang terkesan murahan.
2. **Deep Obsidian & Warm Ivory (Palet Monokromatik Hangat):**
   * Bukan *pure black* `#000000` (terlalu tajam di mata) melainkan **Deep Obsidian & Charcoal** (`#0C0D0E`, `#141517`) dengan teks **Warm Cream / Off-White** (`#F7F7F8`, `#DCDDDF`).
   * Border super-halus (*hairline borders*) berukuran 1px dengan opasitas rendah (`border-white/10`).
3. **Muted Financial Risk Indicators (Bukan Warna Neon):**
   * Indikator status kepatuhan tidak menggunakan warna neon cerah yang mengganggu konsentrasi (*visual noise*).
   * Menggunakan palet muted: **Sage Green** (Compliant), **Terracotta / Muted Rose** (Pelanggaran), **Warm Ochre** (Ambiguitas), dan **Ice Slate** (Info).
4. **Verifiable Groundedness (Setiap Klaim Punya Jangkar):**
   * Seperti Harvey, setiap kata yang dihasilkan AI memiliki *interactive citation badge* yang jika diklik langsung menyorot (*highlight*) pasal asli di dokumen PDF dan dasar hukum regulasinya.

---

## 2. Color Palette & Semantic Design Tokens

```
/* Base Backgrounds */
--bg-canvas:        #0C0D0E;  /* Obsidian Canvas Dasar */
--bg-surface:       #131518;  /* Panel Dokumen & Sidebar */
--bg-elevated:      #1A1D21;  /* Card, Modal, Dropdown */
--bg-subtle:        #22262B;  /* Hover State & Inactive Tabs */

/* Hairline Borders */
--border-hairline:  rgba(255, 255, 255, 0.08);
--border-focus:     rgba(255, 255, 255, 0.22);

/* Typography Colors */
--text-primary:     #F5F5F7;  /* High-contrast Warm Cream */
--text-secondary:   #A0A4AB;  /* Deskripsi, Metadata, Label */
--text-tertiary:    #636770;  /* Placeholder, Inactive Icons */

/* Legal & Compliance Status Tokens (Muted Sophisticated) */
--status-compliant: #10B981;  /* Sage Emerald */
--status-compliant-bg: rgba(16, 185, 129, 0.08);

--status-violation: #F43F5E;  /* Terracotta Rose */
--status-violation-bg: rgba(244, 63, 94, 0.08);

--status-ambiguous: #F59E0B;  /* Warm Ochre Amber */
--status-ambiguous-bg: rgba(245, 158, 11, 0.08);

--status-revised:   #60A5FA;  /* Institutional Cobalt */
--status-revised-bg: rgba(96, 165, 250, 0.08);
```

---

## 3. Typography Hierarchy

Harvey menggabungkan keanggunan firma hukum tradisional dengan ketajaman antarmuka modern:

| Role | Font Family | Size / Weight | Contoh Penggunaan |
| :--- | :--- | :--- | :--- |
| **Editorial Display** | `Newsreader` / `Playfair` / `Cormorant` | 24px - 36px / Serif Medium | Judul Kontrak, Ringkasan Eksekutif, Nilai Skor Kepatuhan. |
| **System Interface** | `Inter` / `Geist Sans` | 13px - 15px / Sans-serif 400 & 500 | Sidebar, Table Headers, Button, Badges, Chat Prompt. |
| **Statute & Code** | `JetBrains Mono` / `Geist Mono` | 11px - 12px / Monospace | Nomor Pasal (`Pasal 29 ayat 2`), Persentase Bunga (`0.30%`), S3 Key. |

---

## 4. Layout Architecture: The "Vault & Split-Canvas"

Antarmuka utama dibagi menjadi 3 kolom utama dengan rasio yang dirancang untuk fokus kerja tinggi (*high cognitive load*):

```
┌──────────────┬─────────────────────────────────────┬─────────────────────────────────────┐
│ MATTERS      │ ORIGINAL CONTRACT VIEWER            │ COMPLIANCE MATRIX & AGENT COPILOT   │
│ VAULT        │ (Left Pane - 50% Width)             │ (Right Pane - 50% Width)            │
├──────────────┼─────────────────────────────────────┼─────────────────────────────────────┤
│ 📁 PT FinTech│ Perjanjian Pinjaman P2P             │ ⚡ Compliance Score: 78/100         │
│  ├ Ingestion │                                     │                                     │
│  ├ Pending   │ Pasal 5: Ketentuan Suku Bunga       │ 🔴 Pasal 5.2 — Batasan Bunga        │
│  └ Audited   │ 5.1 Pemberi dana setuju...          │   Pelanggaran: POJK 10/2022 Ps. 29  │
│              │                                     │   Nilai: 0.45%/hari (Batas: 0.3%)   │
│ 📄 SLA 2026  │ [5.2 Bunga ditetapkan 0.45% per]   │   [ Review Redline Revision ]       │
│ 📄 NDA PT X  │     [hari secara majemuk.]          │                                     │
│              │                                     │ 🟡 Pasal 8.1 — Akses Kontak HP      │
│              │ Pasal 6: Agunan dan Mitigasi...     │   Pelanggaran: UU PDP Ps. 20        │
└──────────────┴─────────────────────────────────────┴─────────────────────────────────────┘
```

### 1. Left Vault (Sidebar - 240px Collapsible)
* Menampilkan daftar dokumen kontrak aktif, status audit, dan riwayat revisi.
* Desain minimalis tanpa ikon warna-warni; hanya monochrome outlines.

### 2. Primary Canvas (Left Pane - 50% Lebar Layar)
* Dokumen kontrak dirender dalam format *clean reader*.
* Baris atau klausul yang memiliki temuan audit memiliki garis tipis di sebelah kirinya (*gutter accent border*).
* Setiap klausul memiliki ID DOM tetap (`id="clause-5.2"`).

### 3. Compliance Matrix & Redline Assistant (Right Pane - 50% Lebar Layar)
* Menampilkan ringkasan eksekutif kepatuhan:
  * **Overall Compliance Score Card** (e.g. `82/100`).
  * **Estimated Regulatory Exposure** (e.g. `Rp 250.000.000` potensi denda OJK).
* Kartu temuan audit interaktif:
  * Mengklik kartu otomatis men-scroll dokumen di sebelah kiri dengan transisi halus dan highlight kuning hangat sementara.

---

## 5. Komponen Kunci Khas Harvey AI

### A. The "Grounding Citation Pill"
Setiap kali AI menyebutkan suatu undang-undang, tampilkan dalam bentuk pill kecil ber-font monospaced:
```tsx
<span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-xs font-mono bg-surface border border-border-hairline text-text-secondary hover:text-text-primary hover:border-border-focus transition cursor-pointer">
  <ScaleIcon className="w-3 h-3 text-status-ambiguous" />
  POJK 10/2022 §29(2)
</span>
```

### B. The Git-Style Legal Redline Diff Modal
Saat user mengklik **[Review Redline Revision]**, muncul panel perbandingan sebelum dan sesudah yang sangat bersih:

```
────────────────────────────────────────────────────────────
REVISION PROPOSAL — PASAL 5 AYAT 2 (BUNGA & BIAYA LAYANAN)
────────────────────────────────────────────────────────────
Original Text (Batal Demi Hukum):
[- Peminjam dikenakan suku bunga pinjaman sebesar 0.45% (nol -]
[- koma empat puluh lima persen) per hari kalender.          -]

Proposed Compliant Clause:
{+ Peminjam dikenakan total manfaat ekonomi dan suku bunga   +}
{+ pinjaman paling banyak sebesar 0.30% (nol koma tiga puluh +}
{+ persen) per hari kalender sesuai batas maksimum POJK.     +}

Rasional Hukum:
Sesuai Surat Edaran OJK No. 19/SEOJK.05/2023, batas maksimum 
bunga harian pendanaan produktif/konsumtif diturunkan menjadi 
0.30% per hari sejak 1 Januari 2024.

[ ✕ Tolak Usulan ]                     [ ✓ Terapkan ke Kontrak ]
```

---

## 6. Micro-Interactions & Motion Standard

1. **Duration:** 150ms – 250ms (Jangan ada animasi lambat atau melayang-layang yang membuat software terasa lambat bagi profesional).
2. **Easing:** `cubic-bezier(0.16, 1, 0.3, 1)` (Apple/Harvey snappy ease-out).
3. **Skeleton Loading:** Shimmer efek gelap monokromatik (`bg-white/5` pulse), bukan warna abu-abu terang.
4. **Agent Step Feedback:** Tampilkan terminal baris kecil di pojok kanan bawah dengan teks monospaced saat AI bekerja:
   `[2/4] Cross-referencing Clause 5.2 with POJK No. 10/POJK.05/2022...`
