import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Fungsi 1: Menghasilkan kunci 256-bit (32 byte) dari password apa pun
def generate_key(password):
    """
    Mengubah password yang diketik user menjadi kunci 32 byte yang valid untuk AES-256
    menggunakan fungsi hash SHA-256.
    """
    return hashlib.sha256(password.encode()).digest()

# Fungsi 2: Proses Enkripsi
def encrypt_aes(plaintext, password):
    try:
        key = generate_key(password)
        # Membuat objek AES dengan mode CBC
        cipher = AES.new(key, AES.MODE_CBC)
        # Proses padding (menyesuaikan panjang teks dengan blok AES) dan enkripsi
        ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
        
        # Menggabungkan Initialization Vector (IV) dan ciphertext
        # lalu diubah ke Base64 agar menjadi string teks yang mudah disisipkan
        encrypted_data = base64.b64encode(cipher.iv + ciphertext).decode('utf-8')
        return encrypted_data
    except Exception as e:
        return f"Error saat enkripsi: {e}"

# Fungsi 3: Proses Dekripsi
def decrypt_aes(encrypted_data, password):
    try:
        key = generate_key(password)
        # Mengubah kembali dari string Base64 ke bentuk byte
        raw_data = base64.b64decode(encrypted_data)
        
        # 16 byte pertama adalah IV, sisanya adalah ciphertext
        iv = raw_data[:16]
        ciphertext = raw_data[16:]
        
        # Proses dekripsi dan membuang padding
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return plaintext.decode('utf-8')
    except ValueError:
        return "ERROR: Password salah atau data telah rusak/dimodifikasi!"
    except Exception as e:
        return f"Error saat dekripsi: {e}"

# --- BLOK PENGUJIAN KODE ---
# Anda bisa menjalankan file ini langsung untuk mengetesnya
if __name__ == "__main__":
    data_ijazah = "NIM: 123456, Nama: Budi Santoso, IPK: 3.85, Lulus: 2023"
    password_rahasia = "KampusMerdeka2024"

    print("=== TEST KRIPTOGRAFI AES ===")
    print(f"Data Asli     : {data_ijazah}")
    
    # Test Enkripsi
    hasil_enkripsi = encrypt_aes(data_ijazah, password_rahasia)
    print(f"Hasil Enkripsi: {hasil_enkripsi}")
    
    # Test Dekripsi
    hasil_dekripsi = decrypt_aes(hasil_enkripsi, password_rahasia)
    print(f"Hasil Dekripsi: {hasil_dekripsi}")