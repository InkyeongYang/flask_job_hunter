from flask import Flask, render_template, request, redirect, send_file
from remoteok import extract_jobs as ext_rmtok
from stackoverflow import extract_jobs as ext_stkovflw
from wework import extract_jobs as ext_wwk
from exporter import save_to_file


app = Flask("Job_Finder")
db = {}

@app.route("/")
def main():
    return render_template("home.html")

@app.route("/search")
def search():
    results = []
    search_words = request.args.get("word")
    if search_words:
        search_words = search_words.lower()
        words = search_words.strip().split(' ')
        for word in words:
            if word not in db:
                stack_over_flow = ext_stkovflw(word)
                remote_ok = ext_rmtok(word)
                we_work = ext_wwk(word)
                db[word] = stack_over_flow + remote_ok + we_work
            results += db.get(word)
    return render_template("search.html", search_word=search_words, count=len(results), results=results)

@app.route("/export")
def export():
    try:
        jobs = []
        word = request.args.get("word")
        if not word:
            raise Exception()
        words = word.lower().split(' ')
        name = ""
        for w in words:
            name += f"{w}+"
            result = db.get(w)
            jobs += result
        if not result:
            raise Exception()
        name=name.strip('+')
        save_to_file(name, jobs)
        return send_file(f"{name}.csv")
    except:
        return redirect("/")
