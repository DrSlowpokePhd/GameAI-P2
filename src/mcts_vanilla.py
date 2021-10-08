from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1000
explore_faction = 2

def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """
    best_child = node
    current_state = state
    #If the node did not try all actions, then expand the node
    if len(node.untried_actions) != 0:
        return expand_leaf(node, board, state)
    if len(best_child.untried_actions) == 0 and len(best_child.child_nodes) > 0:
        if(board.current_player(current_state) == identity):
            #Returns the child with the best win percentage
            best_child = max(best_child.child_nodes.values(), key = lambda a: (a.wins/a.visits) + (explore_faction)*sqrt(2*log(a.parent.visits)/a.visits))
        else:
            #Chose the move that is the lowest win rate for this player (best move for opponent)
            best_child = max(best_child.child_nodes.values(), key = lambda a: (1 - a.wins/a.visits) + (explore_faction)*sqrt(2*log(a.parent.visits)/a.visits))
        #Given the best/worse move, create the next state
        current_state = board.next_state(current_state, best_child.parent_action)
    return best_child, current_state
    # Hint: return leaf_node


def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.
    
    """
    #Default values it returns if conditional is not met
    new_leaf = node
    new_state = state
    #Checks if there are still any untried actions left
    if(len(node.untried_actions) != 0):
        move = choice(node.untried_actions)
        new_state = board.next_state(new_state, move)
        #Creates a new child node and links it to it's parent
        new_leaf = MCTSNode(parent = node, parent_action = move, action_list = board.legal_actions(new_state))
        node.child_nodes[move] = new_leaf
        #Remove untried actions
        node.untried_actions.remove(move)
    return new_leaf, new_state
    # Hint: return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    current_state = state
    while not board.is_ended(current_state):
        # Create next state with random choice of actions
        rollout_move = choice(board.legal_actions(current_state))
        current_state = board.next_state(current_state, rollout_move)
    return current_state


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    if(node.parent is None):
        return

    node.wins += won
    node.visits += 1  
    backpropagate(node.parent, won)


def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))
    root_node.visits = 1

    for step in range(num_nodes):
        sampled_game = state

        node = root_node
        #Select the next node and expand the tree with the best uct value
        leaf_node, depth_state = traverse_nodes(node, board, sampled_game, identity_of_bot)

        #Simulate the rest of the game randomly
        end_state = rollout(board, depth_state)

        # Get winner of the end result and update depending on it
        round_winner = board.win_values(end_state)
        if round_winner[identity_of_bot] == 1:
            backpropagate(leaf_node, 1)     # Win
        elif round_winner[identity_of_bot] == 0.5:
            backpropagate(leaf_node, 0.5)   # Tie
        else:
            backpropagate(leaf_node, 0)     # Loss

    # Get the best win rate move from the possible actions of the root node
    return max(root_node.child_nodes.values(), key = lambda a: a.wins/a.visits).parent_action

