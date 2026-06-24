# %%
"""
Stress Analysis Basics
----------------------
Copy-paste-ready Python notes for:
- axial stress
- bending stress
- direct shear stress
- torsional shear stress
- combined loading
- von Mises stress
- factor of safety

This file is intentionally written like engineering notes:
1. clear formulas
2. small reusable functions
3. readable comments
4. easy to extend later for bolt groups, welds, and fatigue

How to use:
- Save as: stress_analysis_basics.py
- Run as a normal Python file, OR
- Use VS Code Python Interactive with # %% cells
"""

import math


# %%
# ------------------------------------------------------------
# 1. SECTION / GEOMETRY HELPERS
# ------------------------------------------------------------


def area_circle(d):
    """Return area of a solid circular cross-section.

    Parameters
    ----------
    d : float
        Diameter

    Returns
    -------
    float
        Area = pi*d^2/4
    """
    return math.pi * d**2 / 4.0



def area_annulus(do, di):
    """Return area of a hollow circular section.

    Parameters
    ----------
    do : float
        Outside diameter
    di : float
        Inside diameter

    Returns
    -------
    float
        Area = pi*(do^2 - di^2)/4
    """
    return math.pi * (do**2 - di**2) / 4.0



def second_moment_circle(d):
    """Return second moment of area I for a solid circular section.

    Used for bending stress: sigma = M*c/I
    """
    return math.pi * d**4 / 64.0



def second_moment_annulus(do, di):
    """Return second moment of area I for a hollow circular section."""
    return math.pi * (do**4 - di**4) / 64.0



def polar_moment_circle(d):
    """Return polar moment of inertia J for a solid circular shaft.

    Used for torsion: tau = T*c/J
    """
    return math.pi * d**4 / 32.0



def polar_moment_annulus(do, di):
    """Return polar moment of inertia J for a hollow circular shaft."""
    return math.pi * (do**4 - di**4) / 32.0


# %%
# ------------------------------------------------------------
# 2. BASIC STRESS FUNCTIONS
# ------------------------------------------------------------


def axial_stress(P, A):
    """Return axial normal stress.

    Formula:
        sigma = P / A
    """
    return P / A



def bending_stress(M, c, I):
    """Return bending normal stress.

    Formula:
        sigma = M*c / I

    Notes:
    - c is the distance from neutral axis to the point of interest
    - maximum bending stress usually occurs at the outer fiber
    """
    return M * c / I



def direct_shear_stress(V, A):
    """Return average direct shear stress.

    Formula:
        tau = V / A
    """
    return V / A



def torsional_shear_stress(T, c, J):
    """Return torsional shear stress.

    Formula:
        tau = T*c / J
    """
    return T * c / J


# %%
# ------------------------------------------------------------
# 3. COMBINED STRESSES
# ------------------------------------------------------------


def combine_normal_stress(*stresses):
    """Add normal stress components algebraically.

    Example:
        sigma_total = axial + bending

    Use sign convention carefully:
    - tension positive
    - compression negative
    """
    return sum(stresses)



def resultant_shear_2d(tau_x, tau_y):
    """Return resultant shear from two perpendicular shear components.

    Formula:
        tau_resultant = sqrt(tau_x^2 + tau_y^2)
    """
    return math.sqrt(tau_x**2 + tau_y**2)



def resultant_shear_primary_secondary(tau_primary, tau_secondary):
    """Return resultant shear from primary and secondary shear stresses.

    Useful in bolt-group / weld-group style problems when the two
    components act perpendicular to each other.
    """
    return math.sqrt(tau_primary**2 + tau_secondary**2)


# %%
# ------------------------------------------------------------
# 4. VON MISES STRESS
# ------------------------------------------------------------


def von_mises_plane_stress(sigma_x, tau_xy, sigma_y=0.0):
    """Return von Mises stress for plane stress.

    Full plane-stress equation:
        sigma_vm = sqrt(sigma_x^2 + sigma_y^2 - sigma_x*sigma_y + 3*tau_xy^2)

    Common simplified case:
        if sigma_y = 0,
        sigma_vm = sqrt(sigma_x^2 + 3*tau_xy^2)
    """
    return math.sqrt(
        sigma_x**2 + sigma_y**2 - sigma_x * sigma_y + 3.0 * tau_xy**2
    )



def stress_state_2d(sigma_x, sigma_y, tau_xy):
    """Return a dictionary for a 2D stress state.

    Useful when you want clean outputs for debugging or extension later.
    """
    return {
        "sigma_x": sigma_x,
        "sigma_y": sigma_y,
        "tau_xy": tau_xy,
        "sigma_vm": von_mises_plane_stress(sigma_x, tau_xy, sigma_y),
    }


