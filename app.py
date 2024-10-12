from flask import Flask, request, jsonify, render_template
import urllib.parse
import requests
import os
import re

# Khởi tạo ứng dụng Flask
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

# Route cho trang chủ
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

    # Tìm tất cả các link trong văn bản bằng regex chỉ cho các tên miền cụ thể
    links = re.findall(r'(https?://(?:vn\.shp\.ee|s\.shopee\.vn)/[^\s]+)', text)
    results = text  # Khởi tạo kết quả là văn bản gốc

    for link in links:
        full_link = resolve_short_link(link)  # Giải mã liên kết rút gọn

        if not full_link:
            continue  # Bỏ qua nếu không thể giải mã

        encoded_link = encode_link(full_link)  # Mã hóa liên kết

        # Tạo liên kết mới với affiliate_id
        new_link = f"https://shope.ee/an_redir?origin_link={encoded_link}&affiliate_id=17305270177&sub_id=huong"

        # Thay thế liên kết cũ bằng liên kết mới trong văn bản
        results = results.replace(link, new_link)

    # Chuyển đổi ký tự xuống dòng thành <br> để hiển thị đúng định dạng
    results = results.replace("\n", "<br>")

    # Trả về kết quả dưới dạng JSON
    return jsonify(results=[results])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Sử dụng biến môi trường PORT
    app.run(host='0.0.0.0', port=port)
