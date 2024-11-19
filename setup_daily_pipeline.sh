#!/bin/bash

# Define variables
SCRIPT_PATH="/Users/mdayanarshad/Desktop/Data_Science_Projects/HFT_RealTime_DataPipeline/pipelines/run_pipeline.py"
VENV_PATH="/Users/mdayanarshad/Desktop/Data_Science_Projects/HFT_RealTime_DataPipeline/.conda"
CRON_TIME="0 22 * * *"
LOG_FILE="/Users/mdayanarshad/Desktop/Data_Science_Projects/HFT_RealTime_DataPipeline/pipeline_cronjob.log"  # Log file path

# Check if the Python script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "$(date) - Error: Script $SCRIPT_PATH does not exist. Exiting." >> "$LOG_FILE"
    exit 1
fi

# Check if the virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo "$(date) - Error: Virtual environment $VENV_PATH does not exist. Exiting." >> "$LOG_FILE"
    exit 1
fi

# Create the command to activate the virtual environment and run the script
CMD="source $VENV_PATH/bin/activate && python $SCRIPT_PATH && deactivate"

# Add the cron job
(crontab -l 2>/dev/null | grep -v "$SCRIPT_PATH"; echo "$CRON_TIME $CMD >> $LOG_FILE 2>&1") | crontab -

# Display confirmation and log it
echo "$(date) - Cron job scheduled to run $SCRIPT_PATH daily at 10 PM using the virtual environment $VENV_PATH." >> "$LOG_FILE"

