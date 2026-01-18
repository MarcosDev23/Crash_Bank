from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User
import yfinance as yf

def init_routes(app):
    
    @app.route('/')
    def login():
        # Se já estiver logado, vai direto para o dashboard
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return render_template('login.html')

    @app.route('/registrar', methods=['GET'])
    def registrar_page():
        return render_template('cadastro.html')

    @app.route('/cadastro', methods=['POST'])
    def cadastro():
        nome = request.form.get('nome')
        # Limpa o CPF para salvar apenas números
        cpf = "".join(filter(str.isdigit, request.form.get('cpf')))
        email = request.form.get('email')
        senha = request.form.get('senha')

        # Verifica se já existe
        user_exists = User.query.filter((User.cpf == cpf) | (User.email == email)).first()
        if user_exists:
            flash("CPF ou E-mail já cadastrados!")
            return redirect(url_for('registrar_page'))

        # Salva o novo usuário
        hashed_pw = generate_password_hash(senha, method='pbkdf2:sha256')
        novo_usuario = User(nome=nome, cpf=cpf, email=email, senha=hashed_pw)
        db.session.add(novo_usuario)
        db.session.commit()
        
        flash("Conta criada com sucesso! Agora você pode entrar.")
        return redirect(url_for('login')) # Isso evita o erro de "Method Not Allowed"

    @app.route('/login_post', methods=['POST'])
    def login_post():
        identificador = request.form.get('identificador')
        senha = request.form.get('senha')
        
        # Tenta login com o que foi digitado (Email ou CPF com máscara)
        user = User.query.filter((User.email == identificador) | (User.cpf == identificador)).first()

        # Se não achou, tenta limpar o identificador (caso seja CPF com pontos)
        if not user:
            clean_id = "".join(filter(str.isdigit, identificador))
            user = User.query.filter(User.cpf == clean_id).first()

        if user and check_password_hash(user.senha, senha):
            login_user(user)
            return redirect(url_for('dashboard'))
        
        flash("Usuário ou senha incorretos.")
        return redirect(url_for('login'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/balanco')
    @login_required
    def balanco():
        return render_template('balance.html')

    @app.route('/investimentos')
    @login_required
    def investimentos():
        return render_template('investimentos.html')

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login'))