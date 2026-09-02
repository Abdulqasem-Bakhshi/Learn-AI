from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer

app = Flask(__name__)

MODEL_NAME = "Qwen/Qwen3-0.6B"

print("Loading Qwen3...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype="auto",
    device_map="auto"
)

print("Qwen3 is ready.")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    prompt = data["message"]

    # Get thinking mode from the frontend.
    # Default to False if it isn't provided.
    enable_thinking = data.get("enable_thinking", False)

    print("Thinking:", enable_thinking)

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    inputs = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
        enable_thinking=enable_thinking,
    ).to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
    )

    response = tokenizer.decode(
        outputs[0][inputs["input_ids"].shape[-1]:],
        skip_special_tokens=True,
    )

    return jsonify({
        "response": response
    })

if __name__ == "__main__":
    app.run(debug=True)