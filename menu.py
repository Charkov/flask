from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/main_menu')
def menu():
    attractions = {'d1': 'страница 1', 'd2': 'страница 2'}
    return render_template("main menu.html", attractions=attractions)


@app.route('/second_page')
def second():
    return render_template("2_page.html")


@app.route('/d1/<name_page>')
def first(name_page):
    return render_template("страница1.html", name=name_page)


if __name__ == "__main__":
    app.run(port=8000, host='127.0.0.1')
