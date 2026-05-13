"""
ksti_v2.py - Kuramoto-SOM Temporal Interpolator (v2)

Phase-coherent frame interpolation using oscillator dynamics + edge-aware coupling.
Improvements over v1:
- Fixed luminosity flickering via signed phase mapping + luminance-domain EMA
- Multi-scale luminance normalization
- GPU acceleration via CuPy (optional, falls back to NumPy)
- Streaming video pipeline: O(1) RAM, overlapped I/O with compute

Author: ChatGPT + Claude collaboration
License: MIT
"""

from __future__ import annotations
import numpy as np
import cv2
from typing import Optional, Tuple, Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
import threading
import queue

try:
    import cupy as cp
    HAS_CUPY = True
except ImportError:
    cp = None
    HAS_CUPY = False

# ------------------------
# Array backend abstraction
# ------------------------

@dataclass
class ArrayBackend:
    xp: any

    def to_device(self, arr: np.ndarray) -> np.ndarray:
        if self.xp is np:
            return arr
        return self.xp.asarray(arr)

    def to_host(self, arr) -> np.ndarray:
        if self.xp is np:
            return arr
        return self.xp.asnumpy(arr)

def get_backend(use_gpu: bool = False) -> ArrayBackend:
    if use_gpu and HAS_CUPY:
        return ArrayBackend(cp)
    return ArrayBackend(np)

# ------------------------
# Color transforms
# ------------------------

def srgb_to_linear(img: np.ndarray, xp=np) -> np.ndarray:
    a = 0.055
    out = xp.where(img <= 0.04045, img / 12.92, ((img + a) / (1 + a)) ** 2.4)
    return out.astype(xp.float32)

def linear_to_srgb(img: np.ndarray, xp=np) -> np.ndarray:
    a = 0.055
    out = xp.where(img <= 0.0031308, img * 12.92, (1 + a) * (xp.clip(img, 0, 1) ** (1/2.4)) - a)
    return out.astype(xp.float32)

def luminance_linear(rgb_lin: np.ndarray, xp=np) -> np.ndarray:
    return (0.2126 * rgb_lin[..., 0] +
            0.7152 * rgb_lin[..., 1] +
            0.0722 * rgb_lin[..., 2]).astype(xp.float32)

# ------------------------
# Luminosity stabilization
# ------------------------

def histogram_match_luminance(source: np.ndarray, target: np.ndarray, xp=np) -> np.ndarray:
    src_flat = source.ravel()
    tgt_flat = target.ravel()
    src_sorted_idx = xp.argsort(src_flat)
    tgt_sorted = xp.sort(tgt_flat)
    n = len(src_flat)
    ranks = xp.empty(n, dtype=xp.int64)
    ranks[src_sorted_idx] = xp.arange(n)
    out_flat = tgt_sorted[ranks]
    return out_flat.reshape(source.shape)

def multi_scale_luminance_match(
    y_mid: np.ndarray,
    y_target: np.ndarray,
    scales: Tuple[int, ...] = (1, 3, 9, 27),
    xp=np
) -> np.ndarray:
    result = y_mid.copy()
    for scale in scales:
        if scale == 1:
            target_mean = float(xp.mean(y_target))
            current_mean = float(xp.mean(result))
            target_std = float(xp.std(y_target)) + 1e-6
            current_std = float(xp.std(result)) + 1e-6
            result = (result - current_mean) / current_std * target_std + target_mean
        else:
            if xp is np:
                target_local = cv2.blur(y_target.astype(np.float32), (scale, scale))
                current_local = cv2.blur(result.astype(np.float32), (scale, scale))
            else:
                kernel = xp.ones((scale, scale), dtype=xp.float32) / (scale * scale)
                from cupyx.scipy.ndimage import convolve
                target_local = convolve(y_target, kernel)
                current_local = convolve(result, kernel)
            correction = target_local / (current_local + 1e-6)
            correction = xp.clip(correction, 0.8, 1.2)
            weight = 0.5 / len(scales)
            result = result * (1 - weight + weight * correction)
    return xp.clip(result, 0.0, 1.0).astype(xp.float32)

