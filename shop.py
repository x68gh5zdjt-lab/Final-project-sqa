"""
Ironveil Trading Post — shop.py
A simple RPG inventory and shop system.

Students: DO NOT MODIFY THIS FILE.
Your job is to break it, not fix it.
"""


class Item:
    def __init__(self, name, price, item_type, damage=0, defense=0):
        self.name = name
        self.price = price
        self.item_type = item_type  # "weapon", "armor", "potion"
        self.damage = damage
        self.defense = defense

    def __repr__(self):
        return f"Item({self.name}, {self.price}g)"


class Player:
    def __init__(self, name, gold=100):
        self.name = name
        self.gold = gold
        self.inventory = []
        self.equipped_weapon = None
        self.equipped_armor = None
        self.health = 100
        self.max_health = 100

    def use_potion(self):
        """Use the first potion found in inventory."""
        for item in self.inventory:
            if item.item_type == "potion":
                self.inventory.remove(item)
                self.health += 30
                return f"{self.name} used {item.name}. Health: {self.health}"
        return "No potions in inventory."

    def equip(self, item_name):
        """Equip a weapon or armor from inventory."""
        for item in self.inventory:
            if item.name == item_name:
                if item.item_type == "weapon":
                    self.equipped_weapon = item
                    return f"Equipped {item.name}"
                elif item.item_type == "armor":
                    self.equipped_armor = item
                    return f"Equipped {item.name}"
        return "Item not found in inventory."

    def get_stats(self):
        dmg = self.equipped_weapon.damage if self.equipped_weapon else 0
        defense = self.equipped_armor.defense if self.equipped_armor else 0
        return {"name": self.name, "gold": self.gold, "health": self.health,
                "damage": dmg, "defense": defense}


class Shop:
    def __init__(self, name):
        self.name = name
        self.stock = {}      # item_name -> Item
        self.transaction_log = []

    def add_stock(self, item, quantity):
        """Add items to shop stock."""
        if item.name in self.stock:
            self.stock[item.name]["quantity"] += quantity
        else:
            self.stock[item.name] = {"item": item, "quantity": quantity}

    def buy(self, player, item_name, quantity=1):
        """Player buys item(s) from the shop."""
        if item_name not in self.stock:
            return "Item not available."

        entry = self.stock[item_name]
        item = entry["item"]

        if entry["quantity"] < quantity:
            return "Not enough stock."

        total_cost = item.price * quantity

        if player.gold < total_cost:
            return "Not enough gold."

        player.gold -= total_cost
        entry["quantity"] -= quantity

        for _ in range(quantity):
            player.inventory.append(item)

        self.transaction_log.append({
            "type": "buy",
            "player": player.name,
            "item": item_name,
            "quantity": quantity,
            "total": total_cost
        })

        return f"Bought {quantity}x {item_name} for {total_cost}g."

    def sell(self, player, item_name, quantity=1):
        """Player sells item(s) to the shop."""
        sell_price = None
        items_to_sell = []

        for inv_item in player.inventory:
            if inv_item.name == item_name:
                items_to_sell.append(inv_item)
                sell_price = inv_item.price // 2

        if len(items_to_sell) < quantity:
            return "You don't have enough of that item."

        for i in range(quantity):
            player.inventory.remove(items_to_sell[i])

        total = sell_price * quantity
        player.gold += total

        self.transaction_log.append({
            "type": "sell",
            "player": player.name,
            "item": item_name,
            "quantity": quantity,
            "total": total
        })

        return f"Sold {quantity}x {item_name} for {total}g."

    def apply_discount(self, item_name, percent):
        """Apply a percentage discount to an item's price (e.g. 20 = 20% off)."""
        if item_name not in self.stock:
            return "Item not found."
        original = self.stock[item_name]["item"].price
        self.stock[item_name]["item"].price = original - (original * percent / 100)
        return f"Discount applied. New price: {self.stock[item_name]['item'].price}g"

    def get_inventory_value(self, player):
        """Return the total sell value of a player's inventory."""
        total = 0
        for item in player.inventory:
            total += item.price // 2
        return total

    def transfer_item(self, sender, receiver, item_name):
        """Transfer an item between two players."""
        for item in sender.inventory:
            if item.name == item_name:
                sender.inventory.remove(item)
                receiver.inventory.append(item)
                return f"Transferred {item_name} from {sender.name} to {receiver.name}."
        return "Item not found on sender."
