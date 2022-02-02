
class diff_group:
    def __init__(self):
        self.substractions = [] # only accepts strings starting with -
        self.additions = [] # only accepts strings starting with +

        # self.diff_group = ([],[])  #  first list consists of -, second of +
        
    def subs_exist(self):
        return len(self.substractions) != 0

    def adds_exist(self):
        return len(self.additions) != 0

    def subs_count(self):
        return len(self.substractions)

    def adds_count(self):
        return len(self.additions)

    def add_item(self, item):
        if not isinstance(item, str):
            print('Only strings are allowed!')
            return False

        if item[0] == '-':
            if len(item) == 1:
                self.substractions.append('\n')
            else:
                self.substractions.append(item[1:]) # add text row to substractions without the first char for easier pasting
            return True

        elif item[0] == '+':
            if len(item) == 1:
                self.additions.append('\n')
            else:
                self.additions.append(item[1:]) # add text row to additions without the first char for easier pasting
            return True

        else:
            # print('Only strings begining with + or - are allowed!')
            return False

    def clear(self):
        self.clear_subs()
        self.clear_adds()

    def clear_subs(self):
        self.substractions = []

    def clear_adds(self):
        self.additions = []
        
    def print(self):
        print('--------------------')
        print('Substractions:')
        for sub in self.substractions:
            print('-' + sub)
        # print(self.substractions)
        print('--------------------')
        print('Additions:')
        for add in self.additions:
            print('+' + add)
        # print(self.additions)
        print('--------------------')


