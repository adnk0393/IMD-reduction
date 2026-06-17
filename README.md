# MinNet

MinNet is a implementation of IMD reduction method to demonstrate its effect on automated mineral classification. It features a Streamlit web application that demonstrates how aggregating substituting cations in a mineral composition affects dimensionality reduction. The repository also includes comprehensive scripts for demonstration of model training, and validation used in the study.

## 📁 Repository Structure

* **`main.py`**: Main Streamlit web application for interactive data visualization.
* **`model training and validation/`**: Directory containing Python scripts for model training and evaluation used in the study.
* **`data/`**: Directory containing the training and validation datasets used in the study.

## 🚀 Key Features

* **Cation Aggregation**: Simplifies complex mineral compositions by summing up substituting elements.
* **Machine Learning Pipeline**: Includes reproducible scripts to train and validate classification models.
* **Interactive UI**: Offers an intuitive Streamlit interface to test the app in real-time.

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

## 🛠️ Installation

1. Clone this repository:
   ```bash
   git clone https://github.com](https://github.com/adnk0393/MinNet_v1/
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
