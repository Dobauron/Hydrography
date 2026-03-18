import numpy as np
import scipy.linalg
import time
import warnings

class UkladRownan:
    """
    Klasa reprezentująca pojedynczy układ równań liniowych Ax = b.
    Zawiera metody do rozwiązywania układu różnymi algorytmami oraz
    narzędzia do analizy wydajności i dokładności.
    """
    def __init__(self, id_zadania, A, b):
        self.id = id_zadania
        self.A = np.array(A, dtype=float)
        self.b = np.array(b, dtype=float)
        self.n = len(b)  # Rozmiar macierzy (liczba równań)

    def algorytm_wlasny_gauss(self):
        """
        Implementacja eliminacji Gaussa 'na piechotę'.
        Cel: Sprowadzenie macierzy do postaci trójkątnej górnej.
        """
        A = self.A.copy()
        b = self.b.copy()
        n = self.n

        for i in range(n):
            # CZĘŚCIOWY PIVOTING:
            # Szukamy największego elementu w kolumnie, aby uniknąć dzielenia przez zero
            # lub przez bardzo małe liczby (poprawia stabilność numeryczną).
            if abs(A[i, i]) < 1e-12:
                for k in range(i + 1, n):
                    if abs(A[k, i]) > abs(A[i, i]):
                        # Zamiana wierszy w macierzy A i wektorze b
                        A[[i, k]] = A[[k, i]]
                        b[[i, k]] = b[[k, i]]
                        break

            # ELIMINACJA:
            # Zerujemy elementy pod przekątną w bieżącej kolumnie.
            for j in range(i + 1, n):
                # Współczynnik przez który mnożymy wiersz odejmowany
                ratio = A[j, i] / A[i, i]
                # Operacja na całym wierszu macierzy
                A[j, i:] -= ratio * A[i, i:]
                # Ta sama operacja na wyrazie wolnym
                b[j] -= ratio * b[i]

        # PODSTAWIANIE WSTECZ (Backward Substitution):
        # Wyliczamy niewiadome od ostatniej (x_n) do pierwszej (x_1).
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            # x_i = (b_i - suma(A_ij * x_j)) / A_ii
            x[i] = (b[i] - np.dot(A[i, i + 1:], x[i + 1:])) / A[i, i]
        return x

    def algorytm_wlasny_lu(self):
        """
        Własna implementacja rozkładu LU (Metoda Doolittle'a).
        Rozkłada macierz A na L (trójkątna dolna) i U (trójkątna górna).
        """
        n = self.n
        L = np.eye(n) # Macierz jednostkowa (jedynki na przekątnej)
        U = np.zeros((n, n))

        # ROZKŁAD A = LU:
        for i in range(n):
            # Wyznaczanie wierszy macierzy U
            for k in range(i, n):
                U[i][k] = self.A[i][k] - sum(L[i][j] * U[j][k] for j in range(i))
            # Wyznaczanie kolumn macierzy L
            for k in range(i + 1, n):
                L[k][i] = (self.A[k][i] - sum(L[k][j] * U[j][i] for j in range(i))) / U[i][i]

        # ROZWIĄZYWANIE UKŁADU (Dwa kroki):
        # 1. Podstawianie w przód: Ly = b (wyznaczamy wektor pomocniczy y)
        y = np.zeros(n)
        for i in range(n):
            y[i] = self.b[i] - sum(L[i][j] * y[j] for j in range(i))

        # 2. Podstawianie wstecz: Ux = y (wyznaczamy ostateczny wynik x)
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]
        return x

    def analiza_porownawcza(self):
        """
        Metoda wykonująca pełne testy porównawcze między algorytmami
        własnymi a wbudowanymi bibliotekami NumPy/SciPy.
        """
        # Ignorujemy ostrzeżenia o dzieleniu przez zero (obsłużymy to błędem macierzy osobliwej)
        with np.errstate(divide='ignore', invalid='ignore'):
            try:
                # --- POMIARY CZASU DLA GAUSSA ---
                t1_s = time.perf_counter()
                x_gw = self.algorytm_wlasny_gauss()
                t_gw = (time.perf_counter() - t1_s) * 1000 # Czas w milisekundach

                t2_s = time.perf_counter()
                x_gb = np.linalg.solve(self.A, self.b) # Standardowe rozwiązanie biblioteczne
                t_gb = (time.perf_counter() - t2_s) * 1000

                # --- POMIARY CZASU DLA LU ---
                t3_s = time.perf_counter()
                x_luw = self.algorytm_wlasny_lu()
                t_luw = (time.perf_counter() - t3_s) * 1000

                t4_s = time.perf_counter()
                # Profesjonalny, dwuetapowy rozkład LU z biblioteki SciPy
                lu_piv = scipy.linalg.lu_factor(self.A)
                x_lub = scipy.linalg.lu_solve(lu_piv, self.b)
                t_lub = (time.perf_counter() - t4_s) * 1000

                # --- WERYFIKACJA POPRAWNOŚCI ---
                # Obliczamy residuum: r = max|A*x - b|. Powinno być bliskie 0.
                residuum = np.max(np.abs(np.dot(self.A, x_gw) - self.b))

                # Sprawdzamy czy wszystkie 4 metody (2 własne, 2 obce) dają ten sam wynik
                zgodne = np.allclose(x_gw, x_gb) and np.allclose(x_gw, x_luw) and np.allclose(x_gw, x_lub)

                return {
                    "x": x_gw, "t_gw": t_gw, "t_gb": t_gb,
                    "t_luw": t_luw, "t_lub": t_lub,
                    "ok": (residuum < 1e-10 and zgodne), # Sukces jeśli błąd mały i wyniki spójne
                    "res": residuum, "error": False
                }
            except:
                # Jeśli wystąpi dzielenie przez 0 lub macierz jest osobliwa
                return {"error": True}

    def __str__(self):
        """Formatowanie wyników do wyświetlenia w konsoli."""
        res = self.analiza_porownawcza()
        sep = "=" * 70

        if res["error"]:
            return f"\n{sep}\nUKŁAD NR {self.id} | STATUS: BŁĄD (MACIERZ OSOBLIWA)\n{sep}\n"

        status = "SUKCES (Ax=b & Metody zgodne)" if res["ok"] else "BŁĄD WERYFIKACJI"
        return (f"\n{sep}\n"
                f"UKŁAD NR {self.id} | STATUS: {status}\n"
                f"{sep}\n"
                f"ROZWIĄZANIE x: {np.round(res['x'], 3)}\n"
                f"MAX BŁĄD RESIDUUM (A*x-b): {res['res']:.2e}\n"
                f"----------------------------------------------------------------------\n"
                f"CZASY WYKONANIA (milisekundy):\n"
                f"  Metoda Gaussa -> Własna: {res['t_gw']:.5f} | Wbudowana: {res['t_gb']:.5f}\n"
                f"  Metoda LU     -> Własna: {res['t_luw']:.5f} | Wbudowana: {res['t_lub']:.5f}\n")


