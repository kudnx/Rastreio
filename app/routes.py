from flask_login.utils import logout_user
from app import app, db, function
from app.forms import PackageRegistrationForm, LoginForm, RegisterForm
from app.models import Package, PackageInformation, User
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        packages = User.user_packages(current_user)
        return render_template('index.html', title='Página Inicial', packages=packages)
    else:
        return render_template('index.html', title='Página Inicial')    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Nome de usuário ou senha Inválidos')
            return redirect(url_for('index'))
        login_user(user, remember=form.rememberMe.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Entrar', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        newUser = User(username=form.username.data)
        newUser.set_password(form.password.data)
        db.session.add(newUser)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html', title='Cadastrar', form=form)

@app.route('/package_registration', methods=['GET', 'POST'])
@login_required
def package_registration():
    form = PackageRegistrationForm()
    if  form.validate_on_submit():
        package = Package(description=form.description.data, cod=form.cod.data, user=current_user)
        db.session.add(package)
        db.session.commit()
        flash('Encomenda Cadastrada com sucesso!!')
        return redirect(url_for('index'))
    return render_template('package_registration.html', title='Cadastro de Encomendas', form=form)

@app.route('/track/<cod>')
@login_required
def track(cod):   

    data = function.getApiData(cod)

    try:
        mensagem = data["objetos"][0]["mensagem"]
    except: 
        mensagem = ''

    if mensagem != '':
        return render_template('package_not_found.html')

    print ()

    package = Package.package_description(cod)
    
    PackageInformation.quantity = data["quantidade"]
    PackageInformation.cod = cod
    PackageInformation.categoty = data["objetos"][0]["tipoPostal"]["categoria"]

    PackageInformation.data.clear()

    for data in data["objetos"][0]["eventos"]:
        description = data["descricao"]

        dateTime = data["dtHrCriado"].split("T")
        
        day = dateTime[0].split("-")
        day = day[2] + "/" + day[1] + "/" + day[0]
        hour = dateTime[1]

        try:
            city = data["unidade"]["endereco"]["cidade"]
        except: 
            city = data["unidade"]["nome"]

        try:
            destinationCity = data["unidadeDestino"]["endereco"]["cidade"]
        except: 
            destinationCity = ''

        try:
            detail = data["detalhe"]
        except: 
            detail = ''

        PackageInformation.data.append([description, city, destinationCity, day, hour, detail])

    return render_template('track.html', title='Encomenda', packageinformation=PackageInformation, package=package)


