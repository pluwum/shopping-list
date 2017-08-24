"""This file contains logic for all the routes accessible on this Shopping
 list APP
"""
from flask import flash, redirect, render_template, request, session

from app import app

from .classes import ShoppingListApp
from .forms import CreateListForm, LoginForm, RegistrationForm

# Setup an instance of the shopping list functionality
shopping_list_app = ShoppingListApp()


def checkIfUserLoggedIn():
    """Returns true if user is logged in, False otherwise"""
    # Check if current user has a logged in session
    if "user_email" in session:
        return True
    return False


@app.route("/", methods=['GET', 'POST'])
def index():
    """This handles the logic for user login and displaying login page"""
    # Lets make sure the user isn't already logged in
    if not checkIfUserLoggedIn():
        form = LoginForm()

        # POST: Lets Handle the login form submission
        if form.validate_on_submit():
            try:
                shopping_list_app.login(form.email.data, form.password.data)

                # store user's information for this session
                user = shopping_list_app.users[form.email.data]
                session['user_email'] = user.email
                return redirect('/lists')
            except Exception as ex:
                flash('Error: {}\n'.format(ex))
                return redirect('/')

        # GET METHOD: Lets Show login pages
        return render_template('login.html',
                               title='Sign In',
                               form=form)
    return redirect('/lists')


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
            flash('Your account was created succesfully')
            return redirect('/')

        except Exception as ex:
            flash('Error: {}\n'.format(ex))
            return redirect('/register')

    return render_template('registration.html',
                           title='Sign In',
                           form=form)


@app.route("/lists")
def lists():
    if checkIfUserLoggedIn():
        user = session['user_email']
        user = shopping_list_app.getUserDetail(user)
        my_lists = shopping_list_app.getUserShoppingLists(user.email)
        # Check if user is logged in
        return render_template('shopping_lists.html', title='Shopping Lists',
                               my_lists=my_lists,
                               user_id=user.email)
    # Send user back to login if not
    return redirect('/')


@app.route("/logout")
def logout():
    session.pop('user_email', None)
    flash('You been logged out successfully')
    return redirect('/')


@app.route("/list/create", methods=['GET', 'POST'])
def createList():
    if checkIfUserLoggedIn():
        form = CreateListForm()
        user = session['user_email']
        user = shopping_list_app.getUserDetail(user)

        # POST METHOD: Handle login form submission
        if form.validate_on_submit():
            try:
                shopping_list_app.createShoppingList(
                    form.name.data, form.description.data, user.email)

                flash('Yay!: List successfully created')
                return redirect('/lists')

            except Exception as ex:
                flash('Error: {}\n'.format(ex))
                return redirect('/')

        # GET METHOD: Show create list page
        return render_template('create_list.html',
                               title='Sign In',
                               heading="Create New Shopping List",
                               btn_txt="Create List",
                               form=form,
                               action="/list/create",
                               hide_name=False)

    # Send user back to login if not logged in
    return redirect('/')


@app.route("/list/edit/<int:id>")
def editList(id):
    if checkIfUserLoggedIn():
        form = CreateListForm()
        user = session['user_email']
        shopping_list = shopping_list_app.shopping_lists[user][id]
        if shopping_list:
            form.name.data = shopping_list.name
            form.description.data = shopping_list.description

        # Show create list page
            if checkIfUserLoggedIn():
                return render_template('create_list.html',
                                       title='Edit List',
                                       heading="Edit New Shopping List",
                                       btn_txt="Update List",
                                       form=form,
                                       action="/list/edit/{}".format(id),
                                       hide_name=True)
    # Send user back to login if not
    return redirect('/')


@app.route("/list/edit/<int:id>", methods=['POST'])
def updateList(id):
    if checkIfUserLoggedIn():
        form = CreateListForm()
        user = session['user_email']
        user = shopping_list_app.getUserDetail(user)
        # Recreate list object index with new details
        try:
            shopping_list_app.editShoppingList(
                id, user.email, form.name.data, form.description.data)

            flash('Yay!: List successfully updated')
            return redirect('/lists')

        except Exception as ex:
            flash('Error: {}\n'.format(ex))
            return redirect('/lists')
    # Send user back to login if not
    return redirect('/')


