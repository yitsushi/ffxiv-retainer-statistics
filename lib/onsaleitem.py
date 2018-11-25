import hashlib

class OnSaleItem:
    name = None
    quantity = None
    isHQ = False
    price = None
    retainer = None
    character = None

    def __init__(self, row, character, retainer):
        self.character = character
        self.retainer = retainer

        name = row.find('div', attrs={'class': 'item-list__name'})
        img = name.find('img', attrs={'class': 'ic_item_quality'})
        self.isHQ = (img is not None)
        self.name = name.find('a').text.strip('\n\r\t ')

        numbers = row.find_all('div', attrs={'class': 'item-list__item item-list__cell--sm'})
        self.price = int(numbers[0].text.replace(',', ''))
        self.quantity = int(numbers[1].text)
