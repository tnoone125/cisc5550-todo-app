# This is a simple example web app that is meant to illustrate the basics.
from flask import Flask, render_template, redirect, request, url_for, json
import requests

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/")
def show_list():
    resp = requests.get("http://34.27.234.150:5001/api/items")
    resp = resp.json()
    return render_template('index.html', todolist=resp)


@app.route("/add", methods=['POST'])
def add_entry():
    dictToSend = {'what_to_do' : request.form['what_to_do'], 'due_date' : request.form['due_date']}
    res = requests.post('http://34.27.234.150:5001/api/add', json=dictToSend)
    dictFromServer = res.json()
    if dictFromServer['success']:
        return redirect(url_for('show_list'))
    else:
        return render_template('500.html')


@app.route("/delete/<item>")
def delete_entry(item):
    data = {'item': item}
    res = requests.delete('http://34.27.234.150:5001/api/delete', json=data)
    dictFromServer = res.json()
    if dictFromServer['success']:
        return redirect(url_for('show_list'))
    else:
        return render_template('500.html')


@app.route("/mark/<item>")
def mark_as_done(item):
    data = {'item': item}
    res = requests.put('http://34.27.234.150:5001/api/mark', json=data)
    dictFromServer = res.json()
    if dictFromServer['success']:
        return redirect(url_for('show_list'))
    else:
        return render_template('500.html')


if __name__ == "__main__":
    app.run("0.0.0.0")