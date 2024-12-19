import logging
logging.basicConfig(   # Config de base logging
    filename="log_requests.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def creer_compte(username):
    logging.info(f"Creation de compte pour l'utilisateur : {username}")

def connection(userlog):
    logging.info(f"Connection d'un utilisateur : {userlog}")

def ajout_prod(nom, produit, quantite, prix):
    logging.info(f"Ajout de {quantite} {produit} au prix de {prix} de {nom}")