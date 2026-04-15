import numpy as np
from scipy import integrate
import warnings
warnings.filterwarnings("ignore")

# ============================================================
#  Całki oznaczone – 3 metody
#  (a) scipy.integrate.quad  (odpowiednik MATLAB int/trapz)
#  (b) własna metoda trapezów
#  (c) własna metoda Simpsona
# ============================================================

n = 1000  # liczba punktów podziału


# ---------- Implementacje metod numerycznych ----------

def metoda_trapezow(f, a, b, n):
    """Metoda trapezów – własna implementacja."""
    x = np.linspace(a, b, n + 1)
    # np.linspace(a, b, n+1) – tworzy n+1 równoodległych punktów od a do b
    # np.linspace(0, 1, 5) → [0.0, 0.25, 0.5, 0.75, 1.0]
    # używamy n+1 punktów, bo n przedziałów ma n+1 końców
    y = f(x)
    h = (b - a) / n
    return h * (y[0] / 2 + np.sum(y[1:-1]) + y[-1] / 2)


def metoda_simpsona(f, a, b, n):
    """Metoda Simpsona – własna implementacja (n musi być parzyste)."""
    if n % 2 != 0: # warunek ilość punktów podziału musi być parzysta
        n += 1
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    return h / 3 * (y[0] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-2:2]) + y[-1])
# y[0] — pierwsza wartość, f(x₀), mnożnik 1
# y[1:-1:2] — co drugi element zaczynając od indeksu 1, czyli y₁, y₃, y₅, ... (punkty nieparzyste) → mnożnik 4
# y[2:-2:2] — co drugi element zaczynając od indeksu 2, czyli y₂, y₄, y₆, ... (punkty parzyste środkowe) → mnożnik 2
# y[-1] — ostatnia wartość, f(xₙ), mnożnik 1
# np.sum(tablica) — sumuje wszystkie elementy tablicy.


# ---------- Definicje całek ----------

import numpy as np

zadania = [
    # (numer, opis,                              funkcja,                                    a,        b        )
    ( 1,  "∫₀¹ x² dx",                          lambda x: x**2,                             0,        1        ),
    ( 2,  "∫₀² (x²+1) dx",                      lambda x: x**2 + 1,                         0,        2        ),
    ( 3,  "∫₁³ (2x+5) dx",                      lambda x: 2*x + 5,                          1,        3        ),
    ( 4,  "∫₋₁¹ x² dx",                         lambda x: x**2,                            -1,        1        ),
    ( 5,  "∫₀⁴ (3x-2) dx",                      lambda x: 3*x - 2,                          0,        4        ),
    ( 6,  "∫₀¹ (x³+x) dx",                      lambda x: x**3 + x,                         0,        1        ),
    ( 7,  "∫₋₂² (x²+2x+1) dx",                  lambda x: x**2 + 2*x + 1,                  -2,        2        ),
    ( 8,  "∫₀³ √(x+1) dx",                      lambda x: np.sqrt(x + 1),                   0,        3        ),
    ( 9,  "∫₀² 1/(x+1) dx",                     lambda x: 1 / (x + 1),                      0,        2        ),
    (10,  "∫₁² 1/x² dx",                        lambda x: 1 / x**2,                         1,        2        ),
    (11,  "∫₀^π sin(x) dx",                     lambda x: np.sin(x),                        0,        np.pi    ),
    (12,  "∫₀^(π/2) cos(x) dx",                 lambda x: np.cos(x),                        0,        np.pi/2  ),
    (13,  "∫₀^π sin²(x) dx",                    lambda x: np.sin(x)**2,                     0,        np.pi    ),
    (14,  "∫₀^(π/2) (sin(x)+cos(x)) dx",        lambda x: np.sin(x) + np.cos(x),            0,        np.pi/2  ),
    (15,  "∫₀¹ eˣ dx",                          lambda x: np.exp(x),                        0,        1        ),
    (16,  "∫₀¹ e^(-x) dx",                      lambda x: np.exp(-x),                       0,        1        ),
    (17,  "∫₀¹ e^(-x²) dx",                     lambda x: np.exp(-x**2),                    0,        1        ),
    (18,  "∫₀² x·eˣ dx",                        lambda x: x * np.exp(x),                    0,        2        ),
    (19,  "∫₀¹ ln(x+1) dx",                     lambda x: np.log(x + 1),                    0,        1        ),
    (20,  "∫₁^e ln(x) dx",                      lambda x: np.log(x),                        1,        np.e     ),
    (21,  "∫₀¹ 1/(1+x²) dx",                    lambda x: 1 / (1 + x**2),                   0,        1        ),
    (22,  "∫₀¹ x/(1+x²) dx",                    lambda x: x / (1 + x**2),                   0,        1        ),
    (23,  "∫₀² x²/(x+1) dx",                    lambda x: x**2 / (x + 1),                   0,        2        ),
    (24,  "∫₋₁¹ 1/(x²+1) dx",                   lambda x: 1 / (x**2 + 1),                  -1,        1        ),
    (25,  "∫₀³ |x-1| dx",                       lambda x: np.abs(x - 1),                    0,        3        ),
    (26,  "∫₀² (x³-2x²+x+1) dx",               lambda x: x**3 - 2*x**2 + x + 1,            0,        2        ),
    (27,  "∫₋₂⁰ (x²-4x) dx",                    lambda x: x**2 - 4*x,                      -2,        0        ),
    (28,  "∫₀¹ √(1-x²) dx",                     lambda x: np.sqrt(np.maximum(1 - x**2, 0)), 0,        1        ),
    (29,  "∫₀² sin(x²) dx",                     lambda x: np.sin(x**2),                     0,        2        ),
    (30,  "∫₀¹ eˣ/(1+x) dx",                    lambda x: np.exp(x) / (1 + x),              0,        1        ),
]


# ---------- Obliczenia i wyniki ----------

print("=" * 85)
print(f"{'Nr':<4} {'Całka':<35} {'Dokładna':>12} {'Trapezy':>12} {'Simpson':>12}")
print("=" * 85)

for nr, opis, f, a, b in zadania:
    wynik_dokladny, _ = integrate.quad(f, a, b)
    wynik_trapez     = metoda_trapezow(f, a, b, n)
    wynik_simpson    = metoda_simpsona(f, a, b, n)

    print(f"{nr:<4} {opis:<35} {wynik_dokladny:>12.6f} {wynik_trapez:>12.6f} {wynik_simpson:>12.6f}")

print("=" * 85)
print(f"\nLiczba punktów podziału: n = {n}")
print("\nBłędy bezwzględne (|wynik_num - wynik_dokładny|):")
print("-" * 60)
print(f"{'Nr':<4} {'Całka':<35} {'Błąd trapezów':>15} {'Błąd Simpsona':>15}")
print("-" * 60)

for nr, opis, f, a, b in zadania:
    wynik_dokladny, _ = integrate.quad(f, a, b)
    wynik_trapez     = metoda_trapezow(f, a, b, n)
    wynik_simpson    = metoda_simpsona(f, a, b, n)
    blad_t = abs(wynik_trapez - wynik_dokladny)
    blad_s = abs(wynik_simpson - wynik_dokladny)
    print(f"{nr:<4} {opis:<35} {blad_t:>15.2e} {blad_s:>15.2e}")

print("-" * 60)
print("\nGotowe! Metoda Simpsona jest zazwyczaj dokładniejsza od metody trapezów.")