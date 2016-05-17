from alayatodo import db


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column( db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    todos = db.relationship('Todos', backref='owner', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


class Todos (db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column('description', db.String(255), nullable=False)
    completed = db.Column('completed', db.Integer)

    def __init__(self, user_id, description):
        self.user_id = user_id
        self.description = description

    def __repr__(self):
        return '<description %r>' % self.description
