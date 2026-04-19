# Diffusion Processing Unit in IC Fabrication

**Group 7** | **Supervisor: Dr. S. S. Jamuar**  
**K. Siva Rama Krishna (MT25169)** | **Abhishek Maurya (MT25095)**

---

## 📌 Project Overview

This project simulates the **diffusion process** used in integrated circuit fabrication. Diffusion introduces dopant atoms (Boron, Phosphorus, Arsenic) into silicon to create n‑type and p‑type regions, forming essential device structures like MOSFET source/drain, wells, resistors, and PN junctions.

We used **DEVSIM** – an open‑source TCAD simulator – to model:
- Exponential doping profiles
- Transient diffusion (time evolution of Gaussian)
- PN junction formation
- Temperature‑dependent diffusion for different dopants (B, P, As)

All simulations are 1D and based on Fick’s laws and the Arrhenius equation.

---

## 🛠️ Tools & Dependencies

- **DEVSIM** – TCAD simulator (Python‑based)
- **Python 3.7+**
- **Matplotlib** – for plotting
- **NumPy** – for numerical operations
- **Ubuntu / WSL** (recommended) – scripts developed and tested on Ubuntu

---

## 📂 Repository Structure



---

## 🚀 Setup & Installation

### 1. Install DEVSIM and dependencies

Open a terminal and run:

```bash
pip install devsim numpy matplotlib

python3 -m venv devsim_env
source devsim_env/bin/activate
pip install devsim numpy matplotlib

git clone https://github.com/KSivaRamaKrishna25169/diffusion-simulation-devsem.git
cd diffusion-simulation-devsem
