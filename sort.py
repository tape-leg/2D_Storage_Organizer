import random as rand
import book


##organizes pile, puts as many books in as will fit
def remove(pile, case):
    
    ##test##
    
    quickSort(pile, 0, len(pile)-1, "height")
    
    
    print("***TESTING***")
    for book in pile:
        print(book.name)
    print("***END TESTING***")
    
    #print(type(case))
    
    quickSort(case, 0, len(case)-1, "height")

    #for shelf in case:
    #    print(shelf.height)

    temp_pile = []
    
    for book in reversed(pile):
        #print(f"{book} {type(book)}")
        inShelf = False
        for shelf in case:
            #print(f"{shelf} {type(shelf)}")
            if book.height > shelf.height:
                #print(f"{book.name} is too big for {shelf.name}")
                continue
            elif book.width > shelf.max_width - shelf.width:
                #print(f"{shelf.name} is too full for {book.name}")
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
    
    """
    
    for book in pile:
        if book.height < shelf.height and book.width < shelf.max_width-shelf.width:
            temp_shelf.append(book)
            shelf.width += book.width
        else:
            temp_pile.append(book)
    """
    print("Could not fit the following books: ")
    
    
    for book in temp_pile:
        print(book.name)
    



def partition_name(list, low, high):
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

def partition_height(list, low, high):
    pivot = list[high].height
    #print(type(pivot))
    #print(type(list[1].name))

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