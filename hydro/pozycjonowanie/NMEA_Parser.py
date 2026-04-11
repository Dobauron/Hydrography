import math


class NMEAParser:
    """Klasa do parsowania i walidacji sentencji protokołu NMEA 0183."""

    def __init__(self):
        self.talker_id = ""
        self.msg_type = ""

    def validate_checksum(self, sentence: str) -> bool:
        """Oblicza i weryfikuje sumę kontrolną XOR."""
        if not sentence.startswith('$') or '*' not in sentence:
            return False

        # Dane do obliczeń znajdują się między '$' a '*'
        try:
            star_index = sentence.find('*')
            data_to_check = sentence[1:star_index]
            provided_checksum = sentence[star_index + 1: star_index + 3]

            calculated_checksum = 0  # zmienna inicjalna
            for char in data_to_check:  # iteracja po każdym znaku sentencji NMEA
                calculated_checksum ^= ord(char)  # Porównywanie bitowej sumy obecnego znaku iteracji z poprzednim

            # Konwersja na format hexadecymalny i porównanie z ostatnimi dwoma znakami NMEA, także w HEXA
            return f"{calculated_checksum:02X}" == provided_checksum.upper()
        except Exception:
            return False

    def _convert_to_dms(self, value: str, direction: str) -> str:
        """Konwertuje format NMEA (DDMM.MMMM) na format DMS (Stopnie Minuty Sekundy)."""
        if not value or not direction:
            return "Brak danych"

        try:
            # W NMEA szerokość ma 2 cyfry stopni, długość 3
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
        """Formatuje surowy czas NMEA na format HH:MM:SS."""
        if len(raw_time) >= 6:
            hh = raw_time[:2]
            mm = raw_time[2:4]
            ss = raw_time[4:]
            return f"{hh}:{mm}:{ss}"
        return raw_time

    def process_sentence(self, sentence: str):
        """Główna metoda przetwarzająca wejściowy ciąg znaków."""
        sentence = sentence.strip()

        # Jeśli to nie jest NMEA, dodaj prefiks i sufix
        if not sentence.startswith('$'):
            print(f"Zdanie w czystej postaci: {sentence} ***")
            return

        # Sprawdzenie poprawności sumy kontrolnej
        if not self.validate_checksum(sentence):
            print(f"BŁĄD: Niepoprawna suma kontrolna dla: {sentence}")
            return

        # Rozbicie sentencji na pola
        content = sentence[1:sentence.find('*')]  # czyszczenie wiadomości od 2 znaku do *
        parts = content.split(',')
        header = parts[0]
        self.talker_id = header[:2]  # np. GP dla GPS
        self.msg_type = header[2:]  # np. GGA

        print("-" * 30)
        print(f"Nadawca: {self.talker_id}")
        print(f"Typ wiadomości: {self.msg_type}")

        # Obsługa konkretnego typu: GGA
        if self.msg_type == "GGA" and len(parts) >= 12:  # zwiększona walidacja dla dodatkowych pól
            time_utc = self._parse_time(parts[1])
            lat_dms = self._convert_to_dms(parts[2], parts[3])
            lon_dms = self._convert_to_dms(parts[4], parts[5])

            # Nowe pola, o które pytałeś:
            quality = parts[6]  # Wskaźnik jakości (ta '1' po E)
            satellites = parts[7]  # Liczba satelitów
            hdop = parts[8]  # Dokładność pozioma
            altitude = f"{parts[9]} {parts[10]}"  # Wysokość + jednostka (M)

            print(f"Czas (UTC): {time_utc}")
            print(f"Szerokość (DMS): {lat_dms}")
            print(f"Długość (DMS): {lon_dms}")

            # Mapowanie wskaźnika jakości dla czytelności
            quality_desc = "Brak fixu" if quality == "0" else "GPS Fix (SPS)" if quality == "1" else "DGPS Fix"

            print(f"Status sygnału: {quality_desc} ({quality})")
            print(f"Liczba satelitów: {satellites}")
            print(f"Precyzja (HDOP): {hdop}")
            print(f"Wysokość n.p.m.: {altitude}")

        print("-" * 30)


# --- Przykład użycia ---
if __name__ == "__main__":
    parser = NMEAParser()

    # Przykładowa poprawna sentencja GGA z instrukcji
    test_gga = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47"
    parser.process_sentence(test_gga)

    # Przykład błędnej wiadomości (tekst)
    parser.process_sentence("Błędna wiadomość")