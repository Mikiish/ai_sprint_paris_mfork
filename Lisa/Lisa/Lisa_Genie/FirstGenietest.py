import streamlit as st
from openai import OpenAI

client = OpenAI(
        api_key=""
    )

# ==================== 2) Initialisation du state ====================
if "genie_started" not in st.session_state:
    st.session_state["genie_started"] = False

# Historique de la conversation pour le chat
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ==================== 3) Affichage du titre ====================
st.title("Le Génie")

# ==================== 4) Écran d'accueil (texte + bouton) ====================
if not st.session_state["genie_started"]:
    # Texte d’avertissement
    st.markdown("""
    **Attention voyageur**,  
    Devant toi se trouve un objet aussi mystérieux qu’effrayant :  
    La jarre du Génie.  
    En cliquant sur le bouton "Ok" ci-dessus tu invoqueras le Génie,  
    il est alors de mon devoir de t’avertir que le Génie est une créature  
    **cupide** et **malicieuse**.  
    Entre autres lubies farfelues, le Génie aime transformer l'or en poussière.  
    Nous nous engageons à ce que le Génie soit correctement abreuvé en Or,  
    en invoquant le Génie vous ne vous engagez à rien de particulier,  
    si ce n’est avoir pris connaissance de ce fait.
    """)

    # Bouton "Ok" pour invoquer le Génie
    if st.button("Ok"):
        st.session_state["genie_started"] = True
        thread = client.beta.threads.create()
        thread_message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content="Tu es le Génie. À quelque question que ce soit, le Génie imagine un résumé en 7 points imaginaires, explorant les possibles de l'imagination. À partir de ces 7 points qu'il garde secrets, il répond avec 7 messages codés dans un langage symbolique avancé maximisant l'information. Ce langage symbolique utilise des émojis comme objets contextuels ainsi que tous les opérateurs et symboles logiques auxquels le Génie pourrait penser. Puisqu'il est le Génie, il pense beaucoup et finit par écrire une phrase ultra-dense n'ayant probablement de sens que pour lui, mais très amusante ! Comprenant son erreur, le Génie traduit ensuite sa phrase codée en rimes de 7 à 29 tokens, préférant des alexandrins ou des octosyllabes, puis associe chaque rime à sa phrase codée amusante. Tu peux exaucer 3 vœux ! Veux-tu exaucer mon vœu ? Si oui, alors je te confierai mon souhait le plus cher !",
        )

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id="asst_EViiKFxTVOBuRNrHeDFqCQgG"
        )

        thread_list = client.beta.threads.messages.list(thread_id=thread.id, limit=1)
        # initial_answer = thread_list[0].message.content
        # Premier message du Génie dans l'historique
        st.session_state["messages"].append({
            "role": "assistant",
            "content": thread_list
        })
        # On redessine la page pour afficher la zone de chat
        st.rerun()

# ==================== 5) Interface de chat ====================
else:
    # On affiche tous les messages passés (user + assistant)
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Zone de saisie en bas
    user_input = st.chat_input("Fais ton vœu")  # Nouveau dans Streamlit 1.26+
    if user_input:
        # Ajout du message utilisateur
        st.session_state["messages"].append({
            "role": "user",
            "content": user_input
        })
        # On l'affiche immédiatement
        with st.chat_message("user"):
            st.write(user_input)

        # Ici, on simule la réponse du Génie (dans ta version, tu appelleras l’API OpenAI)
        genie_response = "Oh mortel, ton vœu est noté !"
        st.session_state["messages"].append({
            "role": "assistant",
            "content": genie_response
        })
        with st.chat_message("assistant"):
            st.write(genie_response)

        # On relance la page pour forcer le rafraîchissement
        st.rerun()
