class PriorityQueue():
    '''Implementation of Priority Queue using Heap.'''

    def __init__(self, data=[]):
        '''Initialise array'''
        self._data = data
        self._index = {}

    def enqueue(self, node):
        '''Enqueue a node'''
        self._data.append(node)
        index = len(self._data)-1
        self._index[node[1]] = index

    def heapUp(self, index):
        '''Position the Node properly in the tree by shifting it upwards'''
        while index != 0 and self._data[index] >= self._data[(index-1)//2]:
            self._index[self._data[index][1]] = (index-1)//2
            self._index[self._data[(index-1)//2][1]] = index
            self._data[(
                index-1)//2], self._data[index] = self._data[index], self._data[(index-1)//2]
            index = (index-1)//2

    def existChild(self, index):
        '''Return number of childs of a given node'''
        l = len(self._data)
        if 2*index+1 < (l-1):
            return 2
        elif 2*index+1 == (l-1):
            return 1
        else:
            return 0

    def extractMax(self):
        '''Dequeue the priority node'''
        node = self._data[0]
        self._index.pop(node[1])
        self._data[0] = self._data[-1]
        self._index[self._data[0][1]] = 0
        self._data.pop()
        index = 0
        self.heapDown(index)
        return node

    def heapDown(self, index):
        '''Position the node properly by shifting it downwards'''
        while self.existChild(index) != 0:
            if self.existChild(index) == 2 and (self._data[index] <= self._data[2*index+1+1] or self._data[index] <= self._data[2*index+1]):
                if self._data[2*index+1] <= self._data[2*index+1+1]:
                    self._index[self._data[index][1]] = 2*index+1+1
                    self._index[self._data[2*index+1+1][1]] = index
                    self._data[2*index+1 +
                               1], self._data[index] = self._data[index], self._data[2*index+1+1]
                    index = 2*index+1+1
                else:
                    self._index[self._data[index][1]] = 2*index+1
                    self._index[self._data[2*index+1][1]] = index
                    self._data[2*index +
                               1], self._data[index] = self._data[index], self._data[2*index+1]
                    index = 2*index+1
            elif self._data[index] <= self._data[2*index+1]:
                self._index[self._data[index][1]] = 2*index+1
                self._index[self._data[2*index+1][1]] = index
                self._data[2*index +
                           1], self._data[index] = self._data[index], self._data[2*index+1]
                index = 2*index+1
            else:
                break

    def changeKey(self, index, node):
        '''Change Node data'''
        x = self._data[index]
        self._data[index] = node
        self._index[node[1]] = index
        if x <= node:
            self.heapUp(index)
        if x >= node:
            self.heapDown(index)

    def buildHeap(self):
        '''Build Heap from an unsorted array'''
        for i in range(len(self._data)//2-1, -1, -1):
            self.heapDown(i)
        for i in range(len(self._data)):
            self._index[self._data[i][1]] = i


def findMaxCapacity(n, l, s, t):
    adj = []
    for _ in range(n):
        adj.append({})
    for i in range(len(l)):
        try:
            adj[l[i][0]][l[i][1]] = max(l[i][2], adj[l[i][0]][l[i][1]])
        except:
            adj[l[i][0]][l[i][1]] = l[i][2]
        try:
            adj[l[i][1]][l[i][0]] = max(l[i][2], adj[l[i][1]][l[i][0]])
        except:
            adj[l[i][1]][l[i][0]] = l[i][2]
    out = f(adj, s, n, t)
    c = out[t][1]
    i = t
    p = []
    while i != s:
        p.append(i)
        i = out[i][2]
    p.append(s)
    return (c, p[::-1])


def f(adj, s, n, t):
    l = []
    for _ in range(n):
        l.append([True, -1, None])
    # not visited, weight, prev
    l[s][0] = False
    l[s][1] = float('inf')
    l[s][2] = s
    q = PriorityQueue()
    q.enqueue((l[s][1], s))
    for i in range(len(l)):
        if i != s:
            q.enqueue((l[i][1], i))
    while len(q._data) != 0:
        p = q.extractMax()
        p = p[1]
        l[p][0] = False
        for i in adj[p]:
            if min(l[p][1], adj[p][i]) > l[i][1]:
                l[i][1] = min(l[p][1], adj[p][i])
                l[i][2] = p
                q.changeKey(q._index[i], (l[i][1], i))
    return l


# print(findMaxCapacity(3, [(0, 1, 1), (1, 2, 1)], 0, 1))
# # (1, [0, 1])
# print(findMaxCapacity(4, [(0, 1, 30), (0, 3, 10), (1, 2, 40),
#                           (2, 3, 50), (0, 1, 60), (1, 3, 50)], 0, 3))
# # (50, [0, 1, 3])
# print(findMaxCapacity(
#     4, [(0, 1, 30), (1, 2, 40), (2, 3, 50), (0, 3, 10)], 0, 3))
# # (30, [0, 1, 2, 3])
# print(findMaxCapacity(5, [(0, 1, 3), (1, 2, 5), (2, 3, 2),
#                           (3, 4, 3), (4, 0, 8), (0, 3, 7), (1, 3, 4)], 0, 2))
# # (4, [0, 3, 1, 2])
# print(findMaxCapacity(7, [(0, 1, 2), (0, 2, 5), (1, 3, 4), (2, 3, 4),
#                           (3, 4, 6), (3, 5, 4), (2, 6, 1), (6, 5, 2)], 0, 5))
# # (4, [0, 2, 3, 5])
# print(findMaxCapacity(8, [(0, 1, 5), (1, 2, 8), (2, 3, 6), (3, 4, 1), (4, 5, 15), (5, 6, 2), (6, 7, 3),
#       (7, 0, 12), (1, 5, 7), (1, 6, 3), (2, 5, 9), (2, 7, 11), (3, 7, 14), (0, 4, 3), (0, 5, 4)], 0, 4))
# # (9, [0, 7,  2, 5, 4])
