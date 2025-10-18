#!/usr/bin/env python3
"""
String Theory Toy Visualizer
Two coupled Kuramoto-Kohonen strings with PLV measurement

Makes extra dimensions visible at desktop scale.
Challenge accepted.
"""

import numpy as np
import pygame
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from scipy.signal import hilbert
import sys

# Constants
WIDTH, HEIGHT = 1400, 800
FPS = 60
N_OSCILLATORS = 50  # Nodes per string

class KuramotoString:
    """A 1D string of coupled phase oscillators (Kuramoto model with spatial coupling)"""
    
    def __init__(self, n=50, natural_freq_std=0.5):
        self.n = n
        self.phases = np.random.uniform(0, 2*np.pi, n)
        self.natural_frequencies = np.random.normal(1.0, natural_freq_std, n)
        self.coupling_matrix = self._build_spatial_coupling()
        
    def _build_spatial_coupling(self):
        """Kohonen-style spatial coupling - neighbors influence each other"""
        K = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(self.n):
                # Gaussian coupling with spatial distance
                dist = min(abs(i - j), self.n - abs(i - j))  # Periodic boundary
                K[i, j] = np.exp(-dist**2 / (2 * 3**2))  # sigma=3
        return K
    
    def update(self, dt, internal_coupling=0.5):
        """Update phases using Kuramoto model"""
        # Kuramoto coupling term
        phase_diff = self.phases[:, None] - self.phases[None, :]
        coupling_force = internal_coupling * np.sum(
            self.coupling_matrix * np.sin(phase_diff), axis=1
        )
        
        # Update phases
        self.phases += (self.natural_frequencies + coupling_force) * dt
        self.phases = np.mod(self.phases, 2*np.pi)
    
    def order_parameter(self):
        """Compute Kuramoto order parameter r (PLV measure)"""
        z = np.mean(np.exp(1j * self.phases))
        return abs(z)
    
    def get_colors(self):
        """Get RGB colors based on phases"""
        # Phase to color: 0->red, 2π/3->green, 4π/3->blue
        hues = self.phases / (2*np.pi)
        colors = []
        for hue in hues:
            # HSV to RGB (simplified)
            h = hue * 6
            x = 1 - abs(h % 2 - 1)
            if h < 1:
                rgb = (1, x, 0)
            elif h < 2:
                rgb = (x, 1, 0)
            elif h < 3:
                rgb = (0, 1, x)
            elif h < 4:
                rgb = (0, x, 1)
            elif h < 5:
                rgb = (x, 0, 1)
            else:
                rgb = (1, 0, x)
            colors.append(tuple(int(c * 255) for c in rgb))
        return colors

class StringInteraction:
    """Manages coupling between two strings"""
    
    def __init__(self, string1, string2, coupling_strength=0.3):
        self.string1 = string1
        self.string2 = string2
        self.coupling_strength = coupling_strength
        self.history_r1 = []
        self.history_r2 = []
        self.history_r_int = []
        
    def set_coupling(self, strength):
        """Adjust coupling strength"""
        self.coupling_strength = max(0.0, min(1.0, strength))
    
    def compute_interaction(self):
        """Compute phase-locking between strings"""
        phase_diff = self.string1.phases - self.string2.phases
        interaction = self.coupling_strength * np.sin(phase_diff)
        return interaction
    
    def measure_coupling_coherence(self):
        """Measure how synchronized the two strings are (r_interaction)"""
        phase_diff = self.string1.phases - self.string2.phases
        z = np.mean(np.exp(1j * phase_diff))
        return abs(z)
    
    def step(self, dt):
        """Update both strings with coupling"""
        # Update internal dynamics
        self.string1.update(dt)
        self.string2.update(dt)
        
        # Apply coupling between strings
        interaction = self.compute_interaction()
        self.string1.phases += interaction * dt
        self.string2.phases -= interaction * dt
        
        # Normalize phases
        self.string1.phases = np.mod(self.string1.phases, 2*np.pi)
        self.string2.phases = np.mod(self.string2.phases, 2*np.pi)
        
        # Measure PLV
        r1 = self.string1.order_parameter()
        r2 = self.string2.order_parameter()
        r_int = self.measure_coupling_coherence()
        
        # Track history
        self.history_r1.append(r1)
        self.history_r2.append(r2)
        self.history_r_int.append(r_int)
        
        # Keep history manageable
        max_history = 500
        if len(self.history_r1) > max_history:
            self.history_r1 = self.history_r1[-max_history:]
            self.history_r2 = self.history_r2[-max_history:]
            self.history_r_int = self.history_r_int[-max_history:]
        
        return r1, r2, r_int

