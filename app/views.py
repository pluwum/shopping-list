"""This file contains logic for all the routes accessible on this Shopping
 list APP
"""
from flask import flash, redirect, render_template, request, session

from app import app

from .classes import ShoppingListApp
# We import our WTForm classes
from .forms import CreateListForm, LoginForm, RegistrationForm

# Setup an instance of the shopping list functionality
shopping_list_app = ShoppingListApp()


def check_if_user_logged_in():
    """Returns true if user is logged in, False otherwise"""
    # Check if current user has a logged in session
    if "user_email" in session:
        return True
    return False


@app.route("/", methods=['GET', 'POST'])
def index():
    """This handles the logic for user login and displaying login page"""
    # Lets make sure the user isn't already logged in
    if not check_if_user_logged_in():
        form = LoginForm()

        # POST: Lets Handle the login form submission
        if form.validate_on_submit():
            try:
                shopping_list_app.login(form.email.data, form.password.data)

                # Store user's information for this session
                user = shopping_list_app.users[form.email.data]
                session['user_email'] = user.email
                # Send the user to their list view
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
    """This Handles user registration submission and displaying
     registration page
     """
    form = RegistrationForm()

    # POST METHOD: Handle login form submission
    if form.validate_on_submit():
        try:
            # We create a user
            shopping_list_app.register_user(form.first_name.data,
                                           form.last_name.data,
                                           form.email.data,
                                           form.password.data)
            # Display success and redirect to login page if no errors occur
            flash('Your account was created succesfully')
            return redirect('/')

        except Exception as ex:
            # When errors occur, display on the screen and redirect
            flash('Error: {}\n'.format(ex))
            return redirect('/register')

    return render_template('registration.html',
                           title='Sign In',
                           form=form)


@app.route("/lists")
def lists():
    """Displays all lists of a particular user. i.e logged in user"""
    # Make sure our user is logged in
    if check_if_user_logged_in():
        # Get email from session VAR and use it to query user email
        user = session['user_email']
        user = shopping_list_app.get_user_detail(user)

        # Get all shopping lists associated with this user
        my_lists = shopping_list_app.get_user_shopping_lists(user.email)
        # Check if user is logged in
        return render_template('shopping_lists.html', title='Shopping Lists',
                               my_lists=my_lists,
                               user_id=user.email)

    # Send user back to login if not
    return redirect('/')


@app.route("/logout")
def logout():
    """Handles logic to logout user"""
    # Clear email from session data
    session.pop('user_email', None)
    # Inform the User of the login status and redirect to login page
    flash('You been logged out successfully')
    return redirect('/')


@app.route("/list/create", methods=['GET', 'POST'])
def create_list():
    """Handles display of create list page and logic for saving new lists
    submisions
    """
    # First we make sure the user has logged in
    if check_if_user_logged_in():
        form = CreateListForm()
        user_email = session['user_email']

        # POST METHOD: Handles login form submission
        if form.validate_on_submit():
            try:
                # We create the shoppinglist
                shopping_list_app.create_shopping_list(
                    form.name.data, form.description.data, user_email)

                # On success, display success message and redirect
                flash('Yay!: List successfully created')
                return redirect('/lists')

            except Exception as ex:
                # Cath all any errors raised and display them to the user
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
def edit_list(id):
    """GET Request that displays edit form view"""
    # We check that user is logged in
    if check_if_user_logged_in():
        form = CreateListForm()
        user_email = session['user_email']

        # Get all forms associated with the user
        shopping_list = shopping_list_app.shopping_lists[user_email][id]
        if shopping_list:
            # Provide the form with Default data for input fields
            form.name.data = shopping_list.name
            form.description.data = shopping_list.description

        # Show create list page
            if check_if_user_logged_in():
                return render_template('create_list.html',
                                       title='Edit List',
                                       heading="Edit New Shopping List",
                                       btn_txt="Update List",
                                       form=form,
                                       action="/list/edit/{}".format(id),
                                       hide_name=True)

        flash('Error: Could not find the list you are tring to edit')
        return redirect('/lists')

    # Send user back to login if not
    return redirect('/')


@app.route("/list/edit/<int:id>", methods=['POST'])
def update_list(id):
    """This handles saving of updates of the an edited list"""
    # First confirm that user is logged in
    if check_if_user_logged_in():
        form = CreateListForm()
        user_email = session['user_email']

        try:
            # Update list object index with new details
            shopping_list_app.edit_shopping_list(
                id, user_email, form.name.data, form.description.data)

            # If all went well, diplay message and redirect user
            flash('Yay!: List successfully updated')
            return redirect('/lists')

        except Exception as ex:
            # If errors occured, display errors and redirect user
            flash('Error: {}\n'.format(ex))
            return redirect('/lists')

    # Send user back to login if not
    return redirect('/')


