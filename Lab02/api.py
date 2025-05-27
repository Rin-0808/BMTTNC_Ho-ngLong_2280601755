from flask import Flask, request, jsonify
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.Playfair import PlayFairCipher


app = Flask(__name__)

#PlayFair
# Khởi tạo đối tượng PlayFairCipher
playfair_cipher = PlayFairCipher()

# API endpoint để tạo ma trận Playfair
@app.route('/api/playfair/creatematrix', methods=['POST'])
def playfair_creatematrix():
    # Lấy dữ liệu từ request JSON
    data = request.json
    key = data['key']
    
    # Tạo ma trận Playfair
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    
    # Trả về kết quả dưới dạng JSON
    return jsonify({'playfair_matrix': playfair_matrix})  # Sửa từ [] thành {}

# API endpoint để mã hóa văn bản bằng Playfair
@app.route('/api/playfair/encrypt', methods=['POST'])
def playfair_encrypt():
    # Lấy dữ liệu từ request JSON
    data = request.json
    plain_text = data['plain_text']
    key = data['key']
    
    # Tạo ma trận và mã hóa
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    encrypted_text = playfair_cipher.playfair_encrypt(plain_text, playfair_matrix)
    
    # Trả về kết quả dưới dạng JSON
    return jsonify({'encrypted_text': encrypted_text})  # Sửa từ [] thành {}

# API endpoint để giải mã văn bản bằng Playfair
@app.route('/api/playfair/decrypt', methods=['POST'])
def playfair_decrypt():
    # Lấy dữ liệu từ request JSON
    data = request.json
    cipher_text = data['cipher_text']
    key = data['key']
    
    # Tạo ma trận và giải mã
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    decrypted_text = playfair_cipher.playfair_decrypt(cipher_text, playfair_matrix)
    
    # Trả về kết quả dưới dạng JSON
    return jsonify({'decrypted_text': decrypted_text})  # Sửa từ [] thành {}


#RailFence
railfence_cipher = RailFenceCipher()

@app.route('/api/railfence/encrypt', methods=['POST'])
def railfence_encrypt():
    # Lấy dữ liệu từ request JSON
    data = request.json
    plain_text = data['plain_text']
    key = int(data['key']) 
    
    encrypted_text = railfence_cipher.rail_fence_encrypt(plain_text, key)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/railfence/decrypt', methods=['POST'])
def railfence_decrypt():
    # Lấy dữ liệu từ request JSON
    data = request.json
    cipher_text = data['cipher_text']
    key = int(data['key'])  # Chuyển key sang số nguyên
    
    # Giải mã văn bản
    decrypted_text = railfence_cipher.rail_fence_decrypt(cipher_text, key)
    
    # Trả về kết quả dưới dạng JSON
    return jsonify({'decrypted_text': decrypted_text})

#VigenereCipher
vigenere_cipher = VigenereCipher()

@app.route('/api/vigenere/encrypt', methods=['POST'])
def vigenere_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = data['key']
    
    encrypted_text = vigenere_cipher.vigenere_encrypt(plain_text, key)
    return jsonify({'encrypted_text': encrypted_text})
@app.route('/api/vigenere/decrypt', methods=['POST'])
def vigenere_decrypt():

    data = request.json
    cipher_text = data['cipher_text']
    key = data['key']
    

    decrypted_text = vigenere_cipher.vigenere_decrypt(cipher_text, key)

    return jsonify({'decrypted_text': decrypted_text})

# CAESAR CIPHER ALGORITHM
caesar_cipher = CaesarCipher()

@app.route("/api/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = int(data['key'])
    encrypted_text = caesar_cipher.encrypt_text(plain_text, key)
    return jsonify({'encrypted_message': encrypted_text})

@app.route("/api/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = int(data['key'])
    decrypted_text = caesar_cipher.decrypt_text(cipher_text, key)
    return jsonify({'decrypted_message': decrypted_text})

# main function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
