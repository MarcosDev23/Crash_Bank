# 🏦 Crash Bank - Sistema Bancário & Investimentos

O **Crash Bank** é uma aplicação web de gestão financeira pessoal e consulta de investimentos em tempo real. Desenvolvido com Python e Flask, o sistema permite que usuários controlem seu saldo, registrem entradas e saídas e visualizem o histórico de ações da B3 através de gráficos dinâmicos.

## 🚀 Funcionalidades

- **Dashboard Financeiro:** Visualização de saldo total e gráfico de rosca dinâmico (Entradas vs. Saídas).
- **Gestão de Transações:** Registro de depósitos e saques com atualização automática de saldo.
- **Extrato Detalhado:** Histórico completo de movimentações com data, descrição e valores.
- **Mercado em Tempo Real:** Consulta de cotações de ações (B3) e moedas utilizando a API do Yahoo Finance (`yfinance`).
- **Gráficos Interativos:** Gráficos de linha para histórico de ativos e gráficos de rosca para resumo financeiro (Chart.js).
- **Autenticação Segura:** Sistema de login e cadastro com criptografia de senhas e proteção de rotas.
- **Tema Dark/Light:** Interface moderna com suporte a alternância de temas.

## 🛠️ Tecnologias Utilizadas

- **Backend:** [Python](https://www.python.org/) & [Flask](https://flask.palletsprojects.com/)
- **Banco de Dados:** SQLite (SQLAlchemy ORM)
- **Frontend:** HTML5, CSS3, JavaScript
- **Gráficos:** [Chart.js](https://www.chartjs.org/)
- **Dados Financeiros:** [yfinance](https://pypi.org/project/yfinance/)
- **Autenticação:** Flask-Login

## 📦 Como rodar o projeto

1. **Clone o repositório:**
   git clone:[https://github.com/MarcosDev23/Crash_Bank](https://github.com/MarcosDev23/Crash_Bank.git)
   cd crash_bank

2.  **Crie um ambiente virtual e ative-o:**

    python -m venv venv

    # No Windows:
    venv\Scripts\activate

    # No Linux/Mac:
    source venv/bin/activate

3.  **Instale as dependências:**
    
    pip install -r requirements.txt

4. **Inicie a aplicação:**

    python run.py

    Acesse no navegador: http://127.0.0.1:5000

   
