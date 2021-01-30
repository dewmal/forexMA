import queue


class PriceActionPatternAnalyser:

    def __init__(self, max_buffer_length=10):
        self.max_buffer_length = max_buffer_length
        self.__buffer = queue.Queue(maxsize=self.max_buffer_length)

    def pattern(self, data):
        self.__buffer.put(data)
        if self.__buffer.qsize() >= self.max_buffer_length:
            self.__buffer.get()
