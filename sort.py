import random as rand
import book


##organizes pile, puts as many books in as will fit
def remove(pile, shelf):
    temp_shelf = shelf.content.copy()

    
    ##test##
    quickSort(pile, 0, len(pile)-1)
    for book in pile:
        print(book.name)
    

    temp_pile = []
    for book in pile:
        if book.height < shelf.height and book.width < shelf.max_width-shelf.width:
            temp_shelf.append(book)
            shelf.width += book.width
        else:
            temp_pile.append(book)
    print("Could not fit the following books: ")
    for book in temp_pile:
        print(book.name)
    return temp_shelf



def partition(list, low, high):
    pivot = list[high].name
    #print(type(pivot))
    #print(type(list[1].name))

    i = low - 1

    for j in range(low, high):
        if list[j].name < pivot:
            i+=1
            swap(list, i, j)
    
    swap(list, i+1, high)
    return i+1
    

def swap(list, x, y):
    list[x], list[y] = list[y], list[x]

def quickSort(list, low, high):
    if low < high: 

        pi = partition(list, low, high)

        quickSort(list, low, pi - 1)
        quickSort(list, pi + 1, high)