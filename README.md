# decrypt-edge-passwords
POC to show why people should move away from saving passwords within browsers. 
This script extracts and decrypts saved passwords from **Microsoft Edge**'s login data on a Windows machine. It uses the **DPAPI** (Data Protection API) to decrypt the master key, and **AES GCM** decryption to retrieve the saved passwords.
In this POC, Microsoft Edge was used to show that passwords can be easily decrypted and accessed by malicious actors. 

# Disclaimer
This script is intended solely for ethical and educational purposes. It is designed to help demonstrate the risks associated with storing passwords in web browsers and how they can be accessed under certain conditions. Unauthorized access to data, accounts, or devices without explicit permission is illegal and unethical.
By using this script, you agree to take full responsibility for your actions and to use it only in compliance with applicable laws and regulations. You should only use this tool on systems or accounts where you have explicit consent and permission to access the data. Always respect user privacy and follow ethical guidelines when working with sensitive information.

## Requirements
- Python 3.6 or higher
- `pycryptodome` library (listed in `requirements.txt`)

## Setup

1. **Clone the repository**:

```bash
git clone https://github.com/yourusername/edge-password-decryptor.git
cd edge-password-decryptor
 ```
2. **Install dependencies**:
```bash
pip install -r requirements.txt
```
## Usage:
 This script extracts and decrypts passwords stored in Microsoft Edge’s `Login Data` database. It retrieves the encrypted master key from the `Local State` file and uses it to decrypt the passwords using DPAPI or AES GCM encryption.

**Notes**:
- The script uses DPAPI (Data Protection API) to decrypt passwords on Windows. If your system is using additional security measures (like Windows Hello), decryption may not work. Chrome currently works with additional security, hence this only working on edge. Chrome may be added in the future.

## Key Dependencies
 - **pycryptodome**: Required for AES decryption (via AES.new() to handle the AES.MODE_GCM encryption).
 - **ctypes**: A built-in Python library used for interacting with Windows' DPAPI (to decrypt the encrypted master key stored in the Local State file).
 - **sqlite3**: Built-in Python module for working with SQLite databases (used to extract saved login data from the "Login Data" file).
 - **json**: Built-in Python module for reading JSON data (used to read the Local State file that contains the master key).
 - **base64**: Built-in Python module for decoding base64-encoded data (used to decode the encrypted key).
