from flask import Flask, request, render_template, redirect, url_for, flash
from flask_mail import Mail, Message
from FeatureExtractor import featureExtraction
from pycaret.classification import load_model, predict_model

# Charger le modèle
model = load_model('model/phishingdetection')

def predict(url):
    data = featureExtraction(url)
    result = predict_model(model, data=data)
    prediction_score = result['prediction_score'][0]
    prediction_label = result['prediction_label'][0]
    return {
        'prediction_label': prediction_label,
        'prediction_score': prediction_score * 100,
    }

# Créer l'application Flask
app = Flask(__name__)

# Route pour la page d'accueil
@app.route("/")
def home():
    return render_template("home.html")

# Route pour la détection d'URL (GET & POST autorisés)
@app.route("/phishing-check", methods=["GET", "POST"])
def phishing_check():
    data = None
    if request.method == "POST":
        url = request.form["url"]
        data = predict(url)
        return render_template('index.html', url=url, data=data)
    return render_template("index.html", data=data)

# Route pour la page À propos
@app.route("/about")
def about():
    return render_template("about.html")

app.secret_key = 'ton_secret_key_super_securise'  # Important pour utiliser flash()

# Configuration de Flask-Mail pour envoyer un email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Remplace par ton serveur SMTP
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'imen333ay@gmail.com'  # Remplace par ton email
app.config['MAIL_PASSWORD'] = 'xpqudjnkluewkysw'  # Remplace par ton mot de passe
app.config['MAIL_DEFAULT_SENDER'] = 'imen333ay@gmail.com'  # Remplace par ton email

mail = Mail(app)

# Route pour la page Contact
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if name and email and message:
            msg = Message(f"Message de {name}", recipients=["imen333ay@gmail.com"])
            msg.body = f"Nom: {name}\nEmail: {email}\nMessage: {message}"

            try:
                mail.send(msg)
                return redirect(url_for('contact_success'))
            except Exception as e:
                return redirect(url_for('contact'))

        else:
            flash("Veuillez remplir tous les champs.", 'danger')
            return redirect(url_for('contact'))

    return render_template("contact.html")

# Route pour la page de succès
@app.route('/contact-success')
def contact_success():
    return render_template('success.html')


chatbot_data = {
    "c'est quoi le phishing ?": "Le phishing est une tentative de tromper l'utilisateur pour obtenir des informations sensibles, souvent via de faux e-mails ou sites web.",
    "comment se protéger contre le phishing ?": "Utilisez un antivirus, ne cliquez pas sur des liens suspects, et vérifiez toujours l'adresse du site.",
    "quel est le but d'un pare-feu ?": "Un pare-feu bloque les connexions réseau non autorisées et protège votre système.",
    "comment reconnaître un site frauduleux ?": "Soyez attentif aux fautes d'orthographe, à l’absence de HTTPS et aux demandes inhabituelles.",
    "mon mot de passe a été volé, que faire ?": "Changez-le immédiatement sur tous les services et activez l’authentification à deux facteurs.",
    "c'est quoi un malware ?": "Un malware est un logiciel malveillant conçu pour nuire à un système informatique.",
    "l’antivirus est-il suffisant ?": "Il est utile, mais vous devez aussi adopter de bons comportements de sécurité.",
    "c’est quoi le social engineering ?": "C’est une technique de manipulation psychologique pour obtenir des infos sensibles.",
    "comment sécuriser mes comptes en ligne ?": "Utilisez des mots de passe forts, différents pour chaque service, et activez 2FA."
}

# Route pour le Chatbot
@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    response = None
    question = None
    if request.method == "POST":
        question = request.form.get("question", "").strip().lower()
        response = chatbot_data.get(question, "Désolé, je ne connais pas encore la réponse à cette question.")
    return render_template("chatbot.html", question=question, response=response)



# Route pour la page "À propos du phishing"
@app.route("/phishing")
def phishing():
    return render_template("phishing.html")

# Lancement de l'application
if __name__ == "__main__":
    app.run(debug=True)
