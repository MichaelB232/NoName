# DESIGN.md — Compliance-Agent Design System & UI/UX Specification

**Versi:** 1.0 · **Target implementasi:** AI Coding Agent via FigCraft (Figma Variables + Auto Layout) → React/Tailwind/Tiptap
**Filosofi:** *Understated Authority · Editorial Precision · Zero AI Gimmicks*

---

## 0. Prinsip Desain (Wajib Dipatuhi Agent)

1. **Otoritas yang tenang.** Tidak ada gradien dekoratif, glow, sparkle, ikon "magic wand", atau animasi berlebihan. Antarmuka harus terasa seperti ruang kerja firma hukum papan atas.
2. **Presisi editorial.** Teks hukum diperlakukan sebagai dokumen cetak: serif, ritme baris lega, kolom terbaca (max 72ch).
3. **Setiap klaim AI harus dapat ditelusuri.** Tidak ada output hukum tanpa Citation Pill. Tidak ada pill tanpa status verifikasi.
4. **Warna berarti status, bukan dekorasi.** Warna semantik hanya dipakai untuk status kepatuhan.
5. **Kepadatan informasi tinggi, tetapi tenang.** Pengguna (In-House Counsel, Corp Sec, Associate) bekerja berjam-jam: kontras nyaman, tanpa putih menyilaukan.
6. **Bahasa antarmuka: Bahasa Indonesia formal** (label sistem boleh memakai istilah baku bahasa Inggris hukum seperti *redline*, *clause*, bila lazim di praktik).

---

## 1. Color Tokens

### 1.1 Foundation (Dark Mode adalah mode utama)

| Token | Nama | Hex / RGBA | Penggunaan |
|---|---|---|---|
| `color.canvas` | Deep Obsidian Canvas | `#0C0D0E` | Latar halaman, workspace utama |
| `color.surface` | Panel Surface | `#131518` | Sidebar, panel samping, header tabel |
| `color.elevated` | Elevated Card | `#1A1D21` | Kartu, modal, popover, dropdown |
| `color.elevated-hover` | Elevated Hover | `#20242A` | Hover pada kartu/baris interaktif |
| `color.text-primary` | Warm Cream | `#F5F5F7` | Judul, teks utama |
| `color.text-secondary` | Warm Stone | `#A0A4AB` | Teks sekunder, metadata, label |
| `color.text-tertiary` | Muted Stone | `#6E727A` | Placeholder, disabled, caption |
| `color.border-hairline` | Hairline | `rgba(255,255,255,0.08)` | Semua border standar 1px |
| `color.border-strong` | Hairline Strong | `rgba(255,255,255,0.16)` | Border fokus ringan, divider penting |
| `color.focus-ring` | Focus Ring | `rgba(245,245,247,0.40)` | Outline fokus keyboard 2px, offset 2px |
| `color.overlay` | Scrim | `rgba(0,0,0,0.60)` | Latar belakang modal |

### 1.2 Semantic Status (Muted, Tanpa Neon)

Setiap status memiliki tiga varian: **solid** (teks/ikon/border), **tint** (latar), **line** (border).

| Status | Token | Solid | Tint (bg) | Line (border) | Makna |
|---|---|---|---|---|---|
| Sage Emerald | `status.compliant` | `#7FA88B` | `rgba(127,168,139,0.12)` | `rgba(127,168,139,0.32)` | Patuh / Compliant |
| Terracotta Rose | `status.violation` | `#C4786B` | `rgba(196,120,107,0.12)` | `rgba(196,120,107,0.32)` | Pelanggaran / Violation |
| Warm Ochre | `status.ambiguous` | `#C9A25F` | `rgba(201,162,95,0.12)` | `rgba(201,162,95,0.32)` | Multi-tafsir / Peringatan |
| Institutional Cobalt | `status.ai-revised` | `#6F8FC9` | `rgba(111,143,201,0.12)` | `rgba(111,143,201,0.32)` | Telah direvisi AI |
| Slate (netral) | `status.unverified` | `#8A8F98` | `rgba(138,143,152,0.12)` | `rgba(138,143,152,0.32)` | Belum terverifikasi (UNVERIFIED_CITATION) |

**Aturan:**
- Dilarang: warna jenuh (`#00FF00`, `#FF0000`, dll.), gradien, glow, shadow berwarna.
- Kontras teks status solid di atas tint harus ≥ 4.5:1 (WCAG AA). Jika gagal, naikkan luminansi solid maksimal +8%.
- Status **tidak boleh** disampaikan hanya lewat warna: selalu sertakan ikon + label teks (aksesibilitas buta warna).

