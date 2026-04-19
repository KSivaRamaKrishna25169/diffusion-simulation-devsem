import devsim
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --- 1. Create the 1D Mesh (same as before) ---
devsim.create_1d_mesh(mesh="pn_mesh")
x_start, x_end = 0.0, 1e-3
spacing = 1e-5
devsim.add_1d_mesh_line(mesh="pn_mesh", pos=x_start, ps=spacing, tag="surface")
devsim.add_1d_mesh_line(mesh="pn_mesh", pos=x_end, ps=spacing, tag="bottom")
devsim.add_1d_contact(mesh="pn_mesh", name="surface", tag="surface", material="metal")
devsim.add_1d_contact(mesh="pn_mesh", name="bottom", tag="bottom", material="metal")
devsim.add_1d_region(mesh="pn_mesh", material="Si", region="silicon", tag1="surface", tag2="bottom")
devsim.finalize_mesh(mesh="pn_mesh")
devsim.create_device(mesh="pn_mesh", device="pn_device")

# --- 2. Define Background and Diffused Doping ---
# Background p-type doping (Boron)
NA = 1e16  # cm⁻³
# Diffused n-type profile (Phosphorus)
Ns = 1e20  # cm⁻³
λ = 0.5e-4  # 0.5 µm characteristic length

# Net doping = N_D(x) - N_A
devsim.node_model(device="pn_device", region="silicon", name="NetDoping",
                  equation=f"{Ns} * exp(-x / {λ}) - {NA}")

# --- 3. Get Data and Find the Junction ---
x_cm = devsim.get_node_model_values(device="pn_device", region="silicon", name="x")
doping = devsim.get_node_model_values(device="pn_device", region="silicon", name="NetDoping")
x_um = np.array(x_cm) * 1e4
doping_arr = np.array(doping)

# Find the junction depth (where net doping crosses zero)
junction_idx = np.where(np.diff(np.sign(doping_arr)))[0]
if len(junction_idx) > 0:
    xj_um = x_um[junction_idx[0]]
    print(f"Metallurgical junction depth: {xj_um:.3f} µm")
else:
    xj_um = None
    print("Junction depth not found.")

# --- 4. Plot Net Doping (Linear scale to see crossover) ---
plt.figure(figsize=(8,5))
plt.plot(x_um, doping_arr, 'b-', linewidth=2)
plt.axhline(y=0, color='r', linestyle='--', label='Net Doping = 0')
if xj_um:
    plt.axvline(x=xj_um, color='k', linestyle='--', label=f'Junction at {xj_um:.3f} µm')
plt.xlabel("Depth (microns)")
plt.ylabel("Net Doping Concentration (cm⁻³)")
plt.title("PN Junction Doping Profile")
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.savefig("pn_junction.png", dpi=150, bbox_inches='tight')
print("PN junction plot saved as pn_junction.png")
