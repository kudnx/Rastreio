from app import app
from app.forms import PackageRegistrationForm
from flask import render_template, flash, redirect, url_for


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Kyouhime'}
    encomendas = [
        {
            'nome': 'Carregador de Notebook',
            'cod' : '00000000000'
        },
        {
            'nome': 'Ventilador',
            'cod' : '00000000000'
        },
    ]
    return render_template('index.html', title='Página Inicial', user=user, encomendas=encomendas)

@app.route('/package_registration', methods=['GET', 'POST'])
def package_registration():
    form = PackageRegistrationForm()
    if  form.validate_on_submit():
        flash('Erro ao cadastrar encomendas!')
        return redirect('index')
    return render_template('package_registration.html', title='Cadastro de Encomendas', form=form)


