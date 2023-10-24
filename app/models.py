from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
db = SQLAlchemy()



class HeroPower(db.Model,SerializerMixin):
    __tablename__ = 'heropower'
    serialize_rules = ('-hero.powers', '-power.heroes',)
    id = db.Column(db.Integer,primary_key=True)
    strength = db.Column(db.String())
    hero_id = db.Column( db.Integer, db.ForeignKey('heros.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    created_at = db.Column(db.DateTime,default = datetime.utcnow())
    updated_at = db.Column(db.DateTime,default = datetime.utcnow(),onupdate=datetime.utcnow())

    @validates('strength')
    def validates_strength(self,key,strength):
        strengths = ['Strong','Weak','Average']
        if strength not in strengths:
            raise ValueError('Strength must be one of the following values: Strong, Weak, Average')
        return strength


class Hero(db.Model,SerializerMixin):
    __tablename__ = 'heros'

    serialize_rules = ('-powers.hero',)
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String())
    super_name= db.Column(db.String())
    created_at = db.Column(db.DateTime(),default = datetime.utcnow())
    updated_at = db.Column(db.DateTime(),default=datetime.utcnow(),onupdate=datetime.utcnow())
    
    powers = db.relationship("HeroPower",backref= "hero")

 
class Power(db.Model,SerializerMixin):
    __tablename__ = 'powers'

    serialize_rules = ('-heroes.power')
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    created_at = db.Column(db.DateTime(),default = datetime.utcnow())
    updated_at = db.Column(db.DateTime(),default=datetime.utcnow(),onupdate=datetime.utcnow())
    #relationship
    heroes = db.relationship("HeroPower",backref= "power")

    @validates('description')
    def validates_description(self,key,description):
        if len(description) < 20:
            raise ValueError('Description must be at least 20 characters long')
        return description
    