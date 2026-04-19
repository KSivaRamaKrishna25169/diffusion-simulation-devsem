import devsim
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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

NA = 1e18      # very high background p-type
Ns = 1e20
λ = 0.2e-4     # 0.2 µm

devsim.node_model(device="pn_device", region="silicon", name="NetDoping",
                  equation=f"{Ns} * exp(-x / {λ}) - {NA}")

x_cm = devsim.get_node_model_values(device="pn_device", region="silicon", name="x")
doping = devsim.get_node_model_values(device="pn_device", region="silicon", name="NetDoping")
x_um = np.array(x_cm) * 1e4
doping_arr = np.array(doping)

# Find junction depth
junction_idx = np.where(np.diff(np.sign(doping_arr)))[0]
if len(junction_idx) > 0:
    xj_um = x_um[junction_idx[0]]
    print(f"Junction depth: {xj_um:.3f} µm")
else:
    xj_um = None
    print("No junction found.")

plt.figure(figsize=(8,5))
plt.plot(x_um, doping_arr, 'b-', linewidth=2)
plt.axhline(y=0, color='r', linestyle='--', label='Net Doping = 0')
if xj_um:
    plt.axvline(x=xj_um, color='k', linestyle='--', label=f'Junction at {xj_um:.3f} µm')
plt.xlabel("Depth (microns)")
plt.ylabel("Net Doping Concentration (cm⁻³)")
plt.title("PN Junction: High NA (1e18) & Small λ (0.2 µm)")
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.savefig("pn_highNA_smallLambda.png", dpi=150, bbox_inches='tight')
print("Saved: pn_highNA_smallLambda.png")
