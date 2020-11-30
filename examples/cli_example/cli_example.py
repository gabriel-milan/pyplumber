import logging
from pyplumber import Task, Plumber


def setup1():
    class Printer(Task):
        def __init__(self, max_loops, *args, **kwargs):
            super(Printer, self).__init__(*args, **kwargs)
            self.__maxLoops = max_loops
            self.__loopCounter = 0

        def execute(self):
            data = int(self.get("test"))
            self.plumber.logger.info("Test data is {}".format(data))
            self.__loopCounter += 1
            if self.__loopCounter >= self.__maxLoops:
                self.terminate()
            return data

    class Incrementer(Task):
        def setup(self):
            self._dict["delay"] = 1
            self._dict["data"] = 0

        def execute(self):
            data = int(self.get("test"))
            self.set("test", data + 1)

    class Starter(Task):
        def setup(self):
            self.set("test", 0)

    plumber = Plumber()

    start = plumber.add(Starter)
    inc = plumber.add(Incrementer, dependencies=[start])
    plumber.add(Printer, args=(50,), dependencies=[inc], output=True)

    return plumber


def run_example():
    plumber = setup1()
    plumber.setup()
    plumber.start()
    for _ in plumber.loop():
        pass


if __name__ == "__main__":
    run_example()