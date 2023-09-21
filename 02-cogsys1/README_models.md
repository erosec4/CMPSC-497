# When num_turns = 0
def left_rsearch(goal="rsearch left ?dist 0 0", motorInst="busy:False",
				utility=0.1):
	motorInst.turn_left(2)
	num_turns = str(int(num_turns) + 1)
	goal.set("rsearch left ?dist 1 ?dist")

# When num_turns = 1
def left_rsearch(goal="rsearch left ?dist 1 0", motorInst="busy:False",
				utility=0.1):
	motorInst.turn_left(2)
	goal.set("rsearch left ?dist 2 ?dist")

# When num_turns = 2
def left_rsearch(goal="rsearch left ?dist 2 0", motorInst="busy:False",
				utility=0.1):
	motorInst.turn_left(2)
	goal.set("rsearch left ?dist 3 ?dist")

# When num_turns = 3
def left_rsearch(goal="rsearch left ?dist 3 0", motorInst="busy:False",
				utility=0.1):
	motorInst.turn_left(2)
	num_turns = str(int(num_turns) + 1)
	goal.set("rsearch left ?dist 4 ?dist")