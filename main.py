"""Изначально у меня было желание сделать все красиво и с доп приколами,
    но это построение задания заставило меня еще больше времемни потратить,
    проще было бы если бы нормально основную цель разложили, а не объясняли, что должен делать и хранить каждый отдельный
    метод, поле и тд, тильт"""
from abc import ABC, abstractmethod


class AbstractStorage(ABC):

    @abstractmethod
    def add(self, name, amount):
        pass

    @abstractmethod
    def remove(self, name, amount):
        pass

    @abstractmethod
    def get_free_space(self):
        pass

    @abstractmethod
    def get_items(self):
        pass

    @abstractmethod
    def get_unique_items_count(self):
        pass


class Storage(AbstractStorage):
    def __init__(self, items, capacity):
        self.items = items
        self.capacity = capacity

    def add(self, name, amount):
        for item in self.items:
            if name == item["name"]:
                item["amount"] += amount
                return ''
        self.items.append({"name": name, "amount": amount})

    def remove(self, name, amount):
        for item in self.items:
            if name == item["name"]:
                item["amount"] -= amount
        return False

    def get_free_space(self):
        return self.capacity - self._amount_of_items()

    def get_items(self):
        _dict = {}
        for item in self.items:
            _dict[item["name"]] = item["amount"]
        return _dict

    def get_unique_items_count(self):
        unique_count = 0
        for item in self.items:
            if item["amount"] == 1:
                unique_count += 1

    def _amount_of_items(self):
        amount = 0
        for i in self.items:
            amount += i["amount"]

        return amount


class Store(Storage):
    """
    items: [{'name': 'собака', 'amount': 2},{{'name': 'лед', 'amount': 3}},{}...]
    Есть ненужные функции, но я просто шел по шагам и в последнем шаге все переделывал, потому что в начале не особо понимал,
    что требуется
    """
    def __init__(self, items, capacity=100):
        self.items = items
        self.capacity = capacity

    def __repr__(self):
        return "склад"

    def add(self, name, amount):

        reply_text = f"Курьер доставил {amount} {name} в {self}\n"

        if not self._is_free_place(amount):
            amount = self.get_free_space()
            if amount == 0:
                return False, "Места 0, бб"
            reply_text += f"Места не хватало, поэтому поместилось только {amount} {name} в {self}\n"

        for item in self.items:
            if name == item["name"]:
                item["amount"] += amount
                return True, reply_text
        self.items.append({"name": name, "amount": amount})
        reply_text += f"У нас не было такого товара на {self}, но теперь он есть! Ура! Ура! Ура!\n"
        return True, reply_text

    def remove(self, name, amount):

        for item in self.items:
            if name == item["name"]:
                if amount <= item["amount"]:
                    item["amount"] -= amount
                    return True, f"Курьер забрал {amount} {name} со {self}"
                else:
                    return False, f"Запрашиваемое кол-во больше, чем есть на {self}"
        return False, f"Нет товара на {self}"

    def get_free_space(self):
        return self.capacity - self._amount_of_items()

    def get_items(self) -> dict:

        _dict = {}
        for item in self.items:
            _dict[item["name"]] = item["amount"]
        return _dict

    def get_items_repr(self):
        """pretty items info"""
        reply = f'В {self} хранится:\n\n'
        _dict = self.get_items()
        for k, v in _dict.items():
            reply += f'{v} {k}\n'
        return reply

    def get_unique_items_count(self):
        """za4em eto nado bilo"""
        unique_count = 0
        for item in self.items:
            if item["amount"] == 1:
                unique_count += 1

    def _is_free_place(self, value) -> bool:
        if self.get_free_space() >= value:
            return True
        else:
            return False

    def _amount_of_items(self):
        """сумма кол-ва всех товаров"""
        amount = 0
        for i in self.items:
            amount += i["amount"]

        return amount


