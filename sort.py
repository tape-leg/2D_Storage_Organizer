import random as rand
import book
import Book_size as bs


##organizes pile, puts as many books in as will fit
def remove(pile, case):
    
    
    quickSort(pile, 0, len(pile)-1, "height") # initial sort of books by height
    
    
    quickSort(case, 0, len(case)-1, "height") # initial sort of shelves by height


    temp_pile = []
    
    for book in reversed(pile):
        
        inShelf = False
        
        for shelf in case:
            
            if book.height > shelf.height:
                print(f"{book.name} is too big for {shelf.name}")
                continue
            elif book.width > shelf.max_width - shelf.width:
                print(f"{shelf.name} is too full for {book.name}")
                continue
            else:
                shelf.content.append(book)
                #print(shelf.content)
                shelf.width += book.width
                inShelf = True
                break
        if inShelf:
            continue
        else:
            temp_pile.append(book)
    
    for shelf in case:
        quickSort(shelf.content, 0, len(shelf.content)-1, "alpha")
    
    print("Could not fit the following books: ")
    
    
    for book in temp_pile:
        print(book.name)
    



def partition_name(list, low, high): # sorts alphabetically
    pivot = list[high].name

    i = low - 1

    for j in range(low, high):
        if list[j].name < pivot:
            i+=1
            swap(list, i, j)
    
    swap(list, i+1, high)
    return i+1

def partition_height(list, low, high): # sorts by height
    pivot = list[high].height

    i = low - 1

    for j in range(low, high):
        if list[j].height < pivot:
            i+=1
            swap(list, i, j)
    
    swap(list, i+1, high)
    return i+1
    

def swap(list, x, y):
    list[x], list[y] = list[y], list[x]

def quickSort(list, low, high, method):
    if low < high: 

        if method == "alpha":
            pi = partition_name(list, low, high)
        elif method == "height":
            pi = partition_height(list, low, high)

        quickSort(list, low, pi - 1, method)
        quickSort(list, pi + 1, high, method)


## TEST CASE ##
"""
shelf1 = book.Shelf("Shelf one", 2, 0, 3, [])

case1 = [shelf1]

remove(bs.process_image_and_get_books_list("books.jpg"), case1)
for book in shelf1.content:
    print(f"{book.width} x {book.height}")

"""