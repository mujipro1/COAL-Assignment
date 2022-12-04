class Queue:
    array = ["","","",""]
    size = 0

    def enqueue(self, a):
        for i in range(len(self.array)):
            if (self.array[i] == ""):
                self.array[i] = a
                self.size += 1
                break
        else:
            self.array.append(a)
        self.execute()

    def dequeue(self):
        self.size -= 1   
        if(self.array[0] != ''):
            self.array[0] = ''
        else:
            for i in range(len(self.array)):
                if not(self.array[i] == ''):
                    self.array[i] = ''
            
    
    def execute(self):
        if('' in self.array):
            for i in range(len(self.array)):
                if (self.array[i] != ""):
                    return self.array[i]
        else:
            return self.array[0]
            
