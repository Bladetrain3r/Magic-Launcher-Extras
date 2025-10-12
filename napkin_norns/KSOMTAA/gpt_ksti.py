
"""
ksti.py — Kuramoto-SOM Temporal Interpolator (prototype)

Phase-coherent frame interpolation using oscillator dynamics + edge-aware coupling.
Deterministic, no ML. Designed as a drop-in prototype for experimentation.

Author: ChatGPT (with user collaboration)
License: MIT
"""

from __future__ import annotations
import numpy as np
import cv2
from typing import Optional, Tuple

# ------------------------
# Utility: Color transforms
# ------------------------

def srgb_to_linear(img: np.ndarray) -> np.ndarray:
    """Convert sRGB [0,1] to linear light [0,1]."""
    a = 0.055
    out = np.where(img <= 0.04045, img / 12.92, ((img + a) / (1 + a)) ** 2.4)
    return out

def linear_to_srgb(img: np.ndarray) -> np.ndarray:
    """Convert linear light [0,1] to sRGB [0,1]."""
    a = 0.055
    out = np.where(img <= 0.0031308, img * 12.92, (1 + a) * (np.clip(img,0,1) ** (1/2.4)) - a)
    return out

def luminance_linear(rgb_lin: np.ndarray) -> np.ndarray:
    """ITU BT.709 luminance from linear RGB."""
    r,g,b = rgb_lin[...,0], rgb_lin[...,1], rgb_lin[...,2]
    return 0.2126*r + 0.7152*g + 0.0722*b

# ------------------------
# Phase mapping utilities
# ------------------------

TAU = 2*np.pi

def intensity_to_phase(y: np.ndarray) -> np.ndarray:
    """Map luminance [0,1] to phase θ ∈ [0, 2π)."""
    return (np.clip(y,0,1) * TAU).astype(np.float32)

def phase_to_intensity(theta: np.ndarray) -> np.ndarray:
    """Map phase θ back to luminance [0,1]."""
    # Invert linear mapping (note: many-to-one; acceptable for prototype)
    y = (theta % TAU) / TAU
    return np.clip(y, 0.0, 1.0).astype(np.float32)

def complex_from_phase(theta: np.ndarray) -> np.ndarray:
    return np.cos(theta) + 1j*np.sin(theta)

def complex_slerp(z1: np.ndarray, z2: np.ndarray, t: float) -> np.ndarray:
    """
    Geodesic interpolation on the unit circle: z_t = z1 * (z2/z1)^t
    Avoids 2π wrap issues.
    """
    # Prevent divide-by-zero by nudging degenerate cases
    eps = 1e-8
    ratio = z2 / (z1 + eps)
    # Normalize to unit circle to limit numerical drift
    ratio /= np.abs(ratio) + eps
    zt = z1 * (ratio ** t)
    # Re-normalize
    zt /= np.abs(zt) + eps
    return zt

# ------------------------
# Spatial/temporal helpers
# ------------------------

def sobel_grad_mag(img: np.ndarray) -> np.ndarray:
    """Simple gradient magnitude for adaptive coupling (expects single channel float32)."""
    gx = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=3)
    mag = np.sqrt(gx*gx + gy*gy)
    return mag

def box_filter(img: np.ndarray, k: int) -> np.ndarray:
    """Fast box filter (mean) with odd kernel size k."""
    return cv2.blur(img, (k,k))

# ------------------------
# Core interpolator
# ------------------------

