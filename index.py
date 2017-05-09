from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import csv

app = Flask(__name__)


@app.route('/list', methods=['GET'])
@app.route('/', methods=['GET'])
def list_page():
    with open('database.csv') as data:
        data_list = data.read().splitlines()
        data_list = [item.split(",") for item in data_list]
    title = "Cödermeisters's ask-mate"
    top_menu = ['ID', 'Created at', 'Views', 'Votes', 'Title', 'Edit', 'Delete', "Like", "Dislike"]
    return render_template('index.html', title=title, data_list=data_list, top_menu=top_menu)


@app.route("/sortby", methods=['POST'])
def sort_by():
    title = "Super Sprinter 3000"
    top_menu = ['ID', 'Created at', 'Views', 'Votes', 'Title', 'Edit', 'Delete', "Like", "Dislike"]
    search_key = str(request.form['sortby'])
    with open('database.csv') as data:
        data_list = data.read().splitlines()
        data_list = [item.split(",") for item in data_list]
        sort_value = str(request.form['sortby'])
        if search_key == 'ID':
            data_list = sorted(data_list, key=lambda x: int(x[0]))
        elif search_key == 'created':
            data_list = sorted(data_list, key=lambda x: str(x[1]))
        elif search_key == 'views':
            data_list = sorted(data_list, key=lambda x: int(x[2]))
        elif search_key == 'votes':
            data_list = sorted(data_list, key=lambda x: int(x[3]))
        elif search_key == 'title':
            data_list = sorted(data_list, key=lambda x: str(x[4]))
    return render_template('index.html', data_list=data_list, title=title, top_menu=top_menu)


@app.route("/like/<int:id>/<int:like_value>", methods=['GET'])
def handle_like(id, like_value):
    with open('database.csv') as data:
        data_list = data.read().splitlines()
        data_list = [item.split(",") for item in data_list]
        for item in data_list:
            if int(item[0]) == int(id):
                if int(like_value) == 1:
                    item[3] = int(item[3]) + 1
                elif int(like_value) == 0:
                    item[3] = int(item[3]) - 1

    with open('database.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data_list)
    return redirect("/list")


@app.route("/edit/<int:id>/", methods=['GET'])
def handle_like(id):
    with open('database.csv') as data:
        data_list = data.read().splitlines()
        data_list = [item.split("ß¤") for item in data_list]
        selected_story = []
        for item in data_list:
            if int(item[0]) == int(id):
                selected_story = item




def main():
    app.run(debug=None)


if __name__ == '__main__':
    main()
