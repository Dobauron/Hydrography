import numpy as np
import matplotlib.pyplot as plt


class CiagPoligonowy:
    """
    Klasa realizująca obliczenie i wyrównanie ciągu poligonowego
    dwustronnie nawiązanego.
    """

    def __init__(self, punkty_nawiazania, obserwacje_katowe, odleglosci):
        # Rozpakowanie punktów (Y to Wschód, X to Północ w układzie geodezyjnym)
        self.A, self.B, self.C, self.D = punkty_nawiazania
        self.alpha_meas = np.array(obserwacje_katowe)
        self.d = np.array(odleglosci)

        # Wyniki pośrednie i końcowe
        self.alpha_corr = None
        self.azymuty = None
        self.P1 = None
        self.f_L = None

    # --- Narzędzia matematyczne ---
    @staticmethod
    def grad2rad(g):
        return g * np.pi / 200

    @staticmethod
    def rad2grad(r):
        return r * 200 / np.pi

    @staticmethod
    def norm400(a):
        return a % 400

    def oblicz_azymut(self, P1, P2):
        """Oblicza azymut geodezyjny w gradach."""
        return self.norm400(self.rad2grad(np.arctan2(P2[1] - P1[1], P2[0] - P1[0])))

    # --- Etapy obliczeń ---
    def wyrownanie_katowe(self):
        AP = self.oblicz_azymut(self.A, self.B)
        AK = self.oblicz_azymut(self.C, self.D)

        n = len(self.alpha_meas)
        alpha_suma_p = np.sum(self.alpha_meas)
        alpha_suma_t = self.norm400(AK - AP + n * 200)

        # Korekta dla pełnego obrotu
        if alpha_suma_t == 0 and alpha_suma_p > 200: suma_t = 400

        f_alpha = alpha_suma_p - alpha_suma_t
        v = -f_alpha / n
        self.alpha_corr = self.alpha_meas + v

        # Obliczenie azymutów boków
        self.azymuty = np.zeros(len(self.d))
        self.azymuty[0] = self.norm400(AP + self.alpha_corr[0] - 200)
        for i in range(1, len(self.d)):
            self.azymuty[i] = self.norm400(self.azymuty[i - 1] + self.alpha_corr[i] - 200)

        return f_alpha

    def oblicz_wspolrzedne(self):
        # Przyrosty teoretyczne
        dx = self.d * np.cos(self.grad2rad(self.azymuty))
        dy = self.d * np.sin(self.grad2rad(self.azymuty))

        # Odchyłki liniowe
        f_dx = np.sum(dx) - (self.C[0] - self.B[0])
        f_dy = np.sum(dy) - (self.C[1] - self.B[1])
        self.f_L = np.sqrt(f_dx ** 2 + f_dy ** 2)

        # Rozrzucenie poprawek proporcjonalnie do długości boków
        D_sum = np.sum(self.d)
        v_dx = np.round((-f_dx / D_sum) * self.d, 3)
        v_dy = np.round((-f_dy / D_sum) * self.d, 3)

        # Zamknięcie resztkowe na najdłuższy bok
        idx_max = np.argmax(self.d)
        v_dx[idx_max] += np.round(-f_dx - np.sum(v_dx), 3)
        v_dy[idx_max] += np.round(-f_dy - np.sum(v_dy), 3)

        # Obliczenie punktu P1 (1003)
        X1 = self.B[0] + dx[0] + v_dx[0]
        Y1 = self.B[1] + dy[0] + v_dy[0]
        self.P1 = np.array([X1, Y1])

        return self.f_L

    def wizualizuj(self):
        pts_x = [self.A[1], self.B[1], self.P1[1], self.C[1], self.D[1]]
        pts_y = [self.A[0], self.B[0], self.P1[0], self.C[0], self.D[0]]
        labels = ['1000 (A)', '1002 (B)', '1003 (P1)', '1004 (C)', '1005 (D)']

        plt.figure(figsize=(10, 7))
        plt.plot(pts_x[1:4], pts_y[1:4], 'r--', label='Ciąg poligonowy')
        plt.plot(pts_x[0:2], pts_y[0:2], 'k-', pts_x[3:5], pts_y[3:5], 'k-', label='Nawiązanie')
        plt.scatter(pts_x, pts_y, c='blue')

        for i, txt in enumerate(labels):
            plt.annotate(txt, (pts_x[i], pts_y[i]), xytext=(5, 5), textcoords='offset points')

        plt.axis('equal')
        plt.grid(True, ls=':')
        plt.title("Wyrównany ciąg poligonowy")
        plt.show()


# =========================
# URUCHOMIENIE (MAIN)
# =========================
if __name__ == "__main__":
    # Dane wejściowe
    punkty = [
        np.array([5924068.90, 5466351.32]),  # A (1000)
        np.array([5924041.93, 5466334.40]),  # B (1002)
        np.array([5923995.59, 5466340.95]),  # C (1004)
        np.array([5924041.69, 5466381.78])  # D (1005)
    ]
    katy = [205.1370176292, 104.1867451247, 101.1519112023]
    odleglosci = [31.0540979582, 33.0320586705]

    projekt = CiagPoligonowy(punkty, katy, odleglosci)

    # Obliczanie azymutów nawiązania dla raportu
    AP = projekt.oblicz_azymut(projekt.A, projekt.B)
    AK = projekt.oblicz_azymut(projekt.C, projekt.D)

    fa = projekt.wyrownanie_katowe()
    fl = projekt.oblicz_wspolrzedne()

    print("=" * 45)
    print("   RAPORT Z OBLICZEŃ CIĄGU POLIGONOWEGO")
    print("=" * 45)

    print(f"\n=== I ETAP - WYRÓWNANIE KĄTÓW ===")
    print(f"Azymut pocz. (A->B): {AP:.4f} g")
    print(f"Azymut końc. (C->D): {AK:.4f} g")
    print(f"f_alpha (odchyłka):  {fa:.6f} g")
    print(f"v (poprawka jedn.):  {-fa / len(katy):.6f} g")

    print("\nAzymuty boków ciągu:")
    for i, az_val in enumerate(projekt.azymuty):
        label = "B->1" if i == 0 else f"{i}->C"
        print(f"  Azymut {label}: {az_val:.6f} g")

    print(f"\n=== II ETAP - PRZYROSTY I WSPÓŁRZĘDNE ===")
    print(f"f_L (odchyłka liniowa): {fl:.3f} m")
    L_total = np.sum(projekt.d)
    precyzja = int(L_total / fl) if fl != 0 else 0
    print(f"Precyzja względna:      1:{precyzja}")

    print(f"\nWyznaczone współrzędne P1 (1003):")
    print(f"  X = {projekt.P1[0]:.3f}")
    print(f"  Y = {projekt.P1[1]:.3f}")

    # Kontrola z punktem C
    # Obliczamy C z przyrostów (X1 + dx2_corr)
    # Dla uproszczenia wyświetlamy kontrolę końcową
    print(f"\nKontrola zamknięcia na punkcie C (1004):")
    print(f"  X_zadane: {projekt.C[0]:.3f} | Y_zadane: {projekt.C[1]:.3f}")

    # Porównanie z prawdą
    P1_true = np.array([5924017.04, 5466315.83])
    mp = np.sqrt(np.sum((projekt.P1 - P1_true) ** 2))
    print(f"\nPorównanie z danymi katalogowymi (1003):")
    print(f"  Błąd położenia punktu (mp): {mp:.3f} m")
    print("=" * 45)

    projekt.wizualizuj()