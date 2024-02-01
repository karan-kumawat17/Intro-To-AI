import heapq
import time
import numpy as np
import matplotlib.pyplot as plt

class PuzzleNode:
    def __init__(self, state, parent=None, move=None, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


def get_blank_location(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j


def misplaced_tile_heuristic(state):
    misplaced_tiles = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != i * 3 + j + 1:
                misplaced_tiles += 1
    return misplaced_tiles


def get_neighbors(node):
    neighbors = []
    blank_row, blank_col = get_blank_location(node.state)

    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for move in moves:
        new_row, new_col = blank_row + move[0], blank_col + move[1]

        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_state = [row[:] for row in node.state]
            new_state[blank_row][blank_col], new_state[new_row][new_col] = (
                new_state[new_row][new_col],
                new_state[blank_row][blank_col],
            )
            neighbors.append(new_state)

    return neighbors


def reconstruct_path(node):
    path = []
    while node.parent is not None:
        path.append(node.move)
        node = node.parent
    path.reverse()
    return path


def solve_8_puzzle(initial_state, goal_state):
    initial_node = PuzzleNode(state=initial_state, heuristic=misplaced_tile_heuristic(initial_state))
    priority_queue = [initial_node]
    visited_states = set()
    nodes_removed = 0

    while priority_queue:
        current_node = heapq.heappop(priority_queue)
        nodes_removed += 1

        if current_node.state == goal_state:
            return reconstruct_path(current_node), nodes_removed

        visited_states.add(tuple(map(tuple, current_node.state)))

        for neighbor_state in get_neighbors(current_node):
            neighbor_node = PuzzleNode(
                state=neighbor_state,
                parent=current_node,
                move=(current_node.state, neighbor_state),
                cost=current_node.cost + 1,
                heuristic=misplaced_tile_heuristic(neighbor_state),
            )

            if tuple(map(tuple, neighbor_state)) not in visited_states:
                heapq.heappush(priority_queue, neighbor_node)
    # print(f"Total number of nodes removed : {nodes_removed}")
    return None, nodes_removed


def count_inversions_merge_sort(arr):
    if len(arr) <= 1:
        return arr, 0

    mid = len(arr) // 2
    left, left_inversions = count_inversions_merge_sort(arr[:mid])
    right, right_inversions = count_inversions_merge_sort(arr[mid:])
    merged, split_inversions = merge_and_count_split_inversions(left, right)

    total_inversions = left_inversions + right_inversions + split_inversions
    return merged, total_inversions


def merge_and_count_split_inversions(left, right):
    merged = []
    i = j = split_inversions = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            split_inversions += len(left) - i
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, split_inversions


def count_inversions(state):
    flat_state = [item for sublist in state for item in sublist if item != 0]
    _, inversions = count_inversions_merge_sort(flat_state)
    return inversions


# Function to calculate the total time taken
def calculate_time_taken(start_time, end_time):
    elapsed_time = end_time - start_time
    return f"Time taken: {elapsed_time:.6f} seconds"


# Example usage:
initial_state = []
for i in range(3):
    row = [int(x) for x in input(f"Enter values for row {i + 1} (space-separated): ").split()]
    initial_state.append(row)

# Get user input for the goal state
goal_state = []
for i in range(3):
    row = [int(x) for x in input(f"Enter values for goal row {i + 1} (space-separated): ").split()]
    goal_state.append(row)


def is_solvable(initial_state, goal_state):
    initial_inversions = count_inversions(initial_state)
    goal_inversions = count_inversions(goal_state)
    return initial_inversions % 2 == 0 and goal_inversions % 2 == 0


# Example usage for solvability check:
if is_solvable(initial_state, goal_state):
    print("The puzzle is solvable.")
else:
    print("The puzzle is not solvable.")

start_time = time.time()
solution_path, nodes_removed = solve_8_puzzle(initial_state, goal_state)
end_time = time.time()

if solution_path:
    print("Solution found!")
    for i, move in enumerate(solution_path):
        print(f"Step {i + 1}: Move {move[1]}")
else:
    print("No solution found.")

print(calculate_time_taken(start_time, end_time))
print(f"Nodes removed from the frontier: {nodes_removed}")

def get_user_input(message):
    return [list(map(int, input(f"{message} row {i + 1} (space-separated): ").split())) for i in range(3)]


def run_experiment():
    instances = 10
    time_taken_list = []
    nodes_removed_list = []
    steps_list = []

    for instance in range(instances):
        print(f"\nInstance {instance + 1}:")

        # Example: Generate random initial and goal states
        initial_state = get_user_input("Enter values for initial")
        goal_state = get_user_input("Enter values for goal")

        # Check solvability
        if not is_solvable(initial_state, goal_state):
            print("The generated puzzle is not solvable. Regenerating...")
            instance -= 1
            continue

        start_time = time.time()

        priority_queue = []
        visited_states = set()
        nodes_removed = 0

        initial_node = PuzzleNode(state=initial_state, heuristic=misplaced_tile_heuristic(initial_state))
        heapq.heappush(priority_queue, initial_node)

        solution_path = None
        while priority_queue:
            current_node = heapq.heappop(priority_queue)
            nodes_removed += 1

            if np.array_equal(current_node.state, goal_state):
                solution_path = reconstruct_path(current_node)
                break

            visited_states.add(tuple(map(tuple, current_node.state)))

            for neighbor_state in get_neighbors(current_node):
                neighbor_node = PuzzleNode(
                    state=neighbor_state,
                    parent=current_node,
                    move=(current_node.state, neighbor_state),
                    cost=current_node.cost + 1,
                    heuristic=misplaced_tile_heuristic(neighbor_state),
                )

                if tuple(map(tuple, neighbor_state)) not in visited_states:
                    heapq.heappush(priority_queue, neighbor_node)

        end_time = time.time()

        if solution_path:
            print("Solution found!")
            for i, move in enumerate(solution_path):
                print(f"Step {i + 1}: Move {move[1]}")
        else:
            print("No solution found.")

        total_steps = len(solution_path) if solution_path else 0
        time_taken = end_time - start_time

        print(calculate_time_taken(start_time, end_time))
        print(f"Nodes removed from the frontier: {nodes_removed}")
        print(f"Total Steps: {total_steps}")

        # Append results to lists for plotting
        time_taken_list.append(time_taken)
        nodes_removed_list.append(nodes_removed)
        steps_list.append(total_steps)

    # Plotting
    plt.plot(time_taken_list, 'o-')
    plt.title('Time Taken')
    plt.xlabel('Instance')
    plt.ylabel('Time (seconds)')
    plt.show()

if __name__ == "__main__":
    run_experiment()
