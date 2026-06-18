# Inherent mineral dimensionality (IMD) reduction
## 🌟 Core Overview

Automated mineral identification from oxide analyses faces major hurdles: high dimensionality (many measured oxides), compositional redundancy (overlapping elemental substitutions), and severe class imbalance (uneven representation of minerals). 

Conventional approaches (e.g., PCA, SMOTE) are unable on their own to resolve intra-class compositional bias caused by incomplete compositional representation and redundancy. For example, while iron and magnesium substitute for one another in Fe-Mg minerals, treating them as separate variables inflates dimensionality without providing novel crystal-chemical insight. Furthermore, because Mg-rich olivines are far more common than Fe-rich variants in nature, a model trained on such imbalanced datasets will inherently struggle to classify rare Fe-rich compositions, despite their shared structural identity.

**IMD Reduction** solves this as a domain-informed preprocessing step. It converts raw oxide analyses into moles and aggregates substitutable oxides into crystallographically meaningful variables prior to machine-learning classification:
* **M-site aggregation:** Fe + Mg + Mn → M
* **A-site aggregation:** Na + K → A

This framework removes compositional redundancy, enforces strict stoichiometric consistency, and embeds crystal-chemical logic directly into your model's input space.

---

## 🚀 Key Features

* **Crystal-Chemical Preprocessing:** Aggregates oxides in mol.% into structural site variables to enforce physical petrological constraints.
* **Rigorous Benchmark Suite:** Codebase to deploy and evaluate **12 classifier-input combinations** across 3 machine learning algorithms (Support Vector Machines, k-Nearest Neighbors, Random Forests) and 4 input schemes (raw oxides, PCA, IMD-M, and IMD-M+A).
* **High-Performance Training Pipeline:** Tailored for large mineral-chemistry datasets, originally benchmarked on a curated baseline of **47,031 normalized oxide compositions** spanning 19 common rock-forming minerals.
* **Proven Stability (>99% Accuracy):** Built-in evaluation tracking proves that IMD-reduced inputs (especially the M+A variant) maintain stable class-wise performance (>99%), dramatically outperforming raw oxides or PCA on compositionally complex groups (amphiboles, pyroxenes, garnets) and rare boundary-proximal compositions.
* **Independent Validation Module:** Includes data and pipelines to test model generalization using an independent compilation of **3,445 mineral compositions** to pinpoint and evaluate edge cases (e.g., amphibole-pyroxene overlaps).
* **MinNet Integration:** Contains the backend engine powering **MinNet**, a deployed web tool that integrates IMD reduction for rapid, reproducible mineral-group identification from unlabeled electron microprobe (EPMA) or SEM-EDS datasets.

---
## 📊 Experimental Setup

MinNet evaluates **three machine learning models** across **four distinct input combinations (C1–C4)** to study the effects of chemical abstraction and dimensionality reduction:

### Models Evaluated
* **KNN** (K-Nearest Neighbors)
* **SVM** (Support Vector Machine)
* **RF** (Random Forest)

### Input Feature Combinations
* **C1 (Raw Composition)**: 11 standard oxides (SiO₂, TiO₂, Al₂O₃, FeO, MnO, MgO, CaO, Na₂O, K₂O, P₂O₅, CO₂).
* **C2 (Divalent Aggregation)**: Aggregates FeO, MnO, and MgO into a single feature (M) via summation.
* **C3 (Dual Aggregation)**: Aggregates (FeO + MnO + MgO) into one feature (M), and Alkali metals (Na₂O + K₂O) into another (A).
* **C4 (PCA Representation)**: A 5-component Principal Component Analysis (PCA) representation of C1, optimized via scree plot analysis.

## 📁 Repository Structure
* **`MinNet app`**: Main Streamlit web application (using KNN and C3 combination) for interactive data visualization.
* **`Pre-processing scripts`**: Contains the Python scripts used to pre-process GEOROC dataset files to obtain representative training data.
* * **`Trained model`**: Contains the models generated (alongwith data scalering and labeling functions) during the study. 
* **`Data/`**: Contains the training and validation datasets used in the study.
* **`Model training and validation/`**: Contains Python scripts for model training and evaluation used in the study.

## Requirements

### Prerequisites
* **Python 3.10.11** 

### Dependencies
All required libraries are listed in the requirements.txt file. Install them using pip:

```bash
pip install -r main/requirements.txt
## 🛠️ Installation


1. Clone this repository:
   ```bash
   git clone https://github.com](https://github.com/adnk0393/MinNet_v1/](https://github.com/adnk0393/IMD-reduction/
   cd MinNet
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

### Running the Streamlit App
Launch the interactive web application to visualize dimensionality reduction:
```bash
streamlit run app.py
```

### Training and Evaluation
Run the pipeline scripts to retrain or evaluate the KNN, SVM, and RF models across combinations C1–C4:
```bash
python scripts/train.py
python scripts/evaluate.py
```

## 📄 License

This project is licensed under the **GNU GPL v2.0 License** - see the [LICENSE](LICENSE) file for details.
