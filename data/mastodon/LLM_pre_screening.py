import json
import argparse
from tqdm import tqdm
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from dotenv import dotenv_values

# Import your existing preprocessing logic
from data.preprocessor  import PreProcessor

def is_racist(model, tokenizer, text: str) -> bool:
    """
    Uses a GPU-accelerated quantized LLM to classify whether the given text is racist.
    Returns True if the model answers 'yes', False otherwise.
    """
    prompt = (
        "Determine if the following text is racist. "
        "Answer with 'yes' or 'no'.\n\n"
        f"Text: {text}\n"
        "Answer:"
    )
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=1,
            temperature=0,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Extract just the last token (yes/no)
    answer = answer.strip().lower().splitlines()[-1]
    return answer == 'yes'


def main(model_name: str, input_path: str, out_racist: str, out_non_racist: str):
    # Set up device and 4-bit quantization
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16
    )

    config = dotenv_values(".env")

    # Load model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        "meta-llama/Llama-2-7b-chat-hf",
        use_auth_token=config["HF_TOKEN"],
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto",
        torch_dtype=torch.float16
    )

    processor = PreProcessor()

    with open(input_path, 'r') as infile, \
         open(out_racist, 'w') as racist_out, \
         open(out_non_racist, 'w') as non_racist_out:
        for line in tqdm(infile, desc="Filtering posts"):
            data = json.loads(line)
            # Filter non-English posts
            if data.get('language') != 'en':
                continue

            cleaned = processor.preprocess(data['content'])
            content = cleaned['clean_text']

            # Classify content
            if is_racist(model, tokenizer, content):
                racist_out.write(json.dumps(data) + '\n')
            else:
                non_racist_out.write(json.dumps(data) + '\n')


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
    main(args.model, args.input, args.out_racist, args.out_non_racist)


