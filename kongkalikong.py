import matplotlib.pyplot as plt
from matplotlib_venn import venn3

# Set label lingkaran
labels = ('Korupsi', 'Kolusi', 'Nepotisme')

# Jumlah anggota masing-masing dan irisannya (harus 7 elemen)
# Format: (A, B, AB, C, AC, BC, ABC)
# Diatur agar semua bersinggungan
venn_counts = (1, 1, 1, 1, 1, 1, 1)

# Buat diagram Venn
venn = venn3(subsets=venn_counts, set_labels=labels)

# Tambahkan contoh-contoh di setiap irisan
venn.get_label_by_id('100').set_text('Suap pejabat\n(Korupsi)')
venn.get_label_by_id('010').set_text('Kongkalikong tender\n(Kolusi)')
venn.get_label_by_id('001').set_text('Anak jadi pejabat\n(Nepotisme)')

venn.get_label_by_id('110').set_text('Suap antar rekan bisnis\n(Korupsi + Kolusi)')
venn.get_label_by_id('101').set_text('Anak koruptor naik jabatan\n(Korupsi + Nepotisme)')
venn.get_label_by_id('011').set_text('Pejabat bantu saudara menang proyek\n(Kolusi + Nepotisme)')
venn.get_label_by_id('111').set_text('Keluarga pejabat atur proyek & ambil untung\n(KKN lengkap)')

# Judul
plt.title("Diagram Venn: Korupsi, Kolusi, Nepotisme")

# Tampilkan
plt.show()