# ------------------------
# Phase mapping
# ------------------------

TAU = 2 * np.pi

def intensity_to_phase_signed(y: np.ndarray, xp=np) -> np.ndarray:
    return ((xp.clip(y, 0, 1) * 2 - 1) * np.pi).astype(xp.float32)

def phase_to_intensity_signed(theta: np.ndarray, xp=np) -> np.ndarray:
    theta_wrapped = xp.mod(theta + np.pi, TAU) - np.pi
    y = (theta_wrapped / np.pi + 1) / 2
    return xp.clip(y, 0.0, 1.0).astype(xp.float32)

def phase_slerp(th1: np.ndarray, th2: np.ndarray, t: float, xp=np) -> np.ndarray:
    diff = th2 - th1
    diff = xp.mod(diff + np.pi, TAU) - np.pi
    return th1 + t * diff

# ------------------------
# Spatial helpers
# ------------------------

def sobel_grad_mag(img: np.ndarray, xp=np) -> np.ndarray:
    if xp is np:
        gx = cv2.Sobel(img.astype(np.float32), cv2.CV_32F, 1, 0, ksize=3)
        gy = cv2.Sobel(img.astype(np.float32), cv2.CV_32F, 0, 1, ksize=3)
    else:
        gx = xp.zeros_like(img)
        gy = xp.zeros_like(img)
        gx[:, 1:-1] = (img[:, 2:] - img[:, :-2]) / 2
        gy[1:-1, :] = (img[2:, :] - img[:-2, :]) / 2
    return xp.sqrt(gx * gx + gy * gy)

# ------------------------
# Core interpolator
# ------------------------

