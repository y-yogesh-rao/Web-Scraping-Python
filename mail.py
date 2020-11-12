from flask import Flask, request, render_template, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

app = Flask(__name__)
app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_USE_SSL=True,
    MAIL_USERNAME='yogeshrao09011998@gmail.com',
    MAIL_PASSWORD='yoyochennaiexpress',
    MAIL_PORT=465
))
mail = Mail(app)

serializer = URLSafeTimedSerializer('APPLICATION-SECRET')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('emailId')
        token = serializer.dumps(email, salt='confirm-email')

        link = url_for('confirm_email', token=token, _external=True)
        mail_body = 'Your Confirmation Link is: {0}'.format(link)
        msg = Message('Confirm Email', recipients=[email], sender='yogeshrao09011998@gmail.com', body=mail_body)
        mail.send(msg)

        return '<h1>Please verify your email ID: {0}; token = {1}</h1>'.format(email, token)


@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = serializer.loads(token, salt='confirm-email', max_age=60)
    except SignatureExpired:
        return '<h1>Signature has been expired!</h1>'
    return '<h1>Email: {0} Verified Successfully</h1>'.format(email)


if __name__ == "__main__":
    app.run(debug=True)