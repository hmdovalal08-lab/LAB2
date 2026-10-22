# Tapşırıq 2: Brauzer tarixçəsi (Stack)
# Son açılan səhifə üstdə durur və Back basanda ilk o çıxır (LIFO).
from datetime import datetime


class Page:
    def __init__(self, page_id, url):
        self.page_id = page_id
        self.url = url
        self.visit_time = datetime.now().strftime("%H:%M:%S")
        self.next = None          # altındakı səhifə


class Stack:
    def __init__(self):
        self.top = None           # ən üstdəki səhifə
        self.size = 0

    def push(self, page):
        page.next = self.top      # yeni səhifə üstə qoyulur
        self.top = page
        self.size += 1

    def pop(self):
        if self.top is None:
            return None
        page = self.top
        self.top = page.next      # üstdəkini çıxarırıq
        self.size -= 1
        return page

    def peek(self):
        return self.top


def menu():
    stack = Stack()
    next_id = 1
    while True:
        print("\n1. Visit Page")
        print("2. Back")
        print("3. Current Page")
        print("4. Display History")
        print("0. Exit")
        choice = input("Seçim: ")

        if choice == "1":
            stack.push(Page(next_id, input("URL: ")))
            next_id += 1
        elif choice == "2":
            if stack.size > 1:
                stack.pop()
                print("Geri qayıdıldı:", stack.peek().url)
            else:
                print("Geri qayıtmaq olmur.")
        elif choice == "3":
            page = stack.peek()
            print(page.url if page else "Səhifə yoxdur.")
        elif choice == "4":
            current = stack.top
            while current is not None:
                print(current.page_id, current.url, current.visit_time)
                current = current.next
        elif choice == "0":
            break


if __name__ == "__main__":
    menu()
