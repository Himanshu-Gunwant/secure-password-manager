import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import os

def derive_key(master_password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390_000,
    )
    return base64.urlsafe_b64encode(
        kdf.derive(master_password.encode())
    )


#for genrating salt file only required for first use you may delete it later
def create_salt():
    salt = os.urandom(16)
    with open("salt.bin", "wb") as f:
        f.write(salt)
    return salt

def load_salt():
    with open("salt.bin", "rb") as f:
        return f.read()


def get_fernet(master_password: str) -> Fernet:
    try:
        salt = load_salt()
    except FileNotFoundError:
        salt = create_salt()
    key = derive_key(master_password, salt)
    return Fernet(key)

def encrypt_password(master_password: str, password: str) -> bytes:
    fernet = get_fernet(master_password)
    return fernet.encrypt(password.encode())

def decrypt_password(master_password: str, token: bytes) -> str:
    fernet = get_fernet(master_password)
    return fernet.decrypt(token).decode()

master_pwd = input("Enter the master password: ")

def view() :
    print("--------------------------------")
    with open("passwords.txt", "r") as file :
        for line in file.readlines() :
            name, account_id , encrypted = line.strip().split(" : ")
            decrypted = decrypt_password(master_pwd, encrypted.encode("utf-8"))
            print(f"Site name : {name}")
            print(f"Account id : {account_id}")
            print(f"Password : {decrypted}")
            print("--------------------------------")


def add() :
    name = input("Enter the site name: ")
    account_id = input("Enter the account id: ")
    password = input("Enter the password: ")
    encrypted_pwd = encrypt_password(master_pwd, password).decode("utf-8")
    with open("passwords.txt", "a") as file :
        file.write(name + " : " + account_id + " : " + encrypted_pwd + "\n")

print("Welcome to the password manager")
while True :
    action = input("What would you like to do(view, add, quit) ? : ")
    if action == "quit" :
        break
    if action == "view" :
        view()
    elif action == "add" :
        add()

print("Thank you for using password manager")

