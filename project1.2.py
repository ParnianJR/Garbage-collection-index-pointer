class Stack:
    def __init__(self):
        self.stacky = []
    def isEmpty(self):
        return len(self.stacky) == 0
    def push(self,e):
        self.stacky.append(e)
    def pop(self):
        return self.stacky.pop()
class generalList:
    def Memory(self,maxi = 100):
        self.max = maxi
        self.Edl = self.max * [None] # element or down link
        self.link = self.max * [None]
        self.mark = self.max * [0]
        self.headsList= []
    def __init__(self,maxi = 100):
        self.Memory(maxi)
        self.avail = 0
        for i in range(len(self.link)):
            self.link[i] = i+1
        self.link[len(self.link)-1] = None
    def allocate(self):
        if self.avail is None:
            self.normal_garbageCollection()
        if self.avail is None:
            raise Exception("out of memory")
        x = self.avail
        self.avail = self.link[self.avail]
        self.link[x] = self.Edl[x] = None
        self.mark[x] = 0
        return x
    def create(self,ind,stri):
        if stri[ind] != '(':
            raise Exception('invalid expression')
        else:
            E = self.allocate()
            p = E
            ind += 1
            while ind < len(stri) and stri[ind] != ')':
                if stri[ind] == '*':
                    self.link[p] = self.allocate()
                    p = self.link[p]
                    self.Edl[p] = '*'
                    ind += 1
                elif stri[ind] == '(':
                    self.link[p] = self.allocate()
                    p = self.link[p]
                    self.Edl[p], ind = self.create(ind,stri)
            ind += 1
            ad = self.link[E]
            self.add_to_avail(E)
            return ad,ind
    def create_list(self,stri):
        ind = 0
        newHead, ind= self.create(ind,stri)
        self.headsList.append(newHead)      
    def printList(self,head):
        stack = Stack()
        print('(',end=' ')
        i = 0
        p = head
        while 1:
            if p is None:
                print(')',end=' ')
                if stack.isEmpty():
                    break
                p = stack.pop()
                p = self.link[p]
            elif self.Edl[p] != '*':
                print('(',end=' ')
                stack.push(p)
                p = self.Edl[p]
            elif self.Edl[p] == '*':
                print('*',end=' ')
                p = self.link[p]
            i += 1
        #print(')')
    def print_general_list(self,lis_num):
        self.printList(self.headsList[lis_num-1])
        print('')
    def Marking(self,head):
        stack = Stack()
        p = head
        while 1 :
            if p is None:
                if stack.isEmpty():
                    break
                p = stack.pop()
                p = self.link[p]
            elif self.Edl[p] != '*':
                self.mark[p] = 1
                stack.push(p)
                p = self.Edl[p]
            elif self.Edl[p] == '*':
                self.mark[p] = 1
                p = self.link[p]
    def add_to_avail(self,x):
        self.link[x] = self.avail
        self.avail = x
    def normal_garbageCollection(self):
        for i in self.headsList :
            self.Marking(i)
        self.avail = None
        for i in range(len(self.mark)):
            if self.mark[i] == 0:
                self.add_to_avail(i)
            else:
                self.mark[i] = 0
    def Delete(self,lis_num,node_id):
        p = self.find_node_expr(lis_num,node_id)
        self.Edl[p] = '*' #remove p dlink and create garbage
    def find_node_expr(self,li_num,node_id):
        lis = node_id.split('.')
        for i in range(len(lis)):
          lis[i] = int(lis[i])
        p = self.headsList[li_num-1]
        for i in range(len(lis)):
            for j in range(lis[i]-1):
                p = self.link[p]
            if i+1 < len(lis):
                p = self.Edl[p]
        return p
    def add_child(self,lis1_num,lis2_num,node_id):
        p = self.find_node_expr(lis2_num,node_id)
        if self.Edl[p] == '*':
            self.Edl[p] = self.headsList[(lis1_num)-1]
        else:
            print('ERROR! node_expr has dlink')
    def num_of_free_nodes(self):
        if self.avail is None:
            return 0
        count = 0
        g = self.avail
        while g is not None:
            g = self.link[g]
            count += 1
        return count
    def find_num(self,st):
        num = st.replace('L','')
        num = int(num)
        return num
g1 = generalList()
f = open("testcase.txt","r")
while True:
    line = f.readline()
    if line == '':
        break
    line = line.replace('\n','')
    data = line.split(' ')
    if data[0] == 'Garbage_Collection': #fifth command
        n1 = g1.num_of_free_nodes()
        print('the number of nodes in avail list before GC : ',n1)
        g1.normal_garbageCollection()
        n2 = g1.num_of_free_nodes()
        print('the number of nodes in avail list after GC : ',n2)
        print('number of returned nodes to avail list using GC : ',n2-n1)
    elif data[1] == '=': #first command
        g1.create_list(data[-1])
    elif data[0] == 'Make': # second command
        lis1 = g1.find_num(data[1])
        lis2 = g1.find_num(data[4])
        g1.add_child(lis1,lis2,data[-1])
    elif data[0] == 'Delete': #third command
        lis1 = g1.find_num(data[1])
        g1.Delete(lis1,data[-1])
    elif data[0] == 'Print': #forth command
        liNum = g1.find_num(data[-1])
        g1.print_general_list(liNum)