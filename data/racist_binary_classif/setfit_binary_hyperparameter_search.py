from setfit import SetFitModel, SetFitTrainer
from datasets import Dataset
from sentence_transformers.losses import CosineSimilarityLoss
import json
import optuna

"""
Trial 0 finished with value: 1.0 and parameters: {'num_iterations': 40, 'num_epochs': 3, 'learning_rate': 9.567953418283748e-06, 'batch_size': 16, 'warmup_proportion': 0.15325055144065805}. Best is trial 0 with value: 1.0.
"""

# 1) Load & clean your data
with open("data/racist_binary_classif/labeled.jsonl", "r", encoding="utf-8") as f:
    examples = [json.loads(line) for line in f]

from data.preprocessor import PreProcessor
processor = PreProcessor()

cleaned = []
for ex in examples:
    if ex.get("label") in [0, 1] and ex.get("content"):
        cleaned_text = processor.preprocess(ex["content"])["clean_text"]
        cleaned.append({"text": cleaned_text, "label": int(ex["label"])})

dataset = Dataset.from_list(cleaned).shuffle(seed=42)
split = dataset.train_test_split(test_size=0.2)
train_ds, test_ds = split["train"], split["test"]

# 2) Make model_init accept the hparams dict
def model_init(hparams):
    return SetFitModel.from_pretrained("sentence-transformers/paraphrase-mpnet-base-v2")

# 3) Define your (safer) search space
def hp_space(trial):
    return {
        "num_iterations":    trial.suggest_int("num_iterations", 20, 50),
        "num_epochs":        trial.suggest_int("num_epochs", 1, 3),
        "learning_rate":     trial.suggest_float("learning_rate", 1e-6, 5e-5, log=True),
        "batch_size":        trial.suggest_categorical("batch_size", [8, 16]),
        "warmup_proportion": trial.suggest_float("warmup_proportion", 0.0, 0.3),
    }

# 4) Build the trainer with mixed-precision turned on
trainer = SetFitTrainer(
    model_init=model_init,
    train_dataset=train_ds,
    eval_dataset=test_ds,
    loss_class=CosineSimilarityLoss,
    seed=42,
    use_amp=True,         
)

best_run = trainer.hyperparameter_search(
    hp_space=hp_space,
    n_trials=20,
    direction="maximize",
    backend="optuna",
)

trainer.apply_hyperparameters(best_run.hyperparameters, final_model=True)

trainer.train()

trainer.model.save_pretrained("data/racist_binary_classif/best-setfit-model")
print("✅ Trained & saved best model at data/racist_binary_classif/best-setfit-model")
