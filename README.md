# decrypt-edge-passwords
POC to show why people should move away from saving passwords within browsers. In this POC, Microsoft Edge was used to show that passwords can be easily decrypted and accessed by malicious actors. 

# Disclaimer
This script is intended solely for ethical and educational purposes. It is designed to help demonstrate the risks associated with storing passwords in web browsers and how they can be accessed under certain conditions. Unauthorized access to data, accounts, or devices without explicit permission is illegal and unethical.

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
