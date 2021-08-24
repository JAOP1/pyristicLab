# pyristicLab

## Instalar
Para ejecutar el proyecto se necesita cumplir los requerimientos:

- Dash python
- Dash boostrap
- Pyristic 
- plotly

```
conda create --name pyristic-env
pip install pyristic
pip install dash
pip install dash-bootstrap-components
```
*Sí ya se tiene pyristic instalado, es importante tener la versión más reciente.*
```
pip install pyristic --upgrade
``` 

## Observaciones
Para aplicar pyristicLab, es necesario incluir el problema a resolver en la variable **optimizationProblem** del archivo *testFile.py*. Recuerda que el formato se encuentra descrito en [pyristic funciones de prueba](https://jaop1.github.io/pyristic/helpers/).

## Ejecutar el proyecto
```
python main.py
```


¡Listo a optimizar tu función!
