class zStack:
    """Traditional stack implementation"""
    def __init__(self):
        self.arr = []

    # returns the last element in the stack
    def top(self):
        return self.arr[len(self.arr)-1]
    # returns the last element in the stack and removes it
    def pop(self):
        return self.arr.pop()
    # adds an element to the stack
    def push(self, val):
        self.arr.append(val)
    # returns wether the stack is empty or not
    def empty(self):
        return (1 if len(self.arr) else 0)
    # returns the size of the stack
    def size(self):
        return len(self.arr)
    # print the stack
    def print(self):
        print('---')
        for x in range(0, len(self.arr)):
            print('<',x,',',self.arr[x],'>')

class zQueue:
    """Traditional queue implementation"""
    def __init__(self):
        self.arr = []

    # returns the first element in the queue
    def front(self):
        return self.arr[0]
    # returns the first element in the queue and removes it
    def pop(self):
        return self.arr.pop(0)
    # adds an element to the queue
    def push(self, val):
        self.arr.append(val)
    # returns wether the queue is empty or not
    def empty(self):
        return (1 if len(self.arr) else 0)

class zHash:
    """Traditional hash implementation where each bin is a pair, 0 is key 1 is value"""
    def __init__(self, n):
        self.n = n
        self.table = [None] * n

    # hash function, retrieved from https://en.wikibooks.org/wiki/Data_Structures/Hash_Tables
    def _joaat_Hash(self, key):
        hash = 0
        for i in range(0, len(key)):
            hash += ord(key[i])
            hash += (hash << 10)
            hash ^  (hash >> 6)
        hash += (hash << 3)
        hash ^  (hash >> 11)
        hash += (hash << 15)
        return hash

    # function for finding a slot using joaat hash and linear probing
    def _findSlot(self, key):
        i = self._joaat_Hash(key) % self.n
        j = i - 1
        while(self.table[i] and self.table[i][0] != key and j != i):
            i += 1 % self.n
        if(j == i):
            return "Table full"
        return i

    # gets the value on the hash
    def get(self, key):
        i = self._findSlot(key)
        if(not self.table[i]):
            return "Record not found"
        else:
            return self.table[i][1]

    # sets or updates the corresponding key
    def set(self, key, val):
        i = self._findSlot(key)
        if(not self.table[i]):
            #key not in table, adding value
            self.table[i] = [key, val]
            return "Key not found, adding"
        else:
            # key already in table, updating value
            self.table[i][1] = val
            return "Key found, updating"

    # removes a key value pair from the hash
    def remove(self, key):
        i = self._findSlot(key)
        if(not self.table[i]):
            return "Record not found"
        else:
            self.table[i] = None
            return "Erased"

