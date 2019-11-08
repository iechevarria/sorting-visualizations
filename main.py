list_to_sort = [1, 3, 4, 5, 1, 3, 2, 5]


# data
class knowledge_arr():
    def __init__(self, arr):
        self.arr = arr
        self.looking_idxs = set()
        self.length = len(arr)


    def get(self, idx):
        self.looking_idxs.add(idx)
        return self.arr[idx]


    def gt(self, idx1, idx2):
        return self.get(idx1) > self.get(idx2)


    def reset(self):
        self.looking_idxs = set()

    
    def swap(self, idx1, idx2):
        self.looking_idxs.add(idx1)
        self.looking_idxs.add(idx2)
        tmp = self.arr[idx1]
        self.arr[idx1] = self.arr[idx2]
        self.arr[idx2] = tmp



# display stuff
def underline_all_chars(str_):
    ret = ''
    for char in str_:
        ret += '\u0332' + char 

    return ret


def print_annoted_arr(k_arr):
    print(
        ' ' + ' '.join([
            underline_all_chars(str(t)) if idx in k_arr.looking_idxs else str(t)
            for idx, t in enumerate(k_arr.arr)
        ])
    )



# sorting
def sort_thing(thing):
    i = 1

    while i < thing.length:
        thing.reset()
        j = i
        while j > 0 and thing.gt(j - 1, j):
            print_annoted_arr(thing)
            thing.reset()

            thing.swap(j, j-1)
            j -= 1

            print_annoted_arr(thing)
            thing.reset()

        i += 1    
        print_annoted_arr(thing)



if __name__=='__main__':
    sort_thing(knowledge_arr(list_to_sort))