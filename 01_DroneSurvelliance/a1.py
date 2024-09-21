class LinkedStack:
    ''' LIFO Stack implementation using a singly linked list for storage'''

    # --------------------------- nested _Node Class ------------------------
    class _Node:
        ''' Lightweight, nonpublic class for storing a singly linked node'''
        __slots__ = ['_element', '_next']        # streamline memory usage

        def __init__(self, element, next):       # Initialize node's field
            self._element = element                # reference to user's element
            self._next = next                      # reference to next node

    # -------------------Stack Methods ------------------------------------------

    def __init__(self):
        ''' Create an empty stack'''
        self._head = None         # reference to the head node
        self._size = 0

    def __len__(self):
        ''' return the number of elements in the stack'''
        return self._size

    def push(self, e):
        '''Add elements e to the top of the stack'''
        self._head = self._Node(e, self._head)  # create and link a new node
        self._size += 1

    def pop(self):
        '''
        Remove and return the element from the top of the stack
        Raise Empty exception if the stack is empty
        '''
        answer = self._head._element
        self._head = self._head._next   # Bypass the current node
        self._size -= 1
        return answer


def findPositionandDistance(P):
    multiplierStack = LinkedStack()  # create stack to store integers as we parse them
    multiplierStack.push(1)  # Initial multiplier is 1
    multiplier = 1  # Use this variable to store current multiplier
    i = 0       # Store current location of character we are parsing
    oldi = 0    # Stores starting position in case of integers/multipliers
    count = {"X": 0, "Y": 0, "Z": 0, "D": 0}

    '''We use the fact that values -5 to 256 are preallocated in python. So, storing/working with
    them is faster than any other value because we save some time and memory required to create that object.
    Thus, I use a we dummy dictionary to store the count of the string between () and then as soon as
    we are out of the brackets, I multiply the count by multiplier and add to the res dictionary.
    
    Since the count dictionary has additions/subtractions of 1 only, pretty high chance that we stay in 
    the range of -5 to 256, thus saving a lot of time. I checked with random long 100 generated testcases and 
    found that time was almost halved, from 55s to 25s.
    
    This happens only in python so this is a dirty hack to make my program faster in python.'''

    res = {"X": 0, "Y": 0, "Z": 0, "D": 0}      # final result dictionary

    '''Main working code'''

    while i < len(P):       # while loop to parse the whole string character by character
        if P[i] == "+":

            '''Checked if the current character is + then proceed to add +1 to count dictionary
            for the respective coordinate and distance, which can be known by accessing the i+1th character.'''

            count[P[i+1]] += 1
            count["D"] += 1
            i += 1          # the next character, which defines the coordinate is already parsed so skip it

        elif P[i] == "-":

            '''Checked if the current character is + then proceed to add -1 to count dictionary for the 
            respective coordinate and +1 for distance, which can be known by accessing the i+1th character.'''

            count[P[i+1]] -= 1
            count["D"] += 1
            i += 1      # the next character, which defines the coordinate is already parsed so skip it

        elif P[i] == ")":

            '''When I encounter a close bracket, its time to change my multiplier (divide by the integer
            which preceded this pair of brackets). Also, its time to update the count dictionary, and
            add the old values into result dictionary my multiplying with the multiplier.'''

            for q in count:  # updating result dictionary
                res[q] += count[q]*multiplier
            # set count dictionary to default
            count = {"X": 0, "Y": 0, "Z": 0, "D": 0}
            multiplier = multiplier//multiplierStack.pop()      # updating multiplier

        else:

            '''The only case left is that the current character is a digit. We will parse the opening bracket
            here itself and every opening bracket is preceded by an integer so we need not worry about that
            case. The simple logic is to store the starting index of the digit and iterate the characters until
            we find the (. We stop when we find ( and then simply change our multiplier accordingly and even
            update the multiplier stack. 

            We also update the result and count dictionaries as the multiplier changes at this point.'''

            oldi = i
            while P[i] != "(":  # loop to find end index of the integer
                i += 1
            t = P[oldi:i]
            multiplierStack.push(int(t))  # update multiplier stack
            for q in count:  # update result dictionary
                res[q] += count[q]*multiplier
            multiplier *= int(t)
            count = {"X": 0, "Y": 0, "Z": 0, "D": 0}
        i += 1  # proceed to parse next character in the string

    for q in count:  # after the parsing of whole string is done, update the result dictionary using the
        # count dictionary just in case some updates are left
        res[q] += count[q]*multiplier
    # return the answer as a list
    return [res["X"], res["Y"], res["Z"], res["D"]]
