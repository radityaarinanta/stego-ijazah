import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def generate_key(password):
    return hashlib.sha256(password.encode()).digest()

def encrypt_aes(plaintext, password):
    try:
        key = generate_key(password)
        cipher = AES.new(key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
        encrypted_data = base64.b64encode(cipher.iv + ciphertext).decode('utf-8')
        return encrypted_data
    except Exception as e:
        return f"Error saat enkripsi: {e}"

def decrypt_aes(encrypted_data, password):
    try:
        key = generate_key(password)
        raw_data = base64.b64decode(encrypted_data)
        iv = raw_data[:16]
        ciphertext = raw_data[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return plaintext.decode('utf-8')
    except ValueError:
        return "ERROR: Password salah atau data telah rusak/dimodifikasi!"
    except Exception as e:
        return f"Error saat dekripsi: {e}"

if __name__ == "__main__":
    data_ijazah = "NIM: 123456, Nama: Budi Santoso, IPK: 3.85, Lulus: 2023"
    password_rahasia = "KampusMerdeka2024"

    print("=== TEST KRIPTOGRAFI AES ===")
    print(f"Data Asli     : {data_ijazah}")
    
    hasil_enkripsi = encrypt_aes(data_ijazah, password_rahasia)
    print(f"Hasil Enkripsi: {hasil_enkripsi}")
    
    hasil_dekripsi = decrypt_aes(hasil_enkripsi, password_rahasia)
    print(f"Hasil Dekripsi: {hasil_dekripsi}")