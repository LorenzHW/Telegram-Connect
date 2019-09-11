#!/bin/bash
# NOTE: The 'ask deploy --profile "default" --target "lambda"' command takes all site pages inside the .venv folder and
# puts it into the lambda_upload folder. If you don't the .venv folder, use the post_new_hook.sh
# Forget the pre_deploy_hook if you are working with conda

# First copies installed packages from conda environment to virtualenv used inside lambda upload, cuz pip install does not work inside virtualenv....
# Deploys the folder lambda_upload to AWS and then removes it otherwise pycharme is indexing
cp -r /Users/lorenzhofmann-wellenhof/anaconda3/envs/alexa-skills/lib/python3.7/site-packages /Users/lorenzhofmann-wellenhof/Desktop/Coding/github.com/LorenzHW/My-Telegrams/.venv/skill_env/lib/python3.7/
ask deploy --profile "default" --target "lambda"
rm -r lambda/us-east-1_myTelegrams/lambda_upload/