@app.route("/list/delete/<int:id>", methods=['GET'])
def delete_list(id):
    """This handles delete action for a list"""
    # First make sure the user is logged in
    if check_if_user_logged_in():
        user_email = session['user_email']

        try:
            # Remove list item from dictionary
            shopping_list_app.delete_shopping_list(id, user_email)
            # Display success message and redirect if all went well
            flash('Yay!: List successfully deleted')
            return redirect('/lists')

        except Exception as ex:
            # Handle critical errors that are raised during the operation
            flash('Error: {}\n'.format(ex))
            return redirect('/lists')

    # Send user back to login if not
    return redirect('/')


@app.route("/list/<int:shoppinglist_id>")
def view_list_items(shoppinglist_id):
    """This method handles showing of list items under a given list"""
    # Make sure that user is logged in
    if check_if_user_logged_in():
        user = session['user_email']
        # Retrieve shopping list object and query it for list items
        my_list = shopping_list_app.get_shopping_list(shoppinglist_id, user)
        my_list_items = my_list.list_items

        # Return the view with all list items found
        return render_template('shopping_list_items.html', title='Shopping "\
                    "Lists Items',
                               my_list_items=my_list_items,
                               list_id=shoppinglist_id,
                               user_id=user)
    # Send user back to login if not logged in
    return redirect('/')


@app.route("/list/<int:shoppinglist_id>/item/create", methods=['POST', 'GET'])
def add_list_item(shoppinglist_id):
    """Handles showing of add item view and saves the item being added"""
    # Check that user is logged in
    if check_if_user_logged_in():
        form = CreateListForm()
        user = session['user_email']

        # POST METHOD: Handle login form submission
        if form.validate_on_submit():
            try:
                # Find the list we want to add items to
                mylist = shopping_list_app.get_shopping_list(
                    shoppinglist_id, user)
                # Finally add items to the list and display a success message
                shopping_list_app.user_add_item_to_list(
                    mylist, form.name.data, form.description.data)

                flash('Yay!: Item successfully  added to your list')
                # Redirect back to the list view
                return redirect('/list/{}'.format(shoppinglist_id))

            except Exception as ex:
                # If Errors where encoutered, handle here
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
def edit_list_item(shoppinglist_id, id):
    """This displays a specified list item for editing and also saves the item
     being edited
    """
    # Check if user is logged in
    if check_if_user_logged_in():
        form = CreateListForm()
        user = session['user_email']
        # Find list with item being edited
        shopping_list = shopping_list_app.get_shopping_list(
            shoppinglist_id, user)
        # From the shopping list, retrieve item
        list_item = shopping_list.get_list_item(id)

        # POST REQUEST : Handles saving edited fields to data strut=cture
        if form.validate_on_submit():
            try:
                # Update list item
                shopping_list_app.user_update_item_in_list(
                    shopping_list, id, form.name.data, form.description.data)
                # When no errors arise, redirect user to list detail view
                return redirect('/list/{}'.format(shoppinglist_id))

            except Exception as ex:
                # If Errors where encoutered, handle here
                flash('Error: {}\n'.format(ex))
                return redirect('/list/{}'.format(shoppinglist_id))

        if list_item:
            # populate the form with pre-existing data
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
def delete_list_item(list_id, id):
    """Handles the deletion of list items from a given list"""
    # Make sure the user is logged in
    if check_if_user_logged_in():
        user_email = session['user_email']

        # Remove list item from dictionary
        try:
            # Find list with item to delete
            mylist = shopping_list_app.get_shopping_list(list_id, user_email)
            # Remove item from the list
            shopping_list_app.user_remove_item_from_list(mylist, id)
            # Inform the user of the operation success
            flash('Yay!: List Item successfully deleted')
            return redirect('/list/{}'.format(list_id))

        except Exception as ex:
            # If errors where encoutered, display them for user and redirect
            flash('Error: {}\n'.format(ex))
            return redirect('/list/{}'.format(list_id))

    # Send user back to login if not logged in
    return redirect('/')


@app.errorhandler(404)
def page_not_found(e):
    """This handles any other route not explicitly specified
    It displays a 404 page
    """
    return render_template('404.html'), 404
