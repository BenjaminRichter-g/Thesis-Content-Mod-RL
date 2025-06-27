import argparse
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from dotenv import dotenv_values

# Import your existing preprocessing logic
from data.preprocessor  import PreProcessor
from data.classification_filter import classification_filter



def is_racist(text: str) -> bool:
    
    prompt = (
        "Determine if the following text is racist. "
        "It can be part of the following types of racism: Racial, Ethnic, Religious, Nationalistic, Political.\n"
        "Answer with 'yes' or 'no'. ONLY answer with 'yes' or 'no'.\n\n"
        f"Text: {text}\nAnswer:"
    )
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=5,  # give it room to say 'yes' or 'no'
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

    # Decode only the newly generated part
    generated_text = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
    cleaned = generated_text.strip().lower()

    value = "yes" in cleaned

    return value if type(value) == bool else None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Filter JSONL by racist content using a GPU-accelerated LLM."
    )
    parser.add_argument('--model', required=True,
                        help="Hugging Face model name or path (e.g. meta-llama/Llama-2-7b-chat-hf)")
    parser.add_argument('--input', required=True, help="Input JSONL file")
    parser.add_argument('--out-racist', required=True, help="Output JSONL for racist posts")
    parser.add_argument('--out-non-racist', required=True, help="Output JSONL for non-racist posts")
    args = parser.parse_args()


    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16
    )

    # Set up device and 4-bit quantization

    config = dotenv_values(".env")

    # Load model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        "meta-llama/Llama-2-7b-chat-hf",
        use_auth_token=config["HF_TOKEN"],
    )
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        quantization_config=bnb_config,
        device_map="auto",
        torch_dtype=torch.float16
    )

    classification_filter(args.input, args.out_racist, args.out_non_racist, is_racist)


