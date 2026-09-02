from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer

app = Flask(
    __name__,
    template_folder="../../templates",
    static_folder="../../static"
)

MODEL_NAME = "Qwen/Qwen3-0.6B"

print("Loading Qwen3...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype="auto",
    device_map="auto"
)

print("Qwen3 is ready.")


MODEL_DISPLAY_NAME = "Qwen3-0.6B"

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
        max_new_tokens=5000,
    )

    # Calculate the number of generated tokens & print the input, generated, and total tokens.
    generated_tokens = outputs.shape[-1] - inputs["input_ids"].shape[-1]
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