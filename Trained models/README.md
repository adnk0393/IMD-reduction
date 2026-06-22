**Notes**

- The models expect mineral compositions to be in molar% scale.

- - Ensure the compositions being fed to model donot have anions (e.g. F, Cl, S). Rescale data to 100%.

- All the models (**except Random Forest: RF**) require data to be scaled using the appropriate scaler models (included with their respective model).

- Naming convention for models, scalers and label encoders:

    **Model**: <model>_<input_combination>.mdl
  
    **Scaler**: Scaler_<model>_<input_combination>.scl
  
    **Label Encoders**: Labeler_<model>_<input_combination>.lbl

- General pipeline for model implementation is:

Mineral composition (wt%) -> Mineral composition (mol%) -> Remove anions from mineral compositions -> Transform the composition for input combination -> Scale the composition -> Model prediction -> Use label_encoder to decode the prediction.