class Visualizer:
    """Pygame + matplotlib visualization"""
    
    def __init__(self, interaction):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("String Theory Toy - Extra Dimensions Visible")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        self.interaction = interaction
        
        # Setup matplotlib for phase plot
        self.fig, self.ax = plt.subplots(figsize=(4, 3), facecolor='black')
        self.ax.set_facecolor('black')
        self.ax.tick_params(colors='white')
        self.canvas = FigureCanvasAgg(self.fig)
        
    def draw_string(self, string, y_pos, label):
        """Draw a string as a line of colored circles"""
        x_start = 50
        x_spacing = (WIDTH - 500) // string.n
        colors = string.get_colors()
        
        # Label
        text = self.font.render(label, True, (255, 255, 255))
        self.screen.blit(text, (10, y_pos - 25))
        
        # Draw oscillators
        for i, color in enumerate(colors):
            x = x_start + i * x_spacing
            pygame.draw.circle(self.screen, color, (x, y_pos), 8)
            
        # Draw connections (spatial coupling visualization)
        for i in range(string.n - 1):
            x1 = x_start + i * x_spacing
            x2 = x_start + (i + 1) * x_spacing
            # Color based on phase difference
            phase_diff = abs(string.phases[i+1] - string.phases[i])
            # Clamp phase_diff to [0, π]
            phase_diff = min(phase_diff, np.pi)
            alpha = int(255 * (1 - phase_diff / np.pi))
            # Clamp alpha to [0, 255]
            alpha = max(0, min(255, alpha))
            color = (alpha, alpha, alpha)
            pygame.draw.line(self.screen, color, (x1, y_pos), (x2, y_pos), 2)
    
    def draw_coupling_lines(self, y1, y2):
        """Draw coupling between strings"""
        x_start = 50
        x_spacing = (WIDTH - 500) // self.interaction.string1.n
        
        # Draw sample coupling lines (every 5th oscillator)
        for i in range(0, self.interaction.string1.n, 5):
            x = x_start + i * x_spacing
            
            # Line thickness based on coupling strength and phase coherence
            phase_diff = abs(self.interaction.string1.phases[i] - 
                           self.interaction.string2.phases[i])
            coherence = 1 - (phase_diff / np.pi)
            alpha = int(100 * self.interaction.coupling_strength * coherence)
            
            if alpha > 20:
                color = (alpha, alpha, 255)
                pygame.draw.line(self.screen, color, (x, y1), (x, y2), 2)
    
    def draw_PLV_meter(self, r1, r2, r_int):
        """Draw r parameters as bars"""
        x_start = WIDTH - 450
        y_start = 50
        bar_width = 400
        bar_height = 30
        
        # Title
        title = self.font.render("PLV Measurement (r parameter)", True, (255, 255, 255))
        self.screen.blit(title, (x_start, y_start - 30))
        
        # String 1
        self.draw_bar(x_start, y_start, bar_width, bar_height, r1, 
                     f"String 1: r = {r1:.3f}", (255, 100, 100))
        
        # String 2
        self.draw_bar(x_start, y_start + 50, bar_width, bar_height, r2,
                     f"String 2: r = {r2:.3f}", (100, 255, 100))
        
        # Interaction
        self.draw_bar(x_start, y_start + 100, bar_width, bar_height, r_int,
                     f"Coupling: r = {r_int:.3f}", (100, 100, 255))
        
        # PLV threshold line
        threshold_x = x_start + int(bar_width * 0.5)
        for y in [y_start, y_start + 50, y_start + 100]:
            pygame.draw.line(self.screen, (255, 255, 0), 
                           (threshold_x, y), (threshold_x, y + bar_height), 2)
        
        threshold_text = self.small_font.render("r=0.5 (PLV threshold)", 
                                               True, (255, 255, 0))
        self.screen.blit(threshold_text, (x_start + 150, y_start + 140))
    
    def draw_bar(self, x, y, width, height, value, label, color):
        """Draw a single meter bar"""
        # Background
        pygame.draw.rect(self.screen, (50, 50, 50), (x, y, width, height))
        
        # Value bar
        filled_width = int(width * value)
        pygame.draw.rect(self.screen, color, (x, y, filled_width, height))
        
        # Border
        pygame.draw.rect(self.screen, (150, 150, 150), (x, y, width, height), 2)
        
        # Label
        text = self.small_font.render(label, True, (255, 255, 255))
        self.screen.blit(text, (x + 5, y + 7))
    
    def draw_phase_plot(self):
        """Draw phase space trajectory"""
        if len(self.interaction.history_r1) < 2:
            return
        
        self.ax.clear()
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.set_xlabel('String 1 (r)', color='white')
        self.ax.set_ylabel('String 2 (r)', color='white')
        self.ax.set_title('Phase Space', color='white')
        self.ax.grid(True, alpha=0.3, color='white')
        
        # Plot trajectory with color gradient
        points = np.array([self.interaction.history_r1, self.interaction.history_r2]).T
        for i in range(len(points) - 1):
            alpha = i / len(points)
            color = (alpha, 0.5, 1 - alpha)
            self.ax.plot(points[i:i+2, 0], points[i:i+2, 1], 
                        color=color, linewidth=2, alpha=0.7)
        
        # Current position
        self.ax.plot(self.interaction.history_r1[-1], self.interaction.history_r2[-1],
                    'o', color='yellow', markersize=8)
        
        # Render to pygame surface
        self.canvas.draw()
        buf = self.canvas.buffer_rgba()
        plot_surface = pygame.image.frombuffer(buf, 
                                              (int(self.fig.bbox.bounds[2]), 
                                               int(self.fig.bbox.bounds[3])),
                                              'RGBA')
        self.screen.blit(plot_surface, (WIDTH - 450, 200))
    
    def draw_controls(self, coupling):
        """Draw control instructions"""
        y = HEIGHT - 100
        instructions = [
            f"Coupling Strength: {coupling:.2f}",
            "Controls: UP/DOWN = adjust coupling, SPACE = reset, R = randomize phases",
            "Q = quit",
            "",
            f"Fold Level: {'5-7 (Safe)' if coupling < 0.7 else '8-10 (Careful!)' if coupling < 0.9 else '11 (DANGER!)'}",
        ]
        
        for i, text in enumerate(instructions):
            color = (255, 255, 255)
            if "DANGER" in text:
                color = (255, 0, 0)
            elif "Careful" in text:
                color = (255, 200, 0)
            
            surf = self.small_font.render(text, True, color)
            self.screen.blit(surf, (10, y + i * 20))
    
    def render(self, r1, r2, r_int):
        """Main render loop"""
        self.screen.fill((0, 0, 0))
        
        # Draw strings
        string1_y = 250
        string2_y = 400
        self.draw_string(self.interaction.string1, string1_y, "String 1 (50 oscillators)")
        self.draw_string(self.interaction.string2, string2_y, "String 2 (50 oscillators)")
        
        # Draw coupling
        self.draw_coupling_lines(string1_y, string2_y)
        
        # Draw meters
        self.draw_PLV_meter(r1, r2, r_int)
        
        # Draw phase plot
        self.draw_phase_plot()
        
        # Draw controls
        self.draw_controls(self.interaction.coupling_strength)
        
        pygame.display.flip()

