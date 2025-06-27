---
tags:
- setfit
- sentence-transformers
- text-classification
- generated_from_setfit_trainer
widget: []
metrics:
- accuracy
pipeline_tag: text-classification
library_name: setfit
inference: true
base_model: sentence-transformers/paraphrase-mpnet-base-v2
---

# SetFit with sentence-transformers/paraphrase-mpnet-base-v2

This is a [SetFit](https://github.com/huggingface/setfit) model that can be used for Text Classification. This SetFit model uses [sentence-transformers/paraphrase-mpnet-base-v2](https://huggingface.co/sentence-transformers/paraphrase-mpnet-base-v2) as the Sentence Transformer embedding model. A [LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html) instance is used for classification.

The model has been trained using an efficient few-shot learning technique that involves:

1. Fine-tuning a [Sentence Transformer](https://www.sbert.net) with contrastive learning.
2. Training a classification head with features from the fine-tuned Sentence Transformer.

## Model Details

### Model Description
- **Model Type:** SetFit
- **Sentence Transformer body:** [sentence-transformers/paraphrase-mpnet-base-v2](https://huggingface.co/sentence-transformers/paraphrase-mpnet-base-v2)
- **Classification head:** a [LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html) instance
- **Maximum Sequence Length:** 512 tokens
<!-- - **Number of Classes:** Unknown -->
<!-- - **Training Dataset:** [Unknown](https://huggingface.co/datasets/unknown) -->
<!-- - **Language:** Unknown -->
<!-- - **License:** Unknown -->

### Model Sources

- **Repository:** [SetFit on GitHub](https://github.com/huggingface/setfit)
- **Paper:** [Efficient Few-Shot Learning Without Prompts](https://arxiv.org/abs/2209.11055)
- **Blogpost:** [SetFit: Efficient Few-Shot Learning Without Prompts](https://huggingface.co/blog/setfit)

## Uses

### Direct Use for Inference

First install the SetFit library:

```bash
pip install setfit
```

Then you can load this model and run inference.

```python
from setfit import SetFitModel

# Download from the 🤗 Hub
model = SetFitModel.from_pretrained("setfit_model_id")
# Run inference
preds = model("I loved the spiderman movie!")
```

<!--
### Downstream Use

*List how someone could finetune this model on their own dataset.*
-->

<!--
### Out-of-Scope Use

*List how the model may foreseeably be misused and address what users ought not to do with the model.*
-->

<!--
## Bias, Risks and Limitations

*What are the known or foreseeable issues stemming from this model? You could also flag here known failure cases or weaknesses of the model.*
-->

<!--
### Recommendations

*What are recommendations with respect to the foreseeable issues? For example, filtering explicit content.*
-->

## Training Details

### Training Hyperparameters
- batch_size: (16, 16)
- num_epochs: (3, 3)
- max_steps: -1
- sampling_strategy: oversampling
- num_iterations: 40
- body_learning_rate: (2e-05, 2e-05)
- head_learning_rate: 2e-05
- loss: CosineSimilarityLoss
- distance_metric: cosine_distance
- margin: 0.25
- end_to_end: False
- use_amp: True
- warmup_proportion: 0.15325055144065805
- l2_weight: 0.01
- seed: 42
- eval_max_steps: -1
- load_best_model_at_end: False

### Training Results
| Epoch  | Step | Training Loss | Validation Loss |
|:------:|:----:|:-------------:|:---------------:|
| 0.0020 | 1    | 0.5411        | -               |
| 0.1020 | 50   | 0.335         | -               |
| 0.2041 | 100  | 0.3391        | -               |
| 0.3061 | 150  | 0.3258        | -               |
| 0.4082 | 200  | 0.3264        | -               |
| 0.5102 | 250  | 0.3508        | -               |
| 0.6122 | 300  | 0.3355        | -               |
| 0.7143 | 350  | 0.347         | -               |
| 0.8163 | 400  | 0.3361        | -               |
| 0.9184 | 450  | 0.3417        | -               |
| 1.0204 | 500  | 0.3238        | -               |
| 1.1224 | 550  | 0.3315        | -               |
| 1.2245 | 600  | 0.3446        | -               |
| 1.3265 | 650  | 0.3415        | -               |
| 1.4286 | 700  | 0.3282        | -               |
| 1.5306 | 750  | 0.3435        | -               |
| 1.6327 | 800  | 0.3483        | -               |
| 1.7347 | 850  | 0.3382        | -               |
| 1.8367 | 900  | 0.3375        | -               |
| 1.9388 | 950  | 0.3288        | -               |
| 2.0408 | 1000 | 0.3307        | -               |
| 2.1429 | 1050 | 0.3397        | -               |
| 2.2449 | 1100 | 0.3583        | -               |
| 2.3469 | 1150 | 0.3241        | -               |
| 2.4490 | 1200 | 0.3245        | -               |
| 2.5510 | 1250 | 0.3469        | -               |
| 2.6531 | 1300 | 0.3392        | -               |
| 2.7551 | 1350 | 0.3412        | -               |
| 2.8571 | 1400 | 0.3328        | -               |
| 2.9592 | 1450 | 0.334         | -               |

### Framework Versions
- Python: 3.10.8
- SetFit: 1.1.2
- Sentence Transformers: 4.1.0
- Transformers: 4.52.4
- PyTorch: 2.7.1+cu118
- Datasets: 3.6.0
- Tokenizers: 0.21.1

## Citation

### BibTeX
```bibtex
@article{https://doi.org/10.48550/arxiv.2209.11055,
    doi = {10.48550/ARXIV.2209.11055},
    url = {https://arxiv.org/abs/2209.11055},
    author = {Tunstall, Lewis and Reimers, Nils and Jo, Unso Eun Seo and Bates, Luke and Korat, Daniel and Wasserblat, Moshe and Pereg, Oren},
    keywords = {Computation and Language (cs.CL), FOS: Computer and information sciences, FOS: Computer and information sciences},
    title = {Efficient Few-Shot Learning Without Prompts},
    publisher = {arXiv},
    year = {2022},
    copyright = {Creative Commons Attribution 4.0 International}
}
```

<!--
## Glossary

*Clearly define terms in order to be accessible across audiences.*
-->

<!--
## Model Card Authors

*Lists the people who create the model card, providing recognition and accountability for the detailed work that goes into its construction.*
-->

<!--
## Model Card Contact

*Provides a way for people who have updates to the Model Card, suggestions, or questions, to contact the Model Card authors.*
-->