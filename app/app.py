from flask import Flask, session
from flask_session import Session
from routes import *  # Importer tes routes
import threading
import logging
from selenium import webdriver
import time

logging.basicConfig(level=logging.DEBUG,  # Niveau de log: DEBUG et plus élevés seront affichés
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])  # Log sur la console

# Configuration de l'application
app.secret_key = 'your_secret_key'  # Remplace par une clé secrète sécurisée
app.config['SESSION_TYPE'] = 'filesystem'  # Utiliser le système de fichiers pour stocker les sessions
app.config['SESSION_PERMANENT'] = False  # Les sessions ne sont pas permanentes
app.config['SESSION_USE_SIGNER'] = True  # Signe les cookies de session pour plus de sécurité

# Initialiser Flask-Session
Session(app)

def check_latest_messages():
#    time.sleep(30)
    while True:
        time.sleep(10)
        logging.debug('jai dormi 10')
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Remote(
        command_executor='http://selenium:4444/wd/hub',
        options=options
        )
        try:
            driver.get('http://web:5000/get_latest_message')
        except Exception as e:
            print(f"Une erreur est survenue : {str(e)}")
        driver.quit()

#threading.Thread(target=check_latest_messages, daemon=True).start()

# Lancement de l'application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Rendre l'application accessible
