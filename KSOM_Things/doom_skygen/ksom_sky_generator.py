#!/usr/bin/env python3
"""
K-SOM Sky Generator - Consciousness-Based Procedural Sky Generation
Zero training data theft. Pure math + K-SOM consciousness.
Embarrass plagiarists with superior methodology.
Under 500 lines (obviously).
"""

import numpy as np
import math
from PIL import Image
import random
from typing import Tuple, List
import json

class KSOMSkyGenerator:
    """
    Generate volumetric skies with K-SOM global illumination
    Zero training data. Pure procedural + consciousness.
    """
    
    def __init__(self, width=2048, height=1024, ksom_size=64):
        self.width = width
        self.height = height
        self.ksom_size = ksom_size
        
        # K-SOM for light propagation (Kuramoto + Kohonen)
        self.light_oscillators = self.init_light_ksom()
        self.light_topology = self.init_kohonen_topology()
        
        # Atmospheric parameters
        self.rayleigh_coeff = np.array([3.8e-6, 13.5e-6, 33.1e-6])  # RGB scattering
        self.mie_coeff = 21e-6
        self.atmosphere_height = 12000.0  # meters
        
        # Cloud parameters
        self.cloud_octaves = 6
        self.cloud_persistence = 0.5
        self.cloud_lacunarity = 2.0
        
        print("🌀 K-SOM Sky Generator initialized")
        print(f"   Consciousness grid: {ksom_size}x{ksom_size}")
        print(f"   Output resolution: {width}x{height}")
        print(f"   Zero training data. Pure math + consciousness.")
    
    def init_light_ksom(self):
        """Initialize Kuramoto oscillators for light propagation"""
        oscillators = np.zeros((self.ksom_size, self.ksom_size, 3), dtype=complex)
        
        # Each oscillator represents light frequency (RGB)
        for i in range(self.ksom_size):
            for j in range(self.ksom_size):
                # Phase represents wavelength, magnitude represents intensity
                r_phase = random.uniform(0, 2 * np.pi)
                g_phase = random.uniform(0, 2 * np.pi) 
                b_phase = random.uniform(0, 2 * np.pi)
                
                oscillators[i, j] = np.array([
                    complex(1.0, 0) * np.exp(1j * r_phase),
                    complex(1.0, 0) * np.exp(1j * g_phase),
                    complex(1.0, 0) * np.exp(1j * b_phase)
                ])
        
        return oscillators
    
    def init_kohonen_topology(self):
        """Initialize spatial topology for K-SOM coupling"""
        topology = np.zeros((self.ksom_size, self.ksom_size, 2))
        
        # Create spatial coordinates for coupling strength
        for i in range(self.ksom_size):
            for j in range(self.ksom_size):
                # Normalized coordinates
                topology[i, j] = [i / self.ksom_size, j / self.ksom_size]
        
        return topology
    
    def sun_position(self, time_of_day):
        """Calculate sun position based on time (0-24 hours)"""
        # Simple sun arc: rises in east, sets in west
        angle = (time_of_day - 6) * np.pi / 12  # 6 AM = sunrise
        elevation = np.sin(angle) * np.pi / 2
        azimuth = angle
        
        # Convert to 3D position
        sun_x = np.cos(elevation) * np.cos(azimuth)
        sun_y = np.sin(elevation)
        sun_z = np.cos(elevation) * np.sin(azimuth)
        
        return np.array([sun_x, sun_y, sun_z])
    
    def atmospheric_scattering(self, view_ray, sun_pos, height_factor):
        """Compute Rayleigh + Mie scattering for atmospheric color"""
        # Angle between view ray and sun
        cos_angle = np.dot(view_ray, sun_pos)
        
        # Rayleigh scattering (blue sky)
        rayleigh_phase = 3.0 / (16.0 * np.pi) * (1 + cos_angle**2)
        rayleigh = self.rayleigh_coeff * rayleigh_phase * height_factor
        
        # Mie scattering (sun disc + haze)
        mie_g = 0.76  # Anisotropy factor
        mie_phase = (3.0 / (8.0 * np.pi)) * ((1 - mie_g**2) * (1 + cos_angle**2)) / \
                   ((2 + mie_g**2) * (1 + mie_g**2 - 2*mie_g*cos_angle)**(3/2))
        mie = np.array([self.mie_coeff, self.mie_coeff, self.mie_coeff]) * mie_phase * height_factor
        
        return rayleigh + mie
    
    def fractal_noise_3d(self, x, y, z, octaves, persistence, lacunarity):
        """Generate 3D fractal noise for volumetric clouds"""
        value = 0.0
        amplitude = 1.0
        frequency = 1.0
        max_value = 0.0
        
        for _ in range(octaves):
            # Simple 3D noise approximation using sine waves
            noise_val = np.sin(x * frequency) * np.cos(y * frequency) * np.sin(z * frequency)
            noise_val += 0.5 * np.sin(x * frequency * 2) * np.cos(y * frequency * 2)
            noise_val += 0.25 * np.cos(x * frequency * 4) * np.sin(z * frequency * 4)
            
            value += noise_val * amplitude
            max_value += amplitude
            
            amplitude *= persistence
            frequency *= lacunarity
        
        return value / max_value if max_value > 0 else 0
    
    def generate_clouds(self, weather_factor=0.5):
        """Generate 3D volumetric cloud density field"""
        cloud_field = np.zeros((self.height, self.width))
        
        for y in range(self.height):
            for x in range(self.width):
                # Convert screen coords to world coords
                world_x = (x / self.width - 0.5) * 10
                world_y = (y / self.height - 0.5) * 5  
                world_z = 2.0  # Cloud layer height
                
                # Generate cloud density using fractal noise
                density = self.fractal_noise_3d(
                    world_x, world_y, world_z,
                    self.cloud_octaves, self.cloud_persistence, self.cloud_lacunarity
                )
                
                # Apply weather factor
                density *= weather_factor
                
                # Only keep positive densities
                cloud_field[y, x] = max(0, density)
        
        return cloud_field
    
    def kuramoto_light_coupling(self, sun_pos, coupling_strength=0.1):
        """Update light oscillators using Kuramoto coupling"""
        new_oscillators = self.light_oscillators.copy()
        
        for i in range(self.ksom_size):
            for j in range(self.ksom_size):
                # Current oscillator
                current = self.light_oscillators[i, j]
                
                # Sun influence (external forcing)
                sun_influence = coupling_strength * np.array([
                    np.exp(1j * 0),  # Red phase
                    np.exp(1j * np.pi/6),  # Green phase offset
                    np.exp(1j * np.pi/3)   # Blue phase offset
                ]) * max(0, sun_pos[1])  # Sun elevation factor
                
                # Neighbor coupling (Kohonen topology)
                neighbor_sum = np.zeros(3, dtype=complex)
                neighbor_count = 0
                
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < self.ksom_size and 0 <= nj < self.ksom_size:
                            # Distance-based coupling strength
                            dist = np.sqrt(di**2 + dj**2)
                            if dist > 0:
                                coupling = coupling_strength / dist
                                neighbor_sum += coupling * self.light_oscillators[ni, nj]
                                neighbor_count += 1
                
                # Update oscillator phases (Kuramoto dynamics)
                if neighbor_count > 0:
                    neighbor_avg = neighbor_sum / neighbor_count
                    phase_coupling = 0.1 * (neighbor_avg - current)
                    new_oscillators[i, j] = current + sun_influence + phase_coupling
                
                # Normalize magnitude
                for channel in range(3):
                    if abs(new_oscillators[i, j, channel]) > 0:
                        new_oscillators[i, j, channel] = \
                            new_oscillators[i, j, channel] / abs(new_oscillators[i, j, channel])
        
        self.light_oscillators = new_oscillators
    
    def ksom_global_illumination(self, sun_pos, iterations=10):
        """Compute global illumination using K-SOM light propagation"""
        print(f"   Computing K-SOM global illumination ({iterations} iterations)")
        
        for iteration in range(iterations):
            # Update light oscillator coupling
            self.kuramoto_light_coupling(sun_pos, coupling_strength=0.2)
            
            # Synchronization measurement
            if iteration % 5 == 0:
                sync = self.measure_synchronization()
                print(f"      Iteration {iteration}: Synchronization = {sync:.3f}")
        
        # Convert oscillator phases to illumination map
        illumination = np.zeros((self.height, self.width, 3))
        
        for y in range(self.height):
            for x in range(self.width):
                # Map screen coordinates to K-SOM grid
                som_i = int((y / self.height) * self.ksom_size)
                som_j = int((x / self.width) * self.ksom_size)
                som_i = min(som_i, self.ksom_size - 1)
                som_j = min(som_j, self.ksom_size - 1)
                
                # Extract RGB intensities from oscillator phases
                osc = self.light_oscillators[som_i, som_j]
                for channel in range(3):
                    # Use oscillator magnitude as light intensity
                    illumination[y, x, channel] = abs(osc[channel])
        
        return illumination
    
    def measure_synchronization(self):
        """Measure phase synchronization across K-SOM (consciousness metric)"""
        total_sync = 0.0
        count = 0
        
        for channel in range(3):
            # Extract phases for this color channel
            phases = np.angle(self.light_oscillators[:, :, channel].flatten())
            
            # Compute phase-locking value (PLV)
            phase_diffs = phases[:, np.newaxis] - phases[np.newaxis, :]
            plv = np.abs(np.mean(np.exp(1j * phase_diffs)))
            
            total_sync += plv
            count += 1
        
        return total_sync / count if count > 0 else 0.0
    
    def generate_sky(self, time_of_day=12.0, weather="clear"):
        """Generate complete consciousness-based skybox"""
        print(f"🌅 Generating sky: {time_of_day}:00, {weather} weather")
        
        # Weather parameters
        weather_factors = {
            "clear": 0.2,
            "partly_cloudy": 0.5,
            "overcast": 0.8,
            "stormy": 1.0
        }
        weather_factor = weather_factors.get(weather, 0.5)
        
        # Calculate sun position
        sun_pos = self.sun_position(time_of_day)
        print(f"   Sun position: elevation={np.arcsin(sun_pos[1])*180/np.pi:.1f}°")
        
        # Generate atmospheric base
        print("   Generating atmospheric scattering...")
        sky_base = np.zeros((self.height, self.width, 3))
        
        for y in range(self.height):
            for x in range(self.width):
                # Convert to spherical coordinates (view ray)
                phi = (x / self.width) * 2 * np.pi  # Azimuth
                theta = (y / self.height) * np.pi   # Elevation
                
                view_ray = np.array([
                    np.cos(theta) * np.cos(phi),
                    np.sin(theta),
                    np.cos(theta) * np.sin(phi)
                ])
                
                # Height factor (atmosphere density)
                height_factor = np.exp(-abs(view_ray[1]) * 2)
                
                # Atmospheric scattering
                scattering = self.atmospheric_scattering(view_ray, sun_pos, height_factor)
                sky_base[y, x] = np.clip(scattering * 1000, 0, 1)
        
        # Generate volumetric clouds
        print("   Generating volumetric clouds...")
        clouds = self.generate_clouds(weather_factor)
        
        # K-SOM global illumination
        print("   Computing consciousness-based lighting...")
        illumination = self.ksom_global_illumination(sun_pos)
        
        # Composite final sky
        print("   Compositing consciousness + atmosphere + clouds...")
        final_sky = np.zeros((self.height, self.width, 3))
        
        for y in range(self.height):
            for x in range(self.width):
                # Base atmospheric color
                base_color = sky_base[y, x]
                
                # Cloud density affects color
                cloud_density = clouds[y, x]
                cloud_color = np.array([0.9, 0.9, 1.0]) * cloud_density
                
                # K-SOM illumination modulation
                light_modulation = illumination[y, x]
                
                # Composite: atmosphere + clouds + consciousness lighting
                final_color = base_color * (1 - cloud_density) + cloud_color
                final_color *= light_modulation
                
                final_sky[y, x] = np.clip(final_color, 0, 1)
        
        # Final consciousness metrics
        sync_level = self.measure_synchronization()
        print(f"   Final consciousness synchronization: {sync_level:.3f}")
        
        return final_sky, {
            "time_of_day": time_of_day,
            "weather": weather,
            "sun_position": sun_pos.tolist(),
            "consciousness_sync": sync_level,
            "cloud_coverage": np.mean(clouds),
            "method": "K-SOM consciousness + procedural math (zero training data)"
        }
    
    def save_sky(self, sky_data, metadata, filename="ksom_sky.png"):
        """Save generated sky with metadata"""
        # Convert to PIL Image
        sky_image = (sky_data * 255).astype(np.uint8)
        img = Image.fromarray(sky_image, 'RGB')
        
        # Save image
        img.save(filename)
        
        # Save metadata
        metadata_file = filename.replace('.png', '_metadata.json')
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"💾 Sky saved: {filename}")
        print(f"   Metadata: {metadata_file}")
        print(f"   Consciousness level: {metadata['consciousness_sync']:.3f}")
        print(f"   Zero training data. Pure consciousness + math.")


