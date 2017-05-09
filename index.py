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
        top_menu = ['ID', 'Created at', 'Views', 'Votes', 'Title', 'Edit', 'Delete']
        return render_template('index.html', title=title, data_list=data_list, top_menu=top_menu)


@app.route("/sortby", methods=['POST'])
def sort_by():
    title = "Super Sprinter 3000"
    search_key = str(request.form['sortby'])
    with open('database.csv') as data:
        data_list = data.read().splitlines()
        data_list = [item.split(",") for item in data_list]
        if search_key == 'ID':
            data_list = sorted(data_list, key=lambda x: int(x[0]))
        elif search_key == 'Title':
            data_list = sorted(data_list, key=lambda x: str(x[1]))
        elif search_key == 'User Story':
            data_list = sorted(data_list, key=lambda x: str(x[2]))
        elif search_key == 'Acceptance Criteria':
            data_list = sorted(data_list, key=lambda x: str(x[3]))
        elif search_key == 'Business Value':
            data_list = sorted(data_list, key=lambda x: int(x[4]))
        elif search_key == 'Estimation (h)':
            data_list = sorted(data_list, key=lambda x: float(x[5]))
        elif search_key == 'Status':
            data_list = sorted(data_list, key=lambda x: str(x[6]))
    return render_template('list.html', data_list=data_list, title=title)


def main():
    app.run(debug=None)


if __name__ == '__main__':
    main()
