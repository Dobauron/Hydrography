import sympy as sp
from sympy.vector import curl, CoordSys3D

C = CoordSys3D('C')

# 1. Definiujemy zmienne symboliczne
x, y, z = sp.symbols('x y z')

# 2. Definiujemy funkcję temperatury T(x, y, z)
# Podstawiam przykład: T = 10 + x^2 + y^2 (dostosuj do swojego zadania)
T = 10 + x**2 + y**2

# --- OBLICZENIA ---

# Gradient: nabla T
grad_T = [sp.diff(T, var) for var in (x, y, z)]

# Pole przepływu ciepła: F = -nabla T
F = [-y,x,0]
# Dywergencja pola F: div(F) = dFx/dx + dFy/dy + dFz/dz
div_F = sp.diff(F[0], x) + sp.diff(F[1], y) + sp.diff(F[2], z)

# Rotacja pola F: curl(F)
rot_F = [
    sp.diff(F[2], y) - sp.diff(F[1], z),
    sp.diff(F[0], z) - sp.diff(F[2], x),
    sp.diff(F[1], x) - sp.diff(F[0], y)
]
rot_F_2 = curl(F)

# Operator Laplace'a: Delta T = div(grad T)
laplace_T = sp.diff(grad_T[0], x) + sp.diff(grad_T[1], y) + sp.diff(grad_T[2], z)

# --- WYŚWIETLANIE WYNIKÓW ---

print(f"1. Gradient temperatury (∇T): {grad_T}")
print(f"2. Pole przepływu ciepła (F = -∇T): {F}")
print(f"3. Dywergencja pola F: {div_F}")
print(f"4. Rotacja pola F: {rot_F}")
print(f"5. Operator Laplace'a (ΔT): {laplace_T}")

# --- WARTOŚĆ W PUNKCIE ---
# Przykład dla punktu (x=1, y=2, z=0)
punkt = {x: 2, y: 4, z: 6}

print(rot_F_2.to_matrix(C))