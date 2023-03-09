import os
import json
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Drop and create tables
# -----------------------------------------------------------------------
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    add_some_example_data()


# Add some example data
# -----------------------------------------------------------------------
def add_some_example_data():
    drinks = [
     {
       "title": "Soda Water",
       "recipe": [{"name": "Carbonated water", "color": "cyan", "parts": 1}]
     },
     {
       "title": "Summer Coffee",
       "recipe": [
        {"name": "Cream", "color": "#F9F5E7", "parts": 6},
        {"name": "Evaporated milk", "color": "#F9DBBB", "parts": 2},
        {"name": "Espresso", "color": "#A75D5D", "parts": 2}
        ]
     },
     {
       "title": "Fruit Cola",
       "recipe": [
        {"name": "Multifruit juice", "color": "#FFB84C", "parts": 1},
        {"name": "Cola", "color": "#804674", "parts": 1}
        ]
     }
    ]

    for d in drinks:
        drink = Drink(
             title=d['title'],
             recipe=json.dumps(d['recipe'])
            )
        drink.insert()


class Drink(db.Model):
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    title = Column(String(80), unique=True)

    # json string
    # example: "[{'color': string, 'name':string, 'parts':number}]"
    recipe = Column(String(), nullable=False)

    def short(self):
        print(json.loads(self.recipe))
        short_recipe = [
                         {'color': r['color'], 'parts': r['parts']}
                         for r in json.loads(self.recipe)
                        ]

        return {
            'id': self.id,
            'title': self.title,
            'recipe': short_recipe
        }

    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'recipe': json.loads(self.recipe)
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())
