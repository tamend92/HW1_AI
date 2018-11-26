# pacmanAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from pacman import Directions
from game import Agent
from heuristics import *
import random

class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        # returns random action from all the valide actions
        return actions[random.randint(0,len(actions)-1)]

class OneStepLookAheadAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        legal = state.getLegalPacmanActions()
        # get all the successor state for these actions
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal]
        # evaluate the successor states using scoreEvaluation heuristic
        scored = [(admissibleHeuristic(state), action) for state, action in successors]
        # get best choice
        bestScore = min(scored)[0]
        # get all actions that lead to the highest score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        
        # return random action from the list of the best actions
        return random.choice(bestActions)

class BFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write BFS Algorithm instead of returning Directions.STOP
        determined_direction = 'None'
        
        unexplored_nodes = Queue()

        #queue initial state
        unexplored_nodes.enqueue([state,'None', 'None', 0,0])

        discovered_nodes = []

        while not unexplored_nodes.Is_Empty():
            #get next state from queue
            current_state = unexplored_nodes.dequeue()
            
            discovered_nodes.append(current_state)
            
            successor_nodes, calls_depleted = self.getSuccessorNodes(current_state)

            for child_state in successor_nodes:
                #iterate through child nodes at the next level of the tree

                if child_state not in discovered_nodes:
                    
                    if not child_state[0].isLose():

                        if child_state[0].isWin():
                            #return action that is on direction to win
                            determined_direction = self.determineMoveToMake(child_state)
                            break

                        else:
                            #add to unexplored node
                            unexplored_nodes.enqueue(child_state)

            if calls_depleted == True: 
                #unpack all nodes in unexplored_nodes into discovered_nodes so that they can be considered
                while not unexplored_nodes.Is_Empty():
                    discovered_nodes.append(unexplored_nodes.dequeue())

                break
        
        if determined_direction == 'None':
            # use admissable heuristic to determine which direction is optimal if no winning state is found
            # must find minimum total cost
            
            heuristic_array = discovered_nodes[1:]

            heuristic_array.sort(key=lambda x: x[3])

            determined_direction = self.determineMoveToMake(heuristic_array[0])

        return determined_direction

    def getSuccessorNodes(self, current_state):
        # Returns successor nodes based upon current_state
        # Returns if generatePacmanSuccessor() has been depleted

        successor_nodes = []
        
        depleted = False

        legal_actions = current_state[0].getLegalPacmanActions()

        for legal_action in legal_actions:
            new_state = current_state[0].generatePacmanSuccessor(legal_action)

            if not new_state == None:
                new_state_heuristic = admissibleHeuristic(new_state) + current_state[4]+1
                successor_nodes.append([new_state, legal_action, current_state, new_state_heuristic, current_state[4]+1])
            else:
                #calls to successor state function have been depleted
                depleted = True
    
        return successor_nodes, depleted

    def determineMoveToMake(self, desired_state):
        # Iterates backwards through parent path to find initial direction needed

        current_state = desired_state

        while not current_state[2][2] == 'None':
            current_state = current_state[2]

        #return legal action
        return current_state[1]

class DFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write DFS Algorithm instead of returning Directions.STOP

        state_stack = Stack()

        explored_states = []

        #push initial state onto stack
        state_stack.push([state, "None", "None", 0, 0])

        determined_direction = None

        while not state_stack.isEmpty():
            #pop top level state
            current_state = state_stack.pop()
                        
            #check if current state is a loser...if it is....skip
            if not current_state[0].isLose():
                
                #append to explored states list as an explored state
                explored_states.append(current_state)

                if current_state[0].isWin():
                    determined_direction = self.dfsDetermineMOveToMake(current_state)
                    break

                #get successor states generated from current legal actions
                successor_states, successor_depleted = self.getDFSSuccessorNodes(current_state)

                for child_state in successor_states:
                    #push all to stack
                    state_stack.push(child_state)
        
            if successor_depleted:
                #If successor function is depleted; empty state stack and add to explored_states
                #Each state already received a heuristic score and was explored, but not expanded
                while not state_stack.isEmpty():
                    explored_states.append(state_stack.pop())
                break
        
        if determined_direction == None:
            # determined direction not found by finding winning state.  Sorting and navigating towards move with optimal heuristic score
            heuristic_array = explored_states[1:]

            heuristic_array.sort(key=lambda x: x[3])

            determined_direction = self.dfsDetermineMoveToMake(heuristic_array[0])

        return determined_direction

    def dfsDetermineMoveToMake(self, desired_state):
        # Iterates backwards through parent path to find initial direction needed

        current_state = desired_state

        while not current_state[2][2] == "None":
            current_state = current_state[2]

        #return legal action
        return current_state[1]

    def getDFSSuccessorNodes(self, current_state):
        # Returns successor nodes based upon current_state
        # Returns if generatePacmanSuccessor() has been depleted

        successor_nodes = []
        
        depleted = False

        legal_actions = current_state[0].getLegalPacmanActions()

        for legal_action in legal_actions:
            new_state = current_state[0].generatePacmanSuccessor(legal_action)

            if not new_state == None:
                new_state_heuristic = admissibleHeuristic(new_state) + current_state[4] + 1

                successor_nodes.append([new_state, legal_action, current_state, new_state_heuristic, current_state[4]+ 1])
            else:
                #calls to successor state function have been depleted
                depleted = True
    
        return successor_nodes, depleted
        
class AStarAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write A* Algorithm instead of returning Directions.STOP
        
        determined_direction = None
        
        astar_frontier = Priority_Queue()

        astar_frontier.prio_enqueue([state, "None", "None", 0, 0])

        expanded_nodes  = []

        while not astar_frontier.isEmpty():
            
            # Get current state from astar frontier
            current_state = astar_frontier.prio_dequeue()

            if not current_state[0].isLose():
                
                expanded_nodes.append(current_state)

                if current_state[0].isWin():
                    # winner winner chicken dinner
                    determined_direction = self.aStarDetermineMoveToMake(current_state)
                    break

                successor_states, successor_depleted = self.getAStarSuccessors(current_state)
                
                for child_state in successor_states:
                    # enqueue all child nodes so that they can be sorted and the optimal node will be chosen next to explore at next iteration
                    astar_frontier.prio_enqueue(child_state)

                if successor_depleted:
                    while not astar_frontier.isEmpty():
                        expanded_nodes.append(astar_frontier.prio_dequeue())
        
        if determined_direction == None:
            
            heuristic_array = expanded_nodes[1:]

            heuristic_array.sort(key=lambda x: x[3])

            print(max(heuristic_array))
            print(min(heuristic_array))

            determined_direction = self.aStarDetermineMoveToMake(heuristic_array[0])

        return determined_direction

    def getAStarSuccessors(self, current_state):
        # Get successor states for AStar Search
        # Returns successor nodes based upon current_state
        # Returns if generatePacmanSuccessor() has been depleted

        child_states = []

        depleted = False

        legal_actions = current_state[0].getLegalPacmanActions()

        for legal_action in legal_actions:
            new_state = current_state[0].generatePacmanSuccessor(legal_action)

            if not new_state == None:
                
                #heuristic calculation + depth of parent + 1 
                heuristic_new_state = admissibleHeuristic(new_state) + current_state[4] + 1 
                #heuristic_new_state = admissibleHeuristic(new_state) + 0
                child_states.append([new_state, legal_action, current_state, heuristic_new_state, current_state[4]+1])

            else:
                # calls to successor state function have been depleted...suspend calls
                depleted = True
                break

        return child_states, depleted 

    def aStarDetermineMoveToMake(self, desired_state):
        # Iterates backwards through parent path to find initial direction needed

        current_state = desired_state

        while not current_state[2][2] == "None":
            current_state = current_state[2]

        #return legal action
        return current_state[1]

class Queue:
    #implementation of Queue
    def __init__(self):
        self.queue_list = []

    def enqueue(self, queue_node):
        #add node in Fifo Fashion
        self.queue_list.insert(0,queue_node)

    def dequeue(self):
        #dequeue items in fifof fashion
        return self.queue_list.pop()

    def size(self):
        #return size of queue
        return len(self.queue_list)

    def Is_Empty(self):
        #Check for empty queue
        if self.queue_list == []:
            return True
        else:
            return False

class Stack:
    #basic implementation of a Stack
    def __init__(self):
        self.stack_list = []

    def pop(self):
        return self.stack_list.pop(0)
    
    def push(self, new_node):
        self.stack_list.insert(0,new_node)

    def size(self):
        return len(self.stack_list)

    def isEmpty(self):
        #Check for empty stack
        if self.stack_list == []:
            return True
        else:
            return False

class Priority_Queue:
    # Basic implementation of Priority Queue

    def __init__(self):
        self.prio_queue_list = []

    def prio_enqueue(self, new_node):
        # adds node to the priority queue and then sorts based upon admissible heuristic score
        if not self.isEmpty():   
            self.prio_queue_list.insert(0, new_node)

            self.prio_queue_list.sort(key=lambda x: x[3])
        else:
            self.prio_queue_list.insert(0, new_node)    

    def prio_dequeue(self):
        # dequeues 0 index node, which due to sorted enqueue should be lowest cost node
        return self.prio_queue_list.pop(0)

    def isEmpty(self):
        # checks for empty priority queue
        if self.prio_queue_list == []:
            return True
        else:
            return False

    def size(self):
        return len(self.prio_queue_list)