class Shop(Storage):
    def __init__(self, items, capacity=20):
        self.capacity = capacity
        self.items = items

    def __repr__(self):
        return "магазин"

    def add(self, name, amount):
        reply_text = f"Курьер доставил {amount} {name} в {self}\n"
        if not self._is_free_place_capacity(amount):
            amount = self.get_free_space()
            if amount == 0:
                return False, "Места 0, бб"
            reply_text += f"Места не хватало, поэтому поместилось только {amount} {name} в {self}\n"

        for item in self.items:
            if name == item["name"]:
                item["amount"] += amount
                return True, reply_text
        if self._is_free_place_items(): # Проверка, чтобы не было больше 5 различных товаров
            self.items.append({"name": name, "amount": amount})
            reply_text += f"У нас не было такого товара на {self}, но теперь он есть! Ура! Ура! Ура!\n"
            return True, reply_text
        else:
            reply_text = f"не можем хранить СТОЛЬКО различных товаров, извиите -><-"
            return False, reply_text

    def remove(self, name, amount):

        for item in self.items:
            if name == item["name"]:
                if amount <= item["amount"]:
                    item["amount"] -= amount
                    return True, f"Курьер забрал {amount} {name} со {self}"
                else:
                    return False, f"Запрашиваемое кол-во больше, чем есть в {self}"
        return False, f"Нет товара в {self}"

    def get_free_space(self):
        return self.capacity - self._amount_of_items()

    def get_items(self):
        _dict = {}
        for item in self.items:
            _dict[item["name"]] = item["amount"]
        return _dict

    def get_items_repr(self):
        reply = f'В {self} хранится:\n\n'
        _dict = self.get_items()
        for k, v in _dict.items():
            reply += f'{v} {k}\n'
        return reply

    def get_unique_items_count(self):
        unique_count = 0
        for item in self.items:
            if item["amount"] == 1:
                unique_count += 1

    def _is_free_place(self, value):
        return self._is_free_place_items(), self._is_free_place_capacity(value)

    def _is_free_place_items(self):
        """Проверка, чтобы не было больше 5 различных товаров"""
        return len(self.items) < 5

    def _is_free_place_capacity(self, value):
        if self.get_free_space() >= value:
            return True
        else:
            return False

    def _amount_of_items(self):
        amount = 0
        for i in self.items:
            amount += i["amount"]

        return amount


class Request:
    def __init__(self, store_obj, shop_obj, deliver_str, from_=None, to=None):
        query_list = deliver_str.split()
        if from_ is None and to is None:
            self.from_, self.to = self.real_names(query_list[4], query_list[-1],
                                                  {"склад": store_obj, "магазин": shop_obj}
                                                  )
        self.amount = int(query_list[1])
        self.product = query_list[2]


    def real_names(self, from_, to, obj_dict):
        """Нужна, если при инициализации экземпляра не передаются from_, to,
                 тогда приходится узнавать из передаваемой строки"""
        for k, v in obj_dict.items():
            if k == from_:
                from_ = v
            if k == to:
                to = v
        return from_, to

    def process(self):
        remove = self.from_.remove(self.product, self.amount)
        add = self.to.add(self.product, self.amount)
        print(remove[1])
        if not remove[0]:
            print('Попробуйте с другими данными')
            return
        print(add[1])
        if not add[0]:
            print('Попробуйте с другими данными')
        print(f"{self.from_.get_items_repr()}\n{self.to.get_items_repr()}")


if __name__ == '__main__':
    shop = Shop(items=[{'name': 'собака', 'amount': 2}, {'name': 'леденец', 'amount': 3}, {'name': 'чебурек', 'amount': 2}])  # инициализация магазин
    store = Store(items=[{'name': 'собака', 'amount': 30}, {'name': 'лед', 'amount': 3}])  # инициализация склад
    yes = Request(store, shop, 'Доставить 2 чебурек из магазин в склад')  # важно сохранять структуру,
    # писать только "склад" и "магазин",
    # другие окончания работать не будут
    yes.process()  # после ввода всех данных, просто запустите его

