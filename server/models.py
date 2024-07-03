#These lines import necessary tools from SQLAlchemy and Flask to create database models, handle relationships, perform validations,
#  and serialize models to JSON.
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates,relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
'''This is a template for naming foreign keys.
fk_: The prefix fk_ indicates that this is a foreign key.
%(table_name)s: This placeholder will be replaced by the name of the table that contains the foreign key.
%(column_0_name)s: This placeholder will be replaced by the name of the column in the table that holds the foreign key.
%(referred_table_name)s: This placeholder will be replaced by the name of the table that the foreign key refers to.
'''
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
# metadata is a class from SQLAlchemy
# it keeps track of all the tables and their relationships in your database.
#Creates an instance of SQLAlchemy with the custom metadata, allowing us to define our models.

db = SQLAlchemy(metadata=metadata)


class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    hero_powers = relationship('HeroPower', back_populates='hero', cascade='all, delete-orphan')
    

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name
        }

    def __repr__(self):
        return f'<Hero {self.id}>'


class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    hero_powers = relationship('HeroPower', back_populates='power', cascade='all, delete-orphan')
    
    @validates('description')
    def validate_description(self, key, description):
        if not description or len(description) < 20:
            raise ValueError("Description must be at least 20 characters long")
        return description
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }


    def __repr__(self):
        return f'<Power {self.id}>'


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)

    
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))  # Foreign key to Hero
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))  # Foreign key to Power

    hero = relationship('Hero', back_populates='hero_powers')
    power = relationship('Power', back_populates='hero_powers')

    @validates('strength')
    def validate_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Strength must be one of 'Strong', 'Weak', or 'Average'")
        return strength


    def __repr__(self):
        return f'<HeroPower {self.id}>'
    
    

