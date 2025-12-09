#!/bin/bash
# Script para ejecutar en Railway
cd backend
python manage.py reset_and_populate --no-input
