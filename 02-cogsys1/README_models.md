# Pizza Builder
The two pathways for the `pizza.py` execution are illustrated in `pizza_builder.pdf`. Onion was chosen as the topping for the bbq cheddar pizza. Completing this agent did not pose much of a challenge, as the use of the goal buffer in the conditions and new intentions was clear from the given functions. IThe condition of `place_pepperoni` was modified to state pepperoni as the next ingredient, and then the `goal.set` line was changed at the end of the function to specify pepperoni as the previous ingredient. This same procedure was followed for `place_onions`, but with onion instead of pepperoni, and a `goal.set` line was added to specify `cook_pizza` as the next and final step. 
Then, to create the two separate pathways, the function for adding cheddar cheese was added based on the mozzarella function, just with bbq as the previous ingredient.


# Vacuum Agent

### Spiral Path
This agent posed many challenges. Many test runs were executed to inspect the patterns of the output. Initially, a single line was added in the `left_rsearch` function to increment the `dist` variable. This did move the agent in a spiral pattern, but it did not clean every spot on the grid. To solve this, a new function was created to increment `dist` only after `num_turns` hit 4. This worked, but not consistently. Many small syntactical changes were attempted, all with similar results. At one point, there were five different functions for turning left, each with its own `num_turns` value (0-4). Then, attention turned to the `utility=` section of the conditions. Observation of the given functions led to the assumption that a higher utility value for the new function would allow the new function to execute when expected. This worked, and trial and error led to the selection of 1 as the appropriate condition for `num_turns` before a `dist` increment. 

### Tracing the Wall
In order to prevent the program from stopping when all the red boxes were cleared, lines 134 and 135 of `AgentSupport.py` were commented out. Based on the `body="ahead_cell.wall:False"` condition in `forward_rsearch`, the same condition except checking for True was used in the new `trace_wall` function. This function turns the agent and sets `curr_dist` to 8 (the max wall length) so that the agent does not turn before it hits another wall.
