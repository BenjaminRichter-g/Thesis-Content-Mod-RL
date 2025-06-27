from setfit import SetFitModel, SetFitTrainer
from datasets import Dataset
import json
from sentence_transformers.losses import CosineSimilarityLoss

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

# Load SetFit base model (sentence transformer)
model = SetFitModel.from_pretrained("sentence-transformers/paraphrase-mpnet-base-v2")

# Train
trainer = SetFitTrainer(
    model=model,
    train_dataset=train_ds,
    eval_dataset=test_ds,
    loss_class=CosineSimilarityLoss,
    batch_size=16,
    num_iterations=50,
    column_mapping={"text": "text", "label": "label"},
)

trainer.train()
accuracy = trainer.evaluate()["accuracy"]
print(f"✅ Accuracy: {accuracy:.2f}")

# Save model
trainer.model.save_pretrained("data/racist_binary_classif/racism-setfit-model")
