from sympy import *

# ============================================================
#  Szereg Taylora – 5 przykładów z listy zadań
#  Sprawozdanie bonus – Dobromir Matuszak, nr albumu: 20917
#
#  Wybrane zadania:
#   -  2: f(x) = e^x,      x0 = 0
#   -  6: f(x) = e^x,      x0 = 1
#   -  9: f(x) = tan(x),   x0 = 0
#   - 11: f(x) = sin(x²),  x0 = 0
#   - 12: f(x) = 1/(1-x),  x0 = 0
#
#  Dla każdej funkcji wyznaczamy wielomian Taylora stopnia 2, 5, 8,
#  a następnie porównujemy wartości przybliżeń z wynikiem dokładnym
#  w punkcie x = 5
# ============================================================

x = symbols('x')

zadania = [
    # (numer, opis,                   funkcja,      x0 )
    ( 2, "f(x) = e^x,      x0 = 0",  exp(x),       0  ),
    ( 6, "f(x) = e^x,      x0 = 1",  exp(x),       1  ),
    ( 9, "f(x) = tan(x),   x0 = 0",  tan(x),       0  ),
    (11, "f(x) = sin(x²),  x0 = 0",  sin(x**2),    0  ),
    (12, "f(x) = 1/(1-x),  x0 = 0",  1 / (1 - x),  0  ),
]

stopnie = [2, 5, 8]
x_test  = 5  # punkt do porównania z wynikiem dokładnym

print("=" * 70)
print("SZEREGI TAYLORA – wielomiany stopnia 2, 5, 8")
print("=" * 70)

for nr, opis, f, x0 in zadania:
    print(f"\n{'─'*70}")
    print(f"Przykład {nr}: {opis}")
    print(f"{'─'*70}")

    for stopien in stopnie:
        # series() – oblicza szereg Taylora wokół punktu x0
        # n = stopien+1 bo sympy (tak jak MATLAB) używa Order = stopień+1
        szereg    = series(f, x, x0=x0, n=stopien + 1)

        # removeO() – usuwa człon O(xⁿ) (informacja o reszcie, niepotrzebna)
        wielomian = expand(szereg.removeO())

        print(f"\n  T{stopien} = {wielomian}")

    # wartość dokładna funkcji w punkcie x_test
    wartosc_dokladna = float(f.subs(x, x_test).evalf())

    print(f"\n  Porównanie w punkcie x = {x_test}:")
    print(f"  Wartość dokładna f({x_test}) = {wartosc_dokladna:.6f}")
    print(f"\n  {'Stopień':<10} {'Przybliżenie':>15} {'Błąd bezwzgl.':>15}")
    print(f"  {'─'*42}")

    for stopien in stopnie:
        szereg    = series(f, x, x0=x0, n=stopien + 1)
        wielomian = expand(szereg.removeO())

        # podstawiamy x=5 żeby ocenić dokładność przybliżenia
        wartosc_przyblizenia = float(wielomian.subs(x, x_test).evalf())
        blad = abs(wartosc_przyblizenia - wartosc_dokladna)

        print(f"  T{stopien:<9} {wartosc_przyblizenia:>15.6f} {blad:>15.6f}")

print(f"\n{'='*70}")
print("Gotowe!")