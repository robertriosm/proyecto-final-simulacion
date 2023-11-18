import numpy as np

# Initialize the grid
grid = np.zeros((500, 500))

# Add cars to the grid
# For simplicity, let's add cars in the first row
grid[0, :10] = 1

def update_grid(grid):
    # Create a copy of the grid to hold the new state
    new_grid = np.copy(grid)

    # Iterate over each cell in the grid
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1] - 1):  # Subtract 1 to avoid index out of range
            # Check if the current cell is a car
            if grid[i, j] == 1:
                # Check if the cell to the right is empty
                if grid[i, j + 1] == 0:
                    # Move the car to the right
                    new_grid[i, j] = 0
                    new_grid[i, j + 1] = 1

    return new_grid

# Update the grid
for _ in range(100):  # Number of time steps
    grid = update_grid(grid)
    print(grid)
    print()
