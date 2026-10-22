# Tapşırıq 3: Hava limanı növbəsi (Queue)
# İlk gələn sərnişin ilk xidmət alır (FIFO).


class Passenger:
    def __init__(self, passenger_id, name, flight_number):
        self.passenger_id = passenger_id
        self.name = name
        self.flight_number = flight_number
        self.next = None          # arxasındakı sərnişin


class Queue:
    def __init__(self):
        self.front = None         # növbənin əvvəli (buradan çıxır)
        self.rear = None          # növbənin sonu (buraya əlavə olunur)
        self.size = 0

    def enqueue(self, passenger):
        if self.rear is None:     # növbə boşdursa
            self.front = passenger
        else:
            self.rear.next = passenger
        self.rear = passenger
        self.size += 1

    def dequeue(self):
        if self.front is None:
            return None
        passenger = self.front
        self.front = passenger.next
        if self.front is None:    # növbə boşaldı
            self.rear = None
        self.size -= 1
        return passenger

    def peek(self):
        return self.front


def menu():
    queue = Queue()
    while True:
        print("\n1. Add Passenger")
        print("2. Check-In Passenger")
        print("3. Peek Next Passenger")
        print("4. Display Queue")
        print("5. Count Passengers")
        print("0. Çıxış")
        choice = input("Seçim: ")

        if choice == "1":
            passenger_id = int(input("ID: "))
            name = input("Ad: ")
            flight = input("Reys nömrəsi: ")
            queue.enqueue(Passenger(passenger_id, name, flight))
        elif choice == "2":
            p = queue.dequeue()
            print("Check-in oldu:", p.name if p else "Növbə boşdur.")
        elif choice == "3":
            p = queue.peek()
            print("Növbəti:", p.name if p else "Növbə boşdur.")
        elif choice == "4":
            current = queue.front
            while current is not None:
                print(current.passenger_id, current.name, current.flight_number)
                current = current.next
        elif choice == "5":
            print("Sərnişin sayı:", queue.size)
        elif choice == "0":
            break


if __name__ == "__main__":
    menu()
