class Book:
    def __init__(self, name, height, width):
        self.name = name
        self.height = height
        self.width = width
   
    def display_info(self):
        print("Book Name:", self.name)
        print("Book Height:",self.height,"cm")
        print("Book Width:",self.width,"cm")
     
input_name = str(input("Enter book's name: "))
input_height = float(input("Enter book's height: "))
input_width = float(input("Enter book's width: "))


my_book = Book(input_name, input_height, input_width)


my_book.display_info()