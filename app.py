from flask import Flask, request, jsonify, render_template
import urllib.parse
import requests
import os

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

# Hàm xử lý kết quả khi người dùng nhập văn bản và liên kết
@app.route('/generate_links', methods=['POST'])
def generate_links():
    data = request.get_json()  # Nhận dữ liệu JSON từ yêu cầu
    original_link = data.get('link')  # Lấy liên kết gốc
    original_text = data.get('text')  # Lấy văn bản nhập vào

    if not original_link:
        return jsonify(error="Vui lòng cung cấp liên kết.")  # Trả về lỗi nếu không có liên kết

    full_link = resolve_short_link(original_link)  # Giải mã liên kết rút gọn

    if not full_link:
        return jsonify(error="Không thể giải mã liên kết rút gọn.")  # Trả về lỗi nếu không thể giải mã

    encoded_link = encode_link(full_link)  # Mã hóa liên kết

    # Chỉ tạo 1 kết quả với affiliate_id tương ứng
    result_2 = f"https://shope.ee/an_redir?origin_link={encoded_link}&affiliate_id=17305270177&sub_id=1review"

    # Trả về kết quả dưới dạng JSON bao gồm cả văn bản và liên kết mới
    return jsonify(results=[result_2], text=original_text)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Sử dụng biến môi trường PORT
    app.run(host='0.0.0.0', port=port)
