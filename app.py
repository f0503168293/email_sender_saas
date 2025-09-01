from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

@app.route("/", methods=["GET", "POST"])
def send_email():
    if request.method == "POST":
        to_email = request.form["to_email"]
        subject = request.form["subject"]
        message = request.form["message"]

        try:
            msg = MIMEMultipart()
            msg["From"] = EMAIL_USER
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(message, "plain"))

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_USER, EMAIL_PASS)
                server.sendmail(EMAIL_USER, to_email, msg.as_string())

            flash("Email envoyé avec succès !", "success")
        except Exception as e:
            flash(f"Erreur : {str(e)}", "danger")

        return redirect(url_for("send_email"))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
