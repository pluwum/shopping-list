from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm, RegistrationForm
from .classes import ShoppingListApp

shopping_list_app = ShoppingListApp()


@app.route("/", methods=['GET', 'POST'])
def index():
    form = LoginForm()

    # Handle login form submission
    if form.validate_on_submit():
        try:
            shopping_list_app.login(form.email.data, form.password.data)
            return render_template('shopping_lists.html',
                                   title='Shopping Lists')
        except Exception as ex:
            flash('Error: {}\n'.format(ex))
            return redirect('/')

    # Show login pages
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # Handle login form submission
    if form.validate_on_submit():
        try:
            shopping_list_app.registerUser(form.first_name.data,
                                           form.last_name.data,
                                           form.email.data,
                                           form.password.data)

            return redirect('/lists')

        except Exception as ex:
            flash('Error: {}\n'.format(ex))
            return redirect('/register')

    return render_template('registration.html',
                           title='Sign In',
                           form=form)


@app.route("/lists")
def lists():
    print(len(shopping_list_app.users))
    flash(len(shopping_list_app.users))
    return render_template('shopping_lists.html')
