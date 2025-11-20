#!/usr/bin/env python3
"""
Collatz Hopf Bifurcation Explorer
Explores parameter-dependent dynamics in generalized Collatz sequences
Looking for bifurcation points where sequence behavior changes qualitatively
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
import time
from collections import defaultdict
import json

class CollatzHopfExplorer:
    def __init__(self):
        # Bifurcation parameters
        self.param_range = (2.5, 4.0)  # Parameter sweep range
        self.param_steps = 1000
        self.max_iterations = 500
        self.convergence_threshold = 1e-10
        
        # Sphere mapping parameters
        self.sphere_resolution = 200
        self.radius = 1.0
        
        # Animation and display
        self.current_param = 3.0
        self.param_step_size = 0.001
        self.animate_speed = 0.02
        
        # Data storage
        self.bifurcation_data = {}
        self.sphere_points = []
        self.sequence_behaviors = {}
        
        # Generate sphere points
        self.generate_sphere_points()
