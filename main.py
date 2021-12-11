import pandas as pd
import time
import matplotlib.pyplot as plt
from flask import Flask, render_template, send_file, request

app = Flask(__name__)

df = pd.read_csv("data/CAR DETAILS FROM CAR DEKHO.csv")
df['year'] = df['year'].astype(int)
df['selling_price'] = df['selling_price'].astype(int)
df['km_driven'] = df['km_driven'].astype(int)

links = {"Useful links": "/get_links",
         "Download data file (.csv)": "/download_data",
         "Download colab notebook (.ipynb)": "/download_notebook",
         "View Raw Data": "/view_data",
         "View data stat": '/data_stat',
         "Mean price": "/mean_price",
         "Gross price": "/gross_price",
         "Price on market": "/price_on_market",
         "Average selling price": "/average_selling_price",
         "Average km driven": "/average_km_driven",
         "Analysis": "/analysis"}


def render_index(image=None, html_string=None, filters=None, current_filter_value="", errors=[]):
    return render_template("index.html", links=links, image=image, code=time.time(), html_string=html_string, filters=filters, current_filter_value = current_filter_value, errors=errors)


@app.route('/', methods=['GET'])
def main_page():
    return render_index()


@app.route(links["Useful links"], methods=['GET', 'POST'])
def get_link():
    text = "link to my website with raw data: <a href=\"https://makarenkovartem.w3spaces.com/\"> https://makarenkovartem.w3spaces.com </a> <br/>" \
           "link to kagle data: <a href=\"https://www.kaggle.com/nehalbirla/vehicle-dataset-from-cardekho\"> https://www.kaggle.com/nehalbirla/vehicle-dataset-from-cardekho </a> <br/>" \
           "link to my colab notebook: <a href=\"https://colab.research.google.com/drive/1PqSlRaSCMJ3DavEAxhH3cuTlmIWeVNse?usp=sharing\"> https://colab.research.google.com/drive/1PqSlRaSCMJ3DavEAxhH3cuTlmIWeVNse?usp=sharing </a>"
    return render_index(html_string=text)


@app.route(links["Download data file (.csv)"], methods=['GET'])
def download_data():
    return send_file("data/CAR DETAILS FROM CAR DEKHO.csv", as_attachment=True)


@app.route(links["Download colab notebook (.ipynb)"], methods=['GET'])
def download_notebook():
    return send_file("data/Makarenkov_Vehicle_Sales.ipynb", as_attachment=True)


@app.route(links["View Raw Data"], methods=['GET', 'POST'])
def view_data():
    df = pd.read_csv("data/CAR DETAILS FROM CAR DEKHO.csv")
    errors = []
    current_filter_value = ""
    if request.method == "POST":
        current_filter = request.form.get('filters')
        current_filter_value = current_filter
        if current_filter:
            try:
                df = df.query(current_filter)
            except Exception as e:
                errors.append('font color="red">Incorrect filter</font>')
                print(e)
    html_string = df.to_html()
    return render_index(html_string=html_string, filters=True, current_filter_value=current_filter_value, errors=errors)


@app.route(links["View data stat"], methods=['GET', 'POST'])
def view_stat():
    des = df.describe()
    drop_list = ['25%', "max", "75%", "min", "count"]
    for i in drop_list:
        des = des.drop(i)
    des = des.reindex(["mean", "50%", "std"])
    des.index = ["mean", "median", "standard deviation"]
    html_string = des.to_html()
    return render_index(html_string=html_string)


@app.route(links["Mean price"], methods=['GET'])
def mean_price():
    plt.figure(num=None, figsize=(12, 6), dpi=300, facecolor='w', edgecolor='k')
    plt.plot(df.groupby('year')['selling_price'].mean())
    plt.title('Mean price')
    plt.xlabel('Year')
    plt.ylabel('Rubles')
    plt.savefig('static/tmp/mean_price.png')
    return render_index(("mean_price.png", "Mean price"))


@app.route(links["Gross price"], methods=['GET'])
def gross_price():
    plt.figure(num=None, figsize=(12, 6), dpi=300, facecolor='w', edgecolor='k')
    plt.plot(df.groupby('year')['selling_price'].sum())
    plt.title('Gross price')
    plt.xlabel('Year')
    plt.ylabel('Rubles')
    plt.savefig('static/tmp/gross_price.png')
    return render_index(("gross_price.png", "Gross price"))


@app.route(links["Price on market"], methods=['GET', 'POST'])
def price_on_market():
    df = pd.read_csv("data/CAR DETAILS FROM CAR DEKHO.csv")
    errors = []
    current_filter_value = ""
    if request.method == "POST":
        current_filter = request.form.get('filters')
        current_filter_value = current_filter
        if current_filter:
            try:
                df = df.query(current_filter)
            except Exception as e:
                errors.append('font color="red">Incorrect filter</font>')
                print(e)

    fig, ax = plt.subplots(figsize=(12, 8))

    ax.plot(df.groupby('year')['selling_price'].mean(), label="mean price per year")
    ax.plot(df.groupby('year')['selling_price'].median(), label="median price per year")
    ax.plot(df.groupby('year')['selling_price'].std(), label="std price per year")

    ax.legend(loc=2)
    ax.set_xlabel('Year')
    ax.set_ylabel('Rubles')
    ax.set_title('Price on market')
    plt.savefig('static/tmp/price_on_market.png')
    return render_index(("price_on_market.png", "Price on market"), filters=True, current_filter_value=current_filter_value, errors=errors)


@app.route(links["Average selling price"], methods=['GET'])
def average_selling_price():
    plt.figure(num=None, figsize=(14, 6), dpi=100, facecolor='w', edgecolor='k')
    owner_list = list(df.groupby('owner')['selling_price'].mean().index)
    price_list = df.groupby('owner')['selling_price'].mean()
    plt.title('Average selling price')
    plt.ylabel('Rubles')
    plt.bar(owner_list, price_list)
    plt.savefig('static/tmp/average_selling_price.png')
    return render_index(("average_selling_price.png", "Average selling price"))


@app.route(links["Average km driven"], methods=['GET'])
def average_km_driven():
    plt.figure(num=None, figsize=(14, 6), dpi=100, facecolor='w', edgecolor='k')
    owner_list = list(df.groupby('owner')['km_driven'].mean().index)
    price_list = df.groupby('owner')['km_driven'].mean()
    plt.title('Average km driven')
    plt.ylabel('km')
    plt.bar(owner_list, price_list)
    plt.savefig('static/tmp/average_km_driven.png')
    return render_index(("average_km_driven.png", "Average km driven"))


@app.route(links["Analysis"], methods=['GET'])
def download_analysis():
    return render_index(("analysis.jpg", "Analysis"))


if __name__ == '__main__':
    app.run()
