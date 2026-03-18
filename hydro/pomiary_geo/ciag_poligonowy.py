import numpy as np

# =========================
# DANE
# =========================
A = np.array([5924068.90, 5466351.32])   # 1000
B = np.array([5924041.93, 5466334.40])   # 1002
P1_true = np.array([5924017.04, 5466315.83]) # 1003
C = np.array([5923995.59, 5466340.95])   # 1004
D = np.array([5924041.69, 5466381.78])   # 1005

# OBSERWACJE
alpha_meas = np.array([205.1370176292, 104.1867451247, 101.1519112023])
d = np.array([31.0540979582, 33.0320586705])

# =========================
# FUNKCJE POMOCNICZE
# =========================
def grad2rad(g): return g * np.pi / 200
def rad2grad(r): return r * 200 / np.pi
def norm400(a): return a % 400

def azymut_grad(P1, P2):
    # W geodezji (układ współrzędnych) atan2(dy, dx)
    return norm400(rad2grad(np.arctan2(P2[1]-P1[1], P2[0]-P1[0])))

# =========================
# I ETAP - WYRÓWNANIE KĄTÓW
# =========================
AP = azymut_grad(A, B)
AK = azymut_grad(C, D)

n = len(alpha_meas)
alpha_sum_P = np.sum(alpha_meas)
alpha_sum_T = AK - AP + n * 200

# Normalizacja sumy teoretycznej do dodatniej wartości (analogicznie do MATLABa)
if alpha_sum_T < 0:
    alpha_sum_T += 400
# Dodatkowa normalizacja wielokrotności 400, jeśli zajdzie potrzeba
alpha_sum_T = norm400(alpha_sum_T)
if alpha_sum_T == 0 and alpha_sum_P > 200: alpha_sum_T = 400 # korekta dla pełnego obrotu

f_alpha = alpha_sum_P - alpha_sum_T
v = -f_alpha / n
alpha_corr = alpha_meas + v

# Azymuty boków ciągu
az = np.zeros(len(d))
az[0] = norm400(AP + alpha_corr[0] - 200)       # B->1
az[1] = norm400(az[0] + alpha_corr[1] - 200)    # 1->C

AK_ctrl = norm400(az[1] + alpha_corr[2] - 200)

# =========================
# II ETAP - PRZYROSTY
# =========================
# Obliczenia brakujących pól z Twojego szablonu:
dx = d * np.cos(grad2rad(az))
dy = d * np.sin(grad2rad(az))

D_sum = np.sum(d)

dx_sum_P = np.sum(dx)
dy_sum_P = np.sum(dy)

dx_sum_T = C[0] - B[0]
dy_sum_T = C[1] - B[1]

f_dx = dx_sum_P - dx_sum_T
f_dy = dy_sum_P - dy_sum_T
f_L = np.sqrt(f_dx**2 + f_dy**2)

# Poprawki
v_dx = (-f_dx / D_sum) * d
v_dy = (-f_dy / D_sum) * d

# Zaokrąglenia i residua (rozdzielenie reszty z zaokrągleń na najdłuższy bok)
v_dx = np.round(v_dx, 3)
v_dy = np.round(v_dy, 3)

res_dx = np.round(-f_dx - np.sum(v_dx), 3)
res_dy = np.round(-f_dy - np.sum(v_dy), 3)

idx_max = np.argmax(d)
v_dx[idx_max] += res_dx
v_dy[idx_max] += res_dy

dx_corr = dx + v_dx
dy_corr = dy + v_dy

# =========================
# WSPÓŁRZĘDNE PUNKTU 1
# =========================
X1 = B[0] + dx_corr[0]
Y1 = B[1] + dy_corr[0]

Xc_ctrl = X1 + dx_corr[1]
Yc_ctrl = Y1 + dy_corr[1]

P1 = np.array([X1, Y1])
C_ctrl = np.array([Xc_ctrl, Yc_ctrl])

# =========================
# WYNIKI
# =========================
print(f"=== I ETAP ===")
print(f"AP = {AP:.4f} g")
print(f"AK = {AK:.4f} g")
print(f"Suma praktyczna katow = {alpha_sum_P:.4f} g")
print(f"Suma teoretyczna katow = {alpha_sum_T:.4f} g")
print(f"f_alpha = {f_alpha:.6f} g")
print(f"v = {v:.6f} g")

print("\nKaty poprawione:")
for i, val in enumerate(alpha_corr):
    print(f"alpha_corr({i+1}) = {val:.6f} g")

print("\nAzymuty bokow ciagu:")
print(f"B->1 = {az[0]:.6f} g")
print(f"1->C = {az[1]:.6f} g")
print(f"AK kontrolne = {AK_ctrl:.6f} g")

print(f"\n=== II ETAP ===")
print(f"f_dx = {f_dx:.3f} m")
print(f"f_dy = {f_dy:.3f} m")
print(f"f_L  = {f_L:.3f} m")

print("\nPoprawki do przyrostow:")
for i in range(len(d)):
    print(f"bok {i+1}: vdx = {v_dx[i]:.3f} m, vdy = {v_dy[i]:.3f} m")

print(f"\nWspolrzedne wyznaczonego punktu 1:")
print(f"X1 = {P1[0]:.3f}")
print(f"Y1 = {P1[1]:.3f}")

print(f"\nWspolrzedne kontrolne punktu C:")
print(f"Xc obliczone = {C_ctrl[0]:.3f}, Yc obliczone = {C_ctrl[1]:.3f}")
print(f"Xc zadane    = {C[0]:.3f}, Yc zadane    = {C[1]:.3f}")

print(f"\nPorownanie z prawdziwym punktem 1003:")
print(f"X1 true = {P1_true[0]:.3f}, Y1 true = {P1_true[1]:.3f}")