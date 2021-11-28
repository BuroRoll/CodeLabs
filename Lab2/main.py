from flask import Flask, request, jsonify, abort, send_file
from flask import render_template
from LZW import LZW
from Huffman import HuffmanCode

app = Flask("Архиватор")
UPLOAD_FOLDER = '/files'
HC = HuffmanCode()


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/compress", methods=['POST'])
def compress():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save("./files/" + uploaded_file.filename)
        compressed_data, uncompressed_size, compressed_size = compress_file("./files/" + uploaded_file.filename)
    return jsonify(
        compressed_data=compressed_data,
        uncompressed_size=uncompressed_size,
        compressed_size=compressed_size
    )


@app.route("/decompress", methods=['POST'])
def decompress():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save("./files/" + uploaded_file.filename)
        decompressed_data = decompress_file("./files/" + uploaded_file.filename)
    return jsonify(decompressed_data=decompressed_data)


@app.route("/get_file", methods=['POST'])
def get_file():
    file = request.args.get('file', type=str)
    try:
        return send_file('./' + file, download_name=file, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@app.route("/compressHuffman", methods=['POST'])
def compressHuffmane():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save("./files/" + uploaded_file.filename)
        compressed_data, uncompressed_size, compressed_size = compress_Huffman_file("./files/" + uploaded_file.filename)
    return jsonify(
        compressed_data=compressed_data,
        uncompressed_size=uncompressed_size,
        compressed_size=compressed_size
    )


@app.route("/decompressHuffman", methods=['POST'])
def decompressHuffmane():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save("./files/" + uploaded_file.filename)
        decompressed_data = decompress_Huffman_file("./files/" + uploaded_file.filename)
    return jsonify(decompressed_data=decompressed_data)


def compress_file(filename):
    lzw = LZW()
    with open(filename, "rb+") as f:
        lines = f.readlines()
        lines = list(map(lambda x: x.decode("utf-8"), lines))
        lines = ''.join(str(e) for e in lines)
        compressed = lzw.compress(lines)
    stat1, stat2 = lzw.stat_data()
    return compressed, stat1, stat2


def compress_Huffman_file(filename):
    with open(filename, "rb+") as f:
        lines = f.readlines()
        lines = list(map(lambda x: x.decode("utf-8"), lines))
        lines = ''.join(str(e) for e in lines)
        compressed, stat1, stat2 = HC.compress(lines)
    return compressed, stat1, stat2


def decompress_Huffman_file(filename):
    with open(filename, "rb+") as f:
        lines = f.readlines()
        lines = list(map(lambda x: x.decode("utf-8"), lines))
        lines = ''.join(str(e) for e in lines).replace(",", "").split(" ")
        decompressed = HC.decompress(lines)
    return decompressed


def decompress_file(filename):
    lzw = LZW()
    with open(filename, "rb+") as f:
        lines = f.readlines()
        lines = list(map(lambda x: x.decode("utf-8"), lines))
        lines = ''.join(str(e) for e in lines).replace(",", "").split(" ")
        decompressed = lzw.decompress(lines)
    return decompressed


if __name__ == '__main__':
    app.run()