@app.route("/list/delete/<int:id>", methods=['GET'])
def deleteList(id):
    if checkIfUserLoggedIn():
        user_email = session['user_email']

        # Remove list item from dictionary
        try:
            shopping_list_app.deleteShoppingList(id, user_email)

            flash('Yay!: List successfully deleted')
            return redirect('/lists')

        except Exception as ex:
            flash('Error: {}\n'.format(ex))
            return redirect('/lists')

    # Send user back to login if not
    return redirect('/')


@app.route("/list/<int:shoppinglist_id>")
def viewListItems(shoppinglist_id):
    if checkIfUserLoggedIn():
        user = session['user_email']
        my_list = shopping_list_app.viewShoppingList(shoppinglist_id, user)
        my_list_items = my_list.list_items

        return render_template('shopping_list_items.html', title='Shopping "\
                    "Lists Items',
                               my_list_items=my_list_items,
                               list_id=shoppinglist_id,
                               user_id=user)
    # Send user back to login
    return redirect('/')


@app.route("/list/<int:shoppinglist_id>/item/create", methods=['POST', 'GET'])
def addListItem(shoppinglist_id):
    if checkIfUserLoggedIn():
        form = CreateListForm()
        user = session['user_email']

        # POST METHOD: Handle login form submission
        if form.validate_on_submit():
            try:
                mylist = shopping_list_app.viewShoppingList(
                    shoppinglist_id, user)
                result = shopping_list_app.userAddItemToList(
                    mylist, form.name.data, form.description.data)

                flash('Yay!: Item successfully  added to your list')

                return redirect('/list/{}'.format(shoppinglist_id))

            except Exception as ex:
                flash('Error: {}\n'.format(ex))
                return redirect('/list/{}'.format(shoppinglist_id))

        # GET METHOD: Show create list page
        return render_template('create_list.html',
                               title='Add Items',
                               heading="Add An Item to your List",
                               btn_txt="Add Item",
                               form=form,
                               action="/list/{}/item/create".format(
                                   shoppinglist_id),
                               hide_name=False)


@app.route("/list/<int:shoppinglist_id>/edit/<int:id>",
           methods=['POST', 'GET'])
def editListItem(shoppinglist_id, id):
    if checkIfUserLoggedIn():
        form = CreateListForm()
        user = session['user_email']
        shopping_list = shopping_list_app.viewShoppingList(
            shoppinglist_id, user)
        list_item = shopping_list.getListItem(id)

        if form.validate_on_submit():
            shopping_list_app.userUpdateItemInList(
                shopping_list, id, form.name.data, form.description.data)
            return redirect('/list/{}'.format(shoppinglist_id))

        if list_item:
            form.name.data = list_item.name
            form.description.data = list_item.description

        # Show edit item to list page
        return render_template('create_list.html',
                               title='Edit List Item',
                               heading="Edit List Item",
                               btn_txt="Update Item",
                               form=form,
                               action="/list/{}/edit/{}".format(
                                   shoppinglist_id, id),
                               hide_name=True)
    # Send user back to login if not
    return redirect('/')

@app.route("/list/<int:list_id>/delete/<int:id>", methods=['GET'])
def deleteListItem(list_id, id):
    if checkIfUserLoggedIn():
        user_email = session['user_email']

        # Remove list item from dictionary
        try:
            mylist = shopping_list_app.viewShoppingList(list_id, user_email)
            shopping_list_app.userRemoveItemFromList(mylist, id)

            flash('Yay!: List Item successfully deleted')
            return redirect('/list/{}'.format(list_id))

        except Exception as ex:
            flash('Error: {}\n'.format(ex))
            return redirect('/list/{}'.format(list_id))

    # Send user back to login if not
    return redirect('/')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
