from flask import Flask, request, jsonify, render_template
import urllib.parse
import requests
import os
import re

app = Flask(__name__)

# Hàm để mã hóa URL
def encode_link(link):
    base_url = link.split('?')[0]  # Lấy phần URL trước dấu hỏi
    return urllib.parse.quote(base_url, safe='')  # Mã hóa phần đó

# Hàm để giải mã liên kết rút gọn thành liên kết đầy đủ
def resolve_short_link(short_url):
    try:
        response = requests.head(short_url, allow_redirects=True)
        return response.url  # Trả về URL đầy đủ sau khi chuyển hướng
    except requests.RequestException:
        return None

@app.route('/')
def index():
    return render_template('index.html')

# Hàm xử lý kết quả khi người dùng nhập văn bản
@app.route('/generate_links', methods=['POST'])
def generate_links():
    data = request.get_json()  # Nhận dữ liệu JSON từ yêu cầu
    text = data.get('text')  # Lấy văn bản gốc

    if not text:
        return jsonify(error="Vui lòng cung cấp văn bản.")  # Trả về lỗi nếu không có văn bản

    # Tìm tất cả các link trong văn bản bằng regex
    links = re.findall(r'(https?://[^\s]+)', text)
    results = []

    for link in links:
        full_link = resolve_short_link(link)  # Giải mã liên kết rút gọn

        if not full_link:
            continue  # Bỏ qua nếu không thể giải mã

        encoded_link = encode_link(full_link)  # Mã hóa liên kết

        # Tạo liên kết mới với affiliate_id
        result = f"https://shope.ee/an_redir?origin_link={encoded_link}&affiliate_id=17385530062&sub_id=1review"
        results.append(result)

    if not results:
        return jsonify(error="Không tìm thấy liên kết nào để thay thế.")  # Trả về lỗi nếu không tìm thấy liên kết

    # Trả về kết quả dưới dạng JSON
    return jsonify(results=results)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Sử dụng biến môi trường PORT
    app.run(host='0.0.0.0', port=port)
