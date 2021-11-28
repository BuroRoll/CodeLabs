from io import StringIO


class LZW:
    def __init__(self):
        self.bit_size = 8
        self.dict_size = 256

        self.uncompressed_size = 0
        self.compressed_size = 0

    def decimal_to_binary(self, n, dict_size):
        if 2 ** self.bit_size < dict_size:
            self.bit_size += 1
        binary = bin(n)
        # binary = binary.replace("0b", "").zfill(self.bit_size)
        return binary

    def compress(self, uncompressed_data):
        dictionary = {chr(i): i for i in range(self.dict_size)}
        dictionary[''] = 0
        w = ""
        compressed_data = []
        for d in uncompressed_data:
            self.uncompressed_size += 8
            wd = w + d
            if wd in dictionary:
                w = wd
            else:
                compressed_data.append(self.decimal_to_binary(dictionary[w], self.dict_size))
                dictionary[wd] = self.dict_size
                self.dict_size += 1
                w = d
        if w:
            compressed_data.append(self.decimal_to_binary(dictionary[w], self.dict_size))
        with open('compressed.txt', 'w') as f:
            f.write(' '.join(str(e) for e in compressed_data))
        self.compressed_size = sum(list(map(lambda x: len(x), compressed_data)))
        self.stat_data()

        return compressed_data

    def decompress(self, compressed_data):
        dict_size = 256
        dictionary = {i: chr(i) for i in range(dict_size)}
        result = StringIO()
        w = dictionary[int(compressed_data.pop(0), 2)]
        result.write(w)
        for k in compressed_data:
            k = int(k, 2)
            if k in dictionary:
                entry = dictionary[k]
            result.write(entry)

            dictionary[dict_size] = w + entry[0]
            dict_size += 1

            w = entry
        result = result.getvalue()
        with open('decompressed.txt', "w") as f:
            f.write(result)
        return result

    def stat_data(self):
        return self.uncompressed_size, self.compressed_size
