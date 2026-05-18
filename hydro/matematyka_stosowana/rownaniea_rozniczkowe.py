import numpy as np
import matplotlib.pyplot as plt

# 1. Definicja rozwiązania ogólnego: y(x) = C1*exp(4x) + x^2/4 + x/8 + 1/32
def y_sol(x, C1=1):
    return C1 * np.exp(4*x) + (x**2)/4 + x/8 + 1/32

# 2. Przygotowanie danych do wykresu
x_vals = np.linspace(0, 1, 100)
y_vals = y_sol(x_vals, C1=1)

# 3. Tworzenie wykresu
plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_vals, label="Rozwiązanie y(x) dla C1=1", color='blue', linewidth=2)

# Zapisanie wyniku (wzoru) na wykresie
wynik_tekst = r"$y(x) = C_1 e^{4x} + \frac{x^2}{4} + \frac{x}{8} + \frac{1}{32}$"
plt.text(0.05, max(y_vals)*0.8, f"Wynik:\n{wynik_tekst}", fontsize=14,
         bbox=dict(facecolor='white', alpha=0.8))

# Estetyka wykresu
plt.title("Wykres rozwiązania równania $y' = 4y - x^2$", fontsize=14)
plt.xlabel("x")
plt.ylabel("y(x)")
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

# 4. Wyświetlenie wyniku i wykresu
print(f"Rozwiązanie ogólne: y(x) = C1*exp(4*x) + x^2/4 + x/8 + 1/32")
plt.show()