class KSTI:
    """
    Kuramoto-SOM Temporal Interpolator (prototype)
    - Circular slerp mid-phase
    - Edge-aware, adaptive Kuramoto coupling
    - Optional temporal EMA stabilization
    - Local gain normalization
    """
    def __init__(
        self,
        base_coupling: float = 0.3,
        grad_scale: float = 2.0,
        motion_scale: float = 2.0,
        clamp_rad: float = 0.5,
        ema_beta: float = 0.05,
        iters: int = 5,
        kernel_edge: int = 3,
        local_gain_k: int = 9
    ):
        self.K0 = base_coupling
        self.lambda_grad = grad_scale
        self.mu_motion = motion_scale
        self.tau = clamp_rad
        self.beta = ema_beta
        self.iters = iters
        self.ksize = kernel_edge
        self.gain_k = local_gain_k
        self._prev_theta: Optional[np.ndarray] = None  # for EMA across calls

    def _edge_weights(self, y_ref: np.ndarray, sigma_I: float = 0.1) -> Tuple[np.ndarray,...]:
        """
        Compute 4-neighbor bilateral-like weights based on intensity similarity to reduce cross-edge coupling.
        Returns weights for N,S,E,W.
        """
        I = y_ref
        north = np.exp(-((I - np.pad(I[1:,:], ((1,0),(0,0)), mode='edge'))**2) / (2*sigma_I*sigma_I))
        south = np.exp(-((I - np.pad(I[:-1,:], ((0,1),(0,0)), mode='edge'))**2) / (2*sigma_I*sigma_I))
        west  = np.exp(-((I - np.pad(I[:,1:], ((0,0),(1,0)), mode='edge'))**2) / (2*sigma_I*sigma_I))
        east  = np.exp(-((I - np.pad(I[:,:-1], ((0,0),(0,1)), mode='edge'))**2) / (2*sigma_I*sigma_I))
        return north, south, east, west

    def interpolate_midframe(
        self,
        frame_a_bgr: np.ndarray,
        frame_b_bgr: np.ndarray,
        ema_across_calls: bool = True
    ) -> np.ndarray:
        """
        Compute the t=0.5 intermediate frame between frame A and frame B.
        Input frames: uint8 BGR
        Output: uint8 BGR
        """
        # Convert to float in [0,1], BGR->RGB
        a = cv2.cvtColor(frame_a_bgr, cv2.COLOR_BGR2RGB).astype(np.float32)/255.0
        b = cv2.cvtColor(frame_b_bgr, cv2.COLOR_BGR2RGB).astype(np.float32)/255.0

        # Linearize
        a_lin = srgb_to_linear(a)
        b_lin = srgb_to_linear(b)

        # Luminance + per-channel (we'll synth luminance via phase, then color by guided filter to keep prototype simple)
        ya = luminance_linear(a_lin)
        yb = luminance_linear(b_lin)

        # Phase mapping
        th_a = intensity_to_phase(ya)
        th_b = intensity_to_phase(yb)

        # Circular mid via slerp
        z_a = complex_from_phase(th_a)
        z_b = complex_from_phase(th_b)
        z_mid = complex_slerp(z_a, z_b, 0.5)
        th_mid = np.angle(z_mid).astype(np.float32) % TAU

        # Edge-aware Kuramoto coupling (iterative relax)
        grad = sobel_grad_mag((ya+yb)*0.5)
        motion = np.abs(yb - ya)
        # Normalize grad/motion to [0,1] robustly
        g_norm = grad / (np.percentile(grad, 95) + 1e-6)
        m_norm = motion / (np.percentile(motion, 95) + 1e-6)
        K_local = self.K0 / (1.0 + self.lambda_grad * g_norm + self.mu_motion * m_norm)

        n,s,e,w = self._edge_weights((ya+yb)*0.5, sigma_I=0.08)

        for _ in range(self.iters):
            # 4-neighbor coupling; pad for shifts
            th = th_mid
            thN = np.pad(th[1:,:], ((1,0),(0,0)), mode='edge')
            thS = np.pad(th[:-1,:], ((0,1),(0,0)), mode='edge')
            thW = np.pad(th[:,1:], ((0,0),(1,0)), mode='edge')
            thE = np.pad(th[:,:-1], ((0,0),(0,1)), mode='edge')

            delta = (
                n * np.sin(thN - th) +
                s * np.sin(thS - th) +
                e * np.sin(thE - th) +
                w * np.sin(thW - th)
            )
            dtheta = K_local * delta
            # Clamp to avoid overshoot
            dtheta = np.clip(dtheta, -self.tau, self.tau)
            th_mid = (th + dtheta).astype(np.float32)

        # Optional temporal EMA to reduce flicker across a sequence
        if ema_across_calls:
            if self._prev_theta is None or self._prev_theta.shape != th_mid.shape:
                self._prev_theta = th_mid.copy()
            th_mid = (1.0 - self.beta) * th_mid + self.beta * self._prev_theta
            self._prev_theta = th_mid.copy()

        # Map back to luminance
        y_mid = phase_to_intensity(th_mid)

        # Local gain normalization toward mean of source luminances
        target_mean = box_filter((ya + yb) * 0.5, self.gain_k)
        y_mean = box_filter(y_mid, self.gain_k)
        eps = 1e-5
        gain = target_mean / (y_mean + eps)
        y_mid = np.clip(y_mid * gain, 0.0, 1.0)

        # Simple colorization: guide RGB channels by ratio to luminance (preserve chroma)
        # Compute chroma from source 'a' and 'b' and average
        def chroma(rgb_lin, y):
            y_safe = np.maximum(y[...,None], 1e-4)
            return rgb_lin / y_safe
        chroma_avg = 0.5 * (chroma(a_lin, ya) + chroma(b_lin, yb))
        rgb_mid_lin = np.clip(chroma_avg * y_mid[...,None], 0.0, 1.0)

        # Back to sRGB uint8, RGB->BGR
        rgb_mid = linear_to_srgb(rgb_mid_lin)
        out_bgr = cv2.cvtColor((np.clip(rgb_mid,0,1)*255.0).astype(np.uint8), cv2.COLOR_RGB2BGR)
        return out_bgr

# ------------------------
# Simple CLI utilities
# ------------------------

def interpolate_video_midframes(
    in_path: str,
    out_path: str,
    step: int = 1
) -> None:
    """
    Insert a mid-frame between every 'step' frames.
    e.g., step=1 turns N frames into ~2N-1 frames (roughly doubling fps).
    """
    cap = cv2.VideoCapture(in_path)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open {in_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, fps * (1 + 1/step), (w, h))

    ksti = KSTI()

    ret, prev = cap.read()
    if not ret:
        raise RuntimeError("No frames found")

    count = 0
    while True:
        ret, curr = cap.read()
        out.write(prev)
        if not ret:
            break
        if count % step == 0:
            mid = ksti.interpolate_midframe(prev, curr, ema_across_calls=True)
            out.write(mid)
        prev = curr
        count += 1

    cap.release()
    out.release()

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="KSTI — Kuramoto-SOM Temporal Interpolator")
    p.add_argument("input", help="Input video path")
    p.add_argument("output", help="Output video path")
    p.add_argument("--step", type=int, default=1, help="Insert a mid-frame after every N frames (default 1)")
    args = p.parse_args()
    interpolate_video_midframes(args.input, args.output, step=args.step)