### 1.3 Redline Diff Colors (khusus modal perbandingan)

| Token | Hex / RGBA | Penggunaan |
|---|---|---|
| `diff.removed-bg` | `rgba(196,120,107,0.14)` | Latar teks dihapus |
| `diff.removed-text` | `#D9968B` | Teks dihapus (strikethrough) |
| `diff.added-bg` | `rgba(127,168,139,0.14)` | Latar teks ditambah |
| `diff.added-text` | `#9DC4A8` | Teks ditambah (underline tipis) |
| `diff.gutter` | `#131518` | Gutter nomor baris |

---

## 2. Tipografi 3-Tier

| Tier | Peran | Font Utama | Fallback | Lisensi |
|---|---|---|---|---|
| **T1 Editorial Serif** | Judul dokumen hukum, klausul resmi, headline landing page | **Newsreader** | `"Playfair Display", "Source Serif 4", Georgia, serif` | OFL |
| **T2 Geometric Sans** | Navigasi, tombol, label, tabel, form | **Inter** | `Geist, system-ui, -apple-system, "Segoe UI", sans-serif` | OFL |
| **T3 Technical Mono** | Pasal, formula denda, citation pill, angka kalkulator | **JetBrains Mono** | `Consolas, "SF Mono", monospace` | OFL |

### 2.1 Type Scale

| Token | Font | Size / Line-height | Weight | Letter-spacing | Penggunaan |
|---|---|---|---|---|---|
| `display-xl` | Newsreader | 64 / 68 | 400 | -0.02em | Headline hero |
| `display-lg` | Newsreader | 44 / 52 | 400 | -0.015em | Judul seksi landing |
| `title-doc` | Newsreader | 28 / 36 | 500 | -0.01em | Judul kontrak di editor |
| `clause-heading` | Newsreader | 20 / 28 | 600 | 0 | Judul pasal kontrak |
| `clause-body` | Newsreader | 17 / 28 | 400 | 0 | Isi klausul (ritme baca editorial) |
| `ui-h1` | Inter | 20 / 28 | 600 | -0.01em | Judul halaman aplikasi |
| `ui-h2` | Inter | 15 / 22 | 600 | 0 | Judul panel |
| `ui-body` | Inter | 14 / 22 | 400 | 0 | Teks UI standar |
| `ui-label` | Inter | 12 / 16 | 500 | 0.02em | Label form, header tabel |
| `ui-overline` | Inter | 11 / 14 | 600 | 0.08em, uppercase | Overline seksi |
| `mono-body` | JetBrains Mono | 13 / 20 | 400 | 0 | Blok formula, hasil kalkulator |
| `mono-pill` | JetBrains Mono | 12 / 16 | 500 | 0 | Teks citation pill |

**Aturan:**
- Teks klausul kontrak **selalu** `clause-body` (serif). Jangan pernah memakai sans untuk isi klausul.
- Angka tabel memakai `font-variant-numeric: tabular-nums`.
- Lebar baris klausul maksimal `72ch`.
- Dilarang memakai italic untuk teks status; italic hanya untuk istilah asing dalam teks hukum.

---

## 3. Spacing, Radius, Elevation, Motion

| Kategori | Token |
|---|---|
| **Spacing (4px base)** | `4, 8, 12, 16, 20, 24, 32, 40, 56, 80, 120` |
| **Radius** | `radius-sm 4px` (pill, input kecil) · `radius-md 8px` (tombol, input, kartu) · `radius-lg 12px` (modal, bento card) · `radius-full 999px` (hanya avatar & status dot) |
| **Border** | Standar `1px solid var(--border-hairline)`. Tidak ada border tebal. |
| **Elevation** | Dibedakan oleh **warna permukaan**, bukan shadow. Hanya modal/popover yang memakai `box-shadow: 0 12px 40px rgba(0,0,0,0.5)`. |
| **Motion** | Durasi `120ms` (hover), `200ms` (panel/modal), easing `cubic-bezier(0.2, 0, 0, 1)`. Tidak ada bounce, parallax, atau typewriter effect. Hormati `prefers-reduced-motion`. |
| **Grid aplikasi** | 12 kolom, gutter 24px, max-width konten landing 1200px |
| **Breakpoint** | `sm 640 · md 768 · lg 1024 · xl 1280 · 2xl 1536` |

