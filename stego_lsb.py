from PIL import Image

# Fungsi 1: Mengubah teks menjadi bilangan biner (0 dan 1)
def text_to_bin(text):
    return ''.join(format(ord(char), '08b') for char in text)

# Fungsi 2: Mengubah bilangan biner kembali menjadi teks
def bin_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    # Mengabaikan error jika ada sisa biner yang bukan karakter valid
    hasil = ""
    for char in chars:
        try:
            hasil += chr(int(char, 2))
        except ValueError:
            break
    return hasil

# Fungsi 3: Menyisipkan pesan ke dalam gambar (Proses Encode LSB)
def hide_data_lsb(image_path, secret_data, output_path):
    # Menambahkan pembatas (delimiter) '#####' agar sistem tahu kapan pesan berakhir
    secret_data += "#####"
    binary_data = text_to_bin(secret_data)
    data_index = 0
    data_len = len(binary_data)
    
    # Buka gambar dan pastikan formatnya RGB
    image = Image.open(image_path).convert('RGB')
    pixels = image.load()
    width, height = image.size
    
    # Cek apakah kapasitas gambar cukup untuk menampung pesan
    if data_len > width * height * 3:
        return "Error: Gambar terlalu kecil untuk menampung data ini."
    
    # Mulai menyisipkan data ke bit terakhir (LSB) dari warna Red, Green, Blue
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            
            if data_index < data_len:
                # Modifikasi bit terakhir Red
                r = (r & ~1) | int(binary_data[data_index])
                data_index += 1
            if data_index < data_len:
                # Modifikasi bit terakhir Green
                g = (g & ~1) | int(binary_data[data_index])
                data_index += 1
            if data_index < data_len:
                # Modifikasi bit terakhir Blue
                b = (b & ~1) | int(binary_data[data_index])
                data_index += 1
                
            # Simpan pixel yang sudah dimodifikasi
            pixels[x, y] = (r, g, b)
            
            # Jika semua data sudah tersisip, hentikan proses
            if data_index >= data_len:
                break
        if data_index >= data_len:
            break
            
    # WAJIB disimpan dalam format PNG agar nilai bit tidak berubah (lossless)
    image.save(output_path, "PNG")
    return f"Sukses! Data berhasil disembunyikan dan disimpan di {output_path}"

# Fungsi 4: Mengekstrak pesan dari gambar (Proses Decode LSB)
def extract_data_lsb(image_path):
    image = Image.open(image_path).convert('RGB')
    pixels = image.load()
    width, height = image.size
    
    binary_data = ""
    
    # Ekstrak bit terakhir dari setiap pixel
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)
            
    # Ubah kumpulan biner menjadi teks
    text = bin_to_text(binary_data)
    
    # Cari letak pembatas '#####' untuk memotong pesan
    if "#####" in text:
        return text.split("#####")[0]
    else:
        return "Gagal: Tidak ada pesan rahasia yang ditemukan pada gambar ini."

# --- BLOK PENGUJIAN KODE ---
if __name__ == "__main__":
    # Siapkan sebuah gambar sembarang (misal: pas_foto.png) di folder yang sama
    # Pastikan Anda memiliki gambar dengan nama tersebut sebelum menjalankan tes ini
    gambar_asli = "pas_foto.png" 
    gambar_hasil = "pas_foto_stego.png"
    
    pesan_rahasia = "Ini adalah hasil enkripsi AES: XyZ123!@#"
    
    print("=== TEST STEGANOGRAFI LSB ===")
    try:
        # Test Penyisipan
        print("Menyisipkan data...")
        hasil_hide = hide_data_lsb(gambar_asli, pesan_rahasia, gambar_hasil)
        print(hasil_hide)
        
        # Test Ekstraksi
        print("Mengekstrak data...")
        hasil_extract = extract_data_lsb(gambar_hasil)
        print(f"Pesan yang ditemukan: {hasil_extract}")
    except FileNotFoundError:
        print(f"Peringatan: Silakan siapkan gambar bernama '{gambar_asli}' terlebih dahulu di folder ini untuk mengetes kodenya.")