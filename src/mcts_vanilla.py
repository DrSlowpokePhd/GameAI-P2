
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1000
explore_faction = 2.

def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """

    if(board.current_player(state) == identity and len(node.action_list) != 0):
        return node
    else:
        # Select a child node based on uct?
        return traverse_nodes(list(node.child_nodes.values())[0], board, state, identity)
    
    # Hint: return leaf_node


def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.
    
    """
    # How do I figure out the action that got to here?
    new_node = MCTSNode(node, None, None)
    return new_node
    # Hint: return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    pass


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    if(node.parent is None):
        return

    if(won):
        node.wins += 1
    else:
        node.wins -= 1
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
    selectedAction = None
    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!
        leaf_node = traverse_nodes(node, board, sampled_game, identity_of_bot)
        # create new node from the selected leaf (Expansion)
        new_node = expand_leaf(leaf_node, board, sampled_game)
        # Create the new state given the action from the expansion (WIP)
        sampled_game = board.next_state(sampled_game, choice(board.legal_actions(sampled_game)))
        if(board.is_ended(sampled_game)):
            #choose winning move
            break
        # rollout the new_node and determine if its a win
        rollout(board, sampled_game)
        # backpropagate the new_node to update its parents
        backpropagate(new_node)

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    action = choice(board.legal_actions(state))
    print(type(action), action)
    return action # return random node for now

def UCTValue(node):
    return (node.wins/node.visits) * explore_faction(sqrt(log())/node.visits)
