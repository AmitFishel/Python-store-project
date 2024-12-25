from item import Item
import errors


class ShoppingCart:
    def __init__ (self) :
        self.items = [] #Create a list contain all the self item that already in the shopping chart. 

    def add_item(self, item: Item):
        # TODO: Complete
        if item in self.items : #The item is already in the list.
            raise errors.ItemAlreadyExistsError("The item is already in the shopping chart.")
        else:  #Otherwise we want to add this item to the chart.
            self.items.append(item) #we doing append so it will be add to the end of the list.
    
    # We will create a add function that will create a list that will contain all the names that the chart shopping contain.
    def name_in_cart(self):
        names_list = []
        for item in self.items :
            names_list.append(item.name) #pass all the list's items and add their names to the new list.
        return names_list
           
    def remove_item(self, item_name: str):
        # TODO:complete
        #If item is not tn the cart we canr remove it. throw error.
        if item_name not in self.name_in_cart():
            raise errors.ItemNotExistError("There is no item with this name in the shopping chart")
        else:
            for item in self.items:
                if item.name == item_name:
                    self.items.remove(item)
                    break #After finding the item in the list and remobe it stop running the loop
        

    def get_subtotal(self) -> int:
        # TODO: Complete
        #Sum all the prices of all the item's that in the list.
        sum_prices = 0
        for item in self.items:
            sum_prices += item.price 

        return sum_prices    
    
    #Add function to help.
    def get_items(self):
      return self.items
        
