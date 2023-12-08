from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np

print("Pd version :" + pd.__version__)
popular_df = pickle.load(open("pickles/popular.pkl", "rb"))
final_df = pickle.load(open("pickles/final_df.pkl", "rb"))
books_csv = pickle.load(open("pickles/books_csv.pkl", "rb"))
similarity_score = pickle.load(open("pickles/similarity_score.pkl", "rb"))


app = Flask(__name__)

ratings = list(popular_df["avg_rating"].values)
ratings = [round(i, 2) for i in ratings]


@app.route("/")
def index():
    return render_template(
        "index.html",
        book_name=list(popular_df["Book-Title"].values),
        author=list(popular_df["Book-Author"].values),
        votes=list(popular_df["num_rating"].values),
        ratings=ratings,
        image=list(popular_df["Image-URL-M"].values),
    )


@app.route("/recommend")
def recommend():
    return render_template("recmd.html")


@app.route("/recommend_books", methods=["POST"])
def recommend_books():
    book_name = request.form.get("user_input")
    index = np.where(final_df.index == book_name)[0][0]
    similar_scores = sorted(
        list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True
    )[1:6]
    new_indexes = [i[0] for i in similar_scores]

    suggestions = final_df.index[new_indexes]
    books = books_csv[books_csv["Book-Title"].isin(suggestions)]
    books = books.drop_duplicates("Book-Title")
    titles = books["Book-Title"]
    authors = books["Book-Author"]
    images = books["Image-URL-M"]
    data = list(zip(titles, authors, images))
    return render_template("recmd.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
