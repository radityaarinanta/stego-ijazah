from PIL import Image

def text_to_bin(text):
    return ''.join(format(ord(char), '08b') for char in text)

def bin_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    hasil = ""
    for char in chars:
        try:
            hasil += chr(int(char, 2))
        except ValueError:
            break
    return hasil

def hide_data_lsb(image_path, secret_data, output_path):
    secret_data += "#####"
    binary_data = text_to_bin(secret_data)
    data_index = 0
    data_len = len(binary_data)
    
    image = Image.open(image_path).convert('RGB')
    pixels = image.load()
    width, height = image.size
    
    if data_len > width * height * 3:
        return "Error: Gambar terlalu kecil untuk menampung data ini."
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            
            if data_index < data_len:
                r = (r & ~1) | int(binary_data[data_index])
                data_index += 1
            if data_index < data_len:
                g = (g & ~1) | int(binary_data[data_index])
                data_index += 1
            if data_index < data_len:
                b = (b & ~1) | int(binary_data[data_index])
                data_index += 1
                
            pixels[x, y] = (r, g, b)
            
            if data_index >= data_len:
                break
        if data_index >= data_len:
            break
            
    image.save(output_path, "PNG")
    return f"Sukses! Data berhasil disembunyikan dan disimpan di {output_path}"

def extract_data_lsb(image_path):
    image = Image.open(image_path).convert('RGB')
    pixels = image.load()
    width, height = image.size
    
    binary_data = ""
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)
            
    text = bin_to_text(binary_data)
    
    if "#####" in text:
        return text.split("#####")[0]
    else:
        return "Gagal: Tidak ada pesan rahasia yang ditemukan pada gambar ini."

if __name__ == "__main__":
    gambar_asli = "pas_foto.png" 
    gambar_hasil = "pas_foto_stego.png"
    
    pesan_rahasia = "Ini adalah hasil enkripsi AES: XyZ123!@#"
    
    print("=== TEST STEGANOGRAFI LSB ===")
    try:
        print("Menyisipkan data...")
        hasil_hide = hide_data_lsb(gambar_asli, pesan_rahasia, gambar_hasil)
        print(hasil_hide)
        
        print("Mengekstrak data...")
        hasil_extract = extract_data_lsb(gambar_hasil)
        print(f"Pesan yang ditemukan: {hasil_extract}")
    except FileNotFoundError:
        print(f"Peringatan: Silakan siapkan gambar bernama '{gambar_asli}' terlebih dahulu di folder ini untuk mengetes kodenya.")