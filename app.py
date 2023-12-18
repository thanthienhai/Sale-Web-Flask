from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    # Read the CSV file
    csv_file_path = 'data.csv'  # Replace with the path to your CSV file
    df = pd.read_csv(csv_file_path)
    #menu_items = ['Trang chủ', 'Nhập dữ liệu', 'Phân tích khách hàng', 'Phân tích thời gian', 'Phân tích cửa hàng', 'Dự đoán doanh số', 'Dự đoán doanh số']
    return render_template('index.html', table=df.to_html(classes='table table-striped', border=0, justify='unset', col_space=0))

#--------------------------------------------
@app.route('/nhap_button')
def nhap_button():
    # Thực hiện các hành động khi Button 1 được click
    return "Button 1 clicked!"

@app.route('/kh_button')
def kh_button():
    # Thực hiện các hành động khi Button 2 được click
    return "Button 2 clicked!"

@app.route('/tg_button')
def tg_button():
    # Thực hiện các hành động khi Button 3 được click
    return "Button 3 clicked!"

@app.route('/ch_button')
def ch_button():
    # Thực hiện các hành động khi Button 3 được click
    return "Button 4 clicked!"

@app.route('/ds_button')
def ds_button():
    # Thực hiện các hành động khi Button 3 được click
    return "Button 5 clicked!"

if __name__ == '__main__':
    app.run(debug=True)

