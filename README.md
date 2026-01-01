# secure-password-manager (Python)

A simple password manager built in Python using:
- PBKDF2 key derivation
- Fernet authenticated encryption

## Features
- Master-password–derived encryption key
- No stored encryption key
- Encrypted password storage
- Secure by design
  
## Read Before Using
-Install cryptography package using pip
    pip install cryptography
-Keep note of the master password you enter as it will be used to decrypt the passwords later

## Warning
-If you forget the master password or the salt file is deleted, encrypted data cannot be recovered.
-Do not use for storing your important passwords I DO NOT TAKE RESPONSIBILITY 🤣🤣


