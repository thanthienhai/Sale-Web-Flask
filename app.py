import os
import pandas as pd
from flask import Flask, render_template, request

from plot import *

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'userUpload'

csv_file_path = 'data.csv' 
df_origin = pd.read_csv(csv_file_path)

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
    if(d.iloc[-1,1]>5.0):
        data = "Good"
    else:
        data = "Poor"
    return render_template('customer_analytic.html', table_1=table_1, table_2=table_2, table_3=table_3, data=data)


@app.route('/tg_button')
def tg_button():
    table_1 = line_chart(df_origin.copy(), 'City', 'Total', 'mean')
    return render_template('time_analytic.html', table_1=table_1)


@app.route('/ch_button')
def ch_button():
    return "Button 4 clicked!"


@app.route('/ds_button')
def ds_button():
    return "Button 5 clicked!"

if __name__ == '__main__':
    app.run(debug=True)
