from setuptools import setup, find_packages

# Nom du package PyPI ('pip install NAME')
NAME = "HLIT"

# Version du package PyPI
VERSION = "0.0.7"  # la version doit être supérieure à la précédente sinon la publication sera refusée

# Facultatif / Adaptable à souhait
AUTHOR = "Random but skilled people"
AUTHOR_EMAIL = ""
URL = ""
DESCRIPTION = ""
LICENSE = ""

# 'orange3 add-on' permet de rendre l'addon téléchargeable via l'interface addons d'Orange 
KEYWORDS = ["orange3 add-on",]

# Tous les packages python existants dans le projet (avec un __ini__.py)
PACKAGES = find_packages()
#PACKAGES = [pack for pack in PACKAGES if "orangecontrib" in pack]
PACKAGES = [pack for pack in PACKAGES if "orangecontrib" in pack and "OWInterface" in pack or pack=="orangecontrib"]
print(PACKAGES)


# Fichiers additionnels aux fichiers .py (comme les icons ou des .ows)
PACKAGE_DATA = {
    "orangecontrib.OWInterface.widgets": ["icons/*"],
}
# /!\ les noms de fichier 'orangecontrib.hkh_bot.widgets' doivent correspondre à l'arborescence

# Dépendances
INSTALL_REQUIRES = ["torch==2.2.2", "sentence-transformers", "gpt4all", "sacremoses", "transformers",
                    "sentencepiece", "optuna", "spacy==3.7.6", "markdown", "uvicorn", "fastapi",
                    "python-multipart"]

# Spécifie le dossier contenant les widgets et le nom de section qu'aura l'addon sur Orange
ENTRY_POINTS = {
    "orange.widgets": (
        "Advanced Artificial Intelligence Tools = orangecontrib.OWInterface.widgets",
    )
}

NAMESPACE_PACKAGES = ["orangecontrib"]

setup(name=NAME,
      version=VERSION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      description=DESCRIPTION,
      license=LICENSE,
      keywords=KEYWORDS,
      packages=PACKAGES,
      package_data=PACKAGE_DATA,
      install_requires=INSTALL_REQUIRES,
      entry_points=ENTRY_POINTS,
      namespace_packages=NAMESPACE_PACKAGES,
      )
