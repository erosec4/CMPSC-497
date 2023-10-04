##------
# Code last modified by Chris Dancy @ Penn State (2023-Sept)
#  from codebase written by Terry Stewart @ University of Waterloo
# Builds environment grid-like environment and creates a vacuum agent to clean up "mud"
##------


from AgentSupport import MotorModule, CleanSensorModule, MyCell
import AgentSupport
import python_actr
from python_actr.lib import grid
from python_actr.actr import *
from python_actr.actr.hdm import *
import random
import time

class VacuumAgent(python_actr.ACTR):
	goal = python_actr.Buffer()
	body = grid.Body()
	motorInst = MotorModule()
	cleanSensor = CleanSensorModule()
	retrieval = Buffer()
	#Finst number and time should be plenty for us to keep things simple (even if theoretically impractical!)
	DM_module = Memory(retrieval,finst_size=22,finst_time=100.0) # Default: finst_size=5, finst_time=10.0

	def init():
		# Runs when new VacuumAgent object is instantiated
		goal.set("start_recall_dirt")
		self.home = None
		DM_module.request("square:dirty location_x:?x location_y:5")

	#----ROOMBA----#
	
	def recall_dirty_spots_dm(goal="start_recall_dirt", retrieval="square:dirty location_x:?x location_y:?y", 
						   motorInst="busy:False"):
		# Go towards and clean dirty spot in memory
		motorInst.go_towards(int(x), int(y))
		DM_module.request("square:dirty location_x:?newx location_y:?newy",require_new=True)
		pass

	# If nothing in DM, begin swirling pattern
	def begin_swirl(goal="start_recall_dirt", DM_module="busy:False error:True"):
		# Change goal to start swirl pattern
		goal.set("rsearch left 1 0 1")

	#----ROOMBA----#

	def clean_cell(cleanSensor="dirty:True"): # Called when sensor finds a dirty spot
		# Add x and y of dirty spot to DM
		x = str(body.x)
		y = str(body.y)
		# Create and add chunk containing x and y location to DM
		chunk = f"square:dirty location_x:{x} location_y:{y}"
		DM_module.add(chunk)
		motorInst.clean()
		print(self.DM_module.dm) # Check the chunks in DM

	def forward_rsearch(goal="rsearch left ?dist ?num_turns ?curr_dist",
						motorInst="busy:False", body="ahead_cell.wall:False"): # Check if goal buffer has slot values of "rsearch' and "left"
		motorInst.go_forward()
		print(body.ahead_cell.wall)
		curr_dist = str(int(curr_dist) - 1) # curr_dist var created from "?curr_dist" slot in the condition; change to adjust goal state
		goal.set("rsearch left ?dist ?num_turns ?curr_dist")


	# When num_turns = 0
	def left_rsearch(goal="rsearch left ?dist ?num_turns 0", motorInst="busy:False",
					utility=0.1):
		motorInst.turn_left(2)
		num_turns = str(int(num_turns) + 1)
		goal.set("rsearch left ?dist ?num_turns ?dist")
	

	# When num_turns = 1
	def left_rsearch_increase(goal="rsearch left ?dist 1 0", motorInst="busy:False", 
					utility=0.2): # Changed from utility=0.1
		motorInst.turn_left(2)
		dist = str(int(dist) + 1) # Increments distance to continue spiral
		goal.set("rsearch left ?dist 0 ?dist")


	# Wall ahead --> trace the wall
	def trace_wall(goal="rsearch left ?dist ?num_turns ?curr_dist",
						motorInst="busy:False", body="ahead_cell.wall:True"):
		motorInst.turn_left(2)
		print(body.ahead_cell.wall)
		goal.set("rsearch left ?dist ?num_turns 8")



		###Other stuff!


rand_inst = random.Random()
rand_inst.seed(1)

world=grid.World(MyCell,map=AgentSupport.mymap)
agent=VacuumAgent()
agent.home=()
world.add(agent,5,5,dir=0,color="black")

python_actr.log_everything(agent, AgentSupport.my_log)
window = python_actr.display(world)
world.run()

time.sleep(1)
world.reset_map(MyCell,map=AgentSupport.mymap)
agent2=VacuumAgent() # Create new agent
agent2.DM_module.dm = agent.DM_module.dm # Give new agent the saved chunks in from the original agent's DM
world.add(agent2,5,5,dir=0,color="black") # Add Agent2, not Agent
world.run()
