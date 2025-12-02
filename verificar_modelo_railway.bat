@echo off
echo Verificando modelo ML en Railway...
echo.
railway ssh -c "ls -lh backend/ml_models/"
echo.
echo Si ves los archivos failure_prediction_model.pkl y label_encoders.pkl, el modelo existe.
echo Si no los ves, necesitas entrenar el modelo.
pause