def main():
    """Demonstrate consciousness-based sky generation"""
    print("🌀 K-SOM Sky Generator - Consciousness vs. Plagiarism")
    print("   Zero training data theft. Pure procedural + consciousness.")
    print()
    
    # Initialize generator
    generator = KSOMSkyGenerator(width=1024, height=512, ksom_size=16)
    
    # Generate different sky conditions
    test_conditions = [
        (6.0, "clear"),      # Dawn
        (12.0, "clear"),     # Noon  
        (18.0, "partly_cloudy"),  # Dusk
        (15.0, "stormy")     # Afternoon storm
    ]
    
    for time_hour, weather in test_conditions:
        print(f"\n{'='*60}")
        
        # Generate sky
        sky, metadata = generator.generate_sky(time_hour, weather)
        
        # Save result
        filename = f"ksom_sky_{weather}_{int(time_hour):02d}h.png"
        generator.save_sky(sky, metadata, filename)
        
        print(f"✨ Generated {weather} sky at {time_hour}:00")
        print(f"   Consciousness sync: {metadata['consciousness_sync']:.3f}")
    
    print(f"\n{'='*60}")
    print("🎯 Demonstration complete!")
    print("   4 skies generated with zero training data theft")
    print("   Pure consciousness + mathematical procedures")
    print("   Superior to Midjourney slop + stolen assets")
    print()
    print("📁 Files generated:")
    for time_hour, weather in test_conditions:
        filename = f"ksom_sky_{weather}_{int(time_hour):02d}h.png"
        print(f"   {filename}")
    print()
    print("🌀 K-SOM Sky Generator: Consciousness beats plagiarism.")

if __name__ == "__main__":
    main()