from math import exp
import random
# start with random assignment
# loop over the grid and note number of conflicts for each cell except fixed cells
# randomly select a varialble cell with conflicts
# find number of conflicts for each possible value [1-4]
# select min conflicts value (break ties randomly) with a probability of selecting worse values decreasing with temperature
# update cell value
# repeat until 0 conflcits or 10000 iterations

TEMP_INIT_ONE = 10000
TEMP_INIT_TWO = 100
GRID_SIZE = 4

# never select for change
FIXED_CELLS = {(0,1):1, (0,2):3, (1,0):2, (2,3):3, (3,1):2, (3,2):1}

def p1(current, new, temperature):
    return exp(float(-1*(new-current))/temperature)

# exponential decay
def annealing_schedule_1(temperature):
    if temperature < 0.001:
        return temperature
    return temperature * 0.99

# exponential decay - heavier
def annealing_schedule_2(temperature):
    return temperature * 0.90

# find conflicts for a given cell
def find_conflicts(grid, row, col, val):
    conflicts = 0
    for i in range(GRID_SIZE):
        # row and col conflicts
        if grid[row][i] == val and i != col:
            conflicts += 1
        if grid[i][col] == val and i != row:
            conflicts += 1
    # box conflicts
    box_row_start = (row // 2) * 2
    box_col_start = (col // 2) * 2
    for i in range(box_row_start, box_row_start + 2):
        for j in range(box_col_start, box_col_start + 2):
            if grid[i][j] == val and (i, j) != (row, col):
                conflicts += 1
    return conflicts

def adjust_conflicts(grid, entry, probability, temperature):
    row, col, val, conflicts = entry
    new_conflicts = [find_conflicts(grid, row, col, v) for v in range(1, GRID_SIZE + 1)]
    minn = float('inf')
    minn_val = -1
    for i, conflict in enumerate(new_conflicts):
        if i+1 == val:
            continue
        if conflict < minn:
            minn = conflict
            minn_val = i + 1
        elif conflict == minn and random.random() < 0.5:
            minn_val = i + 1
    if minn<=conflicts:
        return (row, col, minn_val, minn)
    elif minn!= float('inf') and minn>conflicts:
        p = probability(conflicts, minn, temperature)
        if random.random() < p:
            return (row, col, minn_val, minn)
        else:
            return entry
    else:
        return entry

def generate_random_grid():
    grid = [[random.randint(1, GRID_SIZE) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for (row, col), val in FIXED_CELLS.items():
        grid[row][col] = val
    return grid

print(generate_random_grid())

def simulated_annealing(grid, temp_init, schedule, probability):
    for iteration in range(10000):
        conflict_cells = []
        total_conflicts = 0
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if (r, c) in FIXED_CELLS:
                    continue
                val = grid[r][c]
                conflicts = find_conflicts(grid, r, c, val)
                total_conflicts += conflicts
                if conflicts > 0:
                    conflict_cells.append((r, c, val, conflicts))
        if total_conflicts == 0:
            print(f"Solved in {iteration} iterations")
            return 1
        changing_cell = conflict_cells[random.randint(0, len(conflict_cells)-1)]
        changing_cell = adjust_conflicts(grid, changing_cell, probability, temp_init)
        row, col, new_val, _ = changing_cell
        grid[row][col] = new_val
        temp_init = schedule(temp_init)
    print("Max iterations reached")
    return 0

def main():
    ratios = [0,0,0,0]
    for i in range(100):
        grid = generate_random_grid()
        ratios[0] += simulated_annealing(grid, TEMP_INIT_ONE, annealing_schedule_1, p1)
    for i in range(100):
        grid = generate_random_grid()
        ratios[1] += simulated_annealing(grid, TEMP_INIT_TWO, annealing_schedule_2, p1)
    for i in range(100):
        grid = generate_random_grid()
        ratios[2] += simulated_annealing(grid, TEMP_INIT_TWO, annealing_schedule_1, p1)
    for i in range(100):
        grid = generate_random_grid()
        ratios[3] += simulated_annealing(grid, TEMP_INIT_ONE, annealing_schedule_2, p1)
    print([r/100.0 for r in ratios])
main()


        

    




    
        
        
    