### 3.1 Kode CSS Variables (Salin ke `tokens.css`)

```css
:root {
  --canvas: #0C0D0E;
  --surface: #131518;
  --elevated: #1A1D21;
  --elevated-hover: #20242A;
  --text-primary: #F5F5F7;
  --text-secondary: #A0A4AB;
  --text-tertiary: #6E727A;
  --border-hairline: rgba(255,255,255,0.08);
  --border-strong: rgba(255,255,255,0.16);
  --focus-ring: rgba(245,245,247,0.40);

  --compliant: #7FA88B;      --compliant-tint: rgba(127,168,139,0.12);   --compliant-line: rgba(127,168,139,0.32);
  --violation: #C4786B;      --violation-tint: rgba(196,120,107,0.12);   --violation-line: rgba(196,120,107,0.32);
  --ambiguous: #C9A25F;      --ambiguous-tint: rgba(201,162,95,0.12);    --ambiguous-line: rgba(201,162,95,0.32);
  --ai-revised: #6F8FC9;     --ai-revised-tint: rgba(111,143,201,0.12);  --ai-revised-line: rgba(111,143,201,0.32);
  --unverified: #8A8F98;     --unverified-tint: rgba(138,143,152,0.12);  --unverified-line: rgba(138,143,152,0.32);

  --diff-removed-bg: rgba(196,120,107,0.14);  --diff-removed-text: #D9968B;
  --diff-added-bg: rgba(127,168,139,0.14);    --diff-added-text: #9DC4A8;

  --font-serif: "Newsreader", "Playfair Display", "Source Serif 4", Georgia, serif;
  --font-sans: "Inter", "Geist", system-ui, -apple-system, "Segoe UI", sans-serif;
  --font-mono: "JetBrains Mono", Consolas, "SF Mono", monospace;
}
```

### 3.2 Struktur Figma Variables (FigCraft)

- **Collection `Primitives`**: `gray/*`, `stone/*`, `sage/*`, `terracotta/*`, `ochre/*`, `cobalt/*`.
- **Collection `Semantic`** (mode: `Dark` default, `Light` opsional): alias ke primitives, mis. `surface/canvas`, `text/primary`, `status/violation/solid`.
- **Collection `Typography`**: text styles dengan prefix `Serif/`, `Sans/`, `Mono/`.
- **Collection `Spacing & Radius`**: numeric variables.
- Seluruh komponen wajib memakai variable, **tidak ada hex hard-coded** di layer.

---

## 4. Layout Aplikasi (Workspace)

```
┌──────────────────────────────────────────────────────────────────────────┐
│ TopBar (56px) — Logo · Matter Switcher · Search (⌘K) · Notifikasi · Akun │
├───────────┬────────────────────────────────────────────┬─────────────────┤
│ Sidebar   │  Document Canvas (Tiptap Viewer/Editor)    │ Compliance      │
│ 248px     │  Kolom klausul, max 72ch, serif            │ Matrix Panel    │
│           │  Highlight status per klausul              │ 400px           │
│ - Matters │                                            │ (collapsible)   │
│ - VDR     │                                            │                 │
│ - Library │                                            │                 │
│ - Audit   │                                            │                 │
└───────────┴────────────────────────────────────────────┴─────────────────┘
```

- Sidebar: `surface`, border kanan hairline. Item aktif: latar `elevated`, teks `text-primary`, indikator kiri 2px `text-primary`.
- Document Canvas: `canvas`. Halaman dokumen berupa kolom tengah tanpa kotak kertas putih.
- Compliance Matrix Panel: `surface`, border kiri hairline; dapat diubah lebarnya (320–560px) dan dilipat.

---

## 5. Komponen Inti

### 5.1 Tombol

| Varian | Latar | Teks | Border | Hover |
|---|---|---|---|---|
| Primary | `#F5F5F7` | `#0C0D0E` | none | `#FFFFFF` |
| Secondary | transparan | `#F5F5F7` | hairline-strong | latar `elevated` |
| Ghost | transparan | `#A0A4AB` | none | teks `#F5F5F7`, latar `rgba(255,255,255,0.04)` |
| Destructive | transparan | `#C4786B` | `violation-line` | latar `violation-tint` |

