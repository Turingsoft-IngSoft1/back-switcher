# back-switcher

## **Requerimientos Linux:**
```
sudo apt install python3 python3-pip python3-venv
=======
## Sinopsis

El proyecto se titula **El Switcher**.

 La aplicación web **Switcher** es una plataforma en línea que digitaliza el popular juego de mesa Switcher, proporcionando una experiencia de juego interactiva de hasta 4 jugadores online. Permite a los usuarios disfrutar del conocido juego de mesa en un formato virtual, simple y fiel al original.

## Requerimientos para montar la aplicación (back-end):

***Instalar la ultima version de Python y Pip***

```
sudo apt install python3 python3-pip
```

***Crear entorno virtual:***

```
python3 -m venv .venv
```

***Entrar al entorno virtual e instalar dependencias:***

```
source .venv/bin/activate
```

```
pip install -r requirements.txt
```

***Como correr el servidor:***

```
uvicorn main:app --reload
```

***Como correr los test:***

```
pytest
```

***Para salir del entorno virutal:***

```
deactivate
```

## **Requerimientos en windows:**

## **Tener instalado python3 en la version más actual:**
```
https://www.python.org/downloads/
```

***Instalar dependencias:***

```
python3 -m pip install -r requirements.txt
```

***Como correr el servidor:***
```
python3 -m uvicorn main:app --reload
```
***Como correr los test:***

```
python3 -m pytest
```