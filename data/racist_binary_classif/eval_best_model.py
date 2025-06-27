from sentence_transformers.losses import CosineSimilarityLoss
import json
from setfit import SetFitModel, Trainer
from datasets import Dataset

# Load and format labeled data
with open("data/racist_binary_classif/labeled.jsonl", "r", encoding="utf-8") as f:
    examples = [json.loads(line) for line in f]

# Optional: apply cleaning
from data.preprocessor import PreProcessor
processor = PreProcessor()

cleaned_examples = []
for ex in examples:
    if ex.get("label") in [0, 1] and ex.get("content"):
        cleaned_text = processor.preprocess(ex["content"])["clean_text"]
        cleaned_examples.append({
            "text": cleaned_text,
            "label": int(ex["label"])
        })

# Convert to HuggingFace Dataset
dataset = Dataset.from_list(cleaned_examples)

# Shuffle & split
dataset = dataset.shuffle(seed=42)
split = dataset.train_test_split(test_size=0.2)
train_ds, test_ds = split["train"], split["test"]


# 2) Load the trained model
model = SetFitModel.from_pretrained("data/racist_binary_classif/best-setfit-model")

# 3) Wrap in a trainer for evaluation
trainer = Trainer(
    model=model,
    train_dataset=None,       # no further training
    eval_dataset=test_ds
)

# 4) Run evaluation
metrics = trainer.evaluate()
print("Test set metrics:")
for k, v in metrics.items():
    print(f"  {k} = {v:.4f}")


from setfit import SetFitModel

# 1) Load your best model
model = SetFitModel.from_pretrained("data/racist_binary_classif/best-setfit-model")

# 2) Confirm the two key sub-modules
print("Encoder module:", model.model_body)
print("Head module:   ", model.model_head)

# 3) Iterate & report
def inspect_module(name, module):
    total, trainable = 0, 0
    print(f"\n=== {name} ===")
    for pname, p in module.named_parameters():
        n = p.numel()
        total += n
        if p.requires_grad:
            trainable += n
        print(f"{pname:50} shape={tuple(p.shape):10}  trainable={p.requires_grad}")
    print(f"→ {name} total: {total:,} params, trainable: {trainable:,}")

inspect_module("Embedding body (model_body)", model.model_body)
inspect_module("Classification head (model_head)", model.model_head)

# 4) Grand total
all_total     = sum(p.numel() for p in model.model_body.parameters()) + sum(p.numel() for p in model.model_head.parameters())
all_trainable = sum(p.numel() for p in model.model_body.parameters() if p.requires_grad) + sum(p.numel() for p in model.model_head.parameters() if p.requires_grad)
print(f"\nOverall model: {all_total:,} params, trainable: {all_trainable:,}")
