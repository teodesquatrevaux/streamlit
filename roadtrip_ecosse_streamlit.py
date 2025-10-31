# Streamlit app: Roadtrip Écosse - Itinéraire Harry Potter
# Fichier: roadtrip_ecosse_streamlit.py
# Pour lancer :
# 1) installer streamlit: pip install streamlit
# 2) lancer: streamlit run roadtrip_ecosse_streamlit.py

import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
from PIL import Image
import requests

st.set_page_config(page_title="Roadtrip Écosse - Harry Potter", layout="wide")

# --- Data: itinerary and HP spots ---
ITINERARY = [
    {"day": 1, "date": "2025-07-07", "title": "Édimbourg - arrivée & premières visites", "desc": "The Elephant House, Greyfriars Kirkyard, Victoria Street, Balmoral (vue)", "lat":55.9500, "lon":-3.1870, "spot":"Edinburgh - Elephant House"},
    {"day": 2, "date": "2025-07-08", "title": "Édimbourg → Stirling → Glencoe", "desc": "Château de Stirling (optionnel), Glencoe (paysages Poudlard)", "lat":56.6829, "lon":-4.4226, "spot":"Glencoe"},
    {"day": 3, "date": "2025-07-09", "title": "Glencoe → Fort William", "desc": "Randos, Steall Falls (scène HP4)", "lat":56.8198, "lon":-5.1067, "spot":"Fort William / Steall Falls"},
    {"day": 4, "date": "2025-07-10", "title": "Fort William → Glenfinnan → Mallaig", "desc": "Glenfinnan Viaduct & (option) Jacobite Steam Train", "lat":56.8717, "lon":-5.4300, "spot":"Glenfinnan Viaduct"},
    {"day": 5, "date": "2025-07-11", "title": "Île de Skye", "desc": "Quiraing, Old Man of Storr, Fairy Pools", "lat":57.4120, "lon":-6.2110, "spot":"Isle of Skye"},
    {"day": 6, "date": "2025-07-12", "title": "Skye → Loch Ness → Inverness", "desc": "Urquhart Castle, Loch Ness", "lat":57.3240, "lon":-4.4244, "spot":"Loch Ness / Urquhart"},
    {"day": 7, "date": "2025-07-13", "title": "Inverness → Cairngorms → Pitlochry", "desc": "Cairngorms (forêts), Aviemore", "lat":56.8180, "lon":-3.7790, "spot":"Cairngorms / Aviemore"},
    {"day": 8, "date": "2025-07-14", "title": "Retour vers Édimbourg - plus de HP", "desc": "Musées, boutiques HP à Victoria Street", "lat":55.9533, "lon":-3.1883, "spot":"Edinburgh - Old Town"},
    {"day": 9, "date": "2025-07-15", "title": "Excursion: Durham Cathedral (option)", "desc": "Intérieurs utilisés pour Poudlard (films)", "lat":54.7753, "lon":-1.5766, "spot":"Durham Cathedral"},
    {"day": 10, "date": "2025-07-16", "title": "Dernier jour rond Édimbourg (Rosslyn Chapel)", "desc": "Rosslyn Chapel, North Berwick ou détente", "lat":55.8540, "lon":-3.1650, "spot":"Rosslyn Chapel"},
]

IMAGES = {
    "The Elephant House": "https://upload.wikimedia.org/wikipedia/commons/6/69/Elephant_House_2013.jpg",
    "Greyfriars Kirkyard": "https://upload.wikimedia.org/wikipedia/commons/3/32/Greyfriars_Kirkyard%2C_Edinburgh_-_panoramio.jpg",
    "Victoria Street": "https://upload.wikimedia.org/wikipedia/commons/0/0f/Victoria_Street%2C_Edinburgh.JPG",
    "Glencoe": "https://upload.wikimedia.org/wikipedia/commons/6/6b/Glencoe_Scotland.jpg",
    "Glenfinnan Viaduct": "https://upload.wikimedia.org/wikipedia/commons/7/75/Glenfinnan_Viaduct.jpg",
    "Isle of Skye": "https://upload.wikimedia.org/wikipedia/commons/1/12/Old_Man_of_Storr_-_Isle_of_Skye.jpg",
    "Loch Ness": "https://upload.wikimedia.org/wikipedia/commons/7/7d/Urquhart_Castle_2016.jpg",
    "Durham Cathedral": "https://upload.wikimedia.org/wikipedia/commons/8/8a/Durham_Cathedral_exterior.jpg",
    "Rosslyn Chapel": "https://upload.wikimedia.org/wikipedia/commons/4/4a/Rosslyn_Chapel.jpg",
}

