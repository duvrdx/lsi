from turtle import width
from click import confirm
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
import webview
from datetime import datetime

from app import app, db
from app.models import Usuario, Produto, Agendamento

db.create_all()
window = webview.create_window('Easy Software', app, width=1280, height=720, resizable=False, confirm_close=True)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username_input = request.form['login_username']
        password_input = request.form['login_password']
        
        # Realizar uma query pra saver se existe um usuario
        user = Usuario.query.filter_by(username=username_input).first()
        
        if not user:
            print('Usuário inexistente')
            return redirect(url_for('login'))
        
        if not user.verify_password(password_input):
            print('Senha incorreta')
            return redirect(url_for('login'))
        
        # Criando sessão para autenticar usuário
        login_user(user)
        return redirect(url_for('homepage'))
    
    
    return render_template('login.html')

@app.route('/cadastro', methods=['GET','POST'])
def cadastro():
    if request.method == 'POST':
        username_input = request.form['cad_username']
        password_input = request.form['cad_password']
        name_input = request.form['cad_name']
        role_input = request.form['cad_role']
        
        # Realizar uma query pra saver se existe um usuario
        user = Usuario.query.filter_by(username=username_input).first()
        
        if not user:
            new_user = Usuario(name_input, username_input, role_input, password_input);
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            print('Usuário existente')
            return redirect(url_for('cadastro'))
    
    
    return render_template('cadastro.html')

@app.route('/logout')
def logout():
    # Realizando query para buscar o usuário atual e realizando o logout
    user = Usuario.query.filter_by(id=current_user.id).first()
    logout_user()
    return redirect(url_for('login'))

@app.route('/homepage')
def homepage():
    if current_user.is_authenticated:
        return render_template('homepage.html', user_role=current_user.role)
    else:
        flash('Você precisa estar logado para acessar essa página.')
        return redirect(url_for('login'))

@app.route('/estoque', methods=['GET','POST'])
def estoque():
    if request.method == 'POST':
        product_name = request.form['product_name']
        brand = request.form['brand']
        product_price = float(request.form['product_price'])
        product_amount = request.form['product_amount']
        product_barcode = request.form['product_barcode']

        new_product = Produto(name=product_name, brand=brand, price=product_price, amount=int(product_amount), barcode=product_barcode)
        db.session.add(new_product)
        db.session.commit()
        
    return render_template('estoque.html')

@app.route('/estoque/info')
def estoque_info():
    products = Produto.query.all()
    return render_template('estoque_info.html', products=products)

@app.route('/estoque/agend', methods=['GET','POST'])
def estoque_agend():
    if request.method == 'POST':
        agend_fornec = request.form['agend_fornec']
        agend_date = datetime.strptime(request.form['agend_date'],"%Y-%m-%d").date() 

        new_agend = Agendamento(agend_fornec, agend_date)
        db.session.add(new_agend)
        db.session.commit()

    agendamentos = Agendamento.query.all()

    return render_template('estoque_agend.html', agendamentos=agendamentos)

@app.route('/produtos', methods=['GET','POST'])
def produtos():
    if request.method == 'POST':
        product = Produto.query.filter_by(barcode=request.form['search']).first()
        
        if product:
            
            # Código para pegar maior produto
            
            #m = db.session.query(Produto.name, func.max(Produto.amount)).first()
            #print(m[0])
            return render_template('produtos.html', brand = product.brand, disponibility=product.status, product=product.name, quantity=product.amount)
        else:
            return render_template('produtos.html', disponibility=False, product="Esse código de barras não existe")
    else:
        return render_template('produtos.html', disponibility=False, product="Pesquise por um produto.")

@app.route('/produtos/estatisticas')
def produtos_estatisticas():
    return render_template("estatisticas.html")

@app.route('/del/<barcode>')
def delete(barcode):
    db.session.delete(Produto.query.filter_by(barcode=barcode).first())
    db.session.commit()

    return redirect(url_for("estoque_info"))

@app.route('/prateleira')
def prateleira():
    products = Produto.query.all()
    return render_template('prateleira.html', products=products)

if __name__ == '__main__':
    db.create_all()
    webview.start()
   
