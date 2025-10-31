import streamlit as st
import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# -----------------------------------------------------------
# 🔧 CONFIGURATION DE L'APPLICATION
# -----------------------------------------------------------

st.set_page_config(
    page_title="🍎 Fruit Classifier - IA",
    page_icon="🍌",
    layout="centered"
)

st.title("🍉 Fruit Classifier - Détection automatique")
st.write("Glissez-déposez une photo d’un fruit ci-dessous pour découvrir dans quel état estfruit! 🍊🍏🍒")

# -----------------------------------------------------------
# 📦 CHARGEMENT DU MODÈLE
# -----------------------------------------------------------

@st.cache_resource
def load_model():
    model = tf.keras.models.load_model("fruit_classifier.keras")  # <-- Format .keras
    return model

model = load_model()

# Liste des classes (à adapter selon ton dataset)
CLASS_NAMES = ["fresh", "mild", "rotten"]  # <-- correspond à ton modèle


IMG_SIZE = (224, 224)

# -----------------------------------------------------------
# 📤 TÉLÉVERSEMENT DE L’IMAGE
# -----------------------------------------------------------

uploaded_file = st.file_uploader(
    "Glissez une image ici ou cliquez pour en choisir une 📁",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    # Affichage de l’image téléchargée
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="🖼️ Image téléchargée", use_container_width=True)

    # Prétraitement (mêmes paramètres que pendant l'entraînement)
    img_resized = image.resize(IMG_SIZE)
    img_array = tf.keras.utils.img_to_array(img_resized)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = (img_array / 127.5) - 1.0  # Normalisation MobileNetV2

    # -----------------------------------------------------------
    # 🔮 PRÉDICTION
    # -----------------------------------------------------------

    with st.spinner("Analyse de l’image... 🧠"):
        predictions = model.predict(img_array)
        scores = tf.nn.softmax(predictions[0]).numpy()

    pred_class = CLASS_NAMES[np.argmax(scores)]
    confidence = np.max(scores) * 100

    # -----------------------------------------------------------
    # 🧾 AFFICHAGE DU RÉSULTAT
    # -----------------------------------------------------------

    st.markdown("---")
    st.subheader("Résultat de la prédiction 🧠")
    st.success(f"**État du fruit : {pred_class}** 🍇")
    #st.write(f"Confiance du modèle : **{confidence:.2f}%**")

    # -----------------------------------------------------------
    # 📊 VISUALISATION DES PROBABILITÉS
    # -----------------------------------------------------------

    # prob_df = pd.DataFrame({
    #     "Fruit": CLASS_NAMES,
    #     "Probabilité (%)": scores * 100
    # }).sort_values("Probabilité (%)", ascending=True)

    # fig, ax = plt.subplots(figsize=(6, 4))
    # ax.barh(prob_df["Fruit"], prob_df["Probabilité (%)"], color="orange")
    # ax.set_xlabel("Probabilité (%)")
    # ax.set_title("Distribution des prédictions")
    # st.pyplot(fig)

else:
    st.info("⬆️ Importez une image pour commencer la prédiction.")

# -----------------------------------------------------------
# 🧩 FOOTER
# -----------------------------------------------------------
