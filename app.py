import os
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import plotly.express as px
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns
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
app.config['SECRET_KEY'] = 'O5y2agwlKXlug2PI92K34MVXnSba96tK'
UPLOAD_FOLDER = 'userUpload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class UploadForm(FlaskForm):
    csv_file = FileField('Choose CSV File')
    submit = SubmitField('Upload')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv'}
    
@app.route('/nhap_button', methods=['GET', 'POST'])
def nhap_button():
    # Thực hiện các hành động khi Button 1 được click
    form = UploadForm()

    if form.validate_on_submit():
        csv_file = form.csv_file.data
        if csv_file and allowed_file(csv_file.filename):
            filename = secure_filename(csv_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            csv_file.save(file_path)
            return redirect(url_for('success'))
        else:
            return "Invalid file type. Please upload a CSV file."

        return redirect(url_for('success'))

    return render_template('upload.html', form=form)
    #return "Button 1 clicked!"

@app.route('/success')
def success():
        return 'File uploaded successfully!'
        
#-------------------------------------------------

@app.route('/kh_button')
def kh_button():
    csv_file_path = 'data.csv'  # Replace with the path to your CSV file
    df = pd.read_csv(csv_file_path)
    if isinstance(df, (pd.DatetimeIndex, pd.MultiIndex)):
        df = df.to_frame(index=False)

# remove any pre-existing indices for ease of use in the D-Tale code, but this is not required
    df = df.reset_index().drop('index', axis=1, errors='ignore')
    df.columns = [str(c) for c in df.columns]  # update columns to strings in case they are numbers

    chart_data = pd.concat([
        df['Product line'],
        df['Quantity'],
        df['Gender'],
    ], axis=1)
    chart_data = chart_data.query("""(`Gender` == 'Female') or (`Gender` == 'Male')""")
    chart_data = chart_data.sort_values(['Gender', 'Product line'])
    chart_data = chart_data.rename(columns={'Product line': 'x'})
    chart_data = chart_data.dropna()
    # WARNING: This is not taking into account grouping of any kind, please apply filter associated with
    #          the group in question in order to replicate chart. For this we're using '"""`Gender` == 'Female'"""'
    chart_data = chart_data.query("""`Gender` == 'Female'""")

    import plotly.graph_objs as go

    charts = []
    charts.append(go.Bar(
        x=chart_data['x'],
        y=chart_data['Quantity'],
        name='(Gender: Female)'
    ))
    figure = go.Figure(data=charts, layout=go.Layout({
        'barmode': 'group',
        'legend': {'orientation': 'h', 'y': -0.3},
        'title': {'text': '(Gender: Female) - Quantity by Product line'},
        'xaxis': {'title': {'text': 'Product line'}},
        'yaxis': {'tickformat': '0:g', 'title': {'text': 'Quantity'}, 'type': 'linear'}
    }))
    chart_div = figure.to_html(full_html=False)
    return render_template('chart.html', chart_div=chart_div)
    # Thực hiện các hành động khi Button 2 được click
    #return "Button 2 clicked!"

#------------------------------------
@app.route('/tg_button')
def tg_button():
    '''
    csv_file_path = 'data.csv'  # Replace with the path to your CSV file
    df = pd.read_csv(csv_file_path)
    plt.figure(figsize=(22, 5))
    ax = sns.barplot(x='Customer type', y='Total', hue='City', data=df, ci=None)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.title('Total Average Sales, Customer type and City Wise', fontsize=20, y=1.02)
    for bar in ax.patches:
        ax.annotate(format(bar.get_height(), '.2f'), (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    ha='center', va='center', size=15, xytext=(0, 8), textcoords='offset points')
    plt.legend(loc='lower center')

    # Create a canvas and render the figure to the canvas
    canvas = FigureCanvas(plt.figure())
    img_path = 'static/matplotlib_chart.png'  # Save the figure as an image in the 'static' folder
    canvas.print_png(img_path)

    return render_template('matplotlib_chart.html', img_path=img_path)
    '''
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

