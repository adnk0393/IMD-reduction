# Trained Models Repository

This repository hosts the pre-trained machine learning models, feature scalers, and label encoders generated during the study submitted to *Computers & Geosciences*. These assets enable reproducible deployment of the classification and predictive models developed in our paper.

## ⚠️ Critical Data Prerequisites

To ensure accurate predictions, input datasets must strictly adhere to the following preprocessing conditions:

* **Molar Scale:** All models expect mineral compositions to be in **molar % (mol%)** scale.
* **Anion Exclusion:** Ensure input compositions **do not contain anions** (e.g., F, Cl, S). If present, remove them before processing.
* **Normalization:** After removing anions and converting to mol%, you must **rescale the remaining data to 100%**.
* **Feature Scaling:** Except for the Random Forest (`RF`) models, all algorithms require feature scaling. You must use the specific, matching scaler model included alongside the respective predictive model.

---

## 📂 File Naming Conventions

All saved objects are organized systematically using the syntax below:

| Object Type | File Naming Pattern | Description |
| :--- | :--- | :--- |
| **Model** | `_<input_combination>.mdl` | The trained machine learning classifier/regressor. |
| **Scaler** | `Scaler__<input_combination>.scl` | The normalization/standardisation model for features. |
| **Label Encoder** | `Labeler__<input_combination>.lbl` | The encoder used to map categorical targets back to text. |

### Input Combination Protocols
Transform your input data into one of the following formats based on the specific model requirements:

* **C1:** Raw oxide composition (no additional chemical transformation needed).
* **C2:** Modified system replacing individual divalent elements with a combined parameter:  
  `M = FeO + MnO + MgO`
* **C3:** Same as **C2**, but additionally groups the alkalies together:  
  `M = FeO + MnO + MgO` and `A = Na2O + K2O`
* **C4:** Dimensionality-reduced features using our pre-trained Principal Component model:  
  `_model_C4_5_components.pc`

---

## ⚙️ Model Implementation Pipeline

Execute the following sequential workflow to pass your raw geological data through the pipeline and generate predictions:

```text
[Raw Mineral Composition (wt%)]
               │
               ▼
[Convert to Mineral Composition (mol%)]
               │
               ▼
[Apply Input Combination Transformation (C1, C2, C3, or C4)]
               │
               ▼
[Rescale Transformed Composition to 100%]
               │
               ▼
[Apply Feature Scaling (Using the appropriate .scl file — skip for RF)]
               │
               ▼
[Generate Model Prediction (Using the target .mdl file)]
               │
               ▼
[Decode Model Output (Using the matching .lbl file)]
```

---

## 🛠️ Environment & Dependencies

To ensure compatibility and avoid serialization errors when loading the `.mdl`, `.scl`, and `.lbl` files, please use the environment setup files provided in the root directory of this repository (`requirements.txt`).