Tinggi: 32 (sm), 40 (md), 48 (lg). Padding horizontal 16px. Font `ui-body` weight 500. Radius 8px. Focus: ring 2px `focus-ring`.

### 5.2 Input & Form
Latar `surface`, border hairline, radius 8px, tinggi 40px. Fokus: border `border-strong` + ring. Error: border `violation-line`, teks bantu `violation`. Label di atas input, `ui-label`.

### 5.3 Status Badge

Bentuk: tinggi 22px, padding 0 8px, radius 4px, font `ui-label`, ikon 12px di kiri, latar `*-tint`, border `*-line`, teks `*-solid`.

| Status | Label | Ikon (stroke 1.5px, Lucide) |
|---|---|---|
| Compliant | `Patuh` | `check` |
| Violation | `Pelanggaran` | `x` |
| Ambiguous | `Multi-tafsir` | `alert-triangle` |
| AI Revised | `Direvisi AI` | `git-compare` |
| Unverified | `Belum Terverifikasi` | `help-circle` |

### 5.4 Compliance Matrix Row

Kolom: **No. Klausul** (mono) · **Ringkasan Klausul** (sans, 2 baris, ellipsis) · **Status** (badge) · **Dasar Hukum** (1–3 citation pill) · **Aksi** (ikon `git-compare` untuk buka Redline).
Tinggi baris 56px, divider hairline, hover `elevated-hover`. Klik baris → scroll sinkron ke klausul pada canvas (lihat §7).

---

## 6. Grounding Citation Pill (Komponen Kritis)

### 6.1 Anatomi

```
┌───────────────────────────────────┐
│ ▍[ POJK 10/2022 §29(2) ]  ↗       │
└───────────────────────────────────┘
  │         │                │
  │         │                └─ ikon tautan 10px (muncul saat hover)
  │         └─ teks mono-pill, tanpa kurung siku tampil (kurung = konvensi teks)
  └─ status dot 6px (warna sesuai status verifikasi)
```

### 6.2 Spesifikasi Visual

| Properti | Nilai |
|---|---|
| Tinggi | 24px |
| Padding | 0 8px 0 6px |
| Radius | 4px |
| Font | JetBrains Mono 12/16, weight 500 |
| Latar default | `rgba(255,255,255,0.04)` |
| Border | 1px hairline |
| Teks | `#F5F5F7` |
| Dot | 6px circle, kiri teks, gap 6px |

### 6.3 Varian Status Verifikasi

| Varian | Dot | Border | Latar | Tooltip |
|---|---|---|---|---|
| `verified` | `compliant` | hairline | netral | "Terverifikasi pada korpus regulasi (Qdrant)" |
| `verified-amended` | `ambiguous` | `ambiguous-line` | `ambiguous-tint` | "Pasal telah diubah. Versi berlaku per {tanggal}" |
| `revoked` | `violation` | `violation-line` | `violation-tint`, teks coret | "Peraturan dicabut oleh {peraturan pengganti}" |
| `unverified` | `unverified` | dashed `unverified-line` | `unverified-tint` | "[UNVERIFIED_CITATION] Pasal tidak ditemukan pada korpus" |

### 6.4 Interaksi

| Aksi | Perilaku |
|---|---|
| Hover (≥150ms) | Popover `elevated` 360px: **Judul peraturan lengkap**, **Bunyi pasal** (serif, maks 6 baris), **Tanggal berlaku**, **Status**, **Sumber** (JDIH/BPK/OJK), tombol "Buka di Panel Sumber". |
| Klik | Membuka **Source Drawer** (sisi kanan, 480px) berisi teks peraturan sumber dengan pasal tersorot (latar `ai-revised-tint`). |
| Klik klausul di canvas | Pill terkait di Compliance Matrix berkedip (outline 1px `border-strong`, 600ms). |
| Keyboard | `Tab` fokus pill · `Enter` buka drawer · `Space` toggle popover · `Esc` tutup. |
| Salin | `⌘C` pada pill terfokus menyalin format sitasi baku, mis. `Pasal 29 ayat (2) POJK Nomor 10/POJK.05/2022`. |

### 6.5 Format Penulisan Pill

