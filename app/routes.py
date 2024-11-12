from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import secrets

app = Flask(__name__)
# Utilisateurs fictifs pour la démonstration
users = {
    'user1': 'p1',
    'user2': 'p2',
}

secrets_bdd = {
    'user1': 'bf6862a86b18850ad6af128d8a9cce68',
    'user2': 'ad6862a86b18850ad6af128d8a9cce25',
}

contact_messages = []
read_messages = []

@app.route('/')
def home():
    return redirect(url_for('login'))  # Redirige vers la page de connexion

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:  # Vérifie le mot de passe
            session['username'] = username
            return redirect(url_for('secret'))
        else:
            flash('Nom d’utilisateur ou mot de passe incorrect.', 'danger')

    return render_template('login.html')  # Affiche le formulaire de connexion

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username not in users:  # Vérifie si l'utilisateur existe déjà
            users[username] = password  # Ajoute l'utilisateur
            secret = secrets.token_hex(16)
            secrets_bdd[username] = secret
            flash('Inscription réussie ! Vous pouvez vous connecter.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Nom d’utilisateur déjà pris.', 'danger')

    return render_template('register.html')  # Affiche le formulaire d'enregistrement

@app.route('/secret')
def secret():
    if 'username' not in session:  # Vérifie si l'utilisateur est connecté
        return redirect(url_for('login'))  # Redirige vers la connexion si non connecté
    else:
        username = session['username']
        secret = secrets_bdd.get(username)
    return render_template('secret.html', username=username, secret=secret)  # Affiche le secret

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        message = request.form['message']  # Récupère le message du formulaire
        contact_messages.append(message)  # Ajoute le message à la liste
        flash('Message envoyé à l\'administrateur.', 'success')

    return render_template('contact.html')  # Affiche le formulaire de contact

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()  # Efface la session de l'utilisateur
    flash('Vous avez été déconnecté avec succès.', 'success')  # Affiche un message de succès
    return redirect(url_for('home'))  # Redirige vers la page d'accueil

#Fonction pour le bot_admin
@app.route('/get_latest_message')
def get_latest_message():
    global read_messages  # Indiquer que nous utilisons la variable globale
    if contact_messages:
        latest_message = contact_messages[-1]  # Récupère le dernier
        return latest_message  # Renvoie le message brut
    return 'empty', 204  # Aucun message, renvoie un code de statut 204 No Content
