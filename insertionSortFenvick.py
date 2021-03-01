'''
calculate the number of shifts an insertion sort performs when sorting an array?
Number of shifts for arr[i] is equal to the count of elements in arr[0..i-1] whose value is greater than arr[i], which can be calculated with BIT efficiently

So What we do?
1. Create a node Class node element will store a value of array and its positions also information that node is array element or query element,

2. Create Frenvick Tree and fill it with zeros, this structure will store information about number of elements before some index

3. array of nodes will store node with value of array and nodes with value of querries for egzample query node will store number of array and info that this is query not number

4. sort array of nodes by values ( if value of array is equal to value of query, query node will go first)

exzample of array of nodes;
                                        numbers of arr      querries (how many items is greather that number from arr[i+1] to arr[n-1])
node original position of number:   [1,   2,  3,  4,  5] + [2,  3,  4,  5]
value of number in array:           [2,   1,  3,  1,  2] + [1,  3,  1,  2]
is node query?:                    [f,   f,  f,  f,  f] + [t,  t,  t,  t]   f means false and t true, I made it short for visual aspects

5. We made one array of nodes and sort it with descending order (look point 4)
So our node array looks like this:

node original position of number:   [3, 3, 5, 1, 5, 2, 4, 2, 4] 
value of number in array:           [3, 3, 2, 2, 2, 1, 1, 1, 1] 
is node query?:                    [t, f, t, f, f, t, t, f, f]    f means false and t true, I made it short for visual aspects

6. We update the Fenvick Tree with 1 (ones) with finding node that is no query, we get sum from Fenvick Tree then node is query; finding number of elements that is greater from value in query (whitch is numbers in arr[i+1] to arr[n-1]) from begin to given index(positon). 
In Fenvick Tree we will use 1 to n indexing so zero index will be left as dummy.

7. At last we sum result of all querries and return it.

'''

class node:
    def __init__(self) -> None:
        self.value = 0
        self.original_position = 0
        self.query_index = 0
        self.is_query = False
        self.query_priority = 0


def update(BIT: list, n: int, idx: int):
    while idx <= n:
        BIT[idx] += 1
        idx += idx & -idx

# Returns the count of numbers of elements
# present from starting till idx.


def query(BIT: list, idx: int) -> int:
    ans = 0
    while idx:
        ans += BIT[idx]
        idx -= idx & -idx
    return ans


def insertionSort(arr: list) -> int:
    n = len(arr)
    arr = arr + arr[1:]
    node_arr = [0 for k in range(n + n - 1 + 1)]

    for i in range(2*n):
        node_arr[i] = node()

    # fill node array with proper nodes, nodes(values) and nodes(querres)

    # nodes for values from array
    for i in range(1, n+1):
        node_arr[i].value = arr[i-1]
        node_arr[i].original_position = i
        node_arr[i].is_query = False

    # node for querries
    for i in range(n+1, 2*n):
        node_arr[i].value = arr[i-1]
        node_arr[i].query_index = i - n + 1
        node_arr[i].is_query = True
        # set higher priority for query so query nodes will be firs even if values of arr are the same
        node_arr[i].query_priority = 100

    # sorting node array in descending order by values starting from 1 (0 node is not used since we use 1 do n indexing)

    node_arr = [node_arr[0]] + \
        sorted(node_arr[1:], key=lambda k: (
            k.value, k.query_priority), reverse=True)

    # making empty (filled with 0) Binary Indexed Tree - BIT
    Bit = [0 for k in range(n+1)]

    no_of_shifts = 0

    # iterate throu node array and sum all shifts
    for i in range(1, 2*n):
        if(node_arr[i].is_query):
            no_of_shifts += query(Bit, node_arr[i].query_index)
        else:
            update(Bit, n, node_arr[i].original_position)

    return no_of_shifts


# Driver code
if __name__ == "__main__":
    # should be 4 shifts of Insertion Sort algorithm to sort this array
    arr1 = [2, 1, 3, 1, 2]
    arr2 = [5, 4, 3, 2, 1]  # should be 10 shifts

    shifts = insertionSort(arr2)
    print("Number of shifts ",shifts)
