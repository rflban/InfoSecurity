import sys
from math import ceil


LEFT = '0'
RIGHT = '1'


class Leaf():
    def __init__(self, data, freq):
        self.code = ''
        self.data = data
        self.freq = freq

    def update_code(self, update):
        self.code = update + self.code


class Node():
    def __init__(self, left, right, freq):
        self.code = ''
        self.freq = freq
        self.left = left
        self.right = right

        self.left.update_code(LEFT)
        self.right.update_code(RIGHT)

    def update_code(self, update):
        self.code = update + self.code
        self.left.update_code(update)
        self.right.update_code(update)


def build_tree(freq_table):
    queue = [Leaf(bf[0], bf[1]) for bf in freq_table]

    leaves = []
    while len(queue) > 1:
        left, right = queue[:2]
        queue = queue[2:]

        if type(left) is Leaf:
            leaves.append(left)
        if type(right) is Leaf:
            leaves.append(right)

        node = Node(left, right, left.freq + right.freq)
        queue.append(node)
        queue = sorted(queue, key=lambda node: node.freq)

    return leaves, queue[0]


def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, sys.byteorder)


def compress(all_bytes):
    freq_table = get_freq_table(all_bytes)
    leaves, _ = build_tree(freq_table)

    symbol_map = {leaf.data: leaf.code for leaf in leaves}

    output_bits = '1'
    for b in all_bytes:
        output_bits = output_bits + symbol_map[b]
    output_bytes = bitstring_to_bytes(output_bits)

    max_count_bytes = ceil(leaves[-1].freq.bit_length() / 8)
    header_bytes = len(leaves).to_bytes(2, sys.byteorder)
    header_bytes += max_count_bytes.to_bytes(8, sys.byteorder)

    for leaf in leaves:
        header_bytes += leaf.data.to_bytes(1, sys.byteorder)
        header_bytes += leaf.freq.to_bytes(max_count_bytes, sys.byteorder)

    return header_bytes+output_bytes


def get_freq_table(all_bytes):
    freq_dict = {b: 0 for b in all_bytes}

    for b in all_bytes:
        freq_dict[b] = freq_dict[b] + 1

    return sorted(freq_dict.items(), key=lambda item: item[1])


def extract(input_bytes, freq_table):
    _, tree = build_tree(freq_table)
    input_bits = bin(int.from_bytes(input_bytes, sys.byteorder))[3:]
    output_bytes = b''
    current_node = tree
    for bit in input_bits:
        if bit == LEFT:
            current_node = current_node.left
        else:
            current_node = current_node.right

        if type(current_node) is Leaf:
            output_bytes += current_node.data
            current_node = tree

    return output_bytes


def parse_compressed(input_file):
    freq_table = []

    leaves_count = int.from_bytes(input_file.read(2), sys.byteorder)
    max_count_bytes = int.from_bytes(input_file.read(8), sys.byteorder)

    while leaves_count > 0:
        symbol = input_file.read(1)
        code = int.from_bytes(input_file.read(max_count_bytes), sys.byteorder)
        freq_table.append((symbol, code))
        leaves_count -= 1

    input_bytes = input_file.read()

    return input_bytes, freq_table
