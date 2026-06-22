**Notes**

- The models expect mineral compositions to be in molar% scale.


- Ensure the compositions being fed to model donot have anions (e.g. F, Cl, S). Rescale data to 100%.


- All the models (**except Random Forest: RF**) require data to be scaled using the appropriate scaler models (included with their respective model).
  
  
- Naming convention for models, scalers and label encoders:

    **Model**: <model>_<input_combination>.mdl
  
    **Scaler**: Scaler_<model>_<input_combination>.scl
  
    **Label Encoders**: Labeler_<model>_<input_combination>.lbl
  

- Input combination (to be done in mol% composition only):

     **C1** : raw oxide (no transformation needed).
  
     **C2** : replace FeO, MnO and MgO with M (= FeO + MnO + MgO).
  
     **C3** : As C2, but also replace Na2O and K2O with A (=Na2O + K2O).
  
     **C4** : transform the data using pre-trained PC model (naming convention: <PC>_model_C4_5_components.pc).
  

- General pipeline for model implementation is:

Mineral composition (wt%) -> Mineral composition (mol%) -> Transform the composition for input combination -> Rescale the composition -> Model prediction -> Decode predictions using **label Encoder**.
