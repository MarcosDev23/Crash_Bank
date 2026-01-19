from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Transaction, db, User
import yfinance as yf

def init_routes(app):
    
    @app.route('/')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return render_template('login.html')

    @app.route('/registrar', methods=['GET'])
    def registrar_page():
        return render_template('cadastro.html')

    @app.route('/cadastro', methods=['POST'])
    def cadastro():
        nome = request.form.get('nome')
        cpf = "".join(filter(str.isdigit, request.form.get('cpf')))
        email = request.form.get('email')
        senha = request.form.get('senha')

        user_exists = User.query.filter((User.cpf == cpf) | (User.email == email)).first()
        if user_exists:
            flash("CPF ou E-mail já cadastrados!")
            return redirect(url_for('registrar_page'))

        hashed_pw = generate_password_hash(senha, method='pbkdf2:sha256')
        novo_usuario = User(nome=nome, cpf=cpf, email=email, senha=hashed_pw)
        
        try:
            db.session.add(novo_usuario)
            db.session.commit()
            flash("Conta criada com sucesso! Agora você pode entrar.")
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash("Erro ao criar conta. Tente novamente.")
            return redirect(url_for('registrar_page'))

    @app.route('/login_post', methods=['POST'])
    def login_post():
        identificador = request.form.get('identificador')
        senha = request.form.get('senha')
        
        user = User.query.filter((User.email == identificador) | (User.cpf == identificador)).first()

        if not user:
            clean_id = "".join(filter(str.isdigit, identificador))
            user = User.query.filter(User.cpf == clean_id).first()

        if user and check_password_hash(user.senha, senha):
            login_user(user)
            return redirect(url_for('dashboard'))
        
        flash("Usuário ou senha incorretos.")
        return redirect(url_for('login'))

    @app.route('/movimentar', methods=['POST'])
    @login_required
    def movimentar():
        try:
            tipo = request.form.get('tipo')
            valor_str = request.form.get('valor')
            descricao = request.form.get('descricao')

            if not valor_str:
                flash("Por favor, insira um valor.")
                return redirect(url_for('dashboard'))

            valor = float(valor_str)

            if tipo == 'saida':
                if valor > current_user.saldo:
                    flash("Saldo insuficiente para realizar esta saída!")
                    return redirect(url_for('dashboard'))
                current_user.saldo -= valor 
            else:
                current_user.saldo += valor

            # Criação da transação vinculada ao usuário
            nova_transacao = Transaction(
                tipo=tipo, 
                valor=valor, 
                descricao=descricao, 
                owner=current_user
            )
            
            db.session.add(nova_transacao)
            db.session.commit()
            
            flash(f"{tipo.capitalize()} de R$ {valor:.2f} realizada!")
            return redirect(url_for('dashboard'))

        except ValueError:
            flash("Erro: O valor inserido não é um número válido.")
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash("Erro ao processar transação.")
            return redirect(url_for('dashboard'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        # Cálculo de totais para o dashboard
        entradas = sum(t.valor for t in current_user.transacoes if t.tipo == 'entrada')
        saidas = sum(t.valor for t in current_user.transacoes if t.tipo == 'saida')
        return render_template('dashboard.html', entradas=entradas, saidas=saidas)

    @app.route('/balanco')
    @login_required
    def balanco():
        return render_template('balance.html')
    
    @app.route('/get_stock_price')
    @login_required
    def get_stock_price():
        ticker = request.args.get('ticker')
        if not ticker:
            return jsonify({'error': 'Ticker não informado'}), 400
            
        try:
            stock = yf.Ticker(ticker)
            # Buscamos 1 mês para garantir que teremos dados mesmo após fins de semana/feriados
            hist = stock.history(period="1mo")
            
            if hist.empty:
                return jsonify({'error': 'Ativo não encontrado ou sem dados recentes'}), 404
                
            # Pegamos os últimos 7 dias de fechamento
            precos = hist['Close'].tail(7).tolist()
            labels = [d.strftime('%d/%m') for d in hist.index[-7:]]
            preco_atual = precos[-1]
            
            return jsonify({
                'price': preco_atual,
                'history': precos,
                'labels': labels
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/investimentos')
    @login_required
    def investimentos():
        return render_template('investimentos.html')

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login'))