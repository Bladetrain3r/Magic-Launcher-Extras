import cv2
import numpy as np
from scipy.integrate import odeint
import os

class CrudeKuramotoSOMUpscaler:
    def __init__(self):
        self.coupling_strength = 0.1
        self.som_size = (32, 32)  # Small SOM grid
        self.phase_resolution = 64  # Downsample for speed
        
    def extract_frames(self, video_path):
        """Extract all frames from video"""
        print(f"Extracting frames from {video_path}...")
        cap = cv2.VideoCapture(video_path)
        frames = []
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # Convert to grayscale for simplicity
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frames.append(gray)
            
        cap.release()
        print(f"Extracted {len(frames)} frames")
        return frames
    
    def downsample_for_phases(self, frame):
        """Downsample frame for phase calculation (speed optimization)"""
        h, w = frame.shape
        new_h, new_w = h // self.phase_resolution, w // self.phase_resolution
        return cv2.resize(frame, (new_w, new_h))
    
    def upsample_phases(self, phases, target_shape):
        """Upsample phase map back to original resolution"""
        return cv2.resize(phases, (target_shape[1], target_shape[0]))
    
    def kuramoto_dynamics(self, phases, t, intensity_field):
        """Kuramoto oscillator dynamics"""
        n_rows, n_cols = phases.shape
        dphases = np.zeros_like(phases)
        
        for i in range(n_rows):
            for j in range(n_cols):
                # Natural frequency based on pixel intensity
                omega = intensity_field[i, j] * 0.1
                
                # Coupling with neighbors
                coupling = 0
                neighbors = [(i-1,j), (i+1,j), (i,j-1), (i,j+1)]
                
                for ni, nj in neighbors:
                    if 0 <= ni < n_rows and 0 <= nj < n_cols:
                        coupling += np.sin(phases[ni, nj] - phases[i, j])
                
                dphases[i, j] = omega + self.coupling_strength * coupling
                
        return dphases.flatten()
    
    def simple_som_weight(self, frame1, frame2, alpha=0.5):
        """Simple SOM-inspired spatial weighting"""
        # Create weight map based on local similarity
        h, w = frame1.shape
        weights = np.ones((h, w)) * alpha
        
        # Reduce weight where frames differ significantly
        diff = np.abs(frame1.astype(float) - frame2.astype(float))
        weights = weights * (1 - diff / 255.0)
        
        return weights
    
    def kuramoto_interpolate(self, frame1, frame2):
        """Generate intermediate frame using Kuramoto dynamics"""
        print("  Generating intermediate frame...")
        
        # Downsample for phase calculation
        small_frame1 = self.downsample_for_phases(frame1)
        small_frame2 = self.downsample_for_phases(frame2)
        
        # Initialize phases from pixel intensities
        phases1 = (small_frame1 / 255.0) * 2 * np.pi
        phases2 = (small_frame2 / 255.0) * 2 * np.pi
        
        # Average intensity field for natural frequencies
        avg_intensity = (small_frame1 + small_frame2) / 2.0 / 255.0
        
        # Solve Kuramoto dynamics for intermediate time
        t_span = np.linspace(0, 1, 10)  # Short integration
        intermediate_phases = phases1.copy()
        
        # Simple phase interpolation with Kuramoto influence
        for _ in range(5):  # Few iterations
            dphases = self.kuramoto_dynamics(intermediate_phases, 0, avg_intensity)
            dphases = dphases.reshape(intermediate_phases.shape)
            intermediate_phases += 0.1 * dphases
        
        # Convert phases back to intensities
        intermediate_intensity = np.abs(np.sin(intermediate_phases))
        
        # Upsample back to original resolution
        upsampled_phases = self.upsample_phases(intermediate_intensity, frame1.shape)
        
        # SOM-inspired spatial blending
        som_weights = self.simple_som_weight(frame1, frame2)
        
        # Blend original interpolation with phase-guided interpolation
        linear_interp = (frame1.astype(float) + frame2.astype(float)) / 2.0
        phase_guided = upsampled_phases * 255.0
        
        # Combine using SOM weights
        result = som_weights * phase_guided + (1 - som_weights) * linear_interp
        
        return np.clip(result, 0, 255).astype(np.uint8)
    
    def save_video(self, frames, output_path, fps=30):
        """Save frames as MP4 video"""
        print(f"Saving {len(frames)} frames to {output_path}...")
        
        if not frames:
            print("No frames to save!")
            return
            
        h, w = frames[0].shape
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(output_path, fourcc, fps, (w, h), isColor=False)
        
        for frame in frames:
            writer.write(frame)
        
        writer.release()
        print(f"Video saved successfully!")
    
    def upscale_video(self, input_path, output_path):
        """Main upscaling function"""
        print("=== KURAMOTO-SOM VIDEO UPSCALER ===")
        
        # Extract frames
        frames = self.extract_frames(input_path)
        if len(frames) < 2:
            print("Need at least 2 frames to upscale!")
            return
        
        # Generate 2x frames using interpolation
        upscaled_frames = []
        for i in range(len(frames) - 1):
            print(f"Processing frame pair {i+1}/{len(frames)-1}")
            
            # Add original frame
            upscaled_frames.append(frames[i])
            
            # Generate intermediate frame
            intermediate = self.kuramoto_interpolate(frames[i], frames[i+1])
            upscaled_frames.append(intermediate)
        
        # Add final frame
        upscaled_frames.append(frames[-1])
        
        # Save result
        self.save_video(upscaled_frames, output_path, fps=60)  # 2x framerate
        
        print(f"Upscaling complete!")
        print(f"Original: {len(frames)} frames")
        print(f"Upscaled: {len(upscaled_frames)} frames")

# Usage example
if __name__ == "__main__":
    upscaler = CrudeKuramotoSOMUpscaler()
    
    # Make sure input/output directories exist
    os.makedirs("input", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    input_file = "input/test_video.mp4"  # Put your test video here
    output_file = "output/upscaled_2x.mp4"
    
    if os.path.exists(input_file):
        upscaler.upscale_video(input_file, output_file)
    else:
        print(f"Please place a test video at: {input_file}")
        print("The upscaler will:")
        print("- Extract frames from input MP4")
        print("- Use Kuramoto phase dynamics for temporal coherence")
        print("- Apply SOM-inspired spatial weighting")
        print("- Generate intermediate frames (2x upscaling)")
        print("- Output upscaled MP4 at 60fps")