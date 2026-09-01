from flask import Flask, request
from transformers import pipeline

app = Flask(__name__)

print("Loading GPT-2...")
generator = pipeline(
    "text-generation",
    model="openai-community/gpt2"
)
print("GPT-2 is ready.")


@app.route("/", methods=["GET", "POST"])
def home():
    result = ""

    if request.method == "POST":
        prompt = request.form["prompt"]

        output = generator(
            prompt,
            max_new_tokens=80,
            do_sample=True,
            temperature=0.8,
        )

        result = output[0]["generated_text"]

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>My Local GPT-2</title>
    </head>

    <body>
        <h1>My Local GPT-2</h1>

        <form method="POST">
            <textarea
                name="prompt"
                rows="5"
                cols="60"
                placeholder="Write something..."
            ></textarea>
            <br><br>
            <button type="submit">Generate</button>
        </form>

        <h2>Result</h2>
        <p>{result}</p>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)