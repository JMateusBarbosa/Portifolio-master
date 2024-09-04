import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'chaveSecreta')

EMAIL = os.getenv('EMAIL')
SENHA = os.getenv('SENHA')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def enviar_email():
    try:
        nome = request.form['nome']
        email = request.form['email']
        mensagem = request.form['mensagem']

        # Configuração do servidor SMTP
        local_hostname = 'your_local_hostname'
        servidor_email = smtplib.SMTP('smtp.gmail.com', 587, local_hostname=local_hostname)
        servidor_email.starttls()
        servidor_email.login(EMAIL, SENHA)  # Usando variáveis de ambiente

        remetente = EMAIL
        destinatario = EMAIL
        assunto = f'Mensagem do formulário de contato de {nome} ({email})'
        corpo_mensagem = f'''
        Nome: {nome}
        Email: {email}
        
        Mensagem:
        {mensagem}
        '''

        mensagem_email = MIMEMultipart()
        mensagem_email['From'] = remetente
        mensagem_email['To'] = destinatario
        mensagem_email['Subject'] = assunto
        mensagem_email.attach(MIMEText(corpo_mensagem, 'plain'))

        # Enviar o e-mail
        servidor_email.sendmail(remetente, destinatario, mensagem_email.as_string())
        servidor_email.quit()

        flash('Mensagem enviada com sucesso!', 'success')
        return redirect(url_for('index'))
    
    except Exception as e:
        flash(f'Erro ao enviar mensagem: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
