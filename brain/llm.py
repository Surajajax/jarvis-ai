import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"


print("🧠 Loading JARVIS brain...")

device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Device: {device}")

if device == "cuda":
    print(f"GPU: {torch.cuda.get_device_name(0)}")


tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype="auto",
    device_map="auto"
)


print("✅ JARVIS brain loaded.")


def ask_jarvis(user_text):

    messages = [
        {
            "role": "system",
            "content": (
                "You are JARVIS, a helpful personal AI assistant. "
                "Answer clearly and concisely."
            )
        },
        {
            "role": "user",
            "content": user_text
        }
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        [text],
        return_tensors="pt"
    ).to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=100
    )

    generated_ids = [
        output_ids[len(input_ids):]
        for input_ids, output_ids
        in zip(inputs.input_ids, outputs)
    ]

    response = tokenizer.batch_decode(
        generated_ids,
        skip_special_tokens=True
    )[0]

    return response.strip()


if __name__ == "__main__":

    print("\n================================")
    print("🤖 JARVIS BRAIN TEST")
    print("================================")

    question = input("\nYou: ")

    answer = ask_jarvis(question)

    print("\nJARVIS:")
    print(answer)