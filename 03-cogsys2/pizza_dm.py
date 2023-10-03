# import python_actr module library for Python ACT-R classes
import python_actr
from python_actr.actr import *
from python_actr.actr.hdm import *



class PizzaBuilder_DM(ACTR):
    goal = Buffer()
    retrieval = Buffer()
    DM_module = HDM(retrieval,finst_size=22,finst_time=100.0) # Added finst_size=22,finst_time=100.0 parameters
    my_pizza = []

    def cook_pizza(self, pizza_ingred):
        '''
        Takes in list of "ingredients" and outputs a "pizza"
        Inputs: pizza_ingred [list of strings]
        Output: cooked_pizza [string]
        '''
        # Whats going on here? - https://docs.python.org/3/library/stdtypes.html#str.join
        return ("_".join(pizza_ingred))

    def init():
        # Add memory chunks to declarative memory module
        DM_module.add("prev:prep next:crust")
        DM_module.add("prev:crust next:bbq")
        DM_module.add("prev:bbq next:cheddar")
        DM_module.add("prev:cheddar next:bacon")
        DM_module.add("prev:bacon next:onion")
        DM_module.add("prev:crust next:marinara")
        DM_module.add("prev:marinara next:mozzarella")
        DM_module.add("prev:mozzarella next:pepperoni")
        DM_module.add("prev:pepperoni next:onion") # Given
        # Set goal so that we can prep ingredients
        goal.set("start_pizza")

    def prep_ingredients(goal="start_pizza"):
        # Start building our pizza!
        goal.set("build_pizza")
        # Request next step from DM
        DM_module.request("prev:prep next:?next_ingred") # Need retrieval
        
    ###Rules to request from declarative memory for next step/ingredient and place that ingredient on your pizza and make sure you can more on to cooking pizza
    def add_toppings(goal="build_pizza", retrieval="prev:?x next:?next_ingred!onion"): # Slot name != value
        my_pizza.append(next_ingred)
        # Request next step from DM
        DM_module.request("prev:?next_ingred next:?y")
    
    # Last step: onion, then cook
    def add_onion(goal="build_pizza", retrieval="prev:?x next:onion"):
        my_pizza.append("onion")
        goal.set("cook_pizza")

    def cook_pizza_step(goal="cook_pizza"):
        my_pizza = self.cook_pizza(my_pizza)
        print("Mmmmmm my " + my_pizza + " pizza is gooooood!")
        self.stop()

class EmptyEnvironment(python_actr.Model):
    pass

env_name = EmptyEnvironment()
agent_name = PizzaBuilder_DM()
env_name.agent = agent_name
python_actr.log_everything(env_name)
env_name.run()