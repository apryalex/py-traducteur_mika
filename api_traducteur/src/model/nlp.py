from transformers import pipeline
from config.parametres import VERSIONS
from model.prompt import Prompt

def traduire(prompt:Prompt) :
    if prompt.version == VERSIONS[0] :
        translator = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en")

    prompt.traduction = translator(prompt.atraduire)
    return(prompt)



# def traduire(prompt: Prompt):
#     # Détermination du modèle de traduction en fonction de la version
#     if prompt.version == VERSIONS[0]:  # "fr >> en"
#         translator = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en")
#     elif prompt.version == VERSIONS[1]:  # "en >> fr"
#         translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")
#     else:
#         raise ValueError(f"Version {prompt.version} non supportée.")

#     try:
#         # Utilisation du traducteur
#         translation_result = translator(prompt.atraduire)
#         # Extraction du texte traduit
#         prompt.traduction = translation_result[0]['translation_text']
#     except Exception as e:
#         print(f"Erreur lors de la traduction : {e}")
#         raise

#     return prompt