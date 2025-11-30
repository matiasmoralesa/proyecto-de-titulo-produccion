#!/bin/bash
set -e

echo "Loading data from backup..."
python backend/manage.py loaddata backend/data_backup.json --settings=config.settings.railway

echo "Data loaded successfully!"
