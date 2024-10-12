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
