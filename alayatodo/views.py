from alayatodo import app
from flask import (
    g,
    redirect,
    render_template,
    request,
    session,
    jsonify,
    flash,
    url_for
    )
from alayatodo.models import db, Users, Todos


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l.decode('utf-8') for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')
    user = Users.query.filter_by(username=username, password=password).first()
    if user:
        session['user'] = {field.name: getattr(user, field.name) for field in user.__table__.columns}
        session['logged_in'] = True
        return redirect('/todo')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    if not session.get('logged_in'):
        return redirect('/login')
    todo = Todos.query.filter_by(id=id, user_id=session['user']['id']).first()

    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1

    return render_template('todo.html', todo=todo, page=page)


@app.route('/todo/<id>/json', methods=['GET'])
def todo_JSON(id):
    if not session.get('logged_in'):
        return redirect('/login')
    todo = Todos.query.filter_by(id=id, user_id=session['user']['id']).first()
    return jsonify({field.name: getattr(todo, field.name) for field in todo.__table__.columns})


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')

    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1

    pagination = Users.query.get(session['user']['id']).todos.paginate(page, 8)
    todos = pagination.items

    return render_template('todos.html',
                           todos=todos,
                           pagination=pagination,
                           )


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')
    description = request.form.get('description', '').strip(' ')
    if len(description) >= 1:
        db.session.add(Todos(user_id=session['user']['id'], description=description))
        db.session.commit()
    flash('Todo created !')
    return redirect('/todo')


@app.route('/todo/complete/<id>', methods=['POST'])
def todo_complete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    completed = 1 if request.form.get('todo-completed') else 0
    todo = Todos.query.filter_by(id=id, user_id=session['user']['id']).first()
    todo.completed = completed
    db.session.commit()

    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1

    return redirect(url_for('todos', page=page))



@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    todo = Todos.query.filter_by(id=id, user_id=session['user']['id']).first()
    db.session.delete(todo)
    db.session.commit()
    flash('Todo deleted !')

    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1

    return redirect(url_for('todos', page=page))
