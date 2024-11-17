import book as bk
import sort as st 
import Book_size as bs
import random as rnd


shelf1 = bk.Shelf("Shelf 1", rnd.randint(10,25),0,rnd.randrange(10,20),[])
shelf2 = bk.Shelf("Shelf 2", rnd.randint(10,25),0,rnd.randrange(10,20),[])
shelf3 = bk.Shelf("Shelf 3", rnd.randint(10,25),0,rnd.randrange(10,20),[])
shelf4 = bk.Shelf("Shelf 4", rnd.randint(10,25),0,rnd.randrange(10,20),[])

bookCase = [shelf1,shelf2,shelf3,shelf4]

books_pile = bs.process_image_and_get_books_list("books2.jpg")
books_pile1 = bs.process_image_and_get_books_list("books.jpg")

file1 = open("book_list.txt", "r")

for book in books_pile:
    book.name = file1.readline()
for book in books_pile1:
    book.name = file1.readline()

file1.close()

st.remove(books_pile,bookCase)
st.remove(books_pile1,bookCase)
bs.cv2.waitKey(0)
bs.cv2.destroyAllWindows()

for shelf in bookCase:
    with open(f"{shelf.name}.txt", 'w') as txt:
        txt.write(f"Books listed in shelf \'{shelf.name}\' with width {shelf.width}cm: ")
        for book in shelf.content:
            txt.write(book.name)
