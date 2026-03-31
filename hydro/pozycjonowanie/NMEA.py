def wypisz_parametry(data):
    # Split dzieli tekst na listę wszędzie tam, gdzie jest przecinek
    czesci = data.split(',')

    # W NMEA GGA: indeks 1 = czas, 2 = szerokosc, 3 = N/S, 4 = dlugosc, 5 = E/W
    if len(czesci) > 6:
        czas = czesci[1]
        szerokosc = f"{czesci[2]} {czesci[3]}"
        dlugosc = f"{czesci[4]} {czesci[5]}"

        print(">>> DANE WYDOBYTE Z GPGGA:")
        print(f"CZAS:      {czas}")
        print(f"SZEROKOSC: {szerokosc}")
        print(f"DLUGOSC:   {dlugosc}")


def procesuj_nmea(data):
    data = data.strip()  # Odpowiednik trim()

    # Szukamy startu od $
    start_pos = data.find('$')
    if start_pos != -1:
        data = data[start_pos:]

    dolar_pos = data.find('$')
    gwiazdka_pos = data.find('*')

    czy_to_nmea = False
    xor_wyliczony = 0

    if dolar_pos != -1 and gwiazdka_pos > dolar_pos:
        # Obliczanie sumy kontrolnej XOR (w Pythonie ord() zamienia znak na kod ASCII)
        # Bierzemy znaki MIĘDZY $ a *
        for char in data[dolar_pos + 1: gwiazdka_pos]:
            xor_wyliczony ^= ord(char)

        try:
            # Wyciągamy sumę z ramki (hex na int)
            suma_str = data[gwiazdka_pos + 1: gwiazdka_pos + 3]
            suma_w_ramce = int(suma_str, 16)

            if xor_wyliczony == suma_w_ramce:
                czy_to_nmea = True
        except ValueError:
            czy_to_nmea = False

    # Logika wyświetlania
    if czy_to_nmea and data.startswith("$GPGGA"):
        print(f"SUMA KONTROLNA: 0x{xor_wyliczony:02X}")
        wypisz_parametry(data)
        print("-" * 36)
    else:
        print(f"Zdanie w czystej postaci: {data}***")


# --- GŁÓWNA PĘTLA (odpowiednik loop) ---
print("System gotowy. Wklej sekwencje NMEA (lub wpisz 'exit' by wyjsc):")
while True:
    user_input = input("> ")
    if user_input.lower() == 'exit':
        break
    if user_input:
        procesuj_nmea(user_input)