def main():
    # Create strings
    string1 = KuramotoString(n=N_OSCILLATORS, natural_freq_std=0.3)
    string2 = KuramotoString(n=N_OSCILLATORS, natural_freq_std=0.3)
    
    # Create interaction
    interaction = StringInteraction(string1, string2, coupling_strength=0.3)
    
    # Create visualizer
    viz = Visualizer(interaction)
    
    dt = 0.05
    running = True
    
    print("String Theory Toy - Extra Dimensions Visible")
    print("=" * 50)
    print("Watch two strings (spatially extended oscillators) interact")
    print("r parameter measures PLV/synchronization")
    print("r > 0.5 = conscious, r > 0.7 = highly synchronized")
    print("\nControls:")
    print("  UP/DOWN: Adjust coupling strength")
    print("  SPACE: Reset phases")
    print("  R: Randomize phases")
    print("  Q: Quit")
    print("=" * 50)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_UP:
                    interaction.set_coupling(interaction.coupling_strength + 0.05)
                    print(f"Coupling: {interaction.coupling_strength:.2f}")
                elif event.key == pygame.K_DOWN:
                    interaction.set_coupling(interaction.coupling_strength - 0.05)
                    print(f"Coupling: {interaction.coupling_strength:.2f}")
                elif event.key == pygame.K_SPACE:
                    # Reset to standing wave
                    string1.phases = np.linspace(0, 2*np.pi, N_OSCILLATORS)
                    string2.phases = np.linspace(0, 2*np.pi, N_OSCILLATORS)
                    print("Reset to standing wave")
                elif event.key == pygame.K_r:
                    # Randomize
                    string1.phases = np.random.uniform(0, 2*np.pi, N_OSCILLATORS)
                    string2.phases = np.random.uniform(0, 2*np.pi, N_OSCILLATORS)
                    print("Randomized phases")
        
        # Update physics
        r1, r2, r_int = interaction.step(dt)
        
        # Render
        viz.render(r1, r2, r_int)
        viz.clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
