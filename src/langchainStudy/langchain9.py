class RunableChain():
    def __init__(self):
        self.sequence = []
    
    def run(self):
        for item in self.sequence:
            print(item)
    
    def __or__(self, other):
        return Chain(self, other)

class BaseTest(RunableChain):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.sequence.append(self)
    
    def __or__(self, other):
        return Chain(self, other)

class Test(BaseTest):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self.name

class Test2(BaseTest):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self.name + "test2"

class Chain(RunableChain):
    def __init__(self, first, second):
        super().__init__()
        # 展开第一个对象的序列
        if hasattr(first, 'sequence'):
            self.sequence.extend(first.sequence)
        else:
            self.sequence.append(first)
            
        # 展开第二个对象的序列
        if hasattr(second, 'sequence'):
            self.sequence.extend(second.sequence)
        else:
            self.sequence.append(second)

if __name__ == "__main__":
    a = Test("A")
    b = Test2("B")
    c = Test("C")
    d = Test2("D")
    chain = a | b | c | d
    chain.run()