# --- LISTA UKŁADÓW RÓWNAŃ (1-14) ---
# Uwaga: Układy 11 i 13 są osobliwe (brak jednoznacznego rozwiązania).
uklady = [
    UkladRownan(1, [[2, -1, -1], [3, 4, -2], [3, -2, 4]], [4, 11, 11]),
    UkladRownan(2, [[3, 2, 1], [2, 3, 1], [2, 1, 3]], [5, 1, 11]),
    UkladRownan(3, [[1, 1, 2], [2, -1, 2], [4, 1, 4]], [-1, -4, -2]),
    UkladRownan(4, [[1, 2, 4], [5, 1, 2], [3, -1, 1]], [31, 29, 10]),
    UkladRownan(5, [[1, 2, -1, 1], [2, 0, 3, 1], [2, -1, 1, -3], [1, -1, 3, 4]], [1, 0, 1, 0]),
    UkladRownan(6, [[0, 1, -3, 4], [1, 0, -2, 3], [3, 2, 0, -5], [4, 3, -5, 0]], [-5, -4, 12, 5]),
    UkladRownan(7, [[2, -1, 3, 2], [3, 3, 3, 2], [3, -2, 0, 2], [3, -1, 3, -1]], [4, 6, 6, 6]),
    UkladRownan(8, [[1, 2, -1], [2, -1, 3], [3, 1, 2]], [3, 14, 13]),
    UkladRownan(9, [[2, 1, 1], [1, -2, 3], [3, 1, -1]], [7, 9, 3]),
    UkladRownan(10, [[1, 1, 1], [2, 3, -1], [3, -1, 2]], [6, 7, 10]),
    UkladRownan(11, [[2, -1, 1], [1, 2, 3], [3, 1, -2]], [5, 14, 1]),
    UkladRownan(12, [[12, 2, 3], [2, -1, 1], [3, 1, 2]], [14, 3, 13]),
    UkladRownan(13, [[1, 1, -1, 1], [2, -1, 3, -1], [1, 2, 1, 2], [3, 1, -2, 1]], [2, 8, 7, 1]),
    UkladRownan(14, [[2, 1, -1, 1], [1, 3, 2, -1], [3, -1, 1, 2], [1, 2, -3, 1]], [4, 9, 8, -1])
]

# URUCHOMIENIE ANALIZY DLA KAŻDEGO UKŁADU
for u in uklady:
    print(u)

