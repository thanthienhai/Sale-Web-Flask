from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    # Read the CSV file
    csv_file_path = 'data.csv'  # Replace with the path to your CSV file
    df = pd.read_csv(csv_file_path)
    #menu_items = ['Trang chủ', 'Nhập dữ liệu', 'Phân tích khách hàng', 'Phân tích thời gian', 'Phân tích cửa hàng', 'Dự đoán doanh số', 'Dự đoán doanh số']
    menu_items = df.columns.tolist()
    return render_template('index.html', menu_items=menu_items, data=df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)