| Jenis Regulasi | Pola | Contoh |
|---|---|---|
| UU | `UU {nama singkat} §{pasal}({ayat})` | `UU PDP §56` · `UU P2SK §{n}` |
| POJK | `POJK {no}/{tahun} §{pasal}({ayat})` | `POJK 10/2022 §29(2)` |
| PBI/PADG | `PBI {no}/{tahun} §…` | `PBI 23/2021 §…` |
| PP/Perpres | `PP {no}/{tahun} §…` | `PP 71/2019 §…` |
| PMK | `PMK {no}/{tahun} §…` | `PMK 169/2015 §…` |
| KPPU | `Perkom {no}/{tahun} §…` | `Perkom 3/2023 §…` |

Pill panjang dipotong tengah dengan ellipsis; nilai penuh tersedia lewat tooltip dan `aria-label`.

### 6.6 Props Komponen (React)

```ts
type CitationStatus = 'verified' | 'verified-amended' | 'revoked' | 'unverified';

interface CitationPillProps {
  regulationType: 'UU' | 'PP' | 'POJK' | 'PBI' | 'PADG' | 'PMK' | 'PERKOM' | 'PERPRES';
  shortLabel: string;            // "POJK 10/2022 §29(2)"
  fullTitle: string;             // judul resmi lengkap
  articleText?: string;          // bunyi pasal (dari Qdrant payload)
  qdrantPointId?: string;        // null jika unverified
  status: CitationStatus;
  effectiveDate?: string;        // ISO 8601
  sourceUrl?: string;            // JDIH / situs otoritas
  onOpenSource: (id: string) => void;
}
```

---

## 7. Interactive Bi-Directional Citation Mapping

- **Klausul → Dasar Hukum:** klik klausul di canvas → Compliance Matrix menggulir ke baris terkait dan menyorot pill.
- **Pasal → Klausul:** klik pill di Matrix → canvas menggulir ke klausul terkait dan menerapkan highlight `ai-revised-tint` 1.2 detik.
- **Garis penghubung (opsional, toggle):** garis vertikal tipis 1px `border-strong` antara klausul dan baris Matrix; tanpa animasi gerak.
- Anchor klausul memakai ID stabil `clause-{nomor}` agar deep-link dapat dibagikan: `/matter/{id}#clause-12.3`.

---

## 8. Git-Style Legal Redline Diff Modal

### 8.1 Struktur Modal

- Lebar: `min(1280px, 92vw)`, tinggi `86vh`, radius 12px, latar `elevated`, border hairline, scrim `rgba(0,0,0,0.60)`.
- **Header (64px):** Judul "Telaah Redline — Pasal {nomor}", badge status, citation pill terkait, tombol tutup.
- **Toolbar (48px):** toggle *Side-by-side / Inline*, filter *Hanya perubahan*, navigasi *Perubahan sebelumnya/berikutnya* (`↑`/`↓`), penghitung "3 dari 7 perubahan".
- **Body:** dua kolom sama lebar (1fr 1fr), gutter 1px hairline, scroll tersinkronisasi.
- **Footer (72px):** kiri = alasan hukum singkat; kanan = aksi **Tolak Revisi**, **Edit Manual**, **Terima Revisi** (Primary).

### 8.2 Kolom Kiri: "Klausul Asli"

- Header kolom: overline `KLAUSUL ASLI` + badge `Pelanggaran`.
- Teks dihapus: warna `diff.removed-text`, latar `diff.removed-bg`, `text-decoration: line-through`, `text-decoration-color: rgba(217,150,139,0.7)`.
- Gutter kiri: nomor baris mono 12px, `text-tertiary`; baris berubah diberi bar kiri 2px `violation`.

### 8.3 Kolom Kanan: "Klausul Revisi Sesuai Regulasi"

- Header kolom: overline `REVISI SESUAI REGULASI` + badge `Direvisi AI`.
- Teks ditambah: `diff.added-text`, latar `diff.added-bg`, `text-decoration: underline` 1px offset 3px (warna sama 50% opasitas).
- Bar kiri baris berubah 2px `compliant`.

### 8.4 Anotasi Alasan (Inline Rationale)

Di bawah blok yang berubah, muncul baris anotasi (serif italic 14px, `text-secondary`) berisi alasan perubahan yang diikuti citation pill, misalnya: *"Batas manfaat ekonomi melampaui ketentuan; sesuaikan."* + `[POJK 10/2022 §…]`. Anotasi dapat dilipat per perubahan.

### 8.5 Aksi Per Perubahan (Hunk-level)

Tiap *hunk* memiliki kontrol kecil di margin kanan: **Terima** (`check`) · **Tolak** (`x`) · **Edit** (`pencil`). Keputusan tersimpan di audit log (pengguna, waktu, versi model, versi korpus regulasi).

