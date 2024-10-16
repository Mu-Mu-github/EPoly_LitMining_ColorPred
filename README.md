# EPoly_LitMining_ColorPred

Demos and supporting data for literature mining and color prediction of electrochromic polymers (ECPs) to enable autonomous experimentation.

# Installation

We recommend installing the package by following the instructions below.

```
conda create --name env-ecp python=3.12
conda activate env-ecp
git clone https://github.com/polybot-nexus/EPoly_LitMining_ColorPred.git
cd EPoly_LitMining_ColorPred
python -m pip install -r requirements.txt
```

# Demostrations

## Demo 1: Literature Mining workflow

Large language model (LLM) assisted extraction of chemical information. See [```demo1.ipynb```](demo1.ipynb).

[<img src="docs/demo1.png">](demo1.ipynb)

## Demo 2: ECPs color prediction webapp

A transformer model for predicting CIELab and Absorption spectra of ECPs. Visit <https://polybot-ecps.streamlit.app/>.

[<img src="docs/demo2.png">](https://polybot-ecps.streamlit.app/)

## Other Demostrations

- ```notebooks/1_ECPs_database_analysis.ipynb``` Plotting the statistics on our database and analysing the trends.
- ```notebooks/2_model_comparison.ipynb``` Comparison of several models on literature data.
- ```notebooks/3_sequential_learning.ipynb``` Model performance on in-house data and finetune it on new data
- ```notebooks/4_physical_insights.ipynb``` After having a full operational model we try to extract feature importances

# Train your own models based on the prefered monomer representation

    python train.py --model <model> --training_data <data> --save_dir <save_dir> -n_epochs <epochs> -lr <learning_rate> --abs_prediction

- `model` The molecular embeddings to use. Choose among:
    - morgan
    - dft
    - mordred
- `training_data` The location of the .csv file containing the molecular pairs for training
- `save_dir` The directory to save the trained model 
- `n_epochs` The number of epochs to use for training    
- `lr` Learning rate
- `use_abs_decoder` Set is to `True` to request absorption spectra prediction 

Example

    python train.py --training_data "datasets/electrochromics_in_house_experiments_with_abs.csv" --save_dir checkpoints -n_epochs 10 -lr 0.01 --dropout_ratio 0.15


