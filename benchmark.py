# Performans testləri: vaxt ms ilə ölçülür.
# İşə salmaq üçün: python benchmark.py
import csv
import os
import time

import matplotlib
matplotlib.use("Agg")           # qrafiki pəncərə açmadan fayla yazır
import matplotlib.pyplot as plt

from playlist import Playlist, Song
from browser_history import Stack, Page
from airport_queue import Queue, Passenger

SIZES = [100, 1000, 10000]
RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "test_results")
os.makedirs(RESULTS, exist_ok=True)
REPEAT = 5                      # hər testi 5 dəfə təkrarlayıb orta götürürük


def average_ms(test_function):
    """test_function-u REPEAT dəfə işlədir, orta vaxtı ms ilə qaytarır."""
    total = 0
    for _ in range(REPEAT):
        total += test_function()
    return total / REPEAT * 1000


def timed(action):
    """action() funksiyasının işləmə vaxtını saniyə ilə qaytarır."""
    start = time.perf_counter()
    action()
    return time.perf_counter() - start


# ---------- Tapşırıq 1: Playlist ----------
def build_playlist(n):
    playlist = Playlist()
    for i in range(1, n + 1):
        playlist.add_song(Song(i, "Mahni" + str(i), "Ifaci" + str(i)))
    return playlist


def playlist_insert(n):
    def run():
        build_playlist(n)
    return timed(run)


def playlist_search(n):
    playlist = build_playlist(n)
    # ən pis hal: ID 1 ilk əlavə olunub, ona görə siyahının sonundadır
    return timed(lambda: playlist.search_song(1))


def playlist_delete(n):
    playlist = build_playlist(n)
    # ən pis hal: ID 1 siyahının sonundadır
    return timed(lambda: playlist.delete_song(1))


# ---------- Tapşırıq 2: Stack ----------
def stack_push(n):
    stack = Stack()
    def run():
        for i in range(n):
            stack.push(Page(i, "https://site" + str(i) + ".az"))
    return timed(run)


def stack_pop(n):
    stack = Stack()
    for i in range(n):
        stack.push(Page(i, "https://site" + str(i) + ".az"))
    def run():
        for _ in range(n):
            stack.pop()
    return timed(run)


# ---------- Tapşırıq 3: Queue ----------
def build_queue(n):
    queue = Queue()
    for i in range(n):
        queue.enqueue(Passenger(i, "Sernisin" + str(i), "AZ" + str(100 + i % 50)))
    return queue


def queue_enqueue(n):
    queue = Queue()
    def run():
        for i in range(n):
            queue.enqueue(Passenger(i, "Sernisin" + str(i), "AZ100"))
    return timed(run)


def queue_dequeue(n):
    queue = build_queue(n)
    def run():
        for _ in range(n):
            queue.dequeue()
    return timed(run)


def queue_peek(n):
    queue = build_queue(n)
    return timed(lambda: queue.peek())


def draw_graph(sizes, data, title, ylabel, filename):
    plt.figure(figsize=(7, 4.5))
    for label, values in data.items():
        plt.plot(sizes, values, marker="o", label=label)
    plt.title(title)
    plt.xlabel("Element sayı")
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS, filename), dpi=150)
    plt.close()


def main():
    results = {"playlist": [], "stack": [], "queue": []}
    for n in SIZES:
        print("Test gedir:", n)
        results["playlist"].append([n,
                                    average_ms(lambda: playlist_insert(n)),
                                    average_ms(lambda: playlist_search(n)),
                                    average_ms(lambda: playlist_delete(n))])
        results["stack"].append([n,
                                 average_ms(lambda: stack_push(n)),
                                 average_ms(lambda: stack_pop(n))])
        results["queue"].append([n,
                                 average_ms(lambda: queue_enqueue(n)),
                                 average_ms(lambda: queue_dequeue(n)),
                                 average_ms(lambda: queue_peek(n))])

    headers = {
        "playlist": ["Element sayi", "Insert (ms)", "Search (ms)", "Delete (ms)"],
        "stack": ["Emeliyyat sayi", "Push (ms)", "Pop (ms)"],
        "queue": ["Element sayi", "Enqueue (ms)", "Dequeue (ms)", "Peek (ms)"],
    }

    # Cədvəlləri ekrana çıxarırıq və CSV fayllara yazırıq
    for name in results:
        print("\n" + name.upper())
        print(" | ".join(headers[name]))
        for row in results[name]:
            print(" | ".join(str(row[0]) if i == 0 else f"{v:.4f}"
                             for i, v in enumerate(row)))
        with open(os.path.join(RESULTS, name + ".csv"), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers[name])
            writer.writerows(results[name])

    # Qrafiklər
    p, s, q = results["playlist"], results["stack"], results["queue"]
    draw_graph(SIZES, {"Insert": [r[1] for r in p],
                       "Search": [r[2] for r in p],
                       "Delete": [r[3] for r in p]},
               "Playlist (Linked List)", "Vaxt (ms)", "playlist_graph.png")
    draw_graph(SIZES, {"Push": [r[1] for r in s],
                       "Pop": [r[2] for r in s]},
               "Browser History (Stack)", "Vaxt (ms)", "stack_graph.png")
    draw_graph(SIZES, {"Enqueue": [r[1] for r in q],
                       "Dequeue": [r[2] for r in q],
                       "Peek": [r[3] for r in q]},
               "Airport Queue", "Vaxt (ms)", "queue_graph.png")
    print("\nHazırdır. Nəticələr test_results qovluğundadır.")


if __name__ == "__main__":
    main()
