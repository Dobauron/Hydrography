class RinexParser:
    """
    Klasa odpowiedzialna za wczytywanie, parsowanie i analizę
    plików nawigacyjnych GNSS w formacie RINEX.
    """

    def __init__(self, sciezka_pliku):
        """
        Inicjalizator obiektu parsera.
        """
        self.sciezka_pliku = sciezka_pliku
        self.linie = []
        self.naglowek = {}
        self.wspolczynniki_jonosfery = {}
        self.indeks_danych = 0

    def wczytaj_i_oczysc_plik(self):
        """
        Otwiera plik bezpieczną konstrukcją 'with open', wczytuje linie
        i oczyszcza je ze znaków końca wiersza (\n) za pomocą list comprehension.
        """
        try:
            with open(self.sciezka_pliku, "r", encoding="utf-8", errors="ignore") as f:
                # Wykorzystanie list comprehension zamiast klasycznej pętli (Krok 17-20)
                self.linie = [linia.rstrip("\n") for linia in f.readlines()]
            print(f"[SUKCES] Wczytano poprawnie {len(self.linie)} linii z pliku '{self.sciezka_pliku}'.")
        except FileNotFoundError:
            print(f"[BŁĄD] Nie znaleziono pliku o ścieżce: {self.sciezka_pliku}")

    def parsuj_naglowek(self):
        """
        Analizuje linię po linii sekcję nagłówkową na podstawie sztywnych kolumn (1-60 oraz 61-80),
        aż do momentu napotkania rekordu 'END OF HEADER' (Krok 21-24).
        """
        if not self.linie:
            print("[OSTRZEŻENIE] Brak danych do parsowania. Najpierw wczytaj plik!")
            return

        i = 0
        while i < len(self.linie):
            linia = self.linie[i]

            # Zabezpieczenie przed liniami krótszymi niż standardowe 80 znaków
            if len(linia) < 60:
                linia = linia.ljust(80)

            # Podział linii na część danych (0-60) oraz etykietę opisu (60-80) (Krok 21)
            wartosc_pola = linia[0:60].strip()
            etykieta_pola = linia[60:].strip()

            # Warunek stopu - wyjście z nagłówka do sekcji danych (Krok 24)
            if etykieta_pola == "END OF HEADER":
                self.indeks_danych = i + 1
                break

            # Zapisanie surowej wartości do słownika nagłówka
            self.naglowek[etykieta_pola] = wartosc_pola

            # Specjalna obsługa parametrów jonosferycznych ION ALPHA (Krok 25)
            if etykieta_pola == "ION ALPHA":
                self._parsuj_ion_alpha(wartosc_pola)

            i += 1

    def _parsuj_ion_alpha(self, surowy_tekst):
        """
        Metoda prywatna (pomocnicza) do rozbicia parametrów ION ALPHA
        na 4 osobne zmienne typu float (Krok 25).
        """
        wspolczynniki = surowy_tekst.split()
        if len(wspolczynniki) >= 4:
            self.wspolczynniki_jonosfery = {
                'alpha_0': float(wspolczynniki[0]),
                'alpha_1': float(wspolczynniki[1]),
                'alpha_2': float(wspolczynniki[2]),
                'alpha_3': float(wspolczynniki[3])
            }

    def wyswietl_podsumowanie_naglowka(self):
        """
        Wypisuje sformatowaną zawartość całego nagłówka.
        """
        print("\n" + "=" * 30 + " PODSUMOWANIE NAGŁÓWKA " + "=" * 30)
        for etykieta, wartosc in self.naglowek.items():
            print(f" -> {etykieta:<25} : {wartosc}")

        # Jeśli udało się sparsować współczynniki jonosfery, wyświetlamy je osobno
        if self.wspolczynniki_jonosfery:
            print("\n" + "-" * 15 + " WYODRĘBNIONE ZMIENNE ION ALPHA " + "-" * 15)
            for nazwa_zmiennej, wartosc_numeryczna in self.wspolczynniki_jonosfery.items():
                print(f"    * {nazwa_zmiennej} = {wartosc_numeryczna}")
        print("=" * 83)

    def wyswietl_pierwsza_epoke_danych(self, liczba_linii=8):
        """
        Wyświetla określoną liczbę linii danych znajdujących się bezpośrednio
        za rekordem END OF HEADER (Krok 26*).
        """
        if self.indeks_danych == 0:
            print("[OSTRZEŻENIE] Najpierw musisz sparsować nagłówek, aby odnaleźć granicę danych!")
            return

        print(f"\n" + "=" * 27 + f" PIERWSZE {liczba_linii} LINII SEKCJI DANYCH " + "=" * 27)
        for j in range(liczba_linii):
            aktualny_indeks = self.indeks_danych + j
            if aktualny_indeks < len(self.linie):
                print(f" Linia danych {j + 1:02d}: {self.linie[aktualny_indeks]}")
        print("=" * 83)


# =============================================================================
# PRZYKŁAD UŻYCIA OBIEKTOWEGO (Do uruchomienia w Jupyter Notebook)
# =============================================================================

# 1. Tworzymy instancję (obiekt) klasy RinexParser, przekazując nazwę pliku
parser = RinexParser("RINEX_n.txt")

# 2. Wywołujemy wczytywanie i czyszczenie znaków końca linii
parser.wczytaj_i_oczysc_plik()

# 3. Wykonujemy proces parsowania struktury nagłówkowej
parser.parsuj_naglowek()

# 4. Wyświetlamy zebrane i posegregowane informacje z nagłówka
parser.wyswietl_podsumowanie_naglowka()

# 5. Wyświetlamy początkowy blok efemeryd/danych satelitarnych (Krok dla chętnych)
parser.wyswietl_pierwsza_epoke_danych(liczba_linii=8)