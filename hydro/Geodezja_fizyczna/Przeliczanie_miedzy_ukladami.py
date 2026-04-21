import math
import pyproj


TRANSFORMERY = {
    "krasowski": pyproj.Transformer.from_crs("EPSG:4326", "EPSG:4284", always_xy=True),
    "xyz92":     pyproj.Transformer.from_crs("EPSG:4326", "EPSG:4978", always_xy=True),
    "uklad1992": pyproj.Transformer.from_crs("EPSG:4326", "EPSG:2180", always_xy=True),
    "uklad2000": {
        5: pyproj.Transformer.from_crs("EPSG:4326", "EPSG:2176", always_xy=True),
        6: pyproj.Transformer.from_crs("EPSG:4326", "EPSG:2177", always_xy=True),
        7: pyproj.Transformer.from_crs("EPSG:4326", "EPSG:2178", always_xy=True),
        8: pyproj.Transformer.from_crs("EPSG:4326", "EPSG:2179", always_xy=True),
    },
}

ZADANIA = {
    "1": {
        "nazwa": "Zadanie 1 – Rozciągłość Polski (N/S/W/E)",
        "punkty": {
            "Północ (N)":  (54.835778, 18.300028),
            "Południe (S)": (49.002250, 22.709778),
            "Zachód (W)":  (52.838389, 14.122917),
            "Wschód (E)":  (54.037972, 24.144306),
        },
    },
    "2": {
        "nazwa": "Zadanie 2 – Miejsce zamieszkania & Sala",
        "punkty": {
            "Zamieszkanie": (53.435978, 14.571755),
            "Sala":         (53.446954, 14.493434),
        },
    },
}

def _strefa_2000(lon: float) -> int:
    if lon < 16.5: return 5
    if lon < 19.5: return 6
    if lon < 22.5: return 7
    return 8


