from setuptools import setup, find_packages

setup(
    name="Ahri_API",                      # Nome del pacchetto
    version="1.0",                      # Versione del pacchetto
    packages=find_packages(),             # Trova tutte le cartelle contenenti moduli
    install_requires=[                    # Dipendenze (se presenti)
        # "requests", # Aggiungi dipendenze come requests, se necessario
    ],
    author="Ahristogatti",                 # Tuo nome
    author_email="dbaitelli97@gmail.com.com",  # La tua email
    description="Una libreria per interagire con le API di Riot Games",  # Descrizione del pacchetto
    long_description=open('README.md').read(),  # Descrizione lunga (legge dal file README)
    long_description_content_type="text/markdown",  # Tipo di contenuto del README
    url=" ",  # URL del progetto (opzionale)
    classifiers=[                          # Classificatori (utile per la ricerca su PyPI)
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',               # Versione minima di Python
)
