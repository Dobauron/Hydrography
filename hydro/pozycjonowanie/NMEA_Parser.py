import math


class NMEAParser:
    """Klasa do parsowania i walidacji sentencji protokołu NMEA 0183[cite: 23, 28]."""

    def __init__(self):
        self.talker_id = ""
        self.msg_type = ""

    def validate_checksum(self, sentence: str) -> bool:
        """Oblicza i weryfikuje sumę kontrolną XOR."""
        if not sentence.startswith('$') or '*' not in sentence:
            return False

        # Dane do obliczeń znajdują się między '$' a '*' [cite: 29]
        try:
            star_index = sentence.find('*')
            data_to_check = sentence[1:star_index]
            provided_checksum = sentence[star_index + 1: star_index + 3]

            calculated_checksum = 0  # zmienna inicjalna
            for char in data_to_check:  # iteracja po każdym znaku sentencji NMEA
                calculated_checksum ^= ord(char)  # Porównywanie bitowej sumy obecnego znaku iteracji z poprzednim
            return f"{calculated_checksum:02X}" == provided_checksum.upper()
            # konwersja na format hexadecymalny
            # i porównanie z ostatnimi dwoma znakami NMEA, także w HEXA
        except Exception:
            return False

    def _convert_to_dms(self, value: str, direction: str) -> str:
        """Konwertuje format NMEA (DDMM.MMMM) na format DMS (Stopnie Minuty Sekundy)."""
        if not value or not direction:
            return "Brak danych"

        try:
            # W NMEA szerokość ma 2 cyfry stopni, długość 3 [cite: 80]
            dot_index = value.find('.')
            degrees_part = value[:dot_index - 2]
            minutes_part = value[dot_index - 2:]

            degrees = int(degrees_part)
            full_minutes = float(minutes_part)

            minutes = int(full_minutes)
            seconds = (full_minutes - minutes) * 60

            return f"{degrees}° {minutes}' {seconds:.4f}\" {direction}"
        except ValueError:
            return "Błąd konwersji"

    def _parse_time(self, raw_time: str) -> str:
        """Formatuje surowy czas NMEA na format HH:MM:SS[cite: 91, 92]."""
        if len(raw_time) >= 6:
            hh = raw_time[:2]
            mm = raw_time[2:4]
            ss = raw_time[4:]
            return f"{hh}:{mm}:{ss}"
        return raw_time

    def process_sentence(self, sentence: str):
        """Główna metoda przetwarzająca wejściowy ciąg znaków[cite: 95, 96]."""
        sentence = sentence.strip()

        # Jeśli to nie jest NMEA, dodaj prefiks i sufix [cite: 97, 98]
        if not sentence.startswith('$'):
            print(f"Zdanie w czystej postaci: {sentence} ***")
            return

        # Sprawdzenie poprawności sumy kontrolnej
        if not self.validate_checksum(sentence):
            print(f"BŁĄD: Niepoprawna suma kontrolna dla: {sentence}")
            return

        # Rozbicie sentencji na pola [cite: 80]
        content = sentence[1:sentence.find('*')]
        parts = content.split(',')

        header = parts[0]
        self.talker_id = header[:2]  # np. GP dla GPS [cite: 80]
        self.msg_type = header[2:]  # np. GGA [cite: 80]

        print("-" * 30)
        print(f"Nadawca: {self.talker_id}")
        print(f"Typ wiadomości: {self.msg_type}")

        # Obsługa konkretnego typu: GGA [cite: 33, 79]
        if self.msg_type == "GGA" and len(parts) >= 6:
            time_utc = self._parse_time(parts[1])
            lat_dms = self._convert_to_dms(parts[2], parts[3])
            lon_dms = self._convert_to_dms(parts[4], parts[5])

            print(f"Czas (UTC): {time_utc}")
            print(f"Szerokość (DMS): {lat_dms}")
            print(f"Długość (DMS): {lon_dms}")
            print(f"Liczba satelitów: {parts[7]}")  # Dodatkowy parametr z tabeli [cite: 80]

        print("-" * 30)


# --- Przykład użycia ---
if __name__ == "__main__":
    parser = NMEAParser()

    # Przykładowa poprawna sentencja GGA z instrukcji [cite: 31]
    test_gga = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*49"
    parser.process_sentence(test_gga)

    # Przykład błędnej wiadomości (tekst) [cite: 97]
    parser.process_sentence("Błędna wiadomość")
