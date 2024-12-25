import yaml

from item import Item
from shopping_cart import ShoppingCart
import errors


class Store:
    def __init__(self, path):
        with open(path) as inventory:
            items_raw = yaml.load(inventory, Loader=yaml.FullLoader)['items']
        self._items = self._convert_to_item_objects(items_raw)
        self._shopping_cart = ShoppingCart()

    @staticmethod
    def _convert_to_item_objects(items_raw):
        return [Item(item['name'],
                     int(item['price']),
                     item['hashtags'],
                     item['description'])
                for item in items_raw]

    def get_items(self) -> list:
        return self._items
    
       
    def search_by_name(self, item_name: str) -> list:
    # Get all items currently in the shopping cart
        cart_items = {item.name for item in self._shopping_cart.get_items()}

    # Filter items in the store by name and ensure they are not in the shopping cart
        all_matches_items = [
            item for item in self._items 
            if item_name in item.name and item.name not in cart_items
        ]

    # Get all hashtags from the current shopping cart
        cart_tags = [tag for item in self._shopping_cart.get_items() for tag in item.hashtags]

        if not cart_tags:
        # If empty, sort only by name
            return sorted(all_matches_items, key=lambda item: item.name)

        def common_hashtag_count(item):
            # Sum the counts of each tag in item.hashtags and save their counts in cart_tags
            return sum(cart_tags.count(tag) for tag in item.hashtags)

        # Sort the items first by the number of common hashtags (descending),
        # and then by name (lexicographic order)
        sorted_items = sorted(
            all_matches_items,
            key = lambda item: (-common_hashtag_count(item), item.name)
        )

        return sorted_items



    def search_by_hashtag(self, hashtag: str) -> list:
        # TODO: Complete
        cart_items = {item.name for item in self._shopping_cart.get_items()} #create a set of all the items we have in the shopping chart.
        
        #Find all the items that contain the input hashtag and checking that this items not already in the cart. making a list of them.
        all_matches_items = [item for item in self._items
                          if hashtag in item.hashtags and item.name not in cart_items]
        
        #Create a list that contain all the hashtags of all the item un the shopping cart.
        cart_tags = [tag for item in self._shopping_cart.get_items() for tag in item.hashtags] 

        #Add function to count the common hashtags dor each item.
        def common_hashtag_count(item) :
            return sum(tag in cart_tags for tag in item.hashtags)
        
        sorted_items = sorted(all_matches_items, key = lambda item : (-common_hashtag_count(item), item.name))

        return sorted_items

                

    def add_item(self, item_name: str):
    # Find items in the store whose names contain the substring 'item_name'
        all_matches_items = [item for item in self._items if item_name in item.name]

        # If no matching items are found, raise an error
        if len(all_matches_items) == 0:
            raise errors.ItemNotExistError(f"item '{item_name}' does not exist")
        # If multiple matching items are found, raise an error
        elif len(all_matches_items) > 1:
            raise errors.TooManyMatchesError(f"there are multiple items matching the name '{item_name}'")

        # The matching item to add
        item_to_add = all_matches_items[0]

        # Check if the item is already in the shopping cart
        cart_items = self._shopping_cart.get_items()
        if any(cart_item.name == item_to_add.name for cart_item in cart_items):
            raise errors.ItemAlreadyExistsError(f"item '{item_to_add.name}' is already in the cart")

        # If everything ok add the item to the shopping cart
        self._shopping_cart.add_item(item_to_add)




    def remove_item(self, item_name: str):
        # Find items in the shopping cart whose names contain the substring 'item_name'
        cart_items = self._shopping_cart.get_items()
        all_matches_items = [item for item in cart_items if item_name in item.name]

        # If no matching items are found, raise an error
        if len(all_matches_items) == 0:
            raise errors.ItemNotExistError(f"item '{item_name}' does not exist in the shopping cart")
        # If multiple matching items are found, raise an error
        elif len(all_matches_items) > 1:
            raise errors.TooManyMatchesError(
                f"there are multiple items matching the name '{item_name}' in the shopping cart"
            )

        # The matching item to remove
        item_to_remove = all_matches_items[0]

        # Remove the item from the shopping cart
        self._shopping_cart.remove_item(item_to_remove.name)


    def checkout(self) -> int:
        # TODO: Completefor item in 
        #return sum(item.price for item in self._shopping_cart.get_items())

        sum_prices = 0 
        
        #pass on all the items in the self.cart.items and add their prices.
        for item in self._shopping_cart.get_items() :
             sum_prices += item.price 

        return sum_prices
      
