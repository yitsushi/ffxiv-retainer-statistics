import hashlib

class Item(object):
  id = None
  recipe_id = None
  job = None
  level = None
  name = None
  ingredients = None
  properties = None

  def __init__(self):
    self.ingredients = {}
    self.properties = {
      'quantity': 1,
      'durability': 0,
      'difficulty': 0,
      'max_quality': 0
    }

  def to_array(self):
    return []

  def add_ingredient(self, id, quantity):
    self.ingredients[id] = quantity

  def set_property(self, key, value):
    self.properties[key] = value

  def from_db_row(item):
    current = Item()
    (
        current.id,
        current.job,
        current.recipe_id,
        current.level,
        current.name,
        current.properties['quantity'],
        current.properties['durability'],
        current.properties['difficulty'],
        current.properties['max_quality']
    ) = item[1:]

    return current
