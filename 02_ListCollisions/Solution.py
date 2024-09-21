'''
Some key observations:
    1) At any time, the i^th box can collide with either the i-1^th or i+1^th box. Similarly, 
    the first and the last box can only collide with boxes on their right and left, respectively.
    2) In between two collisions, the velocities of all the boxes remain the same
    3) From the physics point of view, a reasonable assertion could be that the system's center of mass always 
    has the same velocity since no external force is acting on the system. So the velocities of the boxes can't reach to infinity
'''
class heap_class:
    def __init__(self, num: int) -> None:
        self.heap = [-1] * num
        # position[box_number] = heap_index
        # Required to access other box's time value
        self.position = [-1] * num
        # box_num[heap_index] = box_number
        # Required to know the box number of parent, 
        # to change in position array while swapping
        self.box_num = [-1] * num
        self.length = 0
    
    # Return true of heap value at idx1 < heap value at idx2
    def heap_comparator(self, idx1: int, idx2:int):
        if self.heap[idx1] != self.heap[idx2]:
            return self.heap[idx1] < self.heap[idx2]
        else:
            return idx1 < idx2
    
    # Swapping nodes in Heap 
    def swap_index(self, idx1:int, idx2:int) -> None:
        self.heap[idx1], self.heap[idx2] = self.heap[idx2], self.heap[idx1]
        self.position[self.box_num[idx1]] = idx2
        self.position[self.box_num[idx2]] = idx1
        self.box_num[idx1], self.box_num[idx2] = self.box_num[idx2], self.box_num[idx1]

    # Heapify current node with parent heap i.e. heap above node
    #   - If parent not exist i.e. current node is root node => Done with heapify
    #   - If parent is greater than current node => Swap them and UpHeapify it further else done with heapify
    def heapify(self, curr: int) -> None:
        parent = int((curr-1)/2)
        if parent>=0:
            if self.heap_comparator(curr,parent):
                self.swap_index(parent,curr)
                self.heapify(parent)
    
    # Heapify current node with children heaps i.e. heap below node
    #   - Checked existence of children of current node
    #   - If no child => Heapify done
    #   - Select the smallest child (among existing children)
    #   - If it is smaller than current node => Swap them and DownHeapify it further
    def heapify_down(self, curr:int) -> None:
        left_child = 2*curr+1
        right_child = 2*curr+2
        smaller_child = left_child
        if left_child >= self.length:
            return
        elif right_child >= self.length:
            smaller_child = left_child
        else:
            if self.heap_comparator(right_child,left_child):
                smaller_child = right_child

        if self.heap_comparator(smaller_child,curr):
            self.swap_index(curr, smaller_child)
            self.heapify_down(smaller_child)

    # Inserting node:
    #   - Add new node at last of the heap
    #   - Then do above heapify
    def insert(self, time: int, box_number: int) -> None:
        self.heap[self.length] = time
        self.box_num[self.length] = box_number
        self.position[box_number] = self.length
        self.length += 1
        self.heapify(self.length-1)

    # Deleting node: 
    #   - Replaced node to be deleted with last node in heap
    #   - Delete the last node
    #   - Heapify the node (above and below both) 
    def delete(self, box_number : int) -> None:
        heap_index = self.position[box_number]
        self.swap_index(heap_index,self.length-1)
        self.heap[self.length-1] = -1
        self.box_num[self.length-1] = -1
        self.position[box_number] = -1
        self.length -= 1
        if self.heap[heap_index] != -1:
            self.heapify(heap_index)
            self.heapify_down(heap_index)
    
    # Extract top element of Heap
    def top(self):
        return self.heap[0],self.box_num[0]

max_float = float(10**20)

'''
    Algorithm used:
    1. Intitially find all collision timings between idx and idx+1 boxes using velocity and positions
    2. Put all these timings in MinHeap which is implemented.
    3. Extract top element of Heap which represents next immediate collision
    4. Find final velocities using masses, velocities after collision of those boxes
    5. In heap, Update timings of collision of idx-1 and idx boxes, idx and idx+1, idx+1 and idx+2 boxes
       (Because timings of these three collisions will change because of change in velocities of idx and idx+1 boxes)
    6. To find above timings which are to be updated, we are using object's last collision time and position. 
       - Using object's last collision time and position along with velocity, we can find position at current time
       - And through current position and velocity, we can easily find timings of next respective collisions of boxes
    7. Also, update last collision position and time of just collided boxes.
    
'''