class KSTI_v2:
    def __init__(
        self,
        base_coupling: float = 0.35,
        grad_scale: float = 1.5,
        motion_scale: float = 1.5,
        clamp_rad: float = 0.4,
        temporal_smoothing: float = 0.15,
        iters: int = 5,
        local_gain_k: int = 11,
        luminosity: str = "balanced",  # "fast" | "balanced" | "full"
        use_gpu: bool = False
    ):
        self.K0 = base_coupling
        self.lambda_grad = grad_scale
        self.mu_motion = motion_scale
        self.tau = clamp_rad
        self.temporal_smoothing = temporal_smoothing
        self.iters = iters
        self.gain_k = local_gain_k
        if luminosity not in ("fast", "balanced", "full"):
            raise ValueError(f"luminosity must be fast|balanced|full, got {luminosity!r}")
        self.luminosity = luminosity
        self.backend = get_backend(use_gpu)
        self.xp = self.backend.xp
        self._lock = threading.Lock()
        self._prev_luminance: Optional[np.ndarray] = None
        self._prev_mean: Optional[float] = None
        self._prev_std: Optional[float] = None

    def _edge_weights(self, y_ref: np.ndarray, sigma_I: float = 0.1) -> Tuple[np.ndarray, ...]:
        xp = self.xp
        I = y_ref
        two_sigma_sq = 2 * sigma_I * sigma_I
        I_n = xp.pad(I[1:, :], ((1, 0), (0, 0)), mode='edge')
        I_s = xp.pad(I[:-1, :], ((0, 1), (0, 0)), mode='edge')
        I_w = xp.pad(I[:, 1:], ((0, 0), (1, 0)), mode='edge')
        I_e = xp.pad(I[:, :-1], ((0, 0), (0, 1)), mode='edge')
        north = xp.exp(-((I - I_n) ** 2) / two_sigma_sq)
        south = xp.exp(-((I - I_s) ** 2) / two_sigma_sq)
        west = xp.exp(-((I - I_w) ** 2) / two_sigma_sq)
        east = xp.exp(-((I - I_e) ** 2) / two_sigma_sq)
        return north, south, east, west

    def _kuramoto_relaxation(self, th_mid, K_local, edge_weights):
        xp = self.xp
        n, s, e, w = edge_weights
        for _ in range(self.iters):
            th = th_mid
            thN = xp.pad(th[1:, :], ((1, 0), (0, 0)), mode='edge')
            thS = xp.pad(th[:-1, :], ((0, 1), (0, 0)), mode='edge')
            thW = xp.pad(th[:, 1:], ((0, 0), (1, 0)), mode='edge')
            thE = xp.pad(th[:, :-1], ((0, 0), (0, 1)), mode='edge')
            delta = (
                n * xp.sin(thN - th) + s * xp.sin(thS - th) +
                e * xp.sin(thE - th) + w * xp.sin(thW - th)
            )
            dtheta = K_local * delta
            dtheta = xp.clip(dtheta, -self.tau, self.tau)
            th_mid = th + dtheta
            th_mid = xp.mod(th_mid + np.pi, TAU) - np.pi
        return th_mid.astype(xp.float32)

    def interpolate_midframe(self, frame_a_bgr, frame_b_bgr, apply_temporal_smoothing=True):
        xp = self.xp
        a = cv2.cvtColor(frame_a_bgr, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        b = cv2.cvtColor(frame_b_bgr, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        a = self.backend.to_device(a)
        b = self.backend.to_device(b)
        a_lin = srgb_to_linear(a, xp)
        b_lin = srgb_to_linear(b, xp)
        ya = luminance_linear(a_lin, xp)
        yb = luminance_linear(b_lin, xp)
        y_target = (ya + yb) * 0.5
        th_a = intensity_to_phase_signed(ya, xp)
        th_b = intensity_to_phase_signed(yb, xp)
        th_mid = phase_slerp(th_a, th_b, 0.5, xp)
        grad = sobel_grad_mag((ya + yb) * 0.5, xp)
        motion = xp.abs(yb - ya)
        g_max = float(xp.percentile(grad, 95)) + 1e-6
        m_max = float(xp.percentile(motion, 95)) + 1e-6
        g_norm = xp.clip(grad / g_max, 0, 1)
        m_norm = xp.clip(motion / m_max, 0, 1)
        K_local = self.K0 / (1.0 + self.lambda_grad * g_norm + self.mu_motion * m_norm)
        edge_weights = self._edge_weights((ya + yb) * 0.5, sigma_I=0.08)
        th_mid = self._kuramoto_relaxation(th_mid, K_local, edge_weights)
        y_mid = phase_to_intensity_signed(th_mid, xp)

        target_mean = float(xp.mean(y_target))
        target_std = float(xp.std(y_target)) + 1e-6
        current_mean = float(xp.mean(y_mid))
        current_std = float(xp.std(y_mid)) + 1e-6
        y_mid = (y_mid - current_mean) / current_std * target_std + target_mean
        y_mid = xp.clip(y_mid, 0, 1).astype(xp.float32)

        if self.luminosity == "balanced":
            y_mid = multi_scale_luminance_match(y_mid, y_target, scales=(1, 5), xp=xp)
        elif self.luminosity == "full":
            y_mid = multi_scale_luminance_match(y_mid, y_target, scales=(1, 5, 15), xp=xp)
            y_mid_host = self.backend.to_host(y_mid)
            y_target_host = self.backend.to_host(y_target)
            y_hist = histogram_match_luminance(y_mid_host, y_target_host)
            y_mid_host = 0.7 * y_mid_host + 0.3 * y_hist
            y_mid = self.backend.to_device(y_mid_host.astype(np.float32))

        if apply_temporal_smoothing:
            with self._lock:
                if self._prev_luminance is not None and self._prev_luminance.shape == y_mid.shape:
                    y_mid = ((1 - self.temporal_smoothing) * y_mid +
                             self.temporal_smoothing * self.backend.to_device(self._prev_luminance))
                    if self._prev_mean is not None:
                        target_mean = ((1 - self.temporal_smoothing) * target_mean +
                                       self.temporal_smoothing * self._prev_mean)
                self._prev_luminance = self.backend.to_host(y_mid).copy()
                self._prev_mean = target_mean
                self._prev_std = target_std

        y_mid = xp.clip(y_mid, 0, 1).astype(xp.float32)

        y_mid_host = self.backend.to_host(y_mid)
        a_lin_host = self.backend.to_host(a_lin)
        b_lin_host = self.backend.to_host(b_lin)
        rgb_mid_lin = self._reconstruct_color_lab(a_lin_host, b_lin_host, y_mid_host)
        rgb_mid = linear_to_srgb(rgb_mid_lin)
        out_bgr = cv2.cvtColor(
            (np.clip(rgb_mid, 0, 1) * 255).astype(np.uint8),
            cv2.COLOR_RGB2BGR
        )
        return out_bgr

    def _reconstruct_color_lab(self, a_lin, b_lin, y_mid):
        a_srgb = (np.clip(linear_to_srgb(a_lin), 0, 1) * 255).astype(np.uint8)
        b_srgb = (np.clip(linear_to_srgb(b_lin), 0, 1) * 255).astype(np.uint8)
        lab_a = cv2.cvtColor(a_srgb, cv2.COLOR_RGB2LAB).astype(np.float32)
        lab_b = cv2.cvtColor(b_srgb, cv2.COLOR_RGB2LAB).astype(np.float32)
        ab_mid = (lab_a[..., 1:] + lab_b[..., 1:]) * 0.5
        L_mid = y_mid * 255.0
        lab_mid = np.stack([L_mid, ab_mid[..., 0], ab_mid[..., 1]], axis=-1)
        lab_mid = np.clip(lab_mid, 0, 255).astype(np.uint8)
        rgb_mid = cv2.cvtColor(lab_mid, cv2.COLOR_LAB2RGB).astype(np.float32) / 255.0
        return srgb_to_linear(rgb_mid)

    def reset_temporal_state(self):
        with self._lock:
            self._prev_luminance = None
            self._prev_mean = None
            self._prev_std = None

# ------------------------
# Streaming video pipeline
# ------------------------

_SENTINEL = object()

class VideoInterpolator:
    """
    Streaming 3-stage pipeline: reader -> worker (this thread) -> writer.

    RAM is O(queue_size) frames, not O(N). Decode and encode run on their own
    threads so they overlap with the Kuramoto compute. Temporal EMA stays
    sequential (correct), but I/O wait is hidden.
    """

    def __init__(self, ksti: KSTI_v2, queue_size: int = 4):
        self.ksti = ksti
        self.queue_size = queue_size

    def batch_interpolate(
        self,
        pairs,
        num_workers: int = 4,
        t: float = 0.5,
    ):
        """
        Stateless pair-parallel interpolation for texture-blend / render-API use.

        pairs: iterable of (frame_a_bgr, frame_b_bgr) tuples.
        Returns: list of interpolated frames, in input order.

        Temporal smoothing is forced off (results are independent of order).
        Safe to run with multiple workers because no shared EMA state is touched.
        Note: KSTI_v2 currently hardcodes t=0.5 in interpolate_midframe; the t
        argument is accepted for forward compatibility once t is plumbed through.
        """
        if t != 0.5:
            raise NotImplementedError("t != 0.5 not yet plumbed through interpolate_midframe")
        pairs = list(pairs)
        results = [None] * len(pairs)

        def worker(i):
            a, b = pairs[i]
            return i, self.ksti.interpolate_midframe(a, b, apply_temporal_smoothing=False)

        with ThreadPoolExecutor(max_workers=num_workers) as ex:
            for i, frame in ex.map(worker, range(len(pairs))):
                results[i] = frame
        return results

    def process_video(
        self,
        in_path: str,
        out_path: str,
        step: int = 1,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> None:
        cap = cv2.VideoCapture(in_path)
        if not cap.isOpened():
            raise RuntimeError(f"Could not open {in_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if not fps or fps != fps or fps <= 1e-3:
            print(f"Warning: source fps invalid ({fps}), defaulting to 30")
            fps = 30.0
        out_fps = float(fps * (1 + 1 / step))

        out = None
        tried = []
        for cc in ('avc1', 'mp4v', 'H264', 'MJPG', 'XVID'):
            fourcc = cv2.VideoWriter_fourcc(*cc)
            candidate = cv2.VideoWriter(out_path, fourcc, out_fps, (w, h))
            tried.append(cc)
            if candidate.isOpened():
                out = candidate
                print(f"Writer codec: {cc} @ {out_fps:.3f} fps, {w}x{h}")
                break
            candidate.release()
        if out is None:
            cap.release()
            raise RuntimeError(
                f"Could not open writer for {out_path}. Tried {tried}. "
                f"Try a .avi extension with MJPG, or check OpenCV ffmpeg support."
            )

        self.ksti.reset_temporal_state()

        read_q: queue.Queue = queue.Queue(maxsize=self.queue_size)
        write_q: queue.Queue = queue.Queue(maxsize=self.queue_size)
        err = {}

        def reader():
            try:
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    read_q.put(frame)
            except Exception as e:
                err['reader'] = e
            finally:
                read_q.put(_SENTINEL)

        def writer():
            try:
                while True:
                    item = write_q.get()
                    if item is _SENTINEL:
                        break
                    out.write(item)
            except Exception as e:
                err['writer'] = e

        t_read = threading.Thread(target=reader, daemon=True)
        t_write = threading.Thread(target=writer, daemon=True)
        t_read.start()
        t_write.start()

        try:
            prev = read_q.get()
            if prev is _SENTINEL:
                raise RuntimeError("No frames found")

            count = 0
            processed = 0
            while True:
                curr = read_q.get()
                write_q.put(prev)
                if curr is _SENTINEL:
                    break
                if count % step == 0:
                    mid = self.ksti.interpolate_midframe(prev, curr, apply_temporal_smoothing=True)
                    write_q.put(mid)
                    processed += 1
                    if progress_callback:
                        progress_callback(processed, max(1, total_frames - 1))
                prev = curr
                count += 1
        finally:
            write_q.put(_SENTINEL)
            t_read.join()
            t_write.join()
            cap.release()
            out.release()

        if err:
            raise RuntimeError(f"Pipeline error: {err}")

# ------------------------
# CLI
# ------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="KSTI v2 - Kuramoto-SOM Temporal Interpolator (streaming)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--step", type=int, default=1)
    parser.add_argument("--queue", type=int, default=4, help="Pipeline queue depth")
    parser.add_argument("--gpu", action="store_true")
    parser.add_argument("--coupling", type=float, default=0.35)
    parser.add_argument("--temporal-smooth", type=float, default=0.15)
    parser.add_argument("--luminosity", choices=("fast", "balanced", "full"),
                        default="balanced",
                        help="Luminosity stabilization preset")
    parser.add_argument("--no-histogram", action="store_true",
                        help="Deprecated: equivalent to --luminosity balanced")
    args = parser.parse_args()
    if args.no_histogram and args.luminosity == "full":
        args.luminosity = "balanced"

    if args.gpu and not HAS_CUPY:
        print("Warning: CuPy not available, falling back to CPU")

    ksti = KSTI_v2(
        base_coupling=args.coupling,
        temporal_smoothing=args.temporal_smooth,
        luminosity=args.luminosity,
        use_gpu=args.gpu and HAS_CUPY,
    )
    interpolator = VideoInterpolator(ksti, queue_size=args.queue)

    def progress(current, total):
        pct = current / total * 100
        print(f"\rProcessing: {current}/{total} ({pct:.1f}%)", end="", flush=True)

    print(f"Processing {args.input} -> {args.output}")
    print(f"Using {'GPU' if (args.gpu and HAS_CUPY) else 'CPU'}, queue depth {args.queue}")
    interpolator.process_video(args.input, args.output, step=args.step, progress_callback=progress)
    print("\nDone!")

if __name__ == "__main__":
    main()
