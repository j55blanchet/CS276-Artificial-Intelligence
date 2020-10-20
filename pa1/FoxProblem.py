class FoxProblem:
    """Represents the Chickens-and-Foxes scenario as a search problem. The state
    is represented by the tuple (c,f,b), where c,f, and b are the count of 
    chickens, foxes, and boats on the initial (starting) side of the river.
    """
    def __init__(self, start_state=(3, 3, 1)):
        self.start_state = start_state
        self.goal_state = (0, 0, 0)

        (chickens, foxes, boats) = start_state
        
        self.total_foxes = foxes
        self.total_chickens = chickens
        self.total_boats = boats

        assert boats == 1

    # get successor states for the given state
    def get_successors(self, state):
        (c, f, b) = state

        # If the boat is on the far side (b=0), then foxes / 
        # chickens will be moved (added) to the initial side, 
        # otherwise they'll be substracted
        sign = 1 if b == 0 else -1
        next_b = 0 if b > 0 else self.total_boats

        # Note: this assumes we only have 1 boat which must carry between
        #       1 and 2 animals on each journey. Generalizing to multiple boats
        #       would require changes here and in the is_legal method.
        possible_states = [
            (c, f + 2 * sign, next_b),    # Move 2 foxes
            (c, f + 1 * sign, next_b),    # Move 1 fox
            (c + 1 * sign, f, next_b),    # Move 1 chicken
            (c + 2 * sign, f, next_b),    # Move 2 chickens
            (c + sign, f + sign,  next_b) # Move 1 of each
        ]

        return filter(lambda s: self.is_legal(s), possible_states)

    def is_goal(self, state):
        (c, f, b) = state
        (goal_c, goal_f, goal_b) = self.goal_state
        return f == goal_f and c == goal_c and b == goal_b

    def is_legal(self, state):
        (c, f, b) = state

        farside_f = self.total_foxes - f
        farside_c = self.total_chickens - c
        
        valid_amounts = 0 <= f <= self.total_foxes and \
                        0 <= c <= self.total_chickens and \
                        0 <= b <= self.total_boats and \
                        0 <= farside_f <= self.total_foxes and \
                        0 <= farside_c <= self.total_chickens
    
        chickens_survived_near = c == 0 or c >= f
        chickens_survived_far =  farside_c == 0 or farside_c >= farside_f

        return valid_amounts and chickens_survived_near and chickens_survived_far

    def __str__(self):
        return f"Chickens and foxes problem: {self.start_state}"