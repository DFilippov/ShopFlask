import secrets

from flask import render_template, request, redirect, url_for, flash, session, Response, current_app
from functools import wraps


from packages import app, db
# from packages.config import ITEMS_PER_PAGE, NUMBER_OF_TRUNCATED_SYMBOLS
from packages.models.user import User
from packages.models.item import Item
from packages.models.quantity_history import QuantityHistory
from packages.models.category import Category
from packages.services.hash_service import HashService
from packages.services.database_service import DatabaseService


ITEMS_PER_PAGE = app.config['ITEMS_PER_PAGE']
NUMBER_OF_TRUNCATED_SYMBOLS = app.config['NUMBER_OF_TRUNCATED_SYMBOLS']

def login_required(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        # in case of absence of access_token
        if 'access_token' not in session:
            return Response('Access denied. Please log in')

        # otherwise let call the method
        return func(*args, **kwargs)

    return check_token


def add_access_token_in_session():
    access_token_name = 'access_token'
    token = secrets.token_hex(32)
    update_session_values({access_token_name: token})


def update_session_values(dictionary):
    session.update(dictionary)


def remove_session_key(array_of_keys):
    for key in array_of_keys:
        session.pop(key, None)


def prepare_item():
    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')
    quantity = request.form.get('quantity')
    image_url = request.form.get('image_url')
    category_id = request.form.get('category_id')

    item = Item(
        name=name,
        description=description,
        price=price,
        quantity=quantity,
        image_url=image_url,
        category_id=category_id
    )
    return item


def truncate_string(string, number_of_symbols=NUMBER_OF_TRUNCATED_SYMBOLS):
    if len(string) > number_of_symbols:
        return string[:number_of_symbols] + '...'
    return string


# @app.after_request
# def login_first(response):
#     if response.status_code == 401:
#         return redirect(url_for('login') + '?next=' + response.url)


@app.route('/items/create', methods=['GET', 'POST'])
def create_item():
    if request.method == 'POST':
        item = prepare_item()

        database_service = DatabaseService()
        database_service.add_to_db([item])

        flash("Item '{}' successfully saved to database".format(item.name))
        return redirect('/')

    else:
        categories = Category.query.all()
        return render_template('create_item.html', title='Create Item', body='Create item', categories=categories)


@app.route('/items/<item_id>')
def show_item(item_id):
    item = Item.query.filter(Item.id == item_id).first()
    return render_template('show_item.html', title='Item info', body='Item info', item=item)


@app.route('/items/<item_id>/edit', methods=['GET', 'POST'])
def edit_item(item_id):
    original_item = Item.query.filter(Item.id == item_id).first()
    old_quantity = original_item.quantity
    if request.method == 'POST':
        Item.query.filter(Item.id == item_id).update(request.form)
        db.session.commit()
        changed_item = Item.query.filter(Item.id == item_id).first()

        if old_quantity != changed_item.quantity:
            quantity_history = QuantityHistory(
                old_quantity=old_quantity,
                new_quantity=changed_item.quantity,
                item_id=changed_item.id
            )
            database_service = DatabaseService()
            database_service.add_to_db([quantity_history])

        flash("Item '{}' successfully edited and saved to database".format(request.form.get('name')))
        return redirect(url_for('show_item', item_id=item_id))
    else:
        item = Item.query.filter(Item.id == item_id).first()
        categories = Category.query.all()

        return render_template(
            'edit_item.html',
            title='Edit item',
            body='Edit item',
            item=item,
            categories=categories
        )


@app.route('/items/<item_id>/delete', methods=['GET', 'DELETE'])
def delete_item(item_id):
    item = Item.query.filter(Item.id == item_id)
    item_name = item.first().name
    # TODO: item was not deleted
    item.delete()
    db.session.commit()
    flash("Item '{}' was deleted".format(item_name))
    return redirect(url_for('index'))


@app.route('/categories')
def show_categories():
    categories = Category.query.order_by(Category.id)
    for category in categories:
        if len(category.description) > NUMBER_OF_TRUNCATED_SYMBOLS:
            category.description = truncate_string(category.description)
    return render_template(
        'show_categories.html',
        title='Categories',
        body='List of available categories',
        categories=categories
    )


@app.route('/categories/create', methods=['GET', 'POST'])
def create_category():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')

        category = Category(name=name, description=description)

        database_service = DatabaseService()
        database_service.add_to_db([category])

        flash("Category '{}' successfully created".format(name))
        return redirect(url_for('show_categories'))
    else:
        return render_template('create_category.html', title='Create category', body='Create category')


@app.route('/categories/<category_id>/edit', methods=['GET', 'POST'])
def edit_category(category_id):
    category = Category.query.filter(Category.id == category_id).first()
    if request.method == 'POST':
        params = request.form
        Category.query.filter(Category.id == category_id).update(params)
        db.session.commit()

        flash("Category '{}' successfully edited and saved".format(category.name))
        return redirect(url_for('show_categories'))
    else:
        return render_template('edit_category.html', title='Edit category', body='Edit category', category=category)


@app.route('/categories/<category_id>/delete', methods=['GET', 'POST'])
def delete_category(category_id):
    category = Category.query.filter(Category.id == category_id)
    category_name = category.first().name
    category.delete()
    db.session.commit()

    flash("Category '{}' was deleted".format(category_name))
    return redirect(url_for('show_categories'))


@app.route('/')
@app.route('/index')
@app.route('/index/<page>')
def index(page=1):
    page_number = int(page)
    items = Item.query.paginate(page_number, ITEMS_PER_PAGE, False).items
    return render_template('index.html', title='List of items', body='List of items', items=items)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        password = request.form.get('password')
        password_hasher = HashService()
        hashed = password_hasher.generate_hash(password)
        username = request.form.get('username')
        email = request.form.get('email')

        user = User(username=username, email=email, password_hash=hashed)

        database_service = DatabaseService()
        user_exists = database_service.already_exists(User, User.username, username)
        email_exists = database_service.already_exists(User, User.email, email)

        template = "User with {} already exists. Please enter different value"

        if not user_exists and not email_exists:
            # save object in database
            database_service.add_to_db([user])

            # add token to session after successful registration
            add_access_token_in_session()

            return redirect('/')

        else:
            # something in form is not correct - show flash messages
            def flash_name():
                name_message = "username '{}'".format(username)
                flash(template.format(name_message))

            def flash_email():
                email_message = "email '{}'".format(email)
                flash(template.format(email_message))

            if user_exists and email_exists:
                flash_name()
                flash_email()

            elif user_exists:
                flash_name()

            else:
                flash_email()

            return redirect(url_for('register'))

    else:
        return render_template('register.html', title='Registration', body='Registration')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_hasher = HashService()

        update_session_values({'username': username})

        database_service = DatabaseService()
        user = database_service.get_object(User, User.username, username)
        password_hash = user.password_hash if user else ''
        password_checked = password_hasher.check_hash(password_hash, password)

        if user and password_checked:

            add_access_token_in_session()

            # TODO: implement scenario:
            #  user is not logged in and opens page that requires auth,
            #  redirect user to login page and after successful auth
            #  redirect back to the requested page (page that was requested before login)
            # url_after_login = request.args.get('next')

            # return redirect(url_after_login)
            return redirect(url_for('index'))

        elif not user:
            flash(f'User ( {username} ) is not registered. Please check correct username or register')

        elif not password_checked:
            flash('Password is not correct. Please check the password')

        return redirect(url_for('login'))

    else:
        return render_template('login.html', title='Log in', body='Log in')


@app.route('/logout')
@login_required
def logout():
    remove_session_key(['username', 'access_token'])
    flash('Logged out')
    return redirect(url_for('index'))
