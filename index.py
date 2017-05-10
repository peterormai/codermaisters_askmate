from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import csv
import time

app = Flask(__name__)


@app.route('/list', methods=['GET'])
@app.route('/', methods=['GET'])
def list_questions():
    with open('database.csv') as data:
        data_list = data.read().splitlines()
        data_list = [item.split(",") for item in data_list]
    for item in data_list:
        item[1] = time.strftime("%D %H:%M", time.localtime(int(item[1])))
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
        for item in data_list:
            item[1] = time.strftime("%D %H:%M", time.localtime(int(item[1])))
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


@app.route("/questions/<int:id>", methods=["GET"])
def show_question(id):
    with open('database.csv') as data:
        data_list = data.read().splitlines()
        data_list = [item.split(",") for item in data_list]
        for item in data_list:
            if int(item[0]) == int(id):
                selected_question = item
        return render_template('update.html', selected_question=selected_question)


@app.route("/questions/<int:id>", methods=["POST"])
def update_question(id):
    selected_question = request.form["question_update"]
    with open('database.csv') as data:
        data_list = data.read().splitlines()
        data_list = [item.split(",") for item in data_list]
        for item in data_list:
            if int(item[0]) == int(id):
                item[4] = selected_question.replace("\r\n", " ")

    with open('database.csv', 'w') as file:
        for item in data_list:
            file.write(",".join(item) + "\n")
    return redirect("/list")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


def main():
    app.run(debug=None)


if __name__ == '__main__':
    main()
