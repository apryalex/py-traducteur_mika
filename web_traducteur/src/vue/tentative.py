import pytest
import uuid
import requests
import streamlit as st
from traducteur_app import TraducteurApp  # Remplacez par le nom de votre module

# Utilitaire pour capturer les exceptions et les logs Streamlit
class StreamlitCapture:
    def __init__(self):
        self.messages = []

    def write(self, msg):
        self.messages.append(msg)

@pytest.fixture
def app():
    return TraducteurApp()

def test_add_form(app):
    # Simuler l'état de session
    st.session_state["logged_in"] = "test_user"
    
    # Créer une capture pour les messages Streamlit
    capture = StreamlitCapture()
    st.write = capture.write
    
    # Simuler l'entrée utilisateur
    option = "test_version"
    atraduire = "Bonjour"
    
    # Préparer les données pour la requête
    data = {
        "atraduire": atraduire,
        "version": option,
        "utilisateur": st.session_state["logged_in"]
    }
    
    # Simuler la réponse du serveur de traduction
    response_data = {
        "traduction": [{"translation_text": "Hello"}]
    }
    
    # Envoyer une requête POST simulée
    response = requests.post(app.URL_TRADUCTEUR, json=data)
    
    # Vérifier la réponse
    if response.status_code == 200:
        app.add_form(option)
        
        # Vérifier que les clés sont générées et ajoutées correctement
        generated_keys = set()
        for call in st.write.call_args_list:
            args, kwargs = call
            key = kwargs['key']
            assert key not in generated_keys, f"Duplicate key found: {key}"
            generated_keys.add(key)
        
        assert "Voici votre traduction !" in capture.messages
        assert "Bonjour" in capture.messages
        assert "Hello" in capture.messages
    else:
        assert False, f"Erreur : {response.status_code}"

if __name__ == "__main__":
    pytest.main()

# import pytest
# from unittest.mock import patch, Mock
# from traducteur_app import TraducteurApp  # Remplacez par le nom de votre module

# # Mocking streamlit components
# @patch('your_module.st')
# @patch('your_module.requests.get')
# def test_add_chat(mock_get, mock_st):
#     # Simuler une réponse JSON de l'API
#     mock_response = Mock()
#     mock_response.status_code = 200
#     mock_response.json.return_value = [
#         {"atraduire": "Message 1", "traduction": "Translation 1"},
#         {"atraduire": "Message 2", "traduction": "Translation 2"},
#         {"atraduire": "Message 3", "traduction": "Translation 3"},
#         {"atraduire": "Message 4", "traduction": "Translation 4"},
#         {"atraduire": "Message 5", "traduction": "Translation 5"},
#         {"atraduire": "Message 6", "traduction": "Translation 6"},
#         {"atraduire": "Message 7", "traduction": "Translation 7"},
#         {"atraduire": "Message 8", "traduction": "Translation 8"},
#         {"atraduire": "Message 9", "traduction": "Translation 9"},
#         {"atraduire": "Message 10", "traduction": "Translation 10"}
#     ]
#     mock_get.return_value = mock_response

#     # Initialiser l'application
#     app = TraducteurApp()

#     # Définir l'état de session
#     mock_st.session_state = {"logged_in": "user123"}

#     # Appeler la méthode add_chat
#     app.add_chat()

#     # Vérifier que les clés sont uniques
#     generated_keys = set()
#     for call in mock_st.message.call_args_list:
#         args, kwargs = call
#         key = kwargs['key']
#         assert key not in generated_keys, f"Duplicate key found: {key}"
#         generated_keys.add(key)

# if __name__ == "__main__":
#     pytest.main()
    
    
    
# import uuid
# import pytest
# def test_unique_keys():
#     #simule des message de chat avec 10 entrée
#     chat_messages = [
#         {"atraduire": "Message 1", "traduction": "Translation 1"},
#         {"atraduire": "Message 2", "traduction": "Translation 2"},
#         {"atraduire": "Message 3", "traduction": "Translation 3"},
#         {"atraduire": "Message 4", "traduction": "Translation 4"},
#         {"atraduire": "Message 5", "traduction": "Translation 5"},
#         {"atraduire": "Message 6", "traduction": "Translation 6"},
#         {"atraduire": "Message 7", "traduction": "Translation 7"},
#         {"atraduire": "Message 8", "traduction": "Translation 8"},
#         {"atraduire": "Message 9", "traduction": "Translation 9"},
#         {"atraduire": "Message 10", "traduction": "Translation 10"}
#     ]

#     keys = set()
    
#     for prompt in chat_messages:
#         user_key = str(uuid.uuid4())
#         bot_key = str(uuid.uuid4())

#         # Vérifie si les clés sont bien unique
#         assert user_key not in keys, f"Clé utilisateur dupliquée trouvée: {user_key}"
#         assert bot_key not in keys, f"Clé bot dupliquée trouvée: {bot_key}"

#         keys.add(user_key)
#         keys.add(bot_key)

# if __name__ == "__main__":
   
#     pytest.main()