# --- Helper functions ---
@st.cache_data
def load_image_from_url(url, max_size=(900,600)):
    try:
        resp = requests.get(url, timeout=8)
        img = Image.open(BytesIO(resp.content)).convert('RGB')
        img.thumbnail(max_size)
        return img
    except Exception as e:
        return None

@st.cache_data
def itinerary_df():
    return pd.DataFrame(ITINERARY)

# --- Sidebar controls ---
st.title("🇬🇧 Roadtrip Écosse — Spécial Harry Potter")
st.markdown("Plan interactif de votre voyage du 7 au 17 juillet — personnalisable et avec photos.")

st.sidebar.header("Contrôles")
day_select = st.sidebar.slider("Choisir un jour (numéro)", min_value=1, max_value=10, value=1)
show_map = st.sidebar.checkbox("Afficher la carte des étapes", value=True)
show_photos = st.sidebar.checkbox("Afficher la galerie photo", value=True)
export_csv = st.sidebar.button("Télécharger l'itinéraire (CSV)")

# --- Main layout: two columns ---
col1, col2 = st.columns([1,1])

df = itinerary_df()
selected = df[df['day'] == day_select].iloc[0]

with col1:
    st.subheader(f"Jour {selected['day']} — {selected['date']}")
    st.markdown(f"**{selected['title']}**")
    st.write(selected['desc'])
    st.markdown("---")
    st.markdown("### Détails pratiques")
    st.write("\- Récupération van : 7 juillet, 15h à Édimbourg")
    st.write("\- Restitution van : 17 juillet, 11h à Édimbourg")
    st.write("\- Réservez le Jacobite Steam Train à l'avance si vous voulez le Poudlard Express")
    st.write("\- Penser aux réservations de ferry pour l'île de Skye")

    # Interactive check list of recommended activities for the selected day
    st.markdown("### Activités recommandées")
    default_activities = [a.strip() for a in selected['desc'].split(',')]
    chosen = st.multiselect("Sélectionne ce que vous voulez faire", options=default_activities, default=default_activities)

    # Add personal notes
    notes = st.text_area("Notes personnelles pour ce jour", height=120)

with col2:
    # Photo if available
    spot = selected['spot']
    img = None
    if spot in IMAGES:
        img = load_image_from_url(IMAGES[spot.split(' / ')[0]] if spot.split(' / ')[0] in IMAGES else IMAGES.get(spot))
    if img:
        st.image(img, use_column_width=True, caption=spot)
    else:
        st.info("Aucune image disponible — remplacez l'URL dans le fichier si vous le souhaitez.")

    st.markdown("---")
    st.markdown("### Itinéraire rapide")
    st.dataframe(df[['day','date','title']].set_index('day'))

# Map section
if show_map:
    st.markdown("---")
    st.subheader("Carte des étapes")
    # Simple map using st.map with lat/lon
    map_df = df[['lat','lon','spot']].rename(columns={'lat':'latitude','lon':'longitude'})
    st.map(map_df)

# Photo gallery
if show_photos:
    st.markdown("---")
    st.subheader("Galerie Harry Potter — Écosse")
    cols = st.columns(3)
    i = 0
    for name, url in IMAGES.items():
        img = load_image_from_url(url, max_size=(600,400))
        with cols[i % 3]:
            if img:
                st.image(img, caption=name)
            else:
                st.write(name)
        i += 1

# Export CSV
if export_csv:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(label="Télécharger l'itinéraire (.csv)", data=csv, file_name='itinerire_ecosse.csv', mime='text/csv')

# Small footer and tips
st.markdown("---")
st.markdown("**Conseils pratiques** : prenez des vêtements coupe-vent, réservez le Jacobite Steam Train et les ferries, vérifiez les aires de camping pour vans et les restrictions de stationnement en Écosse.")

st.markdown("---")
st.markdown("_Ce Streamlit est personnalisable : tu peux remplacer les images (dossier `images/` ou changer les URLs), ajuster les dates et ajouter des étapes dans la variable `ITINERARY` en haut du fichier._")

# End
