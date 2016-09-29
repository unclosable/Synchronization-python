class testClass(object):
    test = "123"

    def __init(self):
        self.test = "213"


if __name__ == "__main__":
    test1 = ("a", "b", "c")
    print(type(test1))
    test2 = (("a", "2"), ("b"), ("c"))
    print(type(test2[0]))
    print(test2[0])
    test3 = ()
    print(type(test3))
    test4 = testClass()
    print(isinstance(test4, str))
