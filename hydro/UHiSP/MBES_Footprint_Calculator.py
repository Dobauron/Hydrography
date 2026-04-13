import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# ==========================================
# CZĘŚĆ 1: POBIERANIE DANYCH OD UŻYTKOWNIKA
# ==========================================
def get_user_data():
    """
    Funkcja odpowiada za interakcję z użytkownikiem.
    Pobiera kluczowe parametry echosondy i akwenu.
    """
    print("--- KONFIGURACJA PARAMETRÓW MBES ---")
    try:
        h = float(input("Głębokość akwenu (H) [m]: "))

        # Zgodnie ze specyfikacją MBES:
        # alpha to zazwyczaj szerokość wzdłużna (along-track)
        # beta to zazwyczaj szerokość poprzeczna (across-track)
        alpha = float(input("Szerokość wzdłużna wiązki (alpha) [deg]: "))
        beta = float(input("Szerokość poprzeczna wiązki (beta) [deg]: "))

        # theta to kąt wychylenia konkretnej wiązki (np. 65 stopni dla krawędzi)
        theta = float(input("Kąt wychylenia od nadiru (theta) [deg]: "))

        return h, alpha, beta, theta
    except ValueError:
        print("Błąd: Wprowadź poprawne wartości liczbowe.")
        return None


# ==========================================
# CZĘŚĆ 2: SILNIK OBLICZENIOWY
# ==========================================
def calculate_geometry(h, alpha, beta, theta):
    """
    Wylicza geometrię footprintu przy użyciu wzorów różnicowych.
    Zwraca wyniki w formie słownika.
    """
    # Python wykonuje operacje trygonometryczne na radianach
    a_rad = math.radians(alpha)
    b_rad = math.radians(beta)
    t_rad = math.radians(theta)

    # 1. Obliczenie wymiaru wzdłużnego L (Along-track)
    # Wymiar ten rośnie wraz z odległością od nadiru (dzielenie przez cosinus)
    l_outer = (2 * h * math.tan(a_rad / 2)) / math.cos(t_rad)

    # 2. Obliczenie wymiaru poprzecznego T (Across-track)
    # Wykorzystujemy różnicę tangensów dla krawędzi wiązki
    angle_1 = math.radians(theta + beta / 2)
    angle_2 = math.radians(theta - beta / 2)
    t_outer = h * (math.tan(angle_1) - math.tan(angle_2))

    # 3. Parametry pomocnicze do rysowania
    offset = h * math.tan(t_rad)  # Odległość rzutu środka wiązki od statku
    edge_far = h * math.tan(angle_1)  # Dalsza krawędź uderzenia
    edge_near = h * math.tan(angle_2)  # Bliższa krawędź uderzenia

    return {
        "L": l_outer,
        "T": t_outer,
        "offset": offset,
        "edge_far": edge_far,
        "edge_near": edge_near
    }


# ==========================================
# CZĘŚĆ 3: MODUŁ WIZUALIZACJI GRAFICZNEJ
# ==========================================
def plot_results(h, alpha, beta, theta, res):
    """
    Tworzy zestawienie dwóch wykresów: przekroju wodnego oraz rzutu na dno.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    plt.subplots_adjust(wspace=0.3)

    # --- WYKRES 1: PRZEKRÓJ PIONOWY (Geometria w wodzie) ---
    # Tło i linie odniesienia
    ax1.axhline(0, color='royalblue', linewidth=2, label='Powierzchnia')
    ax1.axhline(-h, color='#8B4513', linewidth=4, label='Dno morskie', zorder=5)

    # Rysowanie wiązki (trójkąt wypełniony kolorem)
    ax1.fill([0, res["edge_far"], res["edge_near"]], [0, -h, -h],
             color='lightcyan', alpha=0.5, zorder=1)

    # Krawędzie rozpiętości (beta) - na czerwono
    ax1.plot([0, res["edge_far"]], [0, -h], color='red', linewidth=2, label='Szerokość wiązki (β)')
    ax1.plot([0, res["edge_near"]], [0, -h], color='red', linewidth=2)

    # Oś główna (theta) - czarna przerywana
    ax1.plot([0, res["offset"]], [0, -h], color='black', linestyle='--', label='Oś wiązki (θ)')

    # Statek/Przetwornik
    ax1.scatter(0, 0, color='darkblue', marker='v', s=150, zorder=6, label='Przetwornik')

    ax1.set_title("Propagacja wiązki w toni wodnej")
    ax1.set_xlabel("Odległość poprzeczna [m]")
    ax1.set_ylabel("Głębokość [m]")
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='lower left')

    # --- WYKRES 2: RZUT NA DNO (Footprint) ---
    # Rysujemy elipsę reprezentującą plamę akustyczną
    # Szerokość elipsy to T, wysokość to L
    footprint = patches.Ellipse((res["offset"], 0), res["T"], res["L"],
                                color='red', alpha=0.4, label='Footprint MBES')
    ax2.add_patch(footprint)
    ax2.plot(res["offset"], 0, 'kx')  # Środek plamy

    # Skalowanie okna wykresu
    padding = max(res["T"], res["L"]) * 1.5
    ax2.set_xlim(res["offset"] - padding, res["offset"] + padding)
    ax2.set_ylim(-padding, padding)
    ax2.set_aspect('equal')

    ax2.set_title(f"Kształt plamy na dnie\n{res['T']:.2f}m (T) x {res['L']:.2f}m (L)")
    ax2.set_xlabel("Across-track (Poprzecznie) [m]")
    ax2.set_ylabel("Along-track (Wzdłużnie) [m]")
    ax2.grid(True, linestyle='--', alpha=0.5)

    plt.suptitle(f"Symulacja dla H = {h}m, θ = {theta}°, Beam = {alpha}°x{beta}°", fontsize=14)
    plt.show()


# ==========================================
# CZĘŚĆ 4: URUCHOMIENIE PROGRAMU
# ==========================================
def main():
    data = get_user_data()
    if data:
        h, alpha, beta, theta = data

        # Obliczenia
        results = calculate_geometry(h, alpha, beta, theta)

        # Wyniki tekstowe w konsoli
        print(f"\n--- OBLICZONE WYMIARY PLAMY ---")
        print(f"Wymiar poprzeczny (T): {results['T']:.2f} m")
        print(f"Wymiar wzdłużny (L):  {results['L']:.2f} m")
        print(f"Środek wiązki od osi: {results['offset']:.2f} m")

        # Generowanie grafiki
        plot_results(h, alpha, beta, theta, results)


if __name__ == "__main__":
    main()