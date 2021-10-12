from requests.models import Response
from requests.sessions import Request
from app import app, db
from app.forms import PackageRegistrationForm
from app.models import Package, PackageInformation
import requests
from flask import render_template, flash, redirect, url_for


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Kyouhime'}
    packages = Package.query.all()
    return render_template('index.html', title='Página Inicial', user=user, packages=packages)

@app.route('/package_registration', methods=['GET', 'POST'])
def package_registration():
    form = PackageRegistrationForm()
    if  form.validate_on_submit():
        package = Package(description=form.description.data, cod=form.cod.data)
        db.session.add(package)
        db.session.commit()
        flash('Encomenda Cadastrada com sucesso!!')
        return redirect(url_for('index'))
    return render_template('package_registration.html', title='Cadastro de Encomendas', form=form)

@app.route('/track/<cod>')
def track(cod):   
    link = "https://proxyapp.correios.com.br/v1/sro-rastro/" + cod
    response = requests.get(link)
    data = response.json()
    PackageInformation.quantity = data["quantidade"]
    PackageInformation.cod = cod
    PackageInformation.categoria = data["objetos"][0]["tipoPostal"]["categoria"]

    PackageInformation.dados.clear()

    for dados in data["objetos"][0]["eventos"]:
        descricao = dados["descricao"]

        dataHora = dados["dtHrCriado"].split("T")
        
        dia = dataHora[0].split("-")
        dia = dia[2] + "/" + dia[1] + "/" + dia[0]
        hora = dataHora[1]

        try:
            cidade = dados["unidade"]["endereco"]["cidade"]
        except: 
            cidade = dados["unidade"]["nome"]

        try:
            cidadeDestino = dados["unidadeDestino"]["endereco"]["cidade"]
        except: 
            cidadeDestino = ''

        try:
            detalhe = dados["detalhe"]
        except: 
            detalhe = ''

        PackageInformation.dados.append([descricao, cidade, cidadeDestino, dia, hora, detalhe])

    return render_template('track.html', title='Encomenda', packageinformation=PackageInformation)


