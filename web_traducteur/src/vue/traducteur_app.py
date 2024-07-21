# traducteur_app.py
import streamlit as st
from streamlit_chat import message
from config.parametres import URL_TRADUCTEUR, URL_VERSIONS, URL_LOGIN, URL_TRADUCTIONS
import requests
import pysnooper
import uuid


class TraducteurApp:
    def __init__(self):
        self.URL_TRADUCTEUR = URL_TRADUCTEUR
        self.URL_VERSIONS = URL_VERSIONS
        self.URL_LOGIN = URL_LOGIN
        self.URL_TRADUCTIONS = URL_TRADUCTIONS
        self.titre = "Traducteur"

        st.set_page_config(
            page_title="Traducteur",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded",
        )

        if "logged_in" not in st.session_state:
            st.session_state["logged_in"] = None

        self.show_login_form()
        self.show_app()

   
    def show_login_form(self):
        """
        Affiche le formulaire de connexion dans la barre latérale.
        Le formulaire permet à l'utilisateur de se connecter.
        """
        def login(username, password):
            """
            Fonction de connexion qui envoie les informations de connexion au serveur et
            met à jour l'état de session si la connexion est réussie.
            """

            data = {
                "login": username,
                "mdp": password
            }

            response = requests.post(self.URL_LOGIN, json=data)

            if response.status_code == 200:
                response_login = response.json()

                if response_login["authentifié"] :
                    st.session_state["logged_in"] = response_login["id"]
            
            if not st.session_state["logged_in"]:
                st.sidebar.error("Nom d'utilisateur ou mot de passe incorrect")

        st.sidebar.title("Connexion")
        username = st.sidebar.text_input("Nom d'utilisateur")
        password = st.sidebar.text_input("Mot de passe", type="password")
        st.sidebar.button("Se connecter", on_click=login, args=(username, password))


    def show_index(self) :
        """
        Affiche le message d'accueil lorsque l'utilisateur n'est pas connecté.
        """
        st.title(self.titre)
        st.write("Veuillez vous connecter pour accéder aux fonctionnalités sécurisées.")
        

    def show_logout_button(self):
        """
        Affiche le bouton de déconnexion dans la barre latérale.
        Permet à l'utilisateur de se déconnecter.
        """
        def logout() :
            """
            Fonction de déconnexion qui réinitialise l'état de session.
            """
            st.session_state["logged_in"] = None
    
        st.sidebar.title("Déconnexion")
        st.sidebar.button("Se déconnecter", on_click=logout)    


    def show_app(self):
        """
        Affiche l'application principale une fois l'utilisateur connecté.
        Permet de sélectionner la version de traduction et d'afficher le formulaire de traduction.
        """
        st.title(self.titre)
        versions = self.get_versions()

        option = st.sidebar.selectbox(
            "Choisissez la traduction à réaliser :",
            versions
        )

        self.add_form(option)

        if st.session_state["logged_in"] :
            self.add_chat()

    def get_versions(self):
        """
        Récupère les versions de traduction disponibles à partir du serveur.
        
        Returns:
            list: Liste des versions disponibles ou message d'erreur en cas d'échec.
        """
        versions = ["Aucune langue détectée !"]
        response = requests.get(self.URL_VERSIONS)

        if response.status_code == 200:
            versions = response.json()
        else:
            st.error(f"Erreur : {response.status_code}")
        return versions
    

    @pysnooper.snoop('debug_add_form.log')
    def add_form(self, option):
        """
        Affiche le formulaire de traduction et gère la demande de traduction.
        Envoie le texte à traduire au serveur et affiche la réponse.

        Parameters:
            option (str): La version de traduction sélectionnée par l'utilisateur.
        """
        st.subheader(option)
        atraduire = st.text_input("Texte à traduire")

        if st.button("Traduire"):
            data = {
                "atraduire": atraduire,
                "version": option,
                "utilisateur":st.session_state["logged_in"]
            }

            response = requests.post(self.URL_TRADUCTEUR, json=data)

            if response.status_code == 200:
                st.success("Voici votre traduction !")
                response_data = response.json()
                reponse = f"{response_data['traduction'][0]['translation_text']}"
                message(atraduire, is_user=True)
                message(reponse)
            else:
                st.error(f"Erreur : {response.status_code}")
                reponse = response.json()
                st.json(response.json())
        


                
    

    @pysnooper.snoop('add_chat_v2.log')
    def add_chat(self):
        """
        Affiche l'historique des messages de chat entre l'utilisateur et le bot.
        Récupère les messages depuis le serveur et les affiche avec des clés uniques via UUID.

        """
        url = f"{self.URL_TRADUCTIONS}{st.session_state.logged_in}"
        chat = requests.get(url)
        
        if chat.status_code == 200:
            chat_messages = chat.json()
            counter_user = 0
            counter_bot = 1
            
            for prompt in chat_messages:
                user_key = str(uuid.uuid4())
                bot_key = str(uuid.uuid4())

                message(prompt["atraduire"], is_user=True, key=user_key)
                message(prompt["traduction"],key=bot_key)
           

            
            else :
               st.error(f"Erreur : {chat.status_code}")

    # ancienne version 
    # def add_chat(self):
    #     url = f"{self.URL_TRADUCTIONS}{st.session_state.logged_in}"
    #     chat = requests.get(url)

    #     if chat.status_code == 200:
    #         chat_messages = chat.json()

    #         for prompt in chat_messages:
    #             message(prompt["atraduire"], is_user=True)
    #             message(prompt["traduction"])
    #     else :
    #         st.error(f"Erreur : {chat.status_code}")