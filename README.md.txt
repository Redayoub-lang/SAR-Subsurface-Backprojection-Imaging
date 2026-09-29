# Synthetic Aperture Radar (SAR) Time-Domain Backprojection Engine

![Python 3](https://img.shields.io/badge/Language-Python%203.10-blue)
![Remote Sensing](https://img.shields.io/badge/Domain-Radar%20Signal%20Processing-orange)
![Developer](https://img.shields.io/badge/Developer-Ayoub%20Lahmar-brightgreen)

An exact Time-Domain Backprojection (TDBP) image formation processor for airborne Synthetic Aperture Radar (SAR) platforms, reconstructing high-resolution 2D radar reflectivity maps without far-field phase approximations.

Implemented by **Ayoub Lahmar** ([@Redayoub-lang](https://github.com/Redayoub-lang)).

## 📐 Mathematical Formulation

The reconstructed complex image reflectivity \(I(x, y)\) at spatial coordinate \((x, y)\) is calculated via coherent phase integration across \(N\) synthetic aperture positions:

$$
I(x, y) = \sum_{i=1}^{N} S_i\left(\frac{2 R_i(x, y)}{c}\right) \exp\left(j \frac{4\pi}{\lambda} R_i(x, y)\right)
$$

Where range \(R_i(x, y)\) represents the instantaneous 3D Euclidean distance between the platform \(\mathbf{P}_i\) and the ground focal point:

$$
R_i(x,y) = \|\mathbf{P}_i - [x, y, 0]^T\|_2
$$

## 💻 Build & Run

```bash
python sar_processor.py