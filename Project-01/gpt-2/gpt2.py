from transformers import pipeline

print("Loading GPT-2...")

generator = pipeline(
    "text-generation",
    model="openai-community/gpt2"
)

print("GPT-2 is ready.")
print("Type a prompt, or type 'quit' to exit.\n")

while True:
    prompt = input("You: ")

    if prompt.lower() == "quit":
        break

    result = generator(
        prompt,
        max_new_tokens=80,
        do_sample=True,
        temperature=0.8,
    )

    print("\nGPT-2:", result[0]["generated_text"])
    print()