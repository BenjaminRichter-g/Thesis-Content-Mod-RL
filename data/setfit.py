from setfit import SetFitModel, SetFitTrainer
from datasets import Dataset
import numpy as np

train_texts = [
    "I despise these people and want them gone.",
    "What a lovely day!",
    "They’re absolutely disgusting and don’t belong here.",
    "I had a great time at the concert.",
]
train_labels = [1, 0, 1, 0]

train_dataset = Dataset.from_dict({
    "text": train_texts,
    "label": train_labels
})

model = SetFitModel.from_pretrained("sentence-transformers/paraphrase-MiniLM-L6-v2")

trainer = SetFitTrainer(
    model=model,
    train_dataset=train_dataset,
    eval_dataset=train_dataset,
    batch_size=8,
    num_iterations=10,
    num_epochs=1,
    metric="accuracy",
)

trainer.train()
metrics = trainer.evaluate()
print(f"▶️ Evaluation metrics: {metrics}")