# Returns the time of collision between boxes idx and idx+1 
# This function uses last collision of box to find current position x1,x2
# Then use this x1,x2 to find time for next collision
def time_for_collision(idx:int, velocity, pos_last_col, time_last_col, curr_time)-> float :
    if velocity[idx+1] - velocity[idx] >= 0:
        return max_float
    x1 = pos_last_col[idx] + (curr_time-time_last_col[idx])*velocity[idx]
    x2 = pos_last_col[idx+1] + (curr_time-time_last_col[idx+1])*velocity[idx+1]
    return curr_time+(x2-x1)/(velocity[idx]-velocity[idx+1])

# Returns the position of collision between boxes idx and idx+1
def pos_for_collision(idx:int, velocity, pos_last_col, time_last_col, time_taken_for_col)-> float :
    return pos_last_col[idx] + velocity[idx]*(time_taken_for_col-time_last_col[idx])

# Velocity calculator after collision
def updated_velocity(idx:int, mass, velocity)-> float:
    return (
        ((mass[idx]-mass[idx+1])*velocity[idx] + (2*mass[idx+1]*velocity[idx+1]))/(mass[idx]+mass[idx+1]),
        ((2*mass[idx]*velocity[idx]+(mass[idx+1]-mass[idx])*velocity[idx+1]))/(mass[idx]+mass[idx+1])
    )

# Main function
def listCollisions(M, x, v, m, T):
    
    # Initialization
    num_boxes = len(M)
    
    # Time of last collision of ith box
    time_last_col = [0]*num_boxes
    
    # Position of last collision of ith box
    pos_last_col = x
    
    # Heap Initialization and inserting times of collisions of ith box with (i+1)th box
    time_heap = heap_class(num_boxes-1)
    for i in range(num_boxes-1):
        time_heap.insert(time_for_collision(i,v,pos_last_col,time_last_col,0),i)
    
    counter = 0
    ans = []

    '''
    Some loop invariants:
        1) At any time t, the tim_last_col[i] denotes the time of the last collision of the i^th box. 
        If it hasn't undergone any collision since the beginning, its value will be 0.
        2) At any time t, the value pos_last_col[i] denotes the position of the last collision of the i^th box. If it hasn't undergone
        any collision till now, its value will be its initial position.
        3) At any time t, v[i] is the velocity of the i^th box.
        4) time_heap contains the time instances of the upcoming collisions in a sorted order.
    '''

    while(counter < m):
        counter += 1
        
        # Find boxes that will collide first
        time_taken_for_col, left_box_idx = time_heap.top()

        # Cut-off time
        if(time_taken_for_col>T):
            break

        # Position of collision between boxes idx and idx+1
        position_of_col = pos_for_collision(left_box_idx,v,pos_last_col,time_last_col,time_taken_for_col)

        # Update Time of last collision for collided objects
        time_last_col[left_box_idx] = time_taken_for_col
        time_last_col[left_box_idx+1] = time_taken_for_col

        # Update Position of last collision of collided objects
        pos_last_col[left_box_idx] = position_of_col
        pos_last_col[left_box_idx+1] = position_of_col
        
        #print(time_taken_for_col,left_box_idx,position_of_col)
        ans.append((time_taken_for_col,left_box_idx,position_of_col))
        
        #Updating Velocity after collision
        v[left_box_idx],v[left_box_idx+1] = updated_velocity(left_box_idx,M,v)

        # Update next collision timings for collided objects
        
        ## For Index i
        time_heap.delete(left_box_idx)
        time_heap.insert(max_float,left_box_idx)

        ## For Index i-1
        if left_box_idx-1 >= 0:
            time_heap.delete(left_box_idx-1)
            time_heap.insert(time_for_collision(left_box_idx-1,v,pos_last_col,time_last_col,time_taken_for_col),left_box_idx-1)
        
        ## For Index i+1
        if left_box_idx + 2 < num_boxes:
            time_heap.delete(left_box_idx+1)
            time_heap.insert(time_for_collision(left_box_idx+1,v,pos_last_col,time_last_col,time_taken_for_col),left_box_idx+1)
    return ans
