import numpy as np


class Punkt:
    """Klasa reprezentująca pojedynczy punkt o współrzędnych X, Y."""

    def __init__(self, x, y, nr=None):
        self.x = float(x)
        self.y = float(y)
        self.nr = nr

    def __repr__(self):
        return f"X: {self.x:.3f}, Y: {self.y:.3f}"


class MetodaBiegunowa:
    """Klasa realizująca obliczenia geodezyjne metodą biegunową."""

    @staticmethod
    def gony_na_radiany(gony):
        """Przelicza jednostki kątowe: grady (gony) na radiany (standard w Pythonie)."""
        return gony * (np.pi / 200)

    @staticmethod
    def oblicz_azymut_nawiazania(st, naw):
        """
        Oblicza kąt (azymut) kierunku między stanowiskiem (st) a nawiązaniem (naw).
        Jest to niezbędne, aby zorientować instrument w terenie.
        """
        dx = naw.x - st.x
        dy = naw.y - st.y
        # arctan2 zwraca kąt w radianach uwzględniając znaki dx i dy (ćwiartki azymutu)
        azymut = np.arctan2(dy, dx)
        if azymut < 0:
            azymut += 2 * np.pi
        return azymut

    def oblicz_punkty(self, stanowisko, nawiazanie, pomiary):
        """
        Główna funkcja przeliczająca dane z terenu na współrzędne płaskie.
        Wzory: X = Xs + d*cos(Az), Y = Ys + d*sin(Az)
        """
        az_naw = self.oblicz_azymut_nawiazania(stanowisko, nawiazanie)
        obliczone_punkty = {}

        for p in pomiary:
            # Azymut na mierzony punkt to azymut nawiązania + zmierzony kąt poziomy
            kat_rad = self.gony_na_radiany(p['kat'])
            az_punktu = az_naw + kat_rad

            # Obliczenie przyrostów współrzędnych i dodanie ich do stanowiska
            x = stanowisko.x + p['d'] * np.cos(az_punktu)
            y = stanowisko.y + p['d'] * np.sin(az_punktu)

            obliczone_punkty[p['nr']] = Punkt(x, y, p['nr'])

        return obliczone_punkty


class RaportGeodezyjny:
    """Klasa generująca czytelne zestawienie wyników i kontrolę dokładności."""

    @staticmethod
    def wyswietl_wyniki(punkty_s1, punkty_s2):
        print("\n" + "=" * 60)
        print(f"{'Nr pkt':<8} | {'Zrodlo':<12} | {'X [m]':<15} | {'Y [m]':<15}")
        print("-" * 60)

        # Punkt 1 (tylko s2)
        p1 = punkty_s2[1]
        print(f"{1:<8} | {'Stan. s2':<12} | {p1.x:<15.3f} | {p1.y:<15.3f}")

        # Punkt 2 (kontrola z obu stanowisk)
        p2a = punkty_s1[2]
        p2b = punkty_s2[2]
        print(f"{2:<8} | {'Stan. s1':<12} | {p2a.x:<15.3f} | {p2a.y:<15.3f}")
        print(f"{2:<8} | {'Stan. s2':<12} | {p2b.x:<15.3f} | {p2b.y:<15.3f}")

        # Punkty 3 i 4 (tylko s1)
        for nr in [3, 4]:
            p = punkty_s1[nr]
            print(f"{nr:<8} | {'Stan. s1':<12} | {p.x:<15.3f} | {p.y:<15.3f}")
        print("=" * 60)

    @staticmethod
    def kontrola_punktu_2(p_s1, p_s2):
        """Oblicza błąd położenia punktu zmierzonego z dwóch niezależnych stanowisk."""
        dx = p_s1.x - p_s2.x
        dy = p_s1.y - p_s2.y
        fL = np.sqrt(dx ** 2 + dy ** 2)

        print("\n--- ANALIZA DOKŁADNOŚCI PUNKTU NR 2 ---")
        print(f"Różnica dX: {dx:.4f} m")
        print(f"Różnica dY: {dy:.4f} m")
        print(f"Odchyłka liniowa fL: {fL:.4f} m (ok. {fL * 1000:.1f} mm)")

        dopuszczalna = 0.10  # 10 cm dla I grupy dokładnościowej
        status = "ZGODNA" if fL <= dopuszczalna else "PRZEKROCZONA"
        print(f"Status (I grupa): {status} (fL <= 0.10m)")


# --- DANE ZADANIA ---
stanowisko_s1 = Punkt(5820523.94, 8458485.07, "s1")
stanowisko_s2 = Punkt(5820527.16, 8458514.69, "s2")

pomiary_s1 = [
    {'nr': 4, 'kat': 56.8220, 'd': 18.82},
    {'nr': 3, 'kat': 48.9574, 'd': 14.78},
    {'nr': 2, 'kat': 22.5229, 'd': 21.93}
]

pomiary_s2 = [
    {'nr': 2, 'kat': 356.1501, 'd': 11.95},
    {'nr': 1, 'kat': 337.7000, 'd': 14.43}
]

# --- URUCHOMIENIE ---
if __name__ == "__main__":
    kalkulator = MetodaBiegunowa()

    # Obliczamy wyniki z obu stanowisk
    wyniki_s1 = kalkulator.oblicz_punkty(stanowisko_s1, stanowisko_s2, pomiary_s1)
    wyniki_s2 = kalkulator.oblicz_punkty(stanowisko_s2, stanowisko_s1, pomiary_s2)

    # Generujemy raport
    raport = RaportGeodezyjny()
    raport.wyswietl_wyniki(wyniki_s1, wyniki_s2)
    raport.kontrola_punktu_2(wyniki_s1[2], wyniki_s2[2])