# %%
# ------------------------------------------------------------
# 5. FACTOR OF SAFETY
# ------------------------------------------------------------


def factor_of_safety_yield(Sy, sigma_vm):
    """Return factor of safety against yielding.

    Formula:
        n = Sy / sigma_vm
    """
    return Sy / sigma_vm


# %%
# ------------------------------------------------------------
# 6. EXAMPLE 1: SOLID SHAFT WITH AXIAL LOAD + TORSION
# ------------------------------------------------------------
# This mirrors your combined loading notes.
#
# Given:
#   P = axial force
#   T = torque
#   d = shaft diameter
#
# Find:
#   axial stress
#   torsional shear stress
#   von Mises stress
#   factor of safety

P = 10_000.0      # axial force
T = 5_000.0       # torque
d = 0.05          # diameter
Sy = 250e6        # sample yield strength (Pa) if SI is used

A = area_circle(d)
I = second_moment_circle(d)
J = polar_moment_circle(d)
c = d / 2.0

sigma_axial = axial_stress(P, A)
tau_torsion = torsional_shear_stress(T, c, J)
sigma_vm = von_mises_plane_stress(sigma_axial, tau_torsion)
n_yield = factor_of_safety_yield(Sy, sigma_vm)

print("EXAMPLE 1: SHAFT WITH AXIAL LOAD + TORSION")
print(f"Area, A              = {A:.6e}")
print(f"Second moment, I     = {I:.6e}")
print(f"Polar moment, J      = {J:.6e}")
print(f"Axial stress         = {sigma_axial:.6e}")
print(f"Torsional shear      = {tau_torsion:.6e}")
print(f"von Mises stress     = {sigma_vm:.6e}")
print(f"Factor of safety, n  = {n_yield:.3f}")
print()


# %%
# ------------------------------------------------------------
# 7. EXAMPLE 2: AXIAL + BENDING + SHEAR
# ------------------------------------------------------------
# This is the usual combined loading workflow:
#
#   sigma_total = sigma_axial + sigma_bending
#   tau_total   = direct shear (or resultant shear)
#   sigma_vm    = sqrt(sigma_total^2 + 3*tau_total^2)

P2 = 12_000.0     # axial load
M2 = 350.0        # bending moment
V2 = 4_000.0      # shear force
d2 = 0.04         # diameter
Sy2 = 300e6       # sample yield strength

A2 = area_circle(d2)
I2 = second_moment_circle(d2)
c2 = d2 / 2.0

sigma_axial_2 = axial_stress(P2, A2)
sigma_bending_2 = bending_stress(M2, c2, I2)
sigma_total_2 = combine_normal_stress(sigma_axial_2, sigma_bending_2)

tau_direct_2 = direct_shear_stress(V2, A2)

sigma_vm_2 = von_mises_plane_stress(sigma_total_2, tau_direct_2)
n_yield_2 = factor_of_safety_yield(Sy2, sigma_vm_2)

print("EXAMPLE 2: AXIAL + BENDING + DIRECT SHEAR")
print(f"Axial stress         = {sigma_axial_2:.6e}")
print(f"Bending stress       = {sigma_bending_2:.6e}")
print(f"Total normal stress  = {sigma_total_2:.6e}")
print(f"Direct shear stress  = {tau_direct_2:.6e}")
print(f"von Mises stress     = {sigma_vm_2:.6e}")
print(f"Factor of safety, n  = {n_yield_2:.3f}")
print()


# %%
# ------------------------------------------------------------
# 8. QUICK REFERENCE / MINI CHEAT SHEET
# ------------------------------------------------------------
# Axial stress:
#   sigma = P / A
#
# Bending stress:
#   sigma = M*c / I
#
# Direct shear stress:
#   tau = V / A
#
# Torsional shear stress:
#   tau = T*c / J
#
# Plane-stress von Mises:
#   sigma_vm = sqrt(sigma_x^2 + sigma_y^2 - sigma_x*sigma_y + 3*tau_xy^2)
#
# Common simplified von Mises when sigma_y = 0:
#   sigma_vm = sqrt(sigma_x^2 + 3*tau^2)
#
# Factor of safety against yielding:
#   n = Sy / sigma_vm


# %%
# ------------------------------------------------------------
# 9. NEXT THINGS TO CODE LATER
# ------------------------------------------------------------
# 1. Bolt group analysis (eccentric loading)
# 2. Weld group analysis
# 3. Fatigue (Goodman / Soderberg)
# 4. Hollow shafts and beams
# 5. Principal stresses / Mohr's circle

print("Script finished successfully.")