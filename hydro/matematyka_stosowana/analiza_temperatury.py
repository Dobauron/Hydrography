import sympy as sp
from sympy.vector import CoordSys3D, gradient, divergence, curl


class TemperatureReport:
    def __init__(self):
        """
        Konstruktor: Przygotowuje 'scenę' do obliczeń.
        Tworzy układ współrzędnych R i definiuje stały punkt P(1,1,1).
        """
        self.R = CoordSys3D('R')
        # Słownik mapujący symbole x,y,z na konkretną wartość 1
        self.point = {self.R.x: 1, self.R.y: 1, self.R.z: 1}

    def run_full_analysis(self, functions_list):
        """
        Główna metoda sterująca: Przetwarza listę funkcji i generuje raport.
        """
        print("=" * 70)
        print(f"{'RAPORT ANALIZY PÓL TEMPERATURY':^70}")
        print("=" * 70)

        for label, T in functions_list:
            # --- 1. OBLICZENIA SYMBOLICZNE (Wzory ogólne) ---
            # Gradient T: pokazuje kierunek najszybszego wzrostu temperatury
            grad_T = gradient(T)

            # Pole F: wektor przepływu ciepła (zawsze przeciwny do gradientu)
            F = -grad_T

            # Dywergencja F: mówi czy w polu są źródła energii (rozbieżność)
            div_F = divergence(F)

            # Rotacja F: sprawdza czy pole 'wiruje' (dla gradientu zawsze 0)
            rot_F = curl(F)

            # Operator Laplace'a: opisuje 'wybrzuszenia' rozkładu temperatury
            laplace_T = divergence(gradient(T))

            # --- 2. OBLICZENIA PUNKTOWE (Konkretne wartości) ---
            # .subs(self.point) -> podmienia x, y, z na 1, 1, 1
            # .evalf(3) -> oblicza wartość numeryczną i zaokrągla do 3 miejsc po przecinku

            # Obliczamy temperaturę w punkcie P
            v_T = T.subs(self.point).evalf(3)

            # Sprawdzamy dywergencję w punkcie P (kluczowe dla interpretacji fizycznej)
            v_div = div_F.subs(self.point).evalf(3)

            # Obliczamy Laplasjan w punkcie P
            v_lap = laplace_T.subs(self.point).evalf(3)

            # --- 3. SEKCJA WYŚWIETLANIA ---
            print(f"\n>>> PRZYKŁAD {label}: T(x,y,z) = {T}")
            print("-" * 40)
            print(f"1. Gradient (grad T):      {grad_T}")
            print(f"2. Pole przepływu (F):     {F}")
            print(f"3. Dywergencja (div F):    {div_F}")
            print(f"4. Rotacja (rot F):        {rot_F}")
            print(f"5. Laplasjan (ΔT):         {laplace_T}")
            print("-" * 40)
            print(f"WARTOŚCI W PUNKCIE (1, 1, 1):")
            print(f"   T = {v_T} (Temperatura w tym miejscu)")
            print(f"   div F = {v_div} (Bilans energii w tym miejscu)")
            print(f"   ΔT = {v_lap} (Zależne od div F)")

            # Prosta logika decyzyjna na podstawie znaku dywergencji
            if v_div > 0:
                wniosek = "ŹRÓDŁO (ciepło wypływa z tego punktu)"
            elif v_div < 0:
                wniosek = "UJŚCIE (ciepło jest pochłaniane w tym punkcie)"
            else:
                wniosek = "BEZZRÓDŁOWE (przepływ jest stały i zachowawczy)"

            print(f"INTERPRETACJA: {wniosek}")
            print("-" * 70)


# --- INICJALIZACJA I START ---
report = TemperatureReport()
R = report.R

# Lista krotek: (Numer zadania, Formuła matematyczna)
odd_tasks = [
    (1, 10 + R.x ** 2 + R.y ** 2 - R.z),
    (3, 5 + R.x - R.y + 2 * R.z),
    (5, 15 - 2 * R.z),
    (7, R.x ** 2 + R.y ** 2 + 2 * R.z ** 2),
    (9, sp.sin(R.x) + sp.cos(R.y) + R.z)
]

if __name__ == "__main__":
    report.run_full_analysis(odd_tasks)