### 8.6 State

| State | Perilaku |
|---|---|
| Loading | Skeleton dua kolom, tanpa spinner dekoratif. Teks "Menyusun redline…". |
| Tanpa perubahan | "Klausul sudah sesuai. Tidak ada revisi yang diperlukan." + badge `Patuh`. |
| Citation unverified | Banner ochre di atas footer: "Revisi ini memuat rujukan yang belum terverifikasi. Tombol Terima dinonaktifkan sampai ditinjau." |
| Konflik multi-tafsir | Banner ochre + tombol "Minta Penilaian Penasihat Hukum". |

### 8.7 Pintasan Keyboard

`J/K` perubahan berikutnya/sebelumnya · `A` terima hunk · `R` tolak hunk · `E` edit · `Shift+A` terima semua · `Esc` tutup.

---

## 9. State UI Khusus Sistem

| State | Tampilan |
|---|---|
| **Upload dropzone** | Kotak border dashed hairline-strong, ikon `file-up`, teks "Tarik berkas ke sini atau pilih dari komputer", subteks "PDF, DOCX · maks 100 MB per berkas". |
| **Progres agen** | Stepper vertikal 4 tahap (Parser → Auditor → Evaluator → Drafter). Tahap aktif: dot `ai-revised`; selesai: `check` `compliant`; gagal: `x` `violation`. Tanpa animasi pulsa berlebihan. |
| **Empty state** | Ikon garis 32px, judul `ui-h2`, satu kalimat bantuan, satu CTA. |
| **Error PDF terenkripsi** | Modal kecil: "Berkas dilindungi kata sandi" + input kata sandi + tombol "Buka Berkas". |
| **OCR kualitas rendah** | Banner ochre: "Kualitas pindaian rendah (kepercayaan OCR {n}%). Hasil analisis dapat kurang akurat." + aksi "Unggah Ulang" / "Lanjutkan dengan Peringatan". |
| **MIME tidak didukung** | Toast `violation`: "Format berkas tidak didukung. Gunakan PDF atau DOCX." |
| **Loop breaker** | Kartu ochre di klausul: "Klausul memuat tafsir ganda. Memerlukan penilaian Penasihat Hukum." |

---

## 10. Aksesibilitas

- WCAG 2.2 AA minimum. Target ukuran sentuh 40px.
- Semua status memiliki ikon + label teks.
- Focus ring terlihat pada semua elemen interaktif.
- Citation pill: `role="button"`, `aria-label="Rujukan hukum: Pasal 29 ayat 2 POJK Nomor 10 Tahun 2022, status terverifikasi"`.
- Modal: focus trap, `aria-modal="true"`, kembalikan fokus ke pemicu saat ditutup.
- Diff: setiap hunk diberi `aria-label` "Dihapus" / "Ditambahkan" untuk pembaca layar.
- Dukungan `prefers-reduced-motion` dan `prefers-contrast`.

---

## 11. Konvensi Penamaan Komponen (Figma → Kode)

| Figma | Kode |
|---|---|
| `Button/Primary/md` | `<Button variant="primary" size="md" />` |
| `Badge/Status/Compliant` | `<StatusBadge status="compliant" />` |
| `Citation/Pill/Verified` | `<CitationPill status="verified" />` |
| `Matrix/Row/Default` | `<ComplianceMatrixRow />` |
| `Modal/Redline` | `<RedlineModal />` |
| `Editor/Clause` | `<ClauseNode />` (Tiptap custom node) |

Tiptap custom nodes/marks: `clause` (node, atribut `id`, `number`, `status`), `citation` (mark, atribut `pillId`), `redlineInsert` / `redlineDelete` (marks).

---

## 12. Larangan (Anti-Pattern Checklist)

- ❌ Gradien, glow, blur dekoratif, partikel, aurora.
- ❌ Ikon robot, bintang AI, "sparkles", avatar chatbot kartun.
- ❌ Warna neon atau jenuh.
- ❌ Emoji dalam UI produk.
- ❌ Animasi mengetik (typewriter) pada output hukum.
- ❌ Teks AI tanpa citation atau tanpa status verifikasi.
- ❌ Disclaimer disembunyikan. Catatan "Bukan nasihat hukum; wajib ditinjau Penasihat Hukum berlisensi" tampil permanen di footer panel hasil.
