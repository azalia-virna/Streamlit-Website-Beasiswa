import streamlit as st
import pandas as pd

def calculate_ranking(data):
    # Bobot untuk setiap kriteria
    bobot = {
        'SEMESTER': 0.1,
        'IPS': 0.2,
        'UKT': 0.2,
        'AKREDITASI PRODI': 0.2,
        'USIA': 0.1,
        'PRESTASI': 0.2
    }

    # Normalisasi data untuk kriteria yang perlu dinormalisasi
    data['SEMESTER'] =  data['SEMESTER'].min() / data['SEMESTER'] # Semakin kecil SEMESTER, semakin besar bobot
    data['IPS'] = data['IPS'] / data['IPS'].max()
    data['UKT'] = data['UKT'] / data['UKT'].max()
    data['AKREDITASI PRODI'] = data['AKREDITASI PRODI'] / data['AKREDITASI PRODI'].max()
    data['USIA'] = data['USIA'].min() / data['USIA'] # Semakin kecil USIA, semakin besar bobot
    data['PRESTASI'] = data['PRESTASI'] / data['PRESTASI'].max()

    # Perhitungan PREFERENSI
    data['PREFERENSI'] = (
        bobot['SEMESTER'] * data['SEMESTER'] +
        bobot['IPS'] * data['IPS'] +
        bobot['UKT'] * data['UKT'] +
        bobot['AKREDITASI PRODI'] * data['AKREDITASI PRODI'] +
        bobot['USIA'] * data['USIA'] +
        bobot['PRESTASI'] * data['PRESTASI']
    )

    # Ranking
    data = data.sort_values(by='PREFERENSI', ascending=False).reset_index(drop=True)
    return data[['NAMA ', 'PREFERENSI']]

def main():
    st.title("Seleksi Beasiswa Pemerintah Kabupaten Bojonegoro")
    st.subheader("Halaman Pengolahan Data")
    st.write("Hasil preferensi nilai dapat dilihat pada tabel berikut ini")
    
    uploaded_file = st.file_uploader("Unggah file Excel", type=["xlsx"])  # Tambahkan tombol unggah file Excel

    if uploaded_file is not None:
        raw_data = pd.read_excel(uploaded_file)
        data = raw_data.loc[:, ~raw_data.columns.str.contains('^Unnamed')]
        if 'NO ' in data.columns:
            data = data.drop(columns=['NO '])
        data.drop(index=range(105, 108), inplace=True)
        data.reset_index(drop=True, inplace=True)
        ranked_data = calculate_ranking(data)
        st.write(ranked_data)

if __name__ == "__main__":
    main()
