def visualize_cpu_topology(map_weights, coherence_data):
    import matplotlib.pyplot as plt
    import numpy as np

    # Extract dimensions of the map
    grid_height, grid_width = map_weights.shape[0:2]

    # Create a meshgrid for plotting
    x = np.arange(grid_width)
    y = np.arange(grid_height)
    X, Y = np.meshgrid(x, y)

    # Plot the CPU load as a heatmap
    plt.figure(figsize=(10, 8))
    plt.imshow(map_weights[:, :, 0], cmap='hot', interpolation='nearest', origin='lower')
    
    # Overlay coherence data
    plt.colorbar(label='CPU Load')
    plt.scatter(X, Y, c=coherence_data, cmap='cool', edgecolors='k', s=100, label='Coherence')
    
    # Add labels and title
    plt.title('CPU Load Topology Visualization')
    plt.xlabel('Process Index')
    plt.ylabel('Cluster Index')
    plt.legend()
    
    # Show the plot
    plt.show()