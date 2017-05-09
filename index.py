from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

app = Flask(__name__)


@app.route('/list', methods=['GET'])
@app.route('/', methods=['GET'])
def list_page():
    with open('database.csv') as data:
        data_list = data.read().splitlines()
        data_list = [item.split(",") for item in data_list]
        title = "Cödermeisters's ask-mate"
        return render_template('index.html', title=title, data_list=data_list)


def main():
    app.run(debug=None)


if __name__ == '__main__':
    main()
