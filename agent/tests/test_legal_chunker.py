import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.tools.legal_chunker import chunk_indonesian_regulation

RAW_POJK_SAMPLE = """
SALINAN
PERATURAN OTORITAS JASA KEUANGAN
REPUBLIK INDONESIA
NOMOR 22 TAHUN 2023
TENTANG
PELINDUNGAN KONSUMEN DAN MASYARAKAT
DI SEKTOR JASA KEUANGAN
DENGAN RAHMAT TUHAN YANG MAHA ESA
DEWAN KOMISIONER OTORITAS JASA KEUANGAN,
Menimbang : a. bahwa dengan berlakunya Undang-Undang Nomor 4
Tahun 2023 tentang Pengembangan dan Penguatan Sektor
Keuangan telah memperkuat kewenangan Otoritas Jasa
Keuangan dalam melakukan pengaturan dan pengawasan
pelindungan konsumen dan masyarakat di sektor jasa
keuangan untuk meningkatkan sistem pelindungan
konsumen yang andal, meningkatkan pemberdayaan
konsumen dan masyarakat, serta menumbuhkan
kesadaran pelaku usaha jasa keuangan;
b. bahwa terdapat perkembangan aspek pelindungan
konsumen dan masyarakat di sektor jasa keuangan yang
disebabkan oleh penambahan prinsip pelindungan
konsumen dan masyarakat, perluasan pelaku usaha jasa
keuangan, dan digitalisasi produk dan/atau layanan di
sektor jasa keuangan, dan perkembangan industri jasa
keuangan yang makin kompleks dan dinamis, sehingga
perlu dilakukan penguatan pengaturan mengenai
pelindungan konsumen dan masyarakat di sektor jasa
keuangan;
c. bahwa Peraturan Otoritas Jasa Keuangan Nomor
6/POJK.07/2022 tentang Perlindungan Konsumen dan
Masyarakat di Sektor Jasa Keuangan perlu diganti untuk
menyesuaikan dengan perkembangan pelindungan
konsumen dan masyarakat;
d. bahwa berdasarkan pertimbangan sebagaimana dimaksud
dalam huruf a, huruf b, dan huruf c, perlu menetapkan
Peraturan Otoritas Jasa Keuangan tentang Pelindungan
Konsumen dan Masyarakat di Sektor Jasa Keuangan;
Mengingat : 1. Undang-Undang Nomor 21 Tahun 2011 tentang Otoritas
Jasa Keuangan (Lembaran Negara Republik Indonesia
Tahun 2011 Nomor 111, Tambahan Lembaran Negara
Republik Indonesia Nomor 5253) sebagaimana telah
diubah dengan Undang-Undang Nomor 4 Tahun 2023
tentang Pengembangan dan Penguatan Sektor Keuangan
(Lembaran Negara Republik Indonesia Tahun 2023 Nomor
4, Tambahan Lembaran Negara Republik Indonesia
Nomor 6845);
- 2 -
2. Undang-Undang Nomor 4 Tahun 2023 tentang
Pengembangan dan Penguatan Sektor Keuangan
(Lembaran Negara Republik Indonesia Tahun 2023 Nomor
4, Tambahan Lembaran Negara Republik Indonesia
Nomor 6845);
MEMUTUSKAN:
Menetapkan : PERATURAN OTORITAS JASA KEUANGAN TENTANG
PELINDUNGAN KONSUMEN DAN MASYARAKAT DI SEKTOR
JASA KEUANGAN.
BAB I
KETENTUAN UMUM
Pasal 1
Dalam Peraturan Otoritas Jasa Keuangan ini yang dimaksud
dengan:
1. Lembaga Jasa Keuangan yang selanjutnya disingkat LJK
adalah lembaga yang melaksanakan kegiatan di sektor
perbankan, pasar modal, perasuransian, dana pensiun,
modal ventura, lembaga keuangan mikro, lembaga
pembiayaan, dan lembaga jasa keuangan lainnya.
2. Pelaku Usaha Jasa Keuangan yang selanjutnya disingkat
PUJK adalah:
a. LJK dan/atau pihak yang melakukan kegiatan usaha
penghimpunan dana, penyaluran dana, dan/atau
pengelolaan dana di sektor jasa keuangan; dan
b. pelaku usaha jasa keuangan lainnya,
baik yang melaksanakan kegiatan usaha secara
konvensional maupun berdasarkan prinsip syariah sesuai
dengan ketentuan peraturan perundang-undangan di
sektor jasa keuangan.
3. Konsumen adalah setiap orang yang memiliki dan/atau
memanfaatkan produk dan/atau layanan yang disediakan
oleh PUJK.
4. Pelindungan Konsumen adalah segala upaya yang
menjamin adanya kepastian hukum untuk memberikan
pelindungan kepada Konsumen.
5. Produk Asuransi Yang Dikaitkan Dengan Investasi yang
selanjutnya disebut PAYDI adalah produk asuransi yang
paling sedikit memberikan perlindungan terhadap risiko
kematian dan memberikan manfaat yang mengacu pada
hasil investasi dari kumpulan dana yang khusus dibentuk
untuk produk asuransi baik yang dinyatakan dalam
bentuk unit maupun bukan unit.
6. Sistem Layanan Konsumen dan Masyarakat Terintegrasi
di Sektor Jasa Keuangan adalah mekanisme dan
perangkat yang dikelola oleh Otoritas Jasa Keuangan
untuk melaksanakan layanan Konsumen dan/atau
masyarakat di sektor jasa keuangan.
7. Pengaduan Berindikasi Sengketa adalah ungkapan
ketidakpuasan Konsumen yang disebabkan oleh adanya
kerugian dan/atau potensi kerugian materi, wajar dan
secara langsung pada Konsumen karena PUJK tidak
memenuhi perjanjian dan/atau dokumen pemanfaatan
produk dan/atau layanan yang telah disepakati.
8. Pengaduan Berindikasi Pelanggaran adalah penyampaian
informasi oleh Konsumen dan/atau masyarakat atas
indikasi pelanggaran ketentuan peraturan perundangundangan di sektor jasa keuangan yang dilakukan oleh
PUJK.
- 3 -
9. Pengaduan adalah Pengaduan Berindikasi Sengketa dan
Pengaduan Berindikasi Pelanggaran.
10. Layanan Pengaduan adalah layanan yang disediakan oleh
PUJK untuk mengupayakan penyelesaian Pengaduan di
sektor jasa keuangan.
11. Tanggapan Pengaduan adalah penjelasan permasalahan
atau penawaran penyelesaian akhir dari PUJK kepada
Konsumen.
12. Sengketa adalah perselisihan antara Konsumen dengan
PUJK yang telah melalui proses penyelesaian Pengaduan
oleh PUJK.
13. Lembaga Alternatif Penyelesaian Sengketa Sektor Jasa
Keuangan yang selanjutnya disebut LAPS Sektor Jasa
Keuangan adalah lembaga yang melakukan penyelesaian
Sengketa antara Konsumen dan PUJK di luar pengadilan.
14. Direksi bagi PUJK atau organ yang setara dengan Direksi
pada badan hukum yang selanjutnya disebut Direksi
adalah organ yang melakukan fungsi pengurusan PUJK
untuk kepentingan PUJK sesuai dengan maksud dan
tujuan masing-masing PUJK serta mewakili PUJK di
dalam maupun di luar pengadilan sesuai dengan
ketentuan anggaran dasar, atau pemimpin kantor cabang
dan pejabat satu tingkat di bawah pemimpin kantor
cabang bagi PUJK yang berstatus sebagai kantor cabang
dari PUJK yang berkedudukan di luar negeri.
15. Dewan Komisaris bagi PUJK atau organ yang setara
dengan Dewan Komisaris pada badan hukum yang
selanjutnya disebut Dewan Komisaris adalah organ pada
masing-masing PUJK yang berperan untuk melakukan
fungsi pengawasan secara umum dan/atau khusus sesuai
dengan anggaran dasar serta memberi nasihat kepada
Direksi, atau pihak yang ditunjuk untuk melaksanakan
fungsi pengawasan bagi PUJK yang berstatus sebagai
kantor cabang dari PUJK yang berkedudukan di luar
negeri.
16. Pegawai adalah semua tenaga kerja yang memperoleh
upah dan/atau gaji dari PUJK.
17. Literasi Keuangan adalah pengetahuan, keterampilan, dan
keyakinan yang memengaruhi sikap dan perilaku untuk
meningkatkan kualitas pengambilan keputusan dan
pengelolaan keuangan untuk mencapai kesejahteraan
keuangan masyarakat.
18. Inklusi Keuangan adalah ketersediaan akses pemanfaatan
atas produk dan/atau layanan PUJK yang terjangkau,
berkualitas, dan berkelanjutan sesuai dengan kebutuhan
dan kemampuan masyarakat untuk meningkatkan
kesejahteraan keuangan masyarakat.
19. Informasi adalah keterangan dan/atau pernyataan baik
data, fakta, maupun penjelasannya yang disajikan dalam
berbagai kemasan dan format melalui media komunikasi
elektronik maupun non elektronik.
20. Pengawasan Perilaku PUJK (Market Conduct) adalah
pengawasan terhadap perilaku PUJK dalam mendesain,
menyediakan dan menyampaikan informasi, menawarkan,
menyusun perjanjian, memberikan pelayanan atas
penggunaan produk dan/atau layanan, serta penanganan
Pengaduan dan penyelesaian Sengketa dalam upaya
mewujudkan Pelindungan Konsumen.
21. Pemeriksaan Tematik adalah Pengawasan Perilaku PUJK
(Market Conduct) dengan melakukan serangkaian kegiatan
menghimpun dan mengolah data, keterangan, dan/atau
- 4 -
bukti, dan analisis atas produk dan/atau layanan jasa
keuangan yang memiliki potensi menimbulkan kerugian
Konsumen berdasarkan tema yang telah ditetapkan.
22. Pemeriksaan Khusus adalah Pengawasan Perilaku PUJK
(Market Conduct) dengan melakukan serangkaian kegiatan
menghimpun dan mengolah data, keterangan, dan/atau
bukti untuk membuktikan dugaan adanya perilaku PUJK
yang melanggar ketentuan peraturan perundangundangan di sektor jasa keuangan dan/atau
menimbulkan kerugian Konsumen.
23. Perintah Tertulis adalah perintah secara tertulis oleh
Otoritas Jasa Keuangan untuk melaksanakan atau tidak
melaksanakan kegiatan tertentu, guna memenuhi
ketentuan peraturan perundang-undangan di sektor jasa
keuangan dan/atau mencegah dan mengurangi kerugian
Konsumen, masyarakat, PUJK, dan sektor jasa keuangan.
24. Lembaga Jasa Keuangan Lainnya adalah pergadaian,
lembaga penjaminan, lembaga pembiayaan ekspor
Indonesia, perusahaan pembiayaan sekunder perumahan,
Penyelenggara Layanan Pendanaan Bersama Berbasis
Teknologi Informasi, dan lembaga yang menyelenggarakan
pengelolaan dana masyarakat yang bersifat wajib, meliputi
penyelenggara program jaminan sosial, pensiun, dan
kesejahteraan, sebagaimana dimaksud dalam peraturan
perundang-undangan mengenai pergadaian, penjaminan,
lembaga pembiayaan ekspor Indonesia, perusahaan
pembiayaan sekunder perumahan, dan pengelolaan dana
masyarakat yang bersifat wajib, serta lembaga jasa
keuangan lain yang dinyatakan diawasi oleh Otoritas Jasa
Keuangan berdasarkan ketentuan peraturan perundangundangan.
Pasal 2
PUJK sebagaimana dimaksud dalam Pasal 1 angka 2 terdiri
atas:
a. LJK yang meliputi:
1. Bank Umum;
2. Bank Perekonomian Rakyat;
3. Perusahaan Efek;
4. Dana Pensiun;
5. Perusahaan Asuransi;
6. Perusahaan Reasuransi;
7. Perusahaan Pembiayaan;
8. Perusahaan Pembiayaan Infrastruktur;
9. Perusahaan Modal Ventura;
10. Lembaga Keuangan Mikro; dan
11. Lembaga Jasa Keuangan Lainnya;
b. pihak yang melakukan kegiatan usaha penghimpunan
dana, penyaluran dana, pengelolaan dana di sektor jasa
keuangan, yang diberikan izin dan dinyatakan diawasi oleh
Otoritas Jasa Keuangan berdasarkan peraturan
perundang-undangan; dan
c. pelaku usaha jasa keuangan lainnya meliputi pihak yang
menyelenggarakan inovasi teknologi sektor keuangan di
sektor jasa keuangan yang diberikan izin dan dinyatakan
diawasi oleh Otoritas Jasa Keuangan berdasarkan
peraturan perundang-undangan,
baik yang melaksanakan kegiatan usahanya secara
konvensional maupun secara syariah.
- 5 -
BAB II
KETENTUAN PELINDUNGAN KONSUMEN DAN MASYARAKAT
DI SEKTOR JASA KEUANGAN
Bagian Kesatu
Prinsip Pelindungan Konsumen
Pasal 3
(1) PUJK dalam menyelenggarakan kegiatan usaha wajib
menerapkan prinsip Pelindungan Konsumen.
(2) Pelindungan Konsumen di sektor jasa keuangan
menerapkan prinsip:
a. edukasi yang memadai;
b. keterbukaan dan transparansi informasi produk
dan/atau layanan;
c. perlakuan yang adil dan perilaku bisnis yang
bertanggung jawab;
d. pelindungan aset, privasi, dan data Konsumen;
e. penanganan Pengaduan dan penyelesaian Sengketa
yang efektif dan efisien;
f. penegakan kepatuhan; dan
g. persaingan yang sehat.
(3) PUJK yang melanggar ketentuan sebagaimana dimaksud
pada ayat (1) dikenai sanksi administratif berupa:
a. peringatan tertulis;
b. pembatasan produk dan/atau layanan dan/atau
kegiatan usaha untuk sebagian atau seluruhnya;
c. pembekuan produk dan/atau layanan dan/atau
kegiatan usaha untuk sebagian atau seluruhnya;
d. pemberhentian pengurus;
e. denda administratif;
f. pencabutan izin produk dan/atau layanan; dan/atau
g. pencabutan izin usaha.
(4) Sanksi sebagaimana dimaksud pada ayat (3) huruf b
sampai dengan huruf g dikenakan dengan atau tanpa
didahului pengenaan sanksi peringatan tertulis
sebagaimana dimaksud pada ayat (3) huruf a.
(5) Sanksi denda sebagaimana dimaksud pada ayat
(3) huruf e dikenakan paling banyak Rp15.000.000.000,00
(lima belas miliar rupiah).

"""


def main():
    reg_name = "POJK No. 10/POJK.05/2022"
    chunks = chunk_indonesian_regulation(RAW_POJK_SAMPLE, reg_name)
    total_chunk = 0
    print(f"=== HASIL CHUNKING STRUKTURAL HUKUM INDONESIA ===")
    print(f"Total Chunks Dihasilkan: {len(chunks)} Pasal\n")

    for c in chunks:
        print(f"📌 CHUNK ID: {c.chunk_id}")
        print(f"   Induk BAB  : {c.bab}")
        print(f"   Pasal      : {c.pasal}")
        print(f"   Header     : {c.header_context}")
        print(f"   Teks Embed :\n   {c.full_embed_text[:120]}...\n")
        total_chunk += 1
    print(f"Total Chunk : {total_chunk}")


if __name__ == "__main__":
    main()
