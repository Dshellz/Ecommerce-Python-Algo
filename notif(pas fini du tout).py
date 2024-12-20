import hashlib
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv

def load_users_from_csv(filename):
    users = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            users.append({'email': row['email'], 'pw_hash': row['pw_hash'], 'salt': row['salt']})
    return users

def check_password(password):
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_password[:5]
    suffix = sha1_password[5:]
    
    url = f'https://api.pwnedpasswords.com/range/{prefix}'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        hashes = response.text.splitlines()
        for hash_suffix in hashes:
            if hash_suffix.startswith(suffix):
                return True
    return False

def send_email(to_email, subject, body):
    from_email = "clientgestion9@gmail.com"
    password = "aSrtkgi87!@"
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print(f"E-mail envoyé à {to_email}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {str(e)}")

def notify_users_of_password_leak(users):
    for user in users:
        password = user['pw_hash']
        
        if check_password(password):
            send_email(
                user['email'], 
                "URGENT : Votre mot de passe a fuité", 
                "Bonjour, nous avons détecté que votre mot de passe a été compromis dans une fuite de données. Veuillez changer votre mot de passe au plus vite."
            )

users = load_users_from_csv('users.csv')
notify_users_of_password_leak(users)