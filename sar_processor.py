"""
Synthetic Aperture Radar (SAR) Time-Domain Backprojection (TDBP) Engine
Developer: Ayoub Lahmar (@Redayoub-lang)
Domain: Military Remote Sensing, Signal Processing & Target Reconnaissance
"""

import numpy as np


class SyntheticApertureRadarProcessor:

  def __init__(
      self,
      center_freq_hz: float = 10e9,
      bandwidth_hz: float = 1e9,
      num_aperture_positions: int = 64,
  ):
    """
    :param center_freq_hz: X-band SAR carrier frequency (10 GHz).
    :param bandwidth_hz: Swept bandwidth (1 GHz -> 15cm range resolution).
    """
    self.fc = center_freq_hz
    self.c = 3e8
    self.wavelength = self.c / self.fc
    self.bandwidth = bandwidth_hz

    # Aperture flight path along X-axis
    self.aperture_x = np.linspace(-15.0, 15.0, num_aperture_positions)
    self.aperture_pos = np.column_stack((
        self.aperture_x,
        np.zeros_like(self.aperture_x),
        np.full_like(self.aperture_x, 1000.0),
    ))

  def process_backprojection(
      self, raw_phase_data: np.ndarray, grid_bounds: tuple[float, float, int]
  ) -> np.ndarray:
    """Executes Exact Time-Domain Backprojection (TDBP) integration over spatial reconstruction grid."""
    min_xy, max_xy, num_pts = grid_bounds
    grid_x = np.linspace(min_xy, max_xy, num_pts)
    grid_y = np.linspace(min_xy, max_xy, num_pts)
    X, Y = np.meshgrid(grid_x, grid_y)

    image_grid = np.zeros((num_pts, num_pts), dtype=np.complex128)

    # Sum phase contributions over all aperture positions
    for idx, sensor_pos in enumerate(self.aperture_pos):
      # Euclidean distance from sensor to each grid pixel
      R = np.sqrt(
          (X - sensor_pos[0]) ** 2
          + (Y - sensor_pos[1]) ** 2
          + (0.0 - sensor_pos[2]) ** 2
      )

      # Two-way delay phase shift
      phase_shift = np.exp(1j * (4.0 * np.pi / self.wavelength) * R)
      image_grid += raw_phase_data[idx] * phase_shift

    return np.abs(image_grid)


if __name__ == "__main__":
  print("[SYSTEM INIT] Military SAR Time-Domain Backprojection Engine...\n")
  sar = SyntheticApertureRadarProcessor()

  # Simulated phase history data from aperture positions
  np.random.seed(42)
  simulated_phase_history = np.exp(
      1j * np.random.uniform(0, 2 * np.pi, len(sar.aperture_pos))
  )

  grid_size = 50
  image = sar.process_backprojection(
      simulated_phase_history, grid_bounds=(-10.0, 10.0, grid_size)
  )

  print(f"[RADAR CONFIG] Carrier Frequency: {sar.fc/1e9:.1f} GHz (X-Band)")
  print(f"[APERTURE] Sensor Positions Evaluated: {len(sar.aperture_pos)}")
  print(
      f"[RECONSTRUCTION] Image Grid Resolved: {grid_size}x{grid_size} Pixels"
  )
  print(f"[REFLECTIVITY] Peak Target Reflectivity: {np.max(image):.4f}\n")
