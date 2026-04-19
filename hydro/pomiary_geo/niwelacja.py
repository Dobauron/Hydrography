from __future__ import annotations
from dataclasses import dataclass
import math

@dataclass #uproszeczenie, gdy klasa ma być jedynie pudełkiem dla danych, bez zarządzania nimi
class Stanowisko:
    od: str
    do: str
    t1: int; p1: int
    t2: int; p2: int
    TOLERANCJA: int = 3

    @property
    def h1(self) -> int: return self.t1 - self.p1
    @property
    def h2(self) -> int: return self.t2 - self.p2
    @property
    def h_sr(self) -> float: return (self.h1 + self.h2) / 2.0
    @property
    def delta(self) -> int: return abs(self.h1 - self.h2)
    @property
    def czy_ok(self) -> bool: return self.delta <= self.TOLERANCJA

class CiagNiwelacyjny:
    def __init__(self, nazwa: str, h_start: float, zamkniety: bool = False):
        self.nazwa = nazwa
        self.h_start = h_start
        self.zamkniety = zamkniety
        self.stanowiska: list[Stanowisko] = []

    def wczytaj_dane(self, dane: list[dict]):
        for d in dane:
            # Automatycznie dopasowuje klucze ze słownika do pól klasy
            self.stanowiska.append(Stanowisko(d['od'], d['do'], d['t1'], d['p1'], d['t2'], d['p2']))

    def raport(self):
        n = len(self.stanowiska)
        suma_h = sum(s.h_sr for s in self.stanowiska) # sumuje wszystkie h_sr stanowisk

        tolerancja = 5.0 * math.sqrt(n)
        poprawka = -suma_h / n if self.zamkniety else 0.0

        print(f"\n--- RAPORT: {self.nazwa} ---")
        print(f"{'Nr':>2} | {'Od':>7} -> {'Do':<8} | {'h_sr [mm]':>9} | {'Status'}")
        print("-" * 45)

        h_akt = self.h_start
        punkty = [(self.stanowiska[0].od, h_akt)]

        # Iterujemy po wszystkich stanowiskach, i to numer (od 1), s to dane stanowiska
        for i, s in enumerate(self.stanowiska, 1):
            # Aktualizujemy wysokość: do obecnej dodajemy średnie przewyższenie ze stanowiska
            # powiększone o poprawkę (wyrównanie). Dzielimy przez 1000, by zamienić [mm] na [m].
            h_akt += (s.h_sr + poprawka) / 1000.0

            # Zapamiętujemy wynik: dodajemy nazwę punktu docelowego i jego obliczoną
            # wysokość (zaokrągloną do 4 miejsc po przecinku) do listy wyników.
            punkty.append((s.do, round(h_akt, 4)))

            # Drukowanie wiersza tabeli: numer, skąd-dokąd, różnica wysokości i status
            # (czy pomiary I i II na tym stanowisku były ze sobą zgodne w granicach 3mm).
            print(f"{i:>2} | {s.od:>7} -> {s.do:<8} | {s.h_sr:>9.1f} | {'OK' if s.czy_ok else 'BŁĄD!'}")

        if self.zamkniety:
            status = "ZALICZONE" if abs(suma_h) <= tolerancja else "DO POPRAWY"
            print(f"\nKontrola zamknięcia: {suma_h:+.1f} mm (Tolerancja: ±{tolerancja:.1f} mm) -> {status}")

        print("\nObliczone wysokości [m]:")
        for pkt, h in punkty:
            print(f"  {pkt:<10}: {h:.4f}")

def kontrola_gnss(dane: list[tuple[int, float]]):
    suma_dh = sum(dane[i][1] - dane[i-1][1] for i in range(1, len(dane)))
    skrajne = dane[-1][1] - dane[0][1]
    print(f"\nGNSS Check: Suma dH = {suma_dh:.4f}, Hn-H1 = {skrajne:.4f}")
    print("Status: " + ("OK" if abs(suma_dh - skrajne) < 1e-9 else "BŁĄD W DANYCH"))
    #abs = wartość bezwzględna liczby

# --- Uruchomienie ---
if __name__ == "__main__":
    # Dane zadania 1
    zad1 = CiagNiwelacyjny("Rp.1345 -> Rp.1346", 234.567)
    zad1.wczytaj_dane([
        {"od": "Rp.1345", "do": "R1", "t1": 1220, "p1": 2344, "t2": 1246, "p2": 2368},
        {"od": "R1", "do": "R2-1", "t1": 1642, "p1": 1530, "t2": 1654, "p2": 1538},
        {"od": "R2-2", "do": "R3-1", "t1": 2204, "p1": 1178, "t2": 2182, "p2": 1156},
        {"od": "R3-2", "do": "Rp.1346", "t1": 796, "p1": 1456, "t2": 782, "p2": 1440}
    ])
    zad1.raport()

    # ZADANIE 2 - Niwelacja geometryczna (dane ze zdjęcia)
    zad2 = CiagNiwelacyjny("Pomiar Kampusu - Zadanie 2", h_start=31.9862, zamkniety=True)

    # dodaj(od, do, t1, p1, t2, p2)
    dane_zad2 = [
        {"od": "REPER", "do": "ZABKA_1", "t1": 1123, "p1": 1217, "t2": 949, "p2": 1042},
        {"od": "ZABKA_1", "do": "STU 1", "t1": 893, "p1": 1044, "t2": 1106, "p2": 1256},
        {"od": "STU 1", "do": "STU 2", "t1": 1335, "p1": 1345, "t2": 1303, "p2": 1313},
        {"od": "STU 2", "do": "STU 3", "t1": 1227, "p1": 1378, "t2": 1310, "p2": 1460},
        {"od": "STU 3", "do": "STU 4", "t1": 1411, "p1": 1397, "t2": 1341, "p2": 1326},
        {"od": "STU 4", "do": "STU 5", "t1": 1187, "p1": 1285, "t2": 1385, "p2": 1480},
        {"od": "STU 5", "do": "STU 6", "t1": 1380, "p1": 1229, "t2": 1121, "p2": 967},
        {"od": "STU 6", "do": "STU 7", "t1": 1134, "p1": 1223, "t2": 1302, "p2": 1392},
        {"od": "STU 7", "do": "STU 8", "t1": 1463, "p1": 1229, "t2": 1564, "p2": 1332},
        {"od": "STU 8", "do": "ZABKA_2", "t1": 1302, "p1": 1366, "t2": 1172, "p2": 1228},
        {"od": "ZABKA_2", "do": "REPER", "t1": 1210, "p1": 1018, "t2": 1307, "p2": 1115},
    ]
    zad2.wczytaj_dane(dane_zad2)


    zad2.raport()

    # ZADANIE 3 - Dane z Twojego pliku niwelacja_gnss.txt
    dane_z_pliku_gnss = [
        (1, 31.9862), (2, 32.3930), (3, 31.7258), (5, 31.7419),
        (6, 31.6043), (7, 31.6690), (8, 31.5655), (9, 31.1342),
        (10, 31.6576), (13, 31.9611), (14, 31.8220), (15, 32.0793)
    ]

    kontrola_gnss(dane_z_pliku_gnss)