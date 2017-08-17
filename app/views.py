from flask import flash, redirect, render_template

from app import app

from .classes import ShoppingListApp
from .forms import CreateListForm, LoginForm, RegistrationForm

# Setup an instance of the shopping list functionality
shopping_list_app = ShoppingListApp()

# Set Up variable user to track the session
user = None

# Check if current user has a logged in session


def checkIfUserLoggedIn():
    global user
    if user is None:
        return False
    return True


@app.route("/", methods=['GET', 'POST'])
def index():
    form = LoginForm()

    # Handle login form submission
    if form.validate_on_submit():
        try:
            shopping_list_app.login(form.email.data, form.password.data)

            # store user's information for this session
            global user
            user = shopping_list_app.users[form.email.data]

            return redirect('/lists')
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
    global user

    # Check if user is logged in
    if checkIfUserLoggedIn():
        return render_template('shopping_lists.html', title='Shopping Lists',
                               my_lists=shopping_list_app.shopping_lists,
                               user_id=user.email)
    # Send user back to login if not
    return redirect('/')


@app.route("/logout")
def logout():
    global user
    user = None
    return redirect('/')


@app.route("/list/create", methods=['GET', 'POST'])
def createList():
    form = CreateListForm()
    global user

    # Handle login form submission
    if form.validate_on_submit():
        try:
            shopping_list_app.createShoppingList(
                form.name.data, form.description.data, user.email)

            flash('Yay!: List successfully created')
            return redirect('/lists')

        except Exception as ex:
            flash('Error: {}\n'.format(ex))
            return redirect('/')

    # Show create list page
    if checkIfUserLoggedIn():
        return render_template('create_list.html',
                               title='Sign In',
                               heading="Create New Shopping List",
                               btn_txt="Create List",
                               form=form,
                               action="/list/create",
                               hide_name=False)

    # Send user back to login if not logged in
    return redirect('/')


@app.route("/list/edit/<string:name>")
def editList(name):
    form = CreateListForm()
    shopping_list = shopping_list_app.shopping_lists[name]
    form.name.data = shopping_list.name
    form.description.data = shopping_list.description

    # Show create list page
    if checkIfUserLoggedIn():
        return render_template('create_list.html',
                               title='Edit List',
                               heading="Edit New Shopping List",
                               btn_txt="Update List",
                               form=form,
                               action="/list/edit/" + name,
                               hide_name=True)
    # Send user back to login if not
    return redirect('/')


@app.route("/list/edit/<string:name>", methods=['POST'])
def updateList(name):
    form = CreateListForm()
    global user
    # Recreate list object index with new details
    try:
        shopping_list_app.createShoppingList(
            name, form.description.data, user.email)

        flash('Yay!: List successfully updated')
        return redirect('/lists')

    except Exception as ex:
        flash('Error: {}\n'.format(ex))
        return redirect('/lists')
    # Send user back to login if not
    return redirect('/lists')


@app.route("/list/delete/<string:name>", methods=['GET'])
def deleteList(name):
    form = CreateListForm()

    # Remove list item from dictionary
    try:
        shopping_list_app.deleteShoppingList(name)

        flash('Yay!: List successfully deleted')
        return redirect('/lists')

    except Exception as ex:
        flash('Error: {}\n'.format(ex))
        return redirect('/lists')

    # Send user back to login if not
    return redirect('/lists')
