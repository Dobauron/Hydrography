import sympy as sp
from sympy.vector import CoordSys3D, divergence, curl


class WaterFlowAnalyzer:
    def __init__(self):
        """Inicjalizacja układu współrzędnych i punktu kontrolnego P(1,1,1)."""
        self.R = CoordSys3D('R')
        # Punkt P(1,1,1) do obliczeń numerycznych
        self.P = {self.R.x: 1, self.R.y: 1, self.R.z: 1}

    def analyze_flow(self, F, label):
        """Metoda obliczająca parametry pola wektorowego i wyświetlająca raport."""
        # 1. Obliczenia symboliczne (ogólne wzory)
        div_F = divergence(F)  # Dywergencja - czy woda wypływa/wpływa do punktu
        rot_F = curl(F)  # Rotacja - czy woda tworzy wiry

        # 2. Obliczenia punktowe (wartości w P=1,1,1)
        # .subs podstawia 1 pod x,y,z;
        # .evalf zamienia na liczbę
        v_div = div_F.subs(self.P).evalf(3)
        #Ponieważ rotacja jest wektorem, nie możemy jej tak po prostu porównać do zera (wektor ma kierunek i zwrot).
        #Metoda .magnitude() oblicza długość (moduł) tego wektora
        v_rot = rot_F.subs(self.P).magnitude().evalf(3)

        # Wyświetlanie wyników
        print(f"\n>>> ZADANIE {label}: F = {F}")
        print("-" * 50)
        print(f"Dywergencja (div F): {div_F}")
        print(f"Rotacja (rot F):     {rot_F}")
        print(f"Wartości w P(1,1,1): div={v_div}, |rot|={v_rot}")

        # Szybka interpretacja fizyczna
        interp_div = "ŹRÓDŁO (woda się rozchodzi)" if v_div > 0 else (
            "UJŚCIE (woda się gromadzi)" if v_div < 0 else "BEZŹRÓDŁOWE")
        interp_rot = "WIROWE (wir/turbulencja)" if v_rot != 0 else "BEZWIROWE (przepływ gładki)"
        print(f"WNIOSEK: {interp_div} | {interp_rot}")


# --- URUCHOMIENIE DLA ZADAŃ NIEPARZYSTYCH ---
analyzer = WaterFlowAnalyzer()
R = analyzer.R

# Lista pól wektorowych z zadania 5 (nieparzyste)
tasks = [
    (1, R.x * R.i + R.y * R.j + R.z * R.k),  # F = (x, y, z)
    (3, R.y * R.i - R.x * R.j),  # F = (y, -x, 0)
    (5, R.x * R.i - R.y * R.j),  # F = (x, -y, 0)
    (7, (R.y * R.z) * R.i + (R.x * R.z) * R.j + (R.x * R.y) * R.k),  # F = (yz, xz, xy)
    (9, sp.sin(R.y) * R.i + sp.cos(R.x) * R.j)  # F = (sin y, cos x, 0)
]

#Gdzie i, j, k to wektory jednostkowe (wersory) skierowane wzdłuż osi OX, OY i OZ.
#R.i to odpowiednik i (kierunek X)
#R.j to odpowiednik j (kierunek Y).
#R.k to odpowiednik k (kierunek Z).




if __name__ == "__main__":
    print("ANALIZA PRZEPŁYWU WODY (ZADANIA NIEPARZYSTE)")
    for label, field in tasks:
        analyzer.analyze_flow(field, label)