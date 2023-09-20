##------
# Code last modified by Chris Dancy @ Penn State (2023-Feb)
#  from codebase written by Terry Stewart @ University of Waterloo
# Builds environment grid-like environment and creates a vacuum agent to clean up "mud"
##------


from AgentSupport import MotorModule, CleanSensorModule, MyCell
import AgentSupport
import python_actr
from python_actr.lib import grid
import random

class VacuumAgent(python_actr.ACTR):
	goal = python_actr.Buffer()
	body = grid.Body()
	motorInst = MotorModule()
	cleanSensor = CleanSensorModule()

	def init(): # Initialize agent
		goal.set("rsearch left 1 0 1") # Initial short-term memory
		self.home = None

	#----ROOMBA----#

	def clean_cell(cleanSensor="dirty:True", motorInst="busy:False", utility=0.6):
		motorInst.clean()

	def forward_rsearch(goal="rsearch left ?dist ?num_turns ?curr_dist",
						motorInst="busy:False", body="ahead_cell.wall:False"): # Check if goal buffer has slot values of "rsearch' and "left"
		motorInst.go_forward()
		print(body.ahead_cell.wall)
		curr_dist = str(int(curr_dist) - 1) # curr_dist var created from "?curr_dist" slot in the condition; change to adjust goal state
		goal.set("rsearch left ?dist ?num_turns ?curr_dist")

	def left_rsearch(goal="rsearch left ?dist ?num_turns 0", motorInst="busy:False",
					utility=0.1):
		motorInst.turn_left(2)
		num_turns = str(int(num_turns) + 1)
		dist = str(int(dist) + 1) # NEW wait it actually worked
		goal.set("rsearch left ?dist ?num_turns ?dist")



		###Other stuff!


world=grid.World(MyCell,map=AgentSupport.mymap)
agent=VacuumAgent()
agent.home=()
world.add(agent,5,5,dir=0,color="black")

python_actr.log_everything(agent, AgentSupport.my_log)
python_actr.display(world)
world.run()
