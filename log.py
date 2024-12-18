import requests 
from datetime import datetime
import csv 
import hashlib

def lire_users(filename):
    users = []
    with open(filename, mode='r', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            users.append({
                "nom": row["name"],
                "password": row["pw_hash"],
                "date": row["date_creation"]
            })
    return users

def check_compromissions(password):
    url = 'https://api.pwnedpasswords.com/range/{password}'
    response = requests.get(url)
    if response.status_code == 200:
        suffix = password[5:]
        for line in response.text.splitlines():
            hashed, count = line.split(":")
            if hashed == suffix:
                return int(count)
    return 0



def log(entre, sortie):
    users = lire_users(entre)

    with open(sortie, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['nom', 'password', 'count', 'time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writerheader()

        for user in users:
            password = user["pw_hash"]
            compromis_count = check_compromissions(password)
            writer.writerow({
                'username': user["name"],
                'password': password,
                'count': compromis_count,
                'time': user["creation_time"]
            })
log()