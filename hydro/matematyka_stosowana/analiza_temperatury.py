import sympy as sp
from sympy.vector import CoordSys3D, gradient, divergence, curl


class TemperatureAnalyzer:
    """Klasa do analizy pól skalarnych temperatury i pól wektorowych przepływu."""

    def __init__(self):
        # Inicjalizacja układu współrzędnych
        self.R = CoordSys3D('R')
        self.x, self.y, self.z = self.R.x, self.R.y, self.R.z

    def analyze(self, T, label):
        """Przeprowadza pełną analizę fizyczną dla podanej funkcji T."""
        print(f"=== ANALIZA PRZYKŁADU {label} ===")
        print(f"Funkcja T(x,y,z) = {T}")

        # Obliczenia bazowe
        grad_T = gradient(T)
        F = -grad_T
        div_F = divergence(F)
        rot_F = curl(F)
        laplace_T = divergence(gradient(T))

        # Wyświetlanie wyników
        self._display_results(grad_T, F, div_F, rot_F, laplace_T)

        # Interpretacja fizyczna w punkcie (1, 1, 1)
        self._interpret_physics(div_F, rot_F, {self.x: 1, self.y: 1, self.z: 1})
        print("\n" + "=" * 40 + "\n")

    def _display_results(self, grad_T, F, div_F, rot_F, laplace_T):
        print(f"• Gradient ∇T: {grad_T}")
        print(f"• Pole przepływu F (-∇T): {F}")
        print(f"• Dywergencja div(F): {div_F}")
        print(f"• Rotacja rot(F): {rot_F}")
        print(f"• Operator Laplace'a ΔT: {laplace_T}")

    def _interpret_physics(self, div_F, rot_F, point_coords):
        val_div = div_F.subs(point_coords).evalf()

        print(f"--- Interpretacja fizyczna w punkcie {list(point_coords.values())} ---")

        # Analiza dywergencji (źródła/ujścia)
        if val_div > 0:
            print("  [!] Punkt jest ŹRÓDŁEM: Ciepło jest generowane/wypływa.")
        elif val_div < 0:
            print("  [!] Punkt jest UJŚCIEM: Ciepło jest pochłaniane/wpływa.")
        else:
            print("  [ ] Przepływ bezźródłowy: Zachowana ciągłość strumienia.")

        # Analiza rotacji (wirowość)
        if rot_F.magnitude() == 0:
            print("  [ ] Pole jest BEZWIROWE (jak każde pole gradientowe).")
        else:
            print("  [!] Uwaga: Wykryto wirowość (nietypowe dla czystego gradientu).")


# --- URUCHOMIENIE ---

if __name__ == "__main__":
    analyzer = TemperatureAnalyzer()
    R = analyzer.R

    # Lista tylko nieparzystych funkcji (1, 3, 5, 7, 9)
    odd_functions = [
        (1, 10 + R.x ** 2 + R.y ** 2 - R.z),
        (3, 5 + R.x - R.y + 2 * R.z),
        (5, 15 - 2 * R.z),
        (7, R.x ** 2 + R.y ** 2 + 2 * R.z ** 2),
        (9, sp.sin(R.x) + sp.cos(R.y) + R.z)
    ]

    for label, func in odd_functions:
        analyzer.analyze(func, label)