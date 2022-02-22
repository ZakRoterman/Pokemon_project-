from app import db, login
from flask_login import UserMixin 
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash

class PokeUserJoin(db.Model):
    pokeparty_id = db.Column(db.Integer, db.ForeignKey('pokeparty.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    def remove(self):
        db.session.delete(self)
        db.session.commit()

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default = dt.utcnow)
    wins = db.Column(db.Integer, default = 0)
    losses = db.Column(db.Integer, default = 0)
    team = db.relationship(
        'PokeParty',
        secondary = 'poke_user_join',
        backref= 'users',        
        lazy='dynamic'
    )
    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'
    
    def hash_password(self, original_password):
        return generate_password_hash(original_password)
    
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def collect_poke(self, poke):
        self.team.append(poke)
        db.session.commit()
        
    def add_to_team(self, Obj):
        if len(list(self.team)) <= 5:
            self.team.append(Obj)
            self.save()

    def remove_from_team(self, Obj):
        if len(list(self.team)) > 0:
            self.team.remove(Obj)
            self.save()

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])
        self.wins = 0
        self.losses = 0

    def total_attack(self):
        total = []
        for pokemon in self.team:
            total.append(int(pokemon.attack))
            attack_total = sum(total)
            return str(attack_total)

    def save(self):
        db.session.add(self) 
        db.session.commit() 

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class PokeParty(db.Model):
    __tablename__ = 'pokeparty'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    hp = db.Column(db.String(50))
    defense = db.Column(db.String(50))
    attack = db.Column(db.String(50))
    ability_1 = db.Column(db.String(50))
    sprite = db.Column(db.String(500))
    
    def __repr__(self):
        return f'<Pokemon: {self.id} | {self.name}>'

    def from_dict(self, data):
        self.name = data['name']
        self.hp = data['hp']
        self.defense = data['defense']
        self.attack = data['attack']
        self.ability_1 = data['ability_1']
        self.sprite = data['sprite']

    def save(self):
        db.session.add(self) 
        db.session.commit() 

    def exists(name):
         return PokeParty.query.filter_by(name=name).first()

    def delete(self):
        db.session.delete(self) 
        db.session.commit() 
        