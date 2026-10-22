# Tapşırıq 1: Musiqi playlisti (Linked List)
# Hər mahnı bir "halqadır" və növbəti mahnını göstərir (next).


class Song:
    def __init__(self, song_id, name, artist):
        self.song_id = song_id
        self.name = name
        self.artist = artist
        self.next = None          # növbəti mahnı


class Playlist:
    def __init__(self):
        self.head = None          # birinci mahnı
        self.size = 0

    def add_song(self, song):
        song.next = self.head     # yeni mahnı əvvələ düşür
        self.head = song
        self.size += 1

    def search_song(self, song_id):
        current = self.head
        while current is not None:
            if current.song_id == song_id:
                return current
            current = current.next
        return None

    def delete_song(self, song_id):
        if self.head is None:
            return False
        if self.head.song_id == song_id:      # birinci mahnı silinir
            self.head = self.head.next
            self.size -= 1
            return True
        current = self.head
        while current.next is not None:
            if current.next.song_id == song_id:
                current.next = current.next.next   # mahnını atlayırıq
                self.size -= 1
                return True
            current = current.next
        return False

    def display(self):
        current = self.head
        while current is not None:
            print(current.song_id, current.name, "-", current.artist)
            current = current.next

    def count(self):
        return self.size


def menu():
    playlist = Playlist()
    while True:
        print("\n1. Mahnı əlavə et")
        print("2. Mahnı sil")
        print("3. Mahnı axtar")
        print("4. Playlisti göstər")
        print("5. Mahnıların sayı")
        print("0. Çıxış")
        choice = input("Seçim: ")

        if choice == "1":
            song_id = int(input("ID: "))
            name = input("Mahnının adı: ")
            artist = input("İfaçı: ")
            playlist.add_song(Song(song_id, name, artist))
        elif choice == "2":
            song_id = int(input("Silinəcək ID: "))
            print("Silindi." if playlist.delete_song(song_id) else "Tapılmadı.")
        elif choice == "3":
            song = playlist.search_song(int(input("Axtarılan ID: ")))
            print(song.name + " - " + song.artist if song else "Tapılmadı.")
        elif choice == "4":
            playlist.display()
        elif choice == "5":
            print("Mahnı sayı:", playlist.count())
        elif choice == "0":
            break


if __name__ == "__main__":
    menu()
