import numpy as np
import math

# DANE
A = np.array([1000.000, 1000.000])
B = np.array([1200.000, 1050.000])
alfa1_g = 45.0200
alfa2_g = 60.1244

def wciecie_w_przod(A, B, alfa1_g, alfa2_g):
    # 1. Obliczenie długości AB
    dX_AB = B[0] - A[0]
    dY_AB = B[1] - A[1]
    AB_len = np.sqrt(dX_AB**2 + dY_AB**2)

    # 2. Odległości z twierdzenia sinusów
    # Przeliczamy sumę i poszczególne kąty na radiany do sinusa
    sin_sum = math.sin((alfa1_g + alfa2_g) * math.pi / 200)
    AP2_dist = AB_len * math.sin(alfa2_g * math.pi / 200) / sin_sum
    BP2_dist = AB_len * math.sin(alfa1_g * math.pi / 200) / sin_sum

    # 3. Azymuty (w radianach)
    A_AB = math.atan2(dY_AB, dX_AB)
    A_BA = math.atan2(-dY_AB, -dX_AB)

    # 4. Kierunki do punktu P2 (zamiana alfa na radiany, aby odjąć od azymutu)
    fiAB = A_AB - (alfa1_g * math.pi / 200)
    fiBA = A_BA + (alfa2_g * math.pi / 200)

    # 5. Współrzędne liczone z punktu A
    P2_z_A = np.array([
        A[0] + AP2_dist * math.cos(fiAB),
        A[1] + AP2_dist * math.sin(fiAB)
    ])

    # 6. Współrzędne liczone z punktu B (kontrola)
    P2_z_B = np.array([
        B[0] + BP2_dist * math.cos(fiBA),
        B[1] + BP2_dist * math.sin(fiBA)
    ])

    # 7. Różnice kontrolne
    roznice = P2_z_A - P2_z_B

    # Zwracamy wyniki w strukturze podobnej do MATLABowej
    return {
        'AB': AB_len,
        'P2_z_A': P2_z_A,
        'P2_z_B': P2_z_B,
        'roznice_kontrolne': roznice
    }

# OBLICZENIA
wynik = wciecie_w_przod(A, B, alfa1_g, alfa2_g)

# WYŚWIETLENIE WYNIKÓW (Formatowanie jak w MATLAB)
print(f"\n=== WYNIKI WCIECIA KATOWEGO W PRZOD ===")
print(f"Dlugosc AB = {wynik['AB']:.3f} m")

print(f"\nPunkt P2 liczony z A:")
print(f"X = {wynik['P2_z_A'][0]:.3f}  Y = {wynik['P2_z_A'][1]:.3f}")

print(f"\nPunkt P2 liczony z B:")
print(f"X = {wynik['P2_z_B'][0]:.3f}  Y = {wynik['P2_z_B'][1]:.3f}")

print(f"\nRoznice kontrolne:")
print(f"dX = {wynik['roznice_kontrolne'][0]:.6f} m")
print(f"dY = {wynik['roznice_kontrolne'][1]:.6f} m")