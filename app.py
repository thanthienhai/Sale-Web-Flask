import os
import pandas as pd
from flask import Flask, render_template, request
import calendar

from plot import *

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'userUpload'

csv_file_path = 'data.csv' 
df_origin = pd.read_csv(csv_file_path)
csv_file_path_chuanhoa = 'data_1.csv' 
df_chuanhoa = pd.read_csv(csv_file_path_chuanhoa)
csv_file_path_predict = 'data_predict.csv' 
df_predict = pd.read_csv(csv_file_path_predict)
#-------------------------------

@app.route('/')
def index():
    first_5_rows = df_origin.head(5)
    thongKe = df_origin.describe()
    
    return render_template('index.html', 
                           table=first_5_rows.to_html(classes='table table-striped', border=0, justify='unset', col_space=0), 
                           table_2=thongKe.to_html(classes='table table-striped', border=0, justify='unset', col_space=0)
                           )


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv'}

@app.route('/nhap_button', methods=['GET', 'POST'])
def nhap_button():
    if request.method == 'POST':
        try:
            file = request.files['file']
            
            if file and allowed_file(file.filename):
                # Save the file to the upload folder
                filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filename)
                message = 'File uploaded successfully!'
                return render_template('upload.html', message=message)
            else:
                message = 'Invalid file type. Allowed file types are csv.'
                return render_template('upload.html', message=message, alert_type='danger')
        
        except Exception as e:
            message = f'An error occurred: {str(e)}'
            return render_template('upload.html', message=message, alert_type='danger')
    
    return render_template('upload.html')


@app.route('/kh_button')
def kh_button():
    table_1 = bar_chart(df_origin.copy(), 'Product line', 'Quantity', 'Gender', 'mean')
    table_2 = bar_chart(df_origin.copy(), 'Customer type', 'Quantity', 'City', 'count')
    table_3 = pie_chart(df_origin.copy(), 'Gender', 'Quantity', 'count')
    d = df_origin.describe().T
    if d.iloc[-1, 1] > 5.0:
        data = {"status": "Good", "color": "green"}
    else:
        data = {"status": "Poor", "color": "red"}
    return render_template('customer_analytic.html', table_1=table_1, table_2=table_2, table_3=table_3, data=data)


@app.route('/tg_button')
def tg_button():

    table_1 = line_chart(df_chuanhoa, 'TimeOfTheDay', 'Total', aggregation='mean', x_index=['Morning', 'Afternoon', 'Evening'])
    table_2 = line_chart(df_chuanhoa, 'TimeOfTheDay', 'Total', 'City', 'mean')
    max_index = df_chuanhoa['Total'].idxmax()
    max_time_of_the_day = df_chuanhoa.loc[max_index, 'TimeOfTheDay']
    df_chuanhoa['Time'] = pd.to_datetime(df_chuanhoa['Time'])
    df_chuanhoa['Hour'] = df_chuanhoa['Time'].dt.hour

    # Nhóm dữ liệu theo cặp 'City' và 'Time', tính tổng số lượng bán
    grouped_df = df_chuanhoa.groupby(['City', 'Time']).sum().reset_index()

    # Tìm giờ bán nhiều nhất và ít nhất cho mỗi thành phố
    max_sales_idx = grouped_df.groupby('City')['Total'].idxmax()
    min_sales_idx = grouped_df.groupby('City')['Total'].idxmin()

    max_sales_time = grouped_df.loc[max_sales_idx, ['City', 'Hour', 'Total']]
    min_sales_time = grouped_df.loc[min_sales_idx, ['City', 'Hour', 'Total']]

    return render_template('time_analytic.html', table_1=table_1, table_2=table_2, data=max_time_of_the_day, 
                            city_min=min_sales_time.to_html(classes='table table-striped', border=0, justify='unset', col_space=0), 
                            city_max=max_sales_time.to_html(classes='table table-striped', border=0, justify='unset', col_space=0))


@app.route('/ch_button')
def ch_button():
    df_chuanhoa1=df_chuanhoa
    df_chuanhoa1['Date'] = pd.to_datetime(df_chuanhoa1['Date'])
    df_chuanhoa1['Month'] = df_chuanhoa1['Date']
    df_sorted = df_chuanhoa1.sort_values(by='Month')
    df_sorted['Month'] = df_sorted['Month'].dt.month_name()
    print(df_sorted)
    table_1 = line_chart(df_sorted.copy(), 'Month', 'Total', aggregation='mean')
    table_2 = bar_chart(df_origin.copy(), 'Product line', 'Total', 'City', aggregation='mean')
    #----------------------------
    grouped_data = df_origin.groupby(['City', 'Product line'])['Total'].sum().reset_index()
    max_total_per_city = grouped_data.loc[grouped_data.groupby('City')['Total'].idxmax()]
    min_total_per_city = grouped_data.loc[grouped_data.groupby('City')['Total'].idxmin()]
    min = pd.DataFrame(min_total_per_city)
    max = pd.DataFrame(max_total_per_city)

    return render_template('store_analytic.html', table_1=table_1, table_2=table_2, 
                            min=min.to_html(classes='table table-striped', border=0, justify='unset', col_space=0, index=False), 
                            max=max.to_html(classes='table table-striped', border=0, justify='unset', col_space=0, index=False))


@app.route('/ds_button')
def ds_button():
    table_1 = df_predict.groupby('Product line')['prediction'].sum().reset_index()
    table_2 = df_predict.groupby('Product line')['Sales'].sum().reset_index()
    total_sales = df_predict['Sales'].sum()
    total_sales = round(total_sales, 0)
    return render_template('predict_site.html', table_1=table_1.to_html(classes='table table-striped', border=0, justify='unset', col_space=0, index=False), 
                            table_2=table_2.to_html(classes='table table-striped', border=0, justify='unset', col_space=0, index=False),
                            total_sales=total_sales)

if __name__ == '__main__':
    app.run(debug=True)
