from collections import Counter
from io import StringIO


class Node(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def walk(self, data, code):
        self.right.walk(data, code + '0')
        self.left.walk(data, code + '1')


class Item(object):
    def __init__(self, item):
        self.item = item

    def walk(self, data, code):
        data[self.item] = code


class HuffmanCode(object):
    def __init__(self):
        self.codeTree = {}
        self.uncompressed_size = 0
        self.compressed_size = 0

    def compress(self, uncompressed_data):
        counter = Counter(uncompressed_data)
        for i, e in counter.items():
            self.uncompressed_size += e * 8
        h = [(freq, Item(ch)) for ch, freq in counter.items()]
        h.sort(key=lambda x: x[0], reverse=True)
        while len(h) > 1:
            f1, item1 = h.pop()
            f2, item2 = h.pop()
            h.append((f1 + f2, Node(item1, item2)))
            h = sorted(h, key=lambda x: x[0], reverse=True)
        h[0][1].walk(self.codeTree, '')
        result = []
        for i in uncompressed_data:
            result.append(self.codeTree[i])
        for i, j in counter.items():
            self.compressed_size += j * len(self.codeTree[i])
        print(self.codeTree.items())
        with open('compressed.txt', 'w') as f:
            f.write(' '.join(e for e in result))
        return result, self.uncompressed_size, self.compressed_size

    def decompress(self, compressed_data):
        result = StringIO()
        inv_code_tree = {v: k for k, v in self.codeTree.items()}
        for e in compressed_data:
            result.write(inv_code_tree[e])
        result = result.getvalue()
        with open('decompressed.txt', "w") as f:
            f.write(result)
        return result
