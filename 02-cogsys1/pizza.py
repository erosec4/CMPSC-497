# import python_actr module library for Python ACT-R classes
import python_actr
from python_actr.actr import *


class PizzaBuilder(ACTR):
	goal = Buffer()
	my_pizza = []

	def cook_pizza(self, pizza_ingred):
		'''
		Takes in list of "ingrediants" and outputs a "pizza"
		Inputs: pizza_ingred [list of strings]
		Output: cooked_pizza [string]
		'''
		# Whats going on here? - https://docs.python.org/3/library/stdtypes.html#str.join
		return ("_".join(pizza_ingred))

	def init():
		goal.set("build_pizza prep")

	def prep_ingredients(goal="build_pizza prep"):
		#start building our sandwich!
		goal.set("build_pizza thincrust")

	def place_crust(goal="build_pizza ?crust"):
		#Place the crust
		my_pizza.append("thincrust")
		goal.set("build_pizza prev:crust next:sauce")

    # Path 1
	def place_sauce_pepperoni(goal="build_pizza prev:crust next:sauce"): #utility=0.1
		my_pizza.append("sauce")
		goal.set("build_pizza prev:sauce next:mozzarella")

    # Path 2
	def place_sauce_bbq(goal="build_pizza prev:crust next:sauce"):
		my_pizza.append("bbq")
		goal.set("build_pizza prev:bbq next:cheddar")

    # Path 1 mozzarella
	def place_mozzarella(goal="build_pizza prev:sauce next:mozzarella"):
		my_pizza.append("mozzarella")
		goal.set("build_pizza prev:mozzarella next:pepperoni")

    # Path 2 cheddar
	def place_cheddar(goal="build_pizza prev:bbq next:cheddar"):
		my_pizza.append("cheddar")
		goal.set("build_pizza prev:cheddar next:onion")

    # Path 1 topping
	def place_pepperoni(goal="build_pizza prev:mozzarella next:pepperoni"):
		# Should place pepperoni, then move on to placing onions
		my_pizza.append("pepperoni")
		goal.set("build_pizza prev:pepperoni next:onion")

    # Topping for both Path 1 and Path 2
	def place_onions(goal="build_pizza prev:? next:onion"):
		# Should place onions then move on to cooking the pizza
		my_pizza.append("onion")
		goal.set("cook_pizza prev:onion next:cook")

	def place_cook_pizza(goal="cook_pizza"):
		my_pizza = self.cook_pizza(my_pizza)
		print("Mmmmmm my " + my_pizza + " pizza is gooooood!")
		self.stop()
		


class EmptyEnvironment(python_actr.Model):
	pass

env_name = EmptyEnvironment()
agent_name = PizzaBuilder()
env_name.agent = agent_name
python_actr.log_everything(env_name)
env_name.run()