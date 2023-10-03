# import python_actr module library for Python ACT-R classes
import python_actr
from python_actr.actr import *
from python_actr.actr.hdm import *



class PizzaBuilder_DM(ACTR):
    goal = Buffer()
    retrieval = Buffer()
    DM_module = Memory(retrieval) # Changed from HDM(retrieval) to stop infinite loop (DM_module was always busy, couldn't request DM)
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
        goal.set("build_pizza done:prep new:any")
        # Request next step from DM
        DM_module.request("prev:prep next:?next_ingred") # Need retrieval to activate add_toppings rule
        
    ###Rules to request from declarative memory for next step/ingredient and place that ingredient on your pizza and make sure you can move on to cooking pizza
    def add_toppings(goal="build_pizza done:?a new:?b", retrieval="prev:?x next:?next_ingred!onion"): # Slot name should not be the same as the value!
        # Goal: takes any values for done and new
        # Retrieval: takes any value for prev, any value except onion for next
        my_pizza.append(next_ingred)
        # Request next step from DM 
        DM_module.request("prev:?next_ingred next:?y") # Specifies prev as the current "next" ingredient, looks for new "next" (y acts as a placeholder)
        # Update goal buffer
        goal.modify(done=next_ingred) # The original "next" value is now the previous after the rule execution
    
    # Last step: onion, then cook
    def add_onion(goal="build_pizza done:?a new:?b", retrieval="prev:?x next:onion"):
        # Will activate when the memory request returns onion as the value for next
        my_pizza.append("onion")
        # Changes goal to initiate the last rule
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