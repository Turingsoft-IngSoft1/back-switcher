# back-switcher

**Requerimientos:**

sudo apt install python3 python3-pip


***Crear entorno virtual:***
```
python3 -m venv .venv
```
***Instalar dependencias:***
```
source .venv/bin/activate
```
```
python3 -m pip install -r requirements.txt
```
***Como correr el servidor:***
```
python3 -m uvicorn main:app --reload
```
***Para salir del entorno virutal:***
```
deactivate
```
