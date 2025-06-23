@echo off
REM Activate Python virtual environment
call myenv\Scripts\activate

REM Aggregate user events
echo Aggregating user events...
python data/scripts/aggregate_user_events.py

REM Combine all features for model input
echo Creating combined features...
python data/scripts/create_combined_features.py

REM Train the VAE model
echo Training VAE model...
python deep-learning/train_vae.py

REM Generate layouts for the frontend
echo Generating layouts...
python deep-learning/generate_layouts.py

echo Retraining pipeline complete! 