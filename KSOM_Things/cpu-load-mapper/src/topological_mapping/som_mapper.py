def initialize_cpu_map_model(grid_dims, feature_dim):
    import numpy as np

    # Initialize a 2D grid of prototype vectors (weights)
    grid_width, grid_height = grid_dims
    # Create a grid of random weights
    weights = np.random.rand(grid_height, grid_width, feature_dim)
    
    return weights