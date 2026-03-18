import numpy as np
import time


class Macierz:
    def __init__(self, id_zadania, dane):
        self.id = id_zadania
        self.data = np.array(dane, dtype=float)  # macierz wejściowa
        self.wiersze, self.kolumny = self.data.shape  # pobranie kształtu macierzy

    def wyznacznik_na_piechote(self, m):
        """Metoda Laplace'a - rekurencyjne obliczanie wyznacznika (jak na kartce)."""
        # Warunek stopu dla macierzy 1x1
        if len(m) == 1:
            return m[0][0]
        # Przypadek dla macierzy 2x2
        if len(m) == 2:
            return m[0][0] * m[1][1] - m[0][1] * m[1][0]

        det = 0
        for c in range(len(m)):
            # Wykreślamy pierwszy wiersz (index 0) i c-tą kolumnę
            podmacierz = np.delete(np.delete(m, 0, axis=0), c, axis=1)
            # Sumujemy iloczyny zgodnie z rozwinięciem Laplace'a
            det += ((-1) ** c) * m[0][c] * self.wyznacznik_na_piechote(podmacierz)
        return det

    def wykonaj_testy(self):
        """Porównuje metodę NumPy z metodą własną pod kątem czasu i wyniku."""
        # Zadanie 1: Transpozycja (zawsze możliwa)
        at = self.data.T

        # Zadanie 2: Wyznaczniki (tylko dla kwadratowych)
        if self.wiersze != self.kolumny:
            return at, None, None, "N/A", "N/A", "N/A"

        # --- POMIAR METODY WBUDOWANEJ (NumPy) ---
        t1_start = time.perf_counter()
        det_np = np.linalg.det(self.data)
        t1_stop = time.perf_counter()
        czas_np = (t1_stop - t1_start) * 1000  # w ms

        # --- POMIAR METODY WŁASNEJ (Na piechotę) ---
        t2_start = time.perf_counter()
        det_wl = self.wyznacznik_na_piechote(self.data)
        t2_stop = time.perf_counter()
        czas_wl = (t2_stop - t2_start) * 1000  # w ms

        # Sprawdzenie czy wyniki są takie same (z tolerancją błędu)
        poprawny = np.isclose(det_np, det_wl, atol=1e-2)

        return at, round(det_np, 2), round(det_wl, 2), f"{czas_np:.6f} ms", f"{czas_wl:.6f} ms", poprawny

    def __str__(self):
        at, d_np, d_wl, t_np, t_wl, ok = self.wykonaj_testy()

        sep = "=" * 60
        wynik = [f"\n{sep}", f"MACIERZ NR {self.id} ({self.wiersze}x{self.kolumny})", sep]

        wynik.append(f"Zadanie 1 (Transpozycja A^T):\n{at}")

        wynik.append(f"\nZadanie 2 (Wyznacznik):")
        if d_np is None:
            wynik.append("   Nie istnieje (macierz niekwadratowa)")
        else:
            wynik.append(f"   - Wynik NumPy:  {d_np}")
            wynik.append(f"   - Wynik Własny: {d_wl}")
            wynik.append(f"   - Zgodność:     {'TAK' if ok else 'BŁĄD'}")

            wynik.append(f"\nPorównanie czasu:")
            wynik.append(f"   - Czas NumPy:   {t_np}")
            wynik.append(f"   - Czas Własny:  {t_wl}")

            # Obliczanie różnicy wydajności
            roznica = float(t_wl[:-3]) / float(t_np[:-3]) if float(t_np[:-3]) > 0 else 0
            wynik.append(f"   - Wniosek:      Metoda NumPy jest ok. {roznica:.1f}x szybsza")

        return "\n".join(wynik)


# --- PEŁNA LISTA WSZYSTKICH MACIERZY (1-12) ---
lista_zadan = [
    Macierz("1", [[2, 4, -1], [3, 0, 7], [5, 4, 4]]),
    Macierz("2", [[5, 2, -1, 4], [2, 0, 3, 1], [1, 2, -7, 2]]),
    Macierz("3", [[2, 3, -1, 7], [2, 2, 4, 1], [-2, 1, -9, 6]]),
    Macierz("4", [[3, 1, -2, 5], [2, 2, -1, 4], [3, -1, 2, 5], [1, -3, 2, -1]]),
    Macierz("5", [[3, 1, -2, 5], [-6, -2, 4, -10]]),
    Macierz("6", [[1, 2, 4, -1], [3, 1, 2, -4], [1, 2, 3, 0], [1, -3, -5, -3]]),
    Macierz("7", [[2, 4, -1], [0, 1, -2], [4, 6, 0], [2, 2, 1]]),
    Macierz("8", [[1, -2], [2, -4], [-1, 2]]),
    Macierz("9", [[1, 2, 3], [4, 1, 0], [2, -1, 5]]),
    Macierz("10", [[2, 1, -3], [1, 4, 2], [3, -2, 1]]),
    Macierz("11", [[3, 1, 2, 4], [1, 5, 0, 2], [2, 3, 4, 1], [0, 2, 1, 3]]),
    Macierz("12", [[4, 2, 1, 0], [1, 3, 2, 1], [2, 1, 5, 2], [0, 2, 3, 4]])
]

for m in lista_zadan:
    print(m)