class TransformatorGeodezyjny:

    def __init__(self, punkty: dict):
        self.PUNKTY_GRS80 = punkty
        self.geod = pyproj.Geod(ellps="GRS80")

    # ── helpers ──────────────────────────────

    @staticmethod
    def _naglowek(tytul: str):
        print(f"\n{'─'*60}")
        print(f"  {tytul}")
        print(f"{'─'*60}")

    @staticmethod
    def _drukuj_rozciaglosc_bl(punkty: dict):
        nazwy = list(punkty.keys())
        bs = [v[0] for v in punkty.values()]
        ls = [v[1] for v in punkty.values()]
        i_bmax, i_bmin = bs.index(max(bs)), bs.index(min(bs))
        i_lmax, i_lmin = ls.index(max(ls)), ls.index(min(ls))
        db, dl = max(bs) - min(bs), max(ls) - min(ls)
        print(f"  Wzory rozciągłości:")
        print(f"    ΔB = B_max − B_min = {nazwy[i_bmax]}({max(bs):.6f}°) − {nazwy[i_bmin]}({min(bs):.6f}°) = {db:.6f}°")
        print(f"    ΔL = L_max − L_min = {nazwy[i_lmax]}({max(ls):.6f}°) − {nazwy[i_lmin]}({min(ls):.6f}°) = {dl:.6f}°")

    @staticmethod
    def _drukuj_rozciaglosc_xy(punkty: dict):
        nazwy = list(punkty.keys())
        xs = [v[0] for v in punkty.values()]
        ys = [v[1] for v in punkty.values()]
        i_xmax, i_xmin = xs.index(max(xs)), xs.index(min(xs))
        i_ymax, i_ymin = ys.index(max(ys)), ys.index(min(ys))
        dx, dy = max(xs) - min(xs), max(ys) - min(ys)
        print(f"  Wzory rozciągłości:")
        print(f"    ΔX = X_max − X_min = {nazwy[i_xmax]}({max(xs):.3f} m) − {nazwy[i_xmin]}({min(xs):.3f} m) = {dx:.3f} m")
        print(f"    ΔY = Y_max − Y_min = {nazwy[i_ymax]}({max(ys):.3f} m) − {nazwy[i_ymin]}({min(ys):.3f} m) = {dy:.3f} m")

    # ── etapy ────────────────────────────────

    def etap1_blh_grs80(self):
        self._naglowek("ETAP 1: BLH – GRS80 (dane wejściowe)")
        for nazwa, (b, l) in self.PUNKTY_GRS80.items():
            print(f"  {nazwa:<16} B={b:.6f}°   L={l:.6f}°")
        print()
        self._drukuj_rozciaglosc_bl(self.PUNKTY_GRS80)

    def etap2_krasowski(self):
        self._naglowek("ETAP 2: BLH – Krasowski (Pulkovo 1942 / EPSG:4284)")
        tr = TRANSFORMERY["krasowski"]
        wyniki = {}
        for nazwa, (b, l) in self.PUNKTY_GRS80.items():
            lk, bk = tr.transform(l, b)
            wyniki[nazwa] = (bk, lk)
            print(f"  {nazwa:<16} B={bk:.6f}°   L={lk:.6f}°")
        print()
        self._drukuj_rozciaglosc_bl(wyniki)

    def etap3_xyz92(self):
        self._naglowek("ETAP 3: XYZ92 – geocentryczny GRS80 (EPSG:4978)")
        tr = TRANSFORMERY["xyz92"]
        wyniki = {}

        for nazwa, (b, l) in self.PUNKTY_GRS80.items():
            x, y, z = tr.transform(l, b, 0)
            wyniki[nazwa] = (x, y, z)
            print(f"  {nazwa:<16} X={x:>13.3f} m   Y={y:>13.3f} m   Z={z:>13.3f} m")

        naz = list(wyniki.keys())

        # ρ = √(X² + Y²)
        rho = {n: math.sqrt(v[0]**2 + v[1]**2) for n, v in wyniki.items()}

        # tg B = ρ / Z  →  B = arctan(ρ / Z)
        B_geo = {n: math.degrees(math.atan(rho[n] / wyniki[n][2])) for n in naz}

        # tg L = X / Y  →  L = arctan(X / Y)
        L_geo = {n: math.degrees(math.atan(wyniki[n][0] / wyniki[n][1])) for n in naz}

        print(f"\n  Kąty geocentryczne (wyznaczone ze wzorów):")
        for n in naz:
            print(f"  {n:<16} ρ={rho[n]:>13.3f} m   B={B_geo[n]:.6f}°   L={L_geo[n]:.6f}°")

        bs = list(B_geo.values())
        ls = list(L_geo.values())
        i_bmax, i_bmin = bs.index(max(bs)), bs.index(min(bs))
        i_lmax, i_lmin = ls.index(max(ls)), ls.index(min(ls))
        delta_b = max(bs) - min(bs)
        delta_l = max(ls) - min(ls)

        print(f"\n  Wzory rozciągłości:")
        print(f"    ρ = √(X² + Y²)")
        print(f"    tg B = ρ / Z  →  B = arctan(ρ / Z)")
        print(f"    tg L = X / Y  →  L = arctan(X / Y)")
        print(f"")
        print(f"    ΔB = B_{naz[i_bmax]} − B_{naz[i_bmin]}")
        print(f"       = {max(bs):.6f}° − {min(bs):.6f}° = {delta_b:.6f}°")
        print(f"    ΔL = L_{naz[i_lmax]} − L_{naz[i_lmin]}")
        print(f"       = {max(ls):.6f}° − {min(ls):.6f}° = {delta_l:.6f}°")

    def etap4_uklad1992(self):
        self._naglowek("ETAP 4: Układ 1992 (EPSG:2180)")
        tr = TRANSFORMERY["uklad1992"]
        wyniki = {}
        for nazwa, (b, l) in self.PUNKTY_GRS80.items():
            # always_xy=True → (easting, northing) = (Y_PL, X_PL)
            y, x = tr.transform(l, b)
            wyniki[nazwa] = (x, y)
            print(f"  {nazwa:<16} X={x:>12.3f} m   Y={y:>12.3f} m")
        print()
        self._drukuj_rozciaglosc_xy(wyniki)

    def etap5_uklad2000(self):
        self._naglowek("ETAP 5: Układ 2000 (EPSG:2176–2179, dobór strefy automatyczny)")
        wyniki = {}

        for nazwa, (b, l) in self.PUNKTY_GRS80.items():
            strefa = _strefa_2000(l)
            # always_xy=True → (easting, northing) = (Y_PL, X_PL)
            y, x = TRANSFORMERY["uklad2000"][strefa].transform(l, b)
            wyniki[nazwa] = (x, y, strefa)

        for nazwa, (x, y, strefa) in wyniki.items():
            print(f"  {nazwa:<16} strefa={strefa}   X={x:>12.3f} m   Y={y:>12.3f} m")

        strefy = {v[2] for v in wyniki.values()}
        naz    = list(wyniki.keys())
        bs     = [v[0] for v in self.PUNKTY_GRS80.values()]
        ls     = [v[1] for v in self.PUNKTY_GRS80.values()]
        i_bmax, i_bmin = bs.index(max(bs)), bs.index(min(bs))
        i_lmax, i_lmin = ls.index(max(ls)), ls.index(min(ls))
        b_mean = sum(bs) / len(bs)
        print()

        if len(strefy) > 1:
            print(f"  ⚠️  Punkty leżą w strefach: {sorted(strefy)}")

        # ΔX (południkowa) – northingi porównywalne bezpośrednio między strefami
        xs = [v[0] for v in wyniki.values()]
        dx = max(xs) - min(xs)
        i_xmax, i_xmin = xs.index(max(xs)), xs.index(min(xs))

        # ΔY (równoleżnikowa) – łuk geodezyjny wzdłuż średniej równoleżnicy
        # (Y w różnych strefach nieporównywalne bezpośrednio)
        _, _, d_rownolegnikowa = self.geod.inv(min(ls), b_mean, max(ls), b_mean)

        print(f"  Wzory rozciągłości:")
        print(f"    ΔX (południkowa)    = X_max − X_min")
        print(f"       = {naz[i_xmax]}({max(xs):.3f} m) − {naz[i_xmin]}({min(xs):.3f} m) = {dx:.3f} m")
        print(f"    ΔY (równoleżnikowa) = łuk geodezyjny wzdłuż B_śr={b_mean:.4f}°")
        print(f"       {naz[i_lmin]}(L={min(ls):.6f}°) → {naz[i_lmax]}(L={max(ls):.6f}°) = {d_rownolegnikowa:.3f} m")

    def uruchom_wszystkie(self):
        self.etap1_blh_grs80()
        self.etap2_krasowski()
        self.etap3_xyz92()
        self.etap4_uklad1992()
        self.etap5_uklad2000()
        print()


# ── MENU ─────────────────────────────────────────────────────
def main():
    print("\n╔══════════════════════════════════════╗")
    print("║    TRANSFORMATOR GEODEZYJNY          ║")
    print("╠══════════════════════════════════════╣")
    for klucz, dane in ZADANIA.items():
        print(f"║  {klucz}. {dane['nazwa']:<35}║")
    print("║  0. Uruchom oba                      ║")
    print("╚══════════════════════════════════════╝")

    wybor = input("\nWybierz zadanie (0/1/2): ").strip()

    if wybor in ("1", "2"):
        zadanie = ZADANIA[wybor]
        print(f"\n>>> {zadanie['nazwa']}")
        TransformatorGeodezyjny(zadanie["punkty"]).uruchom_wszystkie()
    elif wybor == "0":
        for dane in ZADANIA.values():
            print(f"\n{'═'*60}")
            print(f"  {dane['nazwa']}")
            print(f"{'═'*60}")
            TransformatorGeodezyjny(dane["punkty"]).uruchom_wszystkie()
    else:
        print("Nieprawidłowy wybór. Podaj 0, 1 lub 2.")


if __name__ == "__main__":
    main()