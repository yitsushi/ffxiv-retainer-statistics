import hashlib

class SellItem:
    id = None
    name = None
    quantity = None
    isHQ = False
    price = None
    date = None
    buyer = None
    retainer = None
    character = None

    def __init__(self, row, character, retainer):
        self.character = character
        self.retainer = retainer

        name = row.find('p', attrs={'class': 'item-list__name'})
        img = name.find('img')
        self.isHQ = (img is not None)
        (self.name, self.quantity) = [n.strip('()\t ') for n in name.text.strip().split('\n') if n.strip() != '']
        self.quantity = int(self.quantity)

        self.price = int(row.find('div', attrs={'class': 'item-list__item item-list__cell--sm'}).text.replace(',', ''))
        self.date = int(row.find('span')['data-epoch'])
        self.buyer = row.find('div', attrs={'class': 'item-list__item item-list__cell--md'}).text

        base = f'{self.name}|{self.buyer}'
        self.id = "{0}{1}".format(hashlib.sha256(base.encode()).hexdigest(), self.date)

    def to_array(self):
      return [
        self.id, self.name, self.quantity, self.isHQ,
        self.price, self.date, self.buyer,
        self.retainer, self.character
      ]
