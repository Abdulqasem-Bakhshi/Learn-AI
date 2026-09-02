from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer

app = Flask(
    __name__,
    template_folder="../../templates",
    static_folder="../../static"
)

MODEL_NAME = "openai-community/gpt2"

print("Loading GPT-2...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype="auto",
    device_map="auto"
)

print("GPT-2 is ready.")


MODEL_DISPLAY_NAME = "GPT-2"

@app.route("/")
def home():
    return render_template(
        "index.html",
        model_name=MODEL_DISPLAY_NAME
    )


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    prompt = data["message"]

    print("Prompt:", prompt)

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    ).to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=500,
        do_sample=True,
        temperature=0.8,
        top_p=0.95,
    )

    generated_tokens = (
        outputs.shape[-1]
        - inputs["input_ids"].shape[-1]
    )

    print("Input tokens:", inputs["input_ids"].shape[-1])
    print("Generated tokens:", generated_tokens)
    print("Total tokens:", outputs.shape[-1])

    response = tokenizer.decode(
        outputs[0][inputs["input_ids"].shape[-1]:],
        skip_special_tokens=True,
    )

    return jsonify({
        "response": response
    })


if __name__ == "__main__":
    app.run(debug=False)