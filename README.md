# MinNet: IMD preprocessing for automated mineral-group classification
## 🌟 Core overview

MinNet is a Python/Streamlit implementation of Inherent Mineral Dimensionality (IMD) preprocessing for automated mineral-group classification from oxide-composition tables. It is designed for EPMA- and SEM–EDS-derived mineral analyses where the input consists of major-oxide wt.% values rather than image-based mineral maps.

Automated mineral identification from oxide tables is difficult because such datasets commonly contain incomplete oxide reporting, uneven class representation and chemically redundant variables. IMD addresses the redundancy part of this problem by converting oxide wt.% values to normalized mol.% and then aggregating selected substitutable oxides into fixed, chemically interpretable features before supervised classification.

In the implementation used here:

- FeO + MgO + MnO are combined into a ferromagnesian aggregate, M.
- Na2O + K2O are combined into an alkali aggregate, A.

These aggregate variables are not intended to represent complete crystallographic site occupancies for all mineral groups. They are crystal-chemically motivated proxies for major substitutional trends relevant to group-level mineral classification.

---

## 🚀 Key features

- Domain-informed preprocessing of oxide-composition tables using IMD feature aggregation.
- Evaluation of 12 classifier-input combinations using three classifiers: Support Vector Machine, k-Nearest Neighbors and Random Forest.
- Four input schemes: raw oxides, IMD-M, IMD-M+A and PCA-transformed inputs.
- Training and testing on 47,031 normalized oxide compositions spanning 19 common rock-forming mineral groups.
- External validation on 3,445 independently compiled mineral compositions.
- Streamlit-based MinNet application for reproducing and performing group-level mineral identification from EPMA- or SEM–EDS-derived oxide tables.

## 📊 Experimental Setup

MinNet evaluates **three machine learning models** across **four distinct input combinations (C1–C4)** to study the effects of chemical abstraction and dimensionality reduction:

### Models Evaluated
* **KNN** (K-Nearest Neighbors)
* **SVM** (Support Vector Machine)
* **RF** (Random Forest)

### Input Feature Combinations
* **C1 (Raw Composition)**: 11 standard oxides (SiO₂, TiO₂, Al₂O₃, FeO, MnO, MgO, CaO, Na₂O, K₂O, P₂O₅, CO₂).
* **C2 (IMD-M)**: Replaces FeO, MnO and MgO with the ferromagnesian aggregate M = FeO + MnO + MgO.
* **C3 (IMD-M+A)**: Replaces FeO, MnO and MgO with M, and Na2O and K2O with the alkali aggregate A = Na2O + K2O.
* **C4 (PCA Representation)**: A 5-component Principal Component Analysis (PCA) representation of C1, optimized via scree plot analysis.

---

## 📁 Repository Structure
* **`MinNet/`**: Streamlit application source codes for mineral-group prediction using the trained KNN model and C3 input scheme.
* **`Pre-processing scripts/`**: Scripts used to preprocess and filter mineral-composition datasets.
* **`Trained model/`**: Trained models, scaler objects and label-encoding files generated during the study.
* **`Data/`**: Training, testing and external-validation datasets used in the manuscript.
* **`Model training and validation/`**: Notebooks/scripts used for model training, validation and benchmark evaluation.
* **`requirements.txt`**: Python package dependencies required to run the application and reproduce the workflow.

---

## Requirements

### Prerequisites
* **Python 3.10.11**
* **Jupyter Notebook** (Only for training and evaluating the ML models)
* **Streamlit** package (Only for running the MinNet app offline)

### Required Python libraries
All required libraries are listed in the requirements.txt file. Install them using pip:

1. Clone this repository:
   ```bash
   git clone https://github.com](https://github.com/adnk0393/MinNet_v1/](https://github.com/adnk0393/IMD-reduction/
   cd IMD-reduction
   ```
2. Install required python libraries (assumes python is already installed)
```bash
   pip install -r main/requirements.txt
```

---

## 💻 How to use

### Running the Streamlit App 
Visit the link: https://minnet.streamlit.com

### Running the Streamlit App offline
Launch the interactive web application to visualize dimensionality reduction:
```bash
cd IMD-reduction-fixed-main
streamlit run MinNet/main.py
```

### Training and Evaluation
Run the scripts (.ipynb) using Jupyter notebook to retrain or evaluate the KNN, SVM, and RF models across combinations C1–C4:
```bash
cd IMD-reduction-fixed-main/model training and evaluation scripts/
jupyter notebook
```
**Note:** Ensure that the training and validation datasets are available in the expected folder path specified in each notebook. The first column should contain a sample or point identifier, such as `SNo`, and should not be one of the oxide-composition columns. The order of oxide columns does not matter if all required oxide columns are present with the expected names.

---

## Contributors

[Aditya Naik (Post-doctoral Fellow, IISER Mohali)](mailto:naik32.an@gmail.com)

[Sourabh Bhattacharya (Assistant Professor, IISER Mohali)](mailto:sourabh@iisermohali.ac.in)

[Jitendra Kumar Roy (NPDF Fellow, IIT Kharagpur)](mailto:royjitendra11@gmail.com)

[Krishna Oraon (PhD Scholar, IISER Mohali)](mailto:ph24082@iisermohali.ac.in)

---

## 📄 License

This project is licensed under the **GNU GPL v2.0 License** - see the [LICENSE](LICENSE) file for details.
