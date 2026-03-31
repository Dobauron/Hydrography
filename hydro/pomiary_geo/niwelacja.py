# Dane wejściowe: [Numer punktu, Wysokość Z]
dane = [
    [1, 31.9862], [2, 32.3930], [3, 31.7258], [5, 31.7419],
    [6, 31.6043], [7, 31.6690], [8, 31.5655], [9, 31.1342],
    [10, 31.6576], [13, 31.9611], [14, 31.8220], [15, 32.0793]
]


def kontrola_obliczen(lista):
    h_pierwszy = lista[0][1]
    h_ostatni = lista[-1][1]

    suma_czastkowych_delt = 0

    print(f"{'Skok':<10} | {'Obliczona Delta [m]':>20}")
    print("-" * 35)

    # Pętla licząca różnice między sąsiadami i sumująca je
    for i in range(1, len(lista)):
        delta = lista[i][1] - lista[i - 1][1]
        suma_czastkowych_delt += delta
        print(f"Pkt {lista[i - 1][0]:>2}-{lista[i][0]:<2} | {delta:20.4f}")

    print("-" * 35)

    # Bezpośrednie porównanie
    roznica_bezposrednia = h_ostatni - h_pierwszy

    print(f"1. Suma wszystkich delt:    {suma_czastkowych_delt:10.4f} m")
    print(f"2. H_ostatni - H_pierwszy:  {roznica_bezposrednia:10.4f} m")

    # Sprawdzenie czy wyniki są identyczne (z uwzględnieniem precyzji zmiennoprzecinkowej)
    if abs(suma_czastkowych_delt - roznica_bezposrednia) < 1e-10:
        print("\nKONTROLA OK: Wyniki są identyczne.")
    else:
        print("\nBŁĄD: Wyniki się różnią!")


if __name__ == "__main__":
    kontrola_obliczen(dane)