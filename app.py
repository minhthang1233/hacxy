from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# Hàm lọc liên kết từ văn bản
def extract_links(text):
    pattern = r'https?://[^\s]+'
    links = re.findall(pattern, text)
    return links

# Hàm thay thế liên kết
def replace_shopee_links(text):
    def replace_link(match):
        url = match.group(0)
        # Kiểm tra tên miền
        if 's.shopee.vn' in url or 'vn.shp.ee' in url:
            # Thay thế theo yêu cầu
            new_url = f"https://shope.ee/an_redir?origin_link={url}&affiliate_id=17385530062&sub_id=1review"
            return new_url
        return url
    
    # Thay thế các link trong văn bản
    replaced_text = re.sub(r'https?://[^\s]+', replace_link, text)
    return replaced_text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/filter', methods=['POST'])
def filter_links():
    data = request.get_json()
    text = data.get('text')
    links = extract_links(text)
    return jsonify({'links': links})

@app.route('/replace', methods=['POST'])
def replace_links():
    data = request.get_json()
    text = data.get('text')
    replaced_text = replace_shopee_links(text)
    return jsonify({'replaced_text': replaced_text})

if __name__ == '__main__':
    app.run(debug=True)
