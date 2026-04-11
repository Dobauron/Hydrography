import numpy as np


class Punkt:
    def __init__(self, x, y, nr=None):
        self.x = float(x)
        self.y = float(y)
        self.nr = nr

    def __repr__(self):
        return f"X: {self.x:.3f}, Y: {self.y:.3f}"


class MetodaBiegunowa:
    @staticmethod
    def gony_na_radiany(gony):
        return gony * (np.pi / 200)

    @staticmethod
    def oblicz_azymut_nawiazania(st, naw):
        dx = naw.x - st.x
        dy = naw.y - st.y
        azymut = np.arctan2(dy, dx)
        if azymut < 0:
            azymut += 2 * np.pi
        return azymut

    def oblicz_punkty(self, stanowisko, nawiazanie, hz_na_naw, pomiary):
        # 1. Obliczamy azymut teoretyczny nawiązania
        az_teoret = self.oblicz_azymut_nawiazania(stanowisko, nawiazanie)

        # 2. Obliczamy stałą orientacji: Azymut - Odczyt Hz na nawiązanie
        orientacja = az_teoret - self.gony_na_radiany(hz_na_naw)

        obliczone_punkty = {}

        for p in pomiary:
            # 3. Redukcja odległości: d_pozioma = d_skosna * sin(V)
            v_rad = self.gony_na_radiany(p['kat_v'])
            d_pozioma = p['d'] * np.sin(v_rad)

            # 4. Azymut na punkt: Odczyt Hz + Orientacja
            az_punktu = self.gony_na_radiany(p['kat_hz']) + orientacja

            # 5. Współrzędne
            x = stanowisko.x + d_pozioma * np.cos(az_punktu)
            y = stanowisko.y + d_pozioma * np.sin(az_punktu)

            obliczone_punkty[p['nr']] = Punkt(x, y, p['nr'])

        return obliczone_punkty


class RaportGeodezyjny:
    @staticmethod
    def wyswietl_wyniki(punkty_1004, punkty_1005):
        print("\n" + "=" * 70)
        print(f"{'Nr punktu':<18} | {'Stanowisko':<12} | {'X [m]':<15} | {'Y [m]':<15}")
        print("-" * 70)

        # Wyświetlanie wyników ze stanowiska 1004
        for nr, p in punkty_1004.items():
            print(f"{nr:<18} | {'1004':<12} | {p.x:<15.3f} | {p.y:<15.3f}")

        # Wyświetlanie wyników ze stanowiska 1005
        for nr, p in punkty_1005.items():
            print(f"{nr:<18} | {'1005':<12} | {p.x:<15.3f} | {p.y:<15.3f}")
        print("=" * 70)


# --- DANE ZADANIA ---
# Współrzędne osnowy (z image_dab81a.png)
s1004 = Punkt(5923995.565, 5466340.928, "1004")
s1005 = Punkt(5924041.703, 5466381.792, "1005")

# Dane z dziennika (image_db3aa1.png)
# Hz na nawiązanie to odczyt Kierunku Hz na drugi punkt osnowy
hz_na_1005 = 46.14531
hz_na_1004 = 246.14531

pomiary_1004 = [
    {'nr': 'naroznik1', 'kat_hz': 367.27952, 'kat_v': 107.92742, 'd': 10.148},
    {'nr': 'naroznik1laser', 'kat_hz': 367.09228, 'kat_v': 108.01483, 'd': 10.187},
    {'nr': 'naroznik2', 'kat_hz': 352.85856, 'kat_v': 103.28166, 'd': 25.844},
    {'nr': 'naroznik2laser', 'kat_hz': 352.92045, 'kat_v': 103.30777, 'd': 25.809}
]

pomiary_1005 = [
    {'nr': 'naroznik3', 'kat_hz': 328.44419, 'kat_v': 103.52181, 'd': 28.435},
    {'nr': 'naroznik3laser', 'kat_hz': 328.41092, 'kat_v': 103.56217, 'd': 28.408},
    {'nr': 'naroznik4laser', 'kat_hz': 309.45040, 'kat_v': 107.39455, 'd': 13.476},
    {'nr': 'naroznik4', 'kat_hz': 309.52996, 'kat_v': 107.33347, 'd': 13.443}
]

if __name__ == "__main__":
    kalkulator = MetodaBiegunowa()

    # Obliczenia z uwzględnieniem orientacji na punkt nawiązania
    wyniki_1004 = kalkulator.oblicz_punkty(s1004, s1005, hz_na_1005, pomiary_1004)
    wyniki_1005 = kalkulator.oblicz_punkty(s1005, s1004, hz_na_1004, pomiary_1005)

    # Raport
    raport = RaportGeodezyjny()
    raport.wyswietl_wyniki(wyniki_1004, wyniki_1005)