from setuptools import setup

APP = ['programamoneda.py']  # Reemplaza 'nombre_del_archivo.py' con el nombre real de tu archivo Python

OPTIONS = {
    'argv_emulation': True,
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
