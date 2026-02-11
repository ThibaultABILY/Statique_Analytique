import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Physical parameters
# -----------------------------
T = 1e3          # Cable tension [N]
m = 80           # Operator mass [kg]
g = 9.81         # Gravity [m/s^2]
P = m * g        # Operator weight [N]

# -----------------------------
# Range of ladder angles
# -----------------------------
alpha = np.linspace(5, 80, 1000)  # degrees

# -----------------------------
# Reactions at point C
# -----------------------------
Ry = P / 4  # vertical reaction at C

# Horizontal reaction at C:
#   Rx(α) = (P/4) * cot(α) − T/2
Rx = P / (4 * np.tan(np.deg2rad(alpha))) - T / 2

# Minimum friction coefficient needed to avoid slipping at C
mu_min = np.abs(Rx) / Ry

# -----------------------------
# Reference friction coefficients
# -----------------------------
mu_vals = [0.5, 0.3]       # e.g. dry floor, wet floor
colors  = ['g', 'b']

# -----------------------------
# Plot
# -----------------------------
plt.figure()
plt.plot(alpha, mu_min, 'k', label=r'$\mu_{\min}(\alpha)$')

for mu, col in zip(mu_vals, colors):
    # Horizontal line for this friction coefficient
    plt.axhline(mu, color=col, linestyle='--', label=fr'$\mu = {mu}$')

    # Safe angles: mu >= mu_min(alpha)
    safe_mask = mu >= mu_min

    if np.any(safe_mask):
        alpha_safe = alpha[safe_mask]
        alpha_crit = alpha_safe.max()  # critical angle (last safe angle)
        mu_crit    = np.interp(alpha_crit, alpha, mu_min)

        print(f"mu = {mu}: alpha_crit ≈ {alpha_crit:.2f} deg")

        # Mark the critical point
        plt.scatter(alpha_crit, mu_crit, color=col)

        # Text label near the point (avoid \text{} to keep mathtext simple)
        label = r'$\alpha_{\mathrm{crit}} \approx ' + f'{alpha_crit:.1f}' + r'^\circ$'
        plt.annotate(
            label,
            xy=(alpha_crit, mu_crit),
            xytext=(alpha_crit + 2, mu_crit + 0.1),
            arrowprops=dict(arrowstyle='->', color=col),
            color=col
        )
    else:
        print(f"mu = {mu}: no safe angle in [5°, 80°]")

plt.xlabel(r'$\alpha$ (deg)')
plt.ylabel(r'$\mu$')
plt.grid(True)
plt.legend()
plt.title('Adhesion zones and critical angle for different $\mu$')
plt.show()
