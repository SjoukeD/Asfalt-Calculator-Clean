import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import base64
import math
import pandas as pd
from io import BytesIO

###########################################################################################
# logo voor op de sidebar
# ########################################################################################### 
def get_base64_logo():
    import os
    # Haal het pad naar de map waarin het script zich bevindt op
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(script_dir, "NIEUW-RWS-3488526-v1-logo_RWS_ministerie_Infrastructuur_en_Waterstaat_NL.png")
    
    # Controleer of het bestand bestaat
    if not os.path.exists(logo_path):
        raise FileNotFoundError(f"Logo bestand niet gevonden op: {logo_path}")
    
    with open(logo_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

base64_logo = get_base64_logo()

###########################################################################################
# zet de pagina op maximale breedte
############################################################################################ 
st.set_page_config(
    page_title="Asfaltcalculator®",
    layout="wide",
    initial_sidebar_state="expanded",
)

###########################################################################################
# CSS ook wel de layout of lettertype opmaak enzoo voor de pagina
############################################################################################ 
st.markdown("""
<style>
/* Titelkaart bovenaan */
.title-card {
    background: #f2f2f2;
    padding: 2rem 1rem;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 2rem;
}
.title-card h1 {
    color: #154273;
    font-size: 2.6rem;
    margin: 0;
    font-weight: 700;
    letter-spacing: -0.3px;
}
.title-card p {
    color: #535353;
    font-size: 1.2rem;
    margin-top: 0.75rem;
}

/* Kosten-blok */
.cost-title {
    color:#154273;
    font-size:2.0rem;
    font-weight:700;
    text-align:center;
    margin:1.5rem 0 2rem 0;
    font-family: 'Arial', sans-serif;
}
.cost-col-title {
    color:#154273;
    font-size:1.4rem;
    font-weight:700;
    text-align:center;
    margin-bottom:0.8rem;
    font-family:'Arial', sans-serif;
}
.cost-group {
    font-weight:600;
    font-size:1.1rem;
    margin-top:1rem;
    font-family:'Arial', sans-serif;
}
.cost-hint {
    color:#6c6c6c;
    font-size:0.85rem;
    margin:-0.3rem 0 0.5rem 0;
    font-family:'Arial', sans-serif;
}
.cost-estimate {
    color:gray;
    font-size:0.85rem;
    margin:-0.2rem 0 0.15rem 0;
    font-family:'Arial', sans-serif;
}

/* Samenvattende tabellen */
<div class="summary-wrapper">

.summary-title-main {
    text-align: center;
    color: #154273;
    font-size: 1.6rem;
    font-weight: 700;
    margin: 1rem 0 1.5rem 0;
    font-family: 'Arial', sans-serif;
}
.summary-subtitle {
    color:#154273;
    font-size:1.1rem;
    font-weight:600;
    margin-bottom:0.6rem;
    font-family:'Arial', sans-serif;
}
.summary-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'Arial', sans-serif;
    font-size: 0.9rem;
}
.summary-table th {
    background-color: #154273;
    color: #ffffff;
    padding: 8px 10px;
    text-align: left;
    font-weight: 600;
}
.summary-table td {
    background-color: #f5f5f5;
    padding: 6px 10px;
    border-bottom: 1px solid #e0e0e0;
}
.summary-table tr:last-child td {
    background-color: #FFFDD8;
    font-weight: 600;
}
.summary-table tr:hover td {
    background-color: #eceff1;
}

/* Algemene tabellen/grafieken */
.section-title {
    color: #154273;
    font-size: 2rem;
    font-weight: 600;
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 3px solid #154273;
    display: inline-block;
}
.financial-table {
    width: 100%;
    margin: 1.5rem 0 3rem 0;
    border-collapse: separate;
    border-spacing: 0;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.financial-table th {
    background-color: #154273;
    color: white;
    padding: 12px;
    text-align: left;
    font-size: 1.0rem;
}
.financial-table td {
    background-color: #f8f9fa;
    padding: 8px 12px;
    border-bottom: 1px solid #dee2e6;
    font-size: 0.95rem;
}
.financial-table tr:last-child td {
    font-weight: bold;
    background-color: #FFFDD8;
    border-bottom: none;
}
.financial-table tr:hover td {
    background-color: #f0f0f0;
}
.financial-table tr:last-child:hover td {
    background-color: #fff5b8;
}

.bottom-table tr:hover td {
    background-color: #f8f9fa !important;
}

.graph-header {
    color: #154273;
    font-size: 1.8rem;
    font-weight: 600;
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 3px solid #FFFDD8;
}
</style>
""", unsafe_allow_html=True)






###########################################################################################
# De title kaart bovenaan 
############################################################################################ 
st.markdown("""
<div class="title-card">
    <h1>Asfalt Calculator</h1>
    <p>Voor asfaltbeheer: inzicht in kosten, levensduur en CO₂ effecten van conventioneel en LVOv onderhoud</p>
</div>
""", unsafe_allow_html=True)









###########################################################################################
# Sidebar parameters
############################################################################################ 
with st.sidebar:
    # Display logo
    st.markdown("""
        <div style='margin-bottom: 1rem;'>
            <img src='data:image/png;base64,{}' width='300'>
        </div>
    """.format(base64_logo), unsafe_allow_html=True)

    st.markdown("<h2 style='color: #154273; font-size: 1.5rem; margin-bottom: 1rem;'>Input Parameters</h2>", unsafe_allow_html=True)

    type_wegdek = st.selectbox(
    "Type wegdek",
    [
        "ZOAB Regulier",
        "ZOAB Regulier + / DZOAB",
        "DZOAB 30% PR",
        "2L-ZOAB (onderlaag regulier)",
        "2L-ZOAB (onderlaag 30% PR)",
        "AC surf",
        "AC surf 30% PR",
        "AC surf gemodificeerd bitumen",
        "AC surf mod. bitumen 30% PR",
        "SMA-NL 8-11",
        "SMA-NL 8-11 met mod. bitumen",
        "SMA-NL 5",
    ],
    help="Kies het type deklaag. Dit bepaalt de default levensduur, laagopbouw (massa per m²), MKI en CO₂-factoren in het model."
)

    

    ##################
    # Wegdek matrix: mapping + levensduur
    ##################
    WEGDEK_MATRIX = {
        "ZOAB Regulier": {"base_type": "ZOAB Regulier", "levensduur_links": 15, "levensduur_rechts": 10},
        "ZOAB Regulier + / DZOAB": {"base_type": "ZOAB Regulier + / DZOAB", "levensduur_links": 17, "levensduur_rechts": 11},
        "DZOAB 30% PR": {"base_type": "ZOAB Regulier + / DZOAB", "levensduur_links": 17, "levensduur_rechts": 11},

        "2L-ZOAB (onderlaag regulier)": {"base_type": "2L-ZOAB", "levensduur_links": 13, "levensduur_rechts": 9},
        "2L-ZOAB (onderlaag 30% PR)": {"base_type": "2L-ZOAB", "levensduur_links": 13, "levensduur_rechts": 9},

        "AC surf": {"base_type": "AC surf", "levensduur_links": 18, "levensduur_rechts": 12},
        "AC surf 30% PR": {"base_type": "AC surf", "levensduur_links": 18, "levensduur_rechts": 12},
        "AC surf gemodificeerd bitumen": {"base_type": "AC surf", "levensduur_links": 18, "levensduur_rechts": 12},
        "AC surf mod. bitumen 30% PR": {"base_type": "AC surf", "levensduur_links": 18, "levensduur_rechts": 12},

        "SMA-NL 8-11": {"base_type": "SMA-NL 8-11", "levensduur_links": 20, "levensduur_rechts": 15},
        "SMA-NL 8-11 met mod. bitumen": {"base_type": "SMA-NL 8-11", "levensduur_links": 20, "levensduur_rechts": 15},
        "SMA-NL 5": {"base_type": "SMA-NL 5", "levensduur_links": 15, "levensduur_rechts": 12},
    }

    if type_wegdek not in WEGDEK_MATRIX:
        st.error(f"Onbekend wegdeklabel: '{type_wegdek}'. Check selectbox vs WEGDEK_MATRIX.")
        st.stop()

    base_type = WEGDEK_MATRIX[type_wegdek]["base_type"]
    default_left = WEGDEK_MATRIX[type_wegdek]["levensduur_links"]
    default_right = WEGDEK_MATRIX[type_wegdek]["levensduur_rechts"]

    ##################
    # LVOV defaults
    ##################
    lvov_levensduur_verlenging = 3
    aantal_lvov = 2

    speciale_types = [
        "AC surf", "AC surf 30% PR", "AC surf gemodificeerd bitumen", "AC surf mod. bitumen 30% PR",
        "SMA-NL 8-11", "SMA-NL 8-11 met mod. bitumen",
        "SMA-NL 5"
    ]

    ##################
    # LVOV-behandelmethode (alleen voor speciale types)
    ##################
    if type_wegdek in speciale_types:
        st.subheader("Behandelmethode (LVOV)")

        totaal_lvov = st.slider(
            "Aantal LVOV-behandelingen (max. 2)",
            min_value=0, max_value=2, value=0, step=1, key="totaal_lvov"
        )

        lvov_verlengingen = []
        if totaal_lvov >= 1:
            keuze1 = st.selectbox(
                "Behandeling 1",
                ["LVOV 3 jaar verlenging", "LVOV 4 jaar verlenging"],
                key="lvov_behandeling_1"
            )
            lvov_verlengingen.append(3 if "3 jaar" in keuze1 else 4)

        if totaal_lvov == 2:
            keuze2 = st.selectbox(
                "Behandeling 2",
                ["LVOV 3 jaar verlenging", "LVOV 4 jaar verlenging"],
                key="lvov_behandeling_2"
            )
            lvov_verlengingen.append(3 if "3 jaar" in keuze2 else 4)

        aantal_lvov = totaal_lvov
        lvov_levensduur_verlenging = sum(lvov_verlengingen) if lvov_verlengingen else 0

    ##################
    # Basis inputs (altijd)
    ##################
    st.subheader("Aangepaste Levensduur")
    custom_left = st.number_input(
        "Levensduur overige rijstroken (jaren)",
        min_value=5, max_value=30, value=default_left,
        help="Technische levensduur in jaren voor alle rijstroken behalve de rechter. Dit is ook de simulatieduur (horizon) van het model."
    )
    custom_right = st.number_input(
        "Levensduur rechter rijstrook (jaren)",
        min_value=5, max_value=30, value=default_right,
        help="Technische levensduur in jaren voor de rechter rijstrook."
    )

    aantal_rijbanen = st.number_input("Aantal rijstroken", min_value=1, max_value=8, value=2)
    lengte_km = st.number_input("Lengte wegdek (km)", min_value=1.0, value=10.0, step=1.0)
    BREEDTE_RIJBAAN_M = 3.5
    opp_m2 = lengte_km * 1000 * aantal_rijbanen * BREEDTE_RIJBAAN_M

    leeftijd_asfalt = st.slider("Leeftijd huidig asfalt (jaar)", 0, 6, 0)
    simulatieduur = custom_left

    co2_lvov_input = st.number_input(
        "CO₂ uitstoot per m² voor LVOv behandeling (ton)",
        min_value=0.0, max_value=0.1, value=0.000291, step=0.00001, format="%.5f"
    )

with st.sidebar:
    st.markdown(
        "<h3 style='color: #154273; font-size: 1.2rem; margin-top: 1.5rem;'>VVU (Voertuigverlies-uren)</h3>",
        unsafe_allow_html=True
    )

    vvu_warning_placeholder = st.empty()

    intensiteit_conv_veh_per_uur = st.number_input(
        "Intensiteit verkeer conventioneel (voertuigen/uur)",
        min_value=0.0, value=0.0, step=100.0, key="intensiteit_conv_veh_per_uur"
    )

    intensiteit_lvov_veh_per_uur = st.number_input(
        "Intensiteit verkeer LVOv (voertuigen/uur)",
        min_value=0.0, value=0.0, step=100.0, key="intensiteit_lvov_veh_per_uur"
    )

    duur_werk_lvov_uur = st.number_input(
        "Duur werkzaamheden LVOv (uur per onderhoudsactie)",
        min_value=0.0, value=0.0, step=1.0, key="duur_werk_lvov_uur"
    )

    duur_werk_conv_uur = st.number_input(
        "Duur werkzaamheden herasfalteren (uur per onderhoudsactie)",
        min_value=0.0, value=0.0, step=1.0, key="duur_werk_conv_uur"
    )

    extra_tijd_omleiding_min = st.number_input(
        "Extra tijd door omleiding (minuten per voertuig)",
        min_value=0.0, value=0.0, step=5.0, key="extra_tijd_omleiding_min"
    )

    if (
        intensiteit_conv_veh_per_uur == 0.0 or
        intensiteit_lvov_veh_per_uur == 0.0 or
        duur_werk_lvov_uur == 0.0 or
        duur_werk_conv_uur == 0.0 or
        extra_tijd_omleiding_min == 0.0
    ):
        vvu_warning_placeholder.warning(
            "Let op: verkeersintensiteit en duur van de werkzaamheden zijn sterk afhankelijk van het moment "
            "(dag, nacht, weekend) en de gekozen methode (LVOv of herasfalteren). "
            "Zolang deze waarden op 0 staan, wordt geen maatschappelijke hinder (VVU) berekend."
        )
    else:
        vvu_warning_placeholder.empty()

    vvu_ready = (
        intensiteit_conv_veh_per_uur > 0.0 and
        intensiteit_lvov_veh_per_uur > 0.0 and
        duur_werk_lvov_uur > 0.0 and
        duur_werk_conv_uur > 0.0 and
        extra_tijd_omleiding_min > 0.0
    )





 
def bepaal_levensduur(type_wegdek, positie, custom_left=None, custom_right=None):
    """
    Bepaalt de levensduur van het wegdek op basis van:
    - gebruikersinvoer (custom_left / custom_right), indien aanwezig
    - anders: default uit WEGDEK_MATRIX
    """

    if type_wegdek not in WEGDEK_MATRIX:
        raise KeyError(f"Onbekend wegdektype: {type_wegdek}")

    if positie == "Overige rijstroken":
        return custom_left if custom_left is not None else WEGDEK_MATRIX[type_wegdek]["levensduur_links"]

    if positie == "Rechter rijstrook":
        return custom_right if custom_right is not None else WEGDEK_MATRIX[type_wegdek]["levensduur_rechts"]

    raise ValueError(f"Onbekende positie: {positie}")






#########################################################################################################
# event based onderhoudsmodel voor asfaltvervangingen of LVOV 
#########################################################################################################
def generate_events(strategy,
                    type_wegdek,
                    simulatieduur,
                    leeftijd_asfalt,
                    custom_levensduur_links,
                    custom_levensduur_rechts,
                    aantal_lvov_toepassingen,
                    lvov_levensduur_verlenging=3):
    """
    Genereert een lijst van onderhouds-events op basis van de strategie en het wegdektype.

    Args:
        strategy: 'LVOv' of 'Conventioneel'
        type_wegdek: Type asfalt (bijv. 'ZOAB Regulier')
        simulatieduur: Duur van de simulatie in jaren
        leeftijd_asfalt: Huidige leeftijd van het asfalt
        custom_levensduur_links: Aangepaste levensduur overige rijstroken
        custom_levensduur_rechts: Aangepaste levensduur rechter rijstrook
        aantal_lvov_toepassingen: Aantal keren dat LVOv wordt toegepast (0, 1 of 2)
        lvov_levensduur_verlenging: Totale verlenging van de rechter rijstrook (som van 3/4 jaar)
    """
    events = []

    # Levensduur overige rijstroken
    levensduur_links = bepaal_levensduur(
        type_wegdek,
        "Overige rijstroken",
        custom_levensduur_links,
        custom_levensduur_rechts
    )

    # Basis levensduur rechter rijstrook
    basis_levensduur_rechts = bepaal_levensduur(
        type_wegdek,
        "Rechter rijstrook",
        custom_levensduur_links,
        custom_levensduur_rechts
    )

    # Rechter levensduur met/zonder LVOv
    if strategy == 'LVOv':
        levensduur_rechts = basis_levensduur_rechts + lvov_levensduur_verlenging
    else:
        levensduur_rechts = basis_levensduur_rechts

    # Eind van de linker strook (volledige vervanging)
    einde_levensduur_links = levensduur_links - leeftijd_asfalt

    # -----------------------------
    # STRATEGIE: LVOv
    # -----------------------------
    if strategy == 'LVOv':
        # LVOv-behandelingen op de rechter strook
        if aantal_lvov_toepassingen > 0:
            interval = levensduur_links / (aantal_lvov_toepassingen + 1)
            for i in range(1, aantal_lvov_toepassingen + 1):
                jaar = round(i * interval) - leeftijd_asfalt
                # lvov_index = 1 of 2 (voor kosten per behandeling)
                if 0 < jaar <= simulatieduur and jaar < einde_levensduur_links:
                    events.append({
                        'jaar': jaar,
                        'type': 'LVOv',
                        'breedte': 'strookbreed',
                        'lvov_index': i
                    })

        

    # -----------------------------
    # STRATEGIE: Conventioneel
    # -----------------------------
    elif strategy == 'Conventioneel':
        # Rechter strook vervangen op basis van eigen levensduur
        startjaar = levensduur_rechts - leeftijd_asfalt
        for jaar in range(startjaar, simulatieduur + 1, levensduur_rechts):
            if 0 < jaar < einde_levensduur_links:
                events.append({
                    'jaar': jaar,
                    'type': 'Vervanging',
                    'breedte': 'strookbreed'
                })


    # Events op jaar sorteren
    return sorted(events, key=lambda e: e['jaar'])


def calculate_costs_from_events(
    events,
    simulatieduur,
    opp_links,
    opp_rechts,
    vaste_kosten,
    kost_asfalt,
    kost_lvov,
    co2_conv_val,
    co2_lvov_val,
    *,
    lvov_costs=None
):
    """
    Berekent jaarlijkse en cumulatieve DIRECTE kosten en CO2 op basis van events.

    Let op:
    - Hinderkosten zijn volledig verwijderd uit dit model.
    - lvov_costs is keyword-only (door de *), zodat je nooit meer 'multiple values' krijgt.
    """
    jaarlijkse_kosten = np.zeros(simulatieduur)
    jaarlijkse_co2 = np.zeros(simulatieduur)

    for event in events:
        if event.get("type") == "Vervanging met onderlaag":
            continue

        jaar = int(event["jaar"])
        if 1 <= jaar < simulatieduur:
            # Oppervlakte bepalen
            if event["breedte"] == "baanbreed":
                opp = opp_links + opp_rechts
            elif event["breedte"] == "strookbreed":
                opp = opp_rechts
            elif event["breedte"] == "strookbreed_links":
                opp = opp_links
            else:
                raise ValueError(f"Onbekende breedte: {event.get('breedte')}")

            kosten = 0.0
            co2 = 0.0

            # Kosten/CO2 per eventtype
            if "Vervanging" in event["type"]:
                kosten = vaste_kosten + (opp_rechts * kost_asfalt)
                co2 = opp * co2_conv_val

            elif "LVOv" in event["type"]:
                idx = event.get("lvov_index", 1)
                if lvov_costs is not None and idx in lvov_costs:
                    c = lvov_costs[idx]
                    kosten = c["vaste_kosten"] + (opp_rechts * c["kost_m2"])
                else:
                    kosten = vaste_kosten + (opp_rechts * kost_lvov)

                co2 = opp * co2_lvov_val

            jaar_index = jaar - 1
            jaarlijkse_kosten[jaar_index] += kosten
            jaarlijkse_co2[jaar_index] += co2

    cumulatieve_kosten = np.cumsum(jaarlijkse_kosten)
    cumulatieve_co2 = np.cumsum(jaarlijkse_co2)

    return jaarlijkse_kosten, cumulatieve_kosten, jaarlijkse_co2, cumulatieve_co2



def count_events_per_year(events, simulatieduur, match_substring):
    """
    Returns:
        counts: np.array length simulatieduur
                counts[y-1] = aantal events in jaar y
    """
    counts = np.zeros(simulatieduur)
    for e in events:
        jaar = int(e.get("jaar", 0))
        if 1 <= jaar < simulatieduur and match_substring in e.get("type", ""):
            counts[jaar - 1] += 1
    return counts

col_conv, col_lvov = st.columns(2, gap="large")

# ----------------------------------------------------
# CONVENTIONEEL
# ----------------------------------------------------
with col_conv:

    st.markdown("<div class='cost-col-title'>Directe Kosten Conventioneel</div>", unsafe_allow_html=True)

    st.markdown("<div class='cost-group'>Vaste kosten</div>", unsafe_allow_html=True)
    st.markdown("<div class='cost-hint'>Per onderhoudsactie</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        verkeersmaatregelingskosten_conv = st.number_input(
            "Verkeersmaatregelen (€)",
            min_value=0, value=0, step=1000,
            key="vm_conv",
            help="Vaste kosten per onderhoudsactie voor verkeersmaatregelen, inclusief bebording, afzettingen en omleiding."
        )
    with c2:
        overige_projectkosten_conv = st.number_input(
            "Overige Projectkosten (€)",
            min_value=0, value=0, step=1000,
            key="proj_conv",
            help="Vaste projectkosten zoals voorbereiding, engineering en uitvoeringskosten van de onderaannemer."
        )

    st.markdown("<div class='cost-group'>Variabele kosten</div>", unsafe_allow_html=True)
    st.markdown("<div class='cost-hint'>Per m²</div>", unsafe_allow_html=True)

    st.markdown("<div class='cost-estimate'></div>", unsafe_allow_html=True)
    kost_asfalt = st.number_input(
        "Materiaal- en freeswerk kosten(€/m²)",
        value=0.0,
        key="kost_asfalt",
        help="Kosten per m² voor het produceren en aanbrengen van nieuw asfalt, inclusief het frezen en afvoeren van de bestaande asfaltlaag."
    )

    # Hinderkosten verplaatst naar sidebar

# ----------------------------------------------------
# LVOv
# ----------------------------------------------------
with col_lvov:

    st.markdown("<div class='cost-col-title'>Directe Kosten LVOv</div>", unsafe_allow_html=True)

    # ---------- Behandeling 1 ----------
    st.markdown("<div class='cost-group'>Vaste kosten</div>", unsafe_allow_html=True)
    st.markdown("<div class='cost-hint'>Per onderhoudsactie</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        verkeersmaatregelingskosten_lvov_1 = st.number_input(
            "Verkeersmaatregelen (€)",
            min_value=0, value=0, step=1000,
            key="vm_lvov_1",
            help="Vaste kosten per onderhoudsactie voor verkeersmaatregelen, inclusief bebording, afzettingen en omleiding."
        )
    with c2:
        overige_projectkosten_lvov_1 = st.number_input(
            "Overige projectkosten (€)",
            min_value=0, value=0, step=1000,
            key="proj_lvov_1",
            help="Vaste projectkosten zoals voorbereiding, engineering en uitvoeringskosten van de onderaannemer."
        )

    st.markdown("<div class='cost-group'>Variabele kosten</div>", unsafe_allow_html=True)
    st.markdown("<div class='cost-hint'>Per m²</div>", unsafe_allow_html=True)
    st.markdown("<div class='cost-estimate'>Indicatie waarde: €2,06/m² bij een afname van minimaal 50.000 m2 </div>", unsafe_allow_html=True)

    kost_lvov_1 = st.number_input(
        "Materiaalkosten (€/m²) – behandeling 1",
        value=0.0,
        key="kost_lvov_1",
        help="Kosten per m² voor LVOv-oppervlaktebehandeling (materiaal + aanbrengen)"
    )

    # ---------- Optioneel: Behandeling 2 ----------
    # Alleen extra velden tonen als SMA/AC én er echt 2 behandelingen zijn gekozen
    if type_wegdek in speciale_types and 'totaal_lvov' in locals() and totaal_lvov == 2:
        st.markdown("<div class='cost-group'>Behandeling 2 – vaste kosten</div>", unsafe_allow_html=True)
        st.markdown("<div class='cost-hint'>Per onderhoudsactie</div>", unsafe_allow_html=True)

        d1, d2 = st.columns(2)
        with d1:
            verkeersmaatregelingskosten_lvov_2 = st.number_input(
                "Verkeersmaatregelen (€) – behandeling 2",
                min_value=0, value=0, step=1000,
                key="vm_lvov_2",
                help="Vaste kosten per onderhoudsbeurt voor verkeersmaatregelen bij LVOv (behandeling 2)."
            )
        with d2:
            overige_projectkosten_lvov_2 = st.number_input(
                "Overige projectkosten (€) – behandeling 2",
                min_value=0, value=0, step=1000,
                key="proj_lvov_2",
                help="Vaste projectkosten per LVOv-actie (behandeling 2)."
            )

        st.markdown("<div class='cost-group'>Behandeling 2 – variabele kosten</div>", unsafe_allow_html=True)
        st.markdown("<div class='cost-hint'>Per m²</div>", unsafe_allow_html=True)

        kost_lvov_2 = st.number_input(
            "Materiaalkosten (€/m²) – behandeling 2",
            value=0.0,
            key="kost_lvov_2",
            help="Variabele kosten per m² voor LVOv-materiaal (behandeling 2)."
        )
    else:
        # Als er geen tweede behandeling is: gebruik dezelfde waarden als behandeling 1
        verkeersmaatregelingskosten_lvov_2 = verkeersmaatregelingskosten_lvov_1
        overige_projectkosten_lvov_2 = overige_projectkosten_lvov_1
        kost_lvov_2 = kost_lvov_1

    # Hinderkosten verplaatst naar sidebar

# Totale vaste kosten per aanpak
# Totale vaste kosten per aanpak
vaste_kosten_conv = verkeersmaatregelingskosten_conv + overige_projectkosten_conv

vaste_kosten_lvov_1 = verkeersmaatregelingskosten_lvov_1 + overige_projectkosten_lvov_1
vaste_kosten_lvov_2 = verkeersmaatregelingskosten_lvov_2 + overige_projectkosten_lvov_2

# Dictionary met kosten per LVOv-behandeling (wordt gebruikt in de kostencalculatie)
lvov_costs = {
    1: {"vaste_kosten": vaste_kosten_lvov_1, "kost_m2": kost_lvov_1},
    2: {"vaste_kosten": vaste_kosten_lvov_2, "kost_m2": kost_lvov_2},
}


st.markdown("---")






# Rest van de code
verdeling = {
    1: (1.0, 0.0),
    2: (0.5, 0.5),
    3: (1/3, 2/3),
    4: (0.25, 0.75),
    5: (0.2, 0.8),
    6: (1/6, 5/6),
    7: (1/7, 6/7),
    8: (0.125, 0.875)
}
perc_rechts, perc_links = verdeling[aantal_rijbanen]
opp_rechts = opp_m2 * perc_rechts
opp_links = opp_m2 * perc_links

# MKI-plafondwaarden 2026 (€/ton asfalt) per type wegdek
mki_per_ton_dict = {
    "ZOAB Regulier": 7.7,
    "ZOAB Regulier + / DZOAB": 8.4,
    "DZOAB 30% PR": 8.4,

    "2L-ZOAB (onderlaag regulier)": 9.76,
    "2L-ZOAB (onderlaag 30% PR)": 9.76,

    "AC surf": 8.2,
    "AC surf 30% PR": 8.2,
    "AC surf gemodificeerd bitumen": 8.2,
    "AC surf mod. bitumen 30% PR": 8.2,

    "SMA-NL 8-11": 7.9,
    "SMA-NL 8-11 met mod. bitumen": 7.9,
    "SMA-NL 5": 11.7,
}
# Vaste MKI voor LVOv (€/m² per behandeling)
MKI_LVOV_PER_M2 = 0.06
mki_lvov_per_m2 = MKI_LVOV_PER_M2


# kg CO2-eq per ton asfalt (A1-D) - RWS branchereferentiemengsels
co2_kg_per_ton_dict = {
    # ZOAB / DZOAB
    "ZOAB Regulier": 83.7,
    "ZOAB Regulier + / DZOAB": 88.0,   # jij gebruikt deze label ook voor DZOAB
    "DZOAB 30% PR": 73.9,

    # AC surf
    "AC surf": 94.7,
    "AC surf 30% PR": 82.8,
    "AC surf gemodificeerd bitumen": 110.0,
    "AC surf mod. bitumen 30% PR": 95.2,

    # SMA
    "SMA-NL 8-11": 97.5,
    "SMA-NL 8-11 met mod. bitumen": 116.0,
    "SMA-NL 5": 110.0,

    # 2L-ZOAB is speciaal -> doen we hieronder via lagen
}

# 2L-ZOAB: kg CO2-eq per ton per laag
CO2_2L_TOP_KG_PER_TON = 108.0
CO2_2L_UNDER_REG_KG_PER_TON = 96.6
CO2_2L_UNDER_30PR_KG_PER_TON = 79.0


def co2_ton_per_m2(type_wegdek, layers_dict):
    """
    Return: ton CO2-eq per m2 (A1-D), op basis van kg CO2-eq/ton en laagmassa per m2.
    """
    layers = layers_dict[type_wegdek]  # [(dikte_m, dichtheid_kgm3), ...]

    # ton asfalt per m2 per laag
    ton_per_m2_layers = [(d * rho) / 1000.0 for (d, rho) in layers]  # ton/m2

    # Speciaal geval: 2L-ZOAB heeft verschillende CO2-factoren per laag
    if type_wegdek == "2L-ZOAB (onderlaag regulier)":
        # aannames: layers[0] = toplaag, layers[1] = onderlaag (zoals je layers_dict definieert)
        kg_per_m2 = (CO2_2L_TOP_KG_PER_TON * ton_per_m2_layers[0]) + (CO2_2L_UNDER_REG_KG_PER_TON * ton_per_m2_layers[1])
        return kg_per_m2 / 1000.0  # ton/m2

    if type_wegdek == "2L-ZOAB (onderlaag 30% PR)":
        kg_per_m2 = (CO2_2L_TOP_KG_PER_TON * ton_per_m2_layers[0]) + (CO2_2L_UNDER_30PR_KG_PER_TON * ton_per_m2_layers[1])
        return kg_per_m2 / 1000.0  # ton/m2

    # Alle andere types: 1 factor per ton
    kg_per_ton = co2_kg_per_ton_dict[type_wegdek]
    total_ton_per_m2 = sum(ton_per_m2_layers)
    kg_per_m2 = kg_per_ton * total_ton_per_m2
    return kg_per_m2 / 1000.0  # ton/m2


layers_dict = {
    # ZOAB/DZOAB
    "ZOAB Regulier": [(0.05, 2000)],
    "ZOAB Regulier + / DZOAB": [(0.05, 2000)],
    "DZOAB 30% PR": [(0.05, 2000)],

    # 2L-ZOAB: toplaag 0.025 @2000, onderlaag 0.045 @2100 (PCR tabel)
    "2L-ZOAB (onderlaag regulier)": [(0.025, 2000), (0.045, 2100)],
    "2L-ZOAB (onderlaag 30% PR)": [(0.025, 2000), (0.045, 2100)],

    # AC surf varianten (PCR: 0.05, 2350)
    "AC surf": [(0.05, 2350)],
    "AC surf 30% PR": [(0.05, 2350)],
    "AC surf gemodificeerd bitumen": [(0.05, 2350)],
    "AC surf mod. bitumen 30% PR": [(0.05, 2350)],

    # SMA 8-11 varianten (PCR: 0.035, 2350)
    "SMA-NL 8-11": [(0.035, 2350)],
    "SMA-NL 8-11 met mod. bitumen": [(0.035, 2350)],

    # SMA 5 (jij had 0.03, 2300 – als dat jullie keuze is, laat zo. Anders aanpassen.)
    "SMA-NL 5": [(0.03, 2300)],
}

# MKI asfalt per m2 voor het gekozen type wegdek (€/m2)
mki_per_ton = mki_per_ton_dict[type_wegdek]
layers = layers_dict[type_wegdek]  # lijst van (dikte_m, dichtheid_kgm3)
massa_per_m2_kg = sum(d * rho for (d, rho) in layers)
massa_per_m2_ton = massa_per_m2_kg / 1000.0    # ton/m2
mki_asfalt_per_m2 = mki_per_ton * massa_per_m2_ton


co2_conv_per_m2_ton = co2_ton_per_m2(type_wegdek, layers_dict) 

 # Strategiekeuze
duur = simulatieduur

 # -- Event-Based Calculations --

 # Conventioneel
events_conv = generate_events(
     'Conventioneel', type_wegdek, simulatieduur, leeftijd_asfalt, custom_left, custom_right, 0
)

kosten_conv, kosten_conv_cum, co2_conv, co2_conv_cum = calculate_costs_from_events(
    events=events_conv,
    simulatieduur=simulatieduur,
    opp_links=opp_links,
    opp_rechts=opp_rechts,
    vaste_kosten=vaste_kosten_conv,
    kost_asfalt=kost_asfalt,
    kost_lvov=0.0,  # niet gebruikt bij conventioneel, maar vereist door de functie-signature
    co2_conv_val=co2_conv_per_m2_ton,
    co2_lvov_val=co2_lvov_input,
    lvov_costs=None
)




 # LVOv
events_lvov = generate_events(
     'LVOv', type_wegdek, simulatieduur, leeftijd_asfalt, custom_left, custom_right,
     aantal_lvov, lvov_levensduur_verlenging
)

# ---- VVU berekening ----
delta_t_uur = extra_tijd_omleiding_min / 60.0  # minuten -> uur

# Aantal relevante onderhoudsacties per jaar
n_conv_per_year = count_events_per_year(events_conv, simulatieduur, "Vervanging")
n_lvov_per_year = count_events_per_year(events_lvov, simulatieduur, "LVOv")

# VVU per event (veh-uren)
vvu_per_event_conv = intensiteit_conv_veh_per_uur * duur_werk_conv_uur * delta_t_uur
vvu_per_event_lvov = intensiteit_lvov_veh_per_uur * duur_werk_lvov_uur * delta_t_uur


# Jaarlijkse en cumulatieve VVU
vvu_conv_yearly = n_conv_per_year * vvu_per_event_conv
vvu_lvov_yearly = n_lvov_per_year * vvu_per_event_lvov

vvu_conv_cum = np.cumsum(vvu_conv_yearly)
vvu_lvov_cum = np.cumsum(vvu_lvov_yearly)


kosten_lvov, kosten_lvov_cum, co2_lvov, co2_lvov_cum = calculate_costs_from_events(
    events=events_lvov,
    simulatieduur=simulatieduur,
    opp_links=opp_links,
    opp_rechts=opp_rechts,
    vaste_kosten=vaste_kosten_conv,  # fallback; echte vaste kosten per behandeling komen uit lvov_costs
    kost_asfalt=kost_asfalt,
    kost_lvov=kost_lvov_1,
    co2_conv_val=co2_conv_per_m2_ton,
    co2_lvov_val=co2_lvov_input,
    lvov_costs=lvov_costs
)




import streamlit.components.v1 as components

# Calculate lifespans based on current inputs
levensduur_rechts = bepaal_levensduur(type_wegdek, "Rechter rijstrook", custom_left, custom_right)
levensduur_links = bepaal_levensduur(type_wegdek, "Overige rijstroken", custom_left, custom_right)










components.html(f"""
     <div style="
         background-color: #f2f2f2;
         padding: 1.5rem;
         border-radius: 0.5rem;
         border: 1px solid #e0e0e0;
         font-family: Arial, sans-serif;
     ">
         <h3 style="
             color: #154273;
             margin-top: 0;
             margin-bottom: 0.8rem;
             font-size: 1.6rem;
             font-family: Arial, sans-serif;
         ">
             Huidige configuratie
         </h3>
         <p style="
             color: #535353;
             font-size: 1rem;
             margin: 0.4rem 0;
             font-family: Arial, sans-serif;
         ">
             <strong>Wegdek:</strong> {type_wegdek} |
             <strong>Lengte:</strong> {lengte_km} km |
             <strong>Aantal rijstroken:</strong> {aantal_rijbanen} |
             <strong>Oppervlakte:</strong> {opp_m2:,.0f} m²
         </p>
         <p style="
             color: #535353;
             font-size: 1rem;
             margin: 0.4rem 0;
             font-family: Arial, sans-serif;
         ">
             <strong>Leeftijd huidig asfalt:</strong> {leeftijd_asfalt} jaar |
             <strong>Simulatieduur:</strong> {simulatieduur} jaar |
             <strong>Levensduur (zonder LVOv) :</strong> {bepaal_levensduur(type_wegdek, "Rechter rijstrook", custom_left, custom_right)} jr (rechter), {bepaal_levensduur(type_wegdek, "Overige rijstroken", custom_left, custom_right)} jr (Overige)
         </p>
     </div>
 """, height=180)


# ============================================
# TABEL: LEVENSDUUR MET EN ZONDER LVOV
# ============================================

zoab_types = [
    "ZOAB Regulier",
    "ZOAB Regulier + / DZOAB",
    "DZOAB 30% PR",
    "2L-ZOAB (onderlaag regulier)",
    "2L-ZOAB (onderlaag 30% PR)",
]

levensduur_rechts_zonder_lvov = levensduur_rechts
levensduur_links_zonder_lvov = levensduur_links

# LVOV-logica
if type_wegdek in zoab_types:
    levensduur_rechts_met_lvov = levensduur_rechts_zonder_lvov + 6
elif 'aantal_lvov' in locals() and aantal_lvov > 0:
    levensduur_rechts_met_lvov = levensduur_rechts_zonder_lvov + lvov_levensduur_verlenging
else:
    levensduur_rechts_met_lvov = levensduur_rechts_zonder_lvov

levensduur_links_met_lvov = levensduur_links_zonder_lvov

# Extra jaren levensduur door LVOv (per rijstrook)
verlenging_links = levensduur_links_met_lvov - levensduur_links_zonder_lvov
verlenging_rechts = levensduur_rechts_met_lvov - levensduur_rechts_zonder_lvov

# ============================================
# CSS: alles zwart, niets bold, volledig grijze tabel
# ============================================
st.markdown("""
<style>
.lvov-table, .lvov-table td, .lvov-table th {
    background-color: #f2f2f2 !important;
    color: black !important;
    font-weight: normal !important;
}
.lvov-table th {
    border-bottom: 1px solid #dddddd !important;
}
.lvov-table td, .lvov-table th {
    padding: 6px 10px !important;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
/* dropdown en selected value iets kleiner zodat lange labels passen */
div[data-baseweb="select"] span {
    font-size: 0.95rem !important;
    line-height: 1.15rem !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# TABEL RENDEREN (nieuwe versie)
# ============================================
st.markdown(f"""
<div class="summary-wrapper">
    <div class="cost-group">
        Levensduur rijstroken met en zonder LVOv-behandeling
    </div>
    <table class="summary-table lvov-table">
        <tr>
            <th>Rijstrook</th>
            <th>Levensduur zonder LVOv (jaar)</th>
            <th>Extra jaren door LVOv</th>
            <th>Levensduur in model (jaar)</th>
        </tr>
        <tr>
            <td>Overige rijstroken</td>
            <td>{levensduur_links_zonder_lvov}</td>
            <td>{verlenging_links}</td>
            <td>{levensduur_links_met_lvov}</td>
        </tr>
        <tr>
            <td>Rechter rijstrook</td>
            <td>{levensduur_rechts_zonder_lvov}</td>
            <td>{verlenging_rechts}</td>
            <td>{levensduur_rechts_met_lvov}</td>
        </tr>
    </table>
    <p style="margin-top:0.5rem; font-size:0.85rem; color:#555;">
        LVOv wordt in dit model alleen toegepast op de rechter rijstrook; de overige rijstroken blijven ongewijzigd.
    </p>
</div>
""", unsafe_allow_html=True)


# ============================================
# WAARSCHUWING
# ============================================
if levensduur_rechts_met_lvov < levensduur_links_met_lvov:
    verschil = levensduur_links_met_lvov - levensduur_rechts_met_lvov
    st.error(
        f"Let op: de rechter rijstrook heeft met LVOv een kortere levensduur "
        f"({levensduur_rechts_met_lvov} jaar) dan de overige rijstroken "
        f"({levensduur_links_met_lvov} jaar). Verschil: {verschil} jaar."
    )



 # Compacte overzichtstabellen: kosten en CO₂ naast elkaar

# Bereken besparingen
kosten_besp_pct = ((kosten_conv_cum[-1] - kosten_lvov_cum[-1]) / kosten_conv_cum[-1]) * 100
co2_besp_pct = ((co2_conv_cum[-1] - co2_lvov_cum[-1]) / co2_conv_cum[-1]) * 100

financial_data = {
    'Aanpak': ['Conventioneel', 'LVOv', 'Besparing met LVOv'],
    'Totale Directe Kosten': [
        f"€{kosten_conv_cum[-1]:,.0f}",
        f"€{kosten_lvov_cum[-1]:,.0f}",
        f"€{kosten_conv_cum[-1] - kosten_lvov_cum[-1]:,.0f} "
        f"<span style='color:#14853b; font-weight:600; margin-left:6px;'>({kosten_besp_pct:.1f}%)</span>"
    ]
}

environmental_data = {
    'Aanpak': ['Conventioneel', 'LVOv', 'Besparing met LVOv'],
    'CO₂ Uitstoot': [
        f"{co2_conv_cum[-1]:,.0f} ton",
        f"{co2_lvov_cum[-1]:,.0f} ton",
        f"{co2_conv_cum[-1] - co2_lvov_cum[-1]:,.0f} ton "
        f"<span style='color:#14853b; font-weight:600; margin-left:6px;'>({co2_besp_pct:.1f}%)</span>"
    ]
}

st.markdown("""
<style>
.summary-wrapper {
    max-width: 1200px;
    margin: 0 auto 2rem auto;
}
.summary-title-main {
    text-align: center;
    color: #154273;
    font-size: 1.6rem;
    font-weight: 700;
    margin: 1rem 0 1.5rem 0;
    font-family: 'Arial', sans-serif;
}
.summary-subtitle {
    color:#154273;
    font-size:1.1rem;
    font-weight:600;
    margin-bottom:0.6rem;
    font-family:'Arial', sans-serif;
}
.summary-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'Arial', sans-serif;
    font-size: 0.9rem;
}
.summary-table th {
    background-color: #154273;
    color: #ffffff;
    padding: 8px 10px;
    text-align: left;
    font-weight: 600;
}
.summary-table td {
    background-color: #f5f5f5;
    padding: 6px 10px;
    border-bottom: 1px solid #e0e0e0;
}
.summary-table tr:last-child td {
    background-color: #FFFDD8;
    font-weight: 600;
}
.summary-table tr:hover td {
    background-color: #eceff1;
}
</style>
""", unsafe_allow_html=True)


col_fin, col_env = st.columns(2)

# -------- Financiële impact --------
with col_fin:
    st.markdown("<div class='cost-col-title'>Financiële impact directe kosten</div>", unsafe_allow_html=True)
    st.markdown("""
    <table class='summary-table'>
        <tr>
            <th>Aanpak</th>
            <th>Totale directe kosten</th>
        </tr>
        <tr>
            <td>{}</td>
            <td>{}</td>
        </tr>
        <tr>
            <td>{}</td>
            <td>{}</td>
        </tr>
        <tr>
            <td>{}</td>
            <td>{}</td>
        </tr>
    </table>
    """.format(
        financial_data['Aanpak'][0], financial_data['Totale Directe Kosten'][0],
        financial_data['Aanpak'][1], financial_data['Totale Directe Kosten'][1],
        financial_data['Aanpak'][2], financial_data['Totale Directe Kosten'][2]
    ), unsafe_allow_html=True)

# -------- CO₂-impact --------
with col_env:
    st.markdown("<div class='cost-col-title'>CO₂ impact materiaal en uitvoering</div>", unsafe_allow_html=True)

    if 'Maatschappelijke CO₂ (omleiding)' in environmental_data:
        st.markdown("""
        <table class='summary-table'>
            <tr>
                <th>Aanpak</th>
                <th>CO₂ uitstoot</th>
                <th>Maatschappelijke CO₂</th>
            </tr>
            <tr>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
            </tr>
            <tr>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
            </tr>
            <tr>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
            </tr>
        </table>
        """.format(
            environmental_data['Aanpak'][0],
            environmental_data['CO₂ Uitstoot'][0],
            environmental_data['Maatschappelijke CO₂ (omleiding)'][0],
            environmental_data['Aanpak'][1],
            environmental_data['CO₂ Uitstoot'][1],
            environmental_data['Maatschappelijke CO₂ (omleiding)'][1],
            environmental_data['Aanpak'][2],
            environmental_data['CO₂ Uitstoot'][2],
            environmental_data['Maatschappelijke CO₂ (omleiding)'][2]
        ), unsafe_allow_html=True)
    else:
        st.markdown("""
        <table class='summary-table'>
            <tr>
                <th>Aanpak</th>
                <th>CO₂ uitstoot</th>
            </tr>
            <tr>
                <td>{}</td>
                <td>{}</td>
            </tr>
            <tr>
                <td>{}</td>
                <td>{}</td>
            </tr>
            <tr>
                <td>{}</td>
                <td>{}</td>
            </tr>
        </table>
        """.format(
            environmental_data['Aanpak'][0], environmental_data['CO₂ Uitstoot'][0],
            environmental_data['Aanpak'][1], environmental_data['CO₂ Uitstoot'][1],
            environmental_data['Aanpak'][2], environmental_data['CO₂ Uitstoot'][2]
        ), unsafe_allow_html=True)


st.markdown("""
<style>
.viz-wrapper {
    max-width: 1200px;
    margin: 2rem auto 1rem auto;
    padding: 0 1.5rem;
}
.viz-title {
    color: #154273;
    font-size: 1.6rem;
    font-weight: 700;
    border-bottom: 3px solid #154273;
    display: inline-block;
    padding-bottom: 0.3rem;
    font-family: 'Arial', sans-serif;
}
.viz-subtitle {
    color: #4b5563;
    font-size: 0.95rem;
    margin-top: 0.35rem;
    font-family: 'Arial', sans-serif;
}
</style>

<div class="viz-wrapper">
    <div class="viz-title">Visualisaties</div>
    <div class="viz-subtitle">
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================
# VISUALISATIES – 2 KOLLOMMEN LAYOUT
# ============================================

# X-as (jaren)
jaren = np.arange(1, simulatieduur + 1)



# ---------- RIJ 1: CUMULATIEVE KOSTEN & CUMULATIEVE CO2 ----------
row1_col1, row1_col2 = st.columns(2, gap="large")

with row1_col1:
    fig_costs, ax_costs = plt.subplots(figsize=(6, 4))

    ax_costs.plot(jaren, kosten_conv_cum, label='Conventioneel', color='#154273', linewidth=2.5)
    ax_costs.plot(jaren, kosten_lvov_cum, label='LVOv', color='#f5e251', linewidth=2.5)

    ax_costs.set_title('Cumulatieve directe kosten over tijd', pad=20, fontsize=14, fontweight='bold')
    ax_costs.set_xlabel('Jaar', fontsize=12)
    ax_costs.set_ylabel('Directe kosten (€)', fontsize=12)

    ax_costs.grid(True, linestyle='--', alpha=0.7)
    ax_costs.legend(frameon=True, fancybox=True, shadow=True, fontsize=10)

    fmt = ticker.FuncFormatter(lambda x, p: f'€{int(x):,}')
    ax_costs.yaxis.set_major_formatter(fmt)

    for spine in ax_costs.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.5)

    ax_costs.tick_params(axis='both', which='major', labelsize=10)
    ax_costs.set_xticks(jaren)
    ax_costs.set_xticklabels(jaren, rotation=45)

    ax_costs.set_facecolor('#f8f9fa')
    fig_costs.patch.set_facecolor('#ffffff')

    plt.tight_layout()
    st.pyplot(fig_costs)

with row1_col2:
    fig_co2, ax_co2 = plt.subplots(figsize=(6, 4))

    ax_co2.plot(jaren, co2_conv_cum, label='Conventioneel', color='#154273', linewidth=2.5)
    ax_co2.plot(jaren, co2_lvov_cum, label='LVOv', color='#f5e251', linewidth=2.5)

    ax_co2.set_title('Cumulatieve CO$_2$-uitstoot over tijd', pad=20, fontsize=14, fontweight='bold')
    ax_co2.set_xlabel('Jaar', fontsize=12)
    ax_co2.set_ylabel('CO₂-uitstoot (ton)', fontsize=12)

    ax_co2.grid(True, linestyle='--', alpha=0.7)
    ax_co2.legend(frameon=True, fancybox=True, shadow=True, fontsize=10)

    fmt = ticker.FuncFormatter(lambda x, p: f'{int(x):,}')
    ax_co2.yaxis.set_major_formatter(fmt)

    for spine in ax_co2.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.5)

    ax_co2.tick_params(axis='both', which='major', labelsize=10)
    ax_co2.set_xticks(jaren)
    ax_co2.set_xticklabels(jaren, rotation=45)

    ax_co2.set_facecolor('#f8f9fa')
    fig_co2.patch.set_facecolor('#ffffff')

    plt.tight_layout()
    st.pyplot(fig_co2)

# ---------- RIJ 2: JAARLIJKSE KOSTEN & MAATSCHAPPELIJKE CO2 ----------
row2_col1, row2_col2 = st.columns(2, gap="large")

def bereken_mki_asfalt_rechterstrook(events, opp_rechts, mki_asfalt_per_m2, simulatieduur):
    """
    Telt de MKI van alle asfaltvervangingen op de rechterrijstrook
    (conventionele aanpak: volledige asfaltlaag).
    """
    totaal_mki = 0.0
    for e in events:
        jaar = e['jaar']
        if jaar < 1 or jaar > simulatieduur:
            continue

        # We kijken alleen naar events waar asfalt wordt vervangen
        if 'Vervanging' in e['type']:
            # Alleen rechterrijstrook meenemen
            area_right = opp_rechts
            totaal_mki += area_right * mki_asfalt_per_m2

    return totaal_mki


def bereken_mki_lvov_rechterstrook(events, opp_rechts, mki_lvov_per_m2, simulatieduur):
    """
    Telt de MKI van alle LVOv-behandelingen op de rechterrijstrook.
    Aantal behandelingen wordt automatisch meegenomen via de events.
    """
    totaal_mki = 0.0
    for e in events:
        jaar = e['jaar']
        if jaar < 1 or jaar > simulatieduur:
            continue

        if 'LVOv' in e['type']:
            area_right = opp_rechts
            totaal_mki += area_right * mki_lvov_per_m2

    return totaal_mki

# Totale MKI voor asfaltvervanging rechterrijstrook (conventioneel)
totaal_mki_asfalt_rechts = bereken_mki_asfalt_rechterstrook(
    events_conv, opp_rechts, mki_asfalt_per_m2, simulatieduur
)

# Totale MKI voor LVOv-behandelingen rechterrijstrook
totaal_mki_lvov_rechts = bereken_mki_lvov_rechterstrook(
    events_lvov, opp_rechts, mki_lvov_per_m2, simulatieduur
)





with row2_col1:
    fig_yearly, ax_yearly = plt.subplots(figsize=(6, 4))

    width = 0.4
    ax_yearly.bar(jaren - width/2, kosten_conv, width, label='Conventioneel', color='#154273')
    ax_yearly.bar(jaren + width/2, kosten_lvov, width, label='LVOv', color='#f5e251')

    ax_yearly.set_title('Jaarlijkse directe kosten per aanpak', pad=20, fontsize=14, fontweight='bold')
    ax_yearly.set_xlabel('Jaar', fontsize=12)
    ax_yearly.set_ylabel('Kosten (€)', fontsize=12)

    ax_yearly.grid(True, linestyle='--', alpha=0.7, axis='y')
    ax_yearly.legend(frameon=True, fancybox=True, shadow=True, fontsize=10)

    fmt = ticker.FuncFormatter(lambda x, p: f'€{int(x):,}')
    ax_yearly.yaxis.set_major_formatter(fmt)

    ax_yearly.tick_params(axis='both', which='major', labelsize=10)
    plt.xticks(jaren, rotation=45)

    ax_yearly.set_facecolor('#f8f9fa')
    fig_yearly.patch.set_facecolor('#ffffff')

    plt.tight_layout()
    st.pyplot(fig_yearly)






with row2_col2:
    fig_mki, ax_mki = plt.subplots(figsize=(6, 4))

    methods = ['LVOv-behandelingen', 'Asfaltlaag rechterrijstrook']
    mki_values = [totaal_mki_lvov_rechts, totaal_mki_asfalt_rechts]

    bars = ax_mki.bar(methods, mki_values, color=['#f5e251', '#154273'])

    for bar, value in zip(bars, mki_values):
        height = bar.get_height()
        ax_mki.text(
            bar.get_x() + bar.get_width() / 2.0,
            height * 1.01,
            f'€{value:,.0f}',
            ha='center',
            va='bottom',
            fontsize=10
        )

    ax_mki.set_title('MKI voor asfaltlaag vs. LVOv op rechterrijstrook',
                     pad=20, fontsize=14, fontweight='bold')
    ax_mki.set_ylabel('MKI (€/contractperiode)', fontsize=12)
    ax_mki.grid(True, linestyle='--', alpha=0.3, axis='y')
    ax_mki.get_yaxis().set_major_formatter(
        ticker.FuncFormatter(lambda x, p: f'€{int(x):,}')
    )

    ax_mki.spines['top'].set_visible(False)
    ax_mki.spines['right'].set_visible(False)
    ax_mki.set_ylim(0, max(mki_values) * 1.2 if max(mki_values) > 0 else 1)

    plt.tight_layout()
    st.pyplot(fig_mki)





# ---------- RIJ 3: MAATSCHAPPELIJKE HINDER & HINDERKOSTEN ----------
row3_col1, row3_col2 = st.columns(2, gap="large")


with row3_col1:
    if vvu_ready:
        fig_vvu, ax_vvu = plt.subplots(figsize=(6, 4))

        ax_vvu.plot(jaren, vvu_conv_cum, label='Conventioneel (VVU cumulatief)',
                    color='#154273', linewidth=2.5)
        ax_vvu.plot(jaren, vvu_lvov_cum, label='LVOv (VVU cumulatief)',
                    color='#f5e251', linewidth=2.5)

        ax_vvu.set_xlabel('Jaar', fontsize=12)
        ax_vvu.set_ylabel('Cumulatieve VVU (voertuig-uren)', fontsize=12)
        ax_vvu.set_title('Voertuigverlies-uren (VVU) door extra reistijd',
                         fontsize=14, fontweight='bold', pad=20)

        ax_vvu.grid(True, linestyle='--', alpha=0.7)
        ax_vvu.legend(fontsize=10, framealpha=1)
        ax_vvu.set_facecolor('#f8f9fa')
        ax_vvu.yaxis.set_major_formatter(
            ticker.FuncFormatter(lambda x, p: format(int(x), ','))
        )

        plt.tight_layout()
        st.pyplot(fig_vvu)

    else:
        st.info(
            "VVU-grafiek verschijnt zodra alle VVU-velden zijn ingevuld"
        )


    






 


 # Table 2: Yearly costs comparison
st.markdown("""<div style='margin-top: 2rem;'></div>""", unsafe_allow_html=True)
st.markdown('<div class="section-title">Jaarlijkse directe Kosten Vergelijking</div>', unsafe_allow_html=True)

 # Create yearly costs comparison table
yearly_data = []
for i, (conv, lvov) in enumerate(zip(kosten_conv, kosten_lvov), start=1):
    yearly_data.append({
        'Jaar': i,
        'Conventioneel': conv,
        'LVOv': lvov
    })


 # Convert to HTML table
yearly_table_html = '<table class="financial-table bottom-table"><thead><tr>'
yearly_table_html += '<th>Jaar</th><th>Conventioneel (€)</th><th>LVOv (€)</th>'
yearly_table_html += '</tr></thead><tbody>'

for row in yearly_data:
     yearly_table_html += f'<tr>'
     yearly_table_html += f'<td>{row["Jaar"]}</td>'
     # Color conventional costs
     conv_color = '#dc3545' if row["Conventioneel"] > 0 else '#000000'
     yearly_table_html += f'<td style="color: {conv_color}">€{row["Conventioneel"]:,.0f}</td>'
     # Color LVOv costs
     lvov_color = '#dc3545' if row["LVOv"] > 0 else '#000000'
     yearly_table_html += f'<td style="color: {lvov_color}">€{row["LVOv"]:,.0f}</td>'
     yearly_table_html += '</tr>'

# Compacte styling: kleinere cellen, compactere hoogte, maar breedte blijft 100%
st.markdown("""
<style>
.compact-table th, .compact-table td {
    padding: 4px 6px !important;    /* compacter */
    font-size: 0.85rem !important;  /* kleinere tekst */
}
.compact-table tr:hover td {
    background-color: #f2f4f5 !important; /* subtiele hover */
}
</style>
""", unsafe_allow_html=True)

# Wrap de tabel, maar laat breedte gewoon 100% van het blad
st.markdown(f"""
<div style="width:100%;">
    <table class="financial-table bottom-table compact-table">
        {yearly_table_html.replace('<table class="financial-table bottom-table">','').replace('</table>','')}
    </table>
</div>
""", unsafe_allow_html=True)

fig_costs.savefig("fig_costs.png", dpi=200)
fig_co2.savefig("fig_co2.png", dpi=200)
fig_yearly.savefig("fig_yearly.png", dpi=200)

fig_mki.savefig("fig_mki.png", dpi=200)

if vvu_ready:
    fig_vvu.savefig("fig_vvu.png", dpi=200)






# ============================================
# EXCEL EXPORT – INPUT + SAMENVATTENDE TABELLEN
# ============================================


# LVOV-configuratie veilig ophalen
aantal_lvov_val = aantal_lvov if 'aantal_lvov' in locals() else 0
lvov_verlenging_val = lvov_levensduur_verlenging if 'lvov_levensduur_verlenging' in locals() else 0

# 1) Inputparameters als DataFrame (één rij)
input_data = {
    "Type wegdek": [type_wegdek],
    "Levensduur overige rijstroken (jaar)": [custom_left],
    "Levensduur rechter rijstrook (jaar)": [custom_right],
    "Aantal LVOV-behandelingen": [aantal_lvov_val],
    "Totale LVOV-verlenging (jaar)": [lvov_verlenging_val],
    "Aantal rijstroken": [aantal_rijbanen],
    "Lengte wegdek (km)": [lengte_km],
    "Oppervlakte (m²)": [opp_m2],
    "Leeftijd huidig asfalt (jaar)": [leeftijd_asfalt],
    "Simulatieduur (jaar)": [simulatieduur],

    "CO₂ conventioneel (ton/m²)": [co2_conv_per_m2_ton],
    "CO₂ LVOv (ton/m²)": [co2_lvov_input],

    "Vaste kosten conv – verkeersmaatregelen (€)": [verkeersmaatregelingskosten_conv],
    "Vaste kosten conv – overige projectkosten (€)": [overige_projectkosten_conv],
    "Vaste kosten LVOv – verkeersmaatregelen 1 (€)": [verkeersmaatregelingskosten_lvov_1],
    "Vaste kosten LVOv – overige projectkosten 1 (€)": [overige_projectkosten_lvov_1],
    "Vaste kosten LVOv – verkeersmaatregelen 2 (€)": [verkeersmaatregelingskosten_lvov_2],
    "Vaste kosten LVOv – overige projectkosten 2 (€)": [overige_projectkosten_lvov_2],
    "Materiaalkosten LVOv 1 (€/m²)": [kost_lvov_1],
    "Materiaalkosten LVOv 2 (€/m²)": [kost_lvov_2],

    # --- NIEUW: VVU ---
    "Intensiteit verkeer conventioneel (voertuigen/uur)": [intensiteit_conv_veh_per_uur],
    "Intensiteit verkeer LVOv (voertuigen/uur)": [intensiteit_lvov_veh_per_uur],
    "Duur werkzaamheden LVOv (uur per actie)": [duur_werk_lvov_uur],
    "Duur werkzaamheden herasfalteren (uur per actie)": [duur_werk_conv_uur],
    "Extra tijd door omleiding (min per voertuig)": [extra_tijd_omleiding_min],
}


df_input = pd.DataFrame(input_data)

# 2) Samenvattende tabellen als DataFrames
# 2) Samenvattende tabellen als DataFrames (schone versie voor Excel)
financial_data_excel = {
    'Aanpak': ['Conventioneel', 'LVOv', 'Besparing met LVOv'],
    'Totale Directe Kosten': [
        f"€{kosten_conv_cum[-1]:,.0f}",
        f"€{kosten_lvov_cum[-1]:,.0f}",
        f"€{kosten_conv_cum[-1] - kosten_lvov_cum[-1]:,.0f} ({kosten_besp_pct:.1f}%)"
    ]
}

environmental_data_excel = {
    'Aanpak': ['Conventioneel', 'LVOv', 'Besparing met LVOv'],
    'CO₂ Uitstoot': [
        f"{co2_conv_cum[-1]:,.0f} ton",
        f"{co2_lvov_cum[-1]:,.0f} ton",
        f"{co2_conv_cum[-1] - co2_lvov_cum[-1]:,.0f} ton ({co2_besp_pct:.1f}%)"
    ]
}

df_financial = pd.DataFrame(financial_data_excel)
df_environmental = pd.DataFrame(environmental_data_excel)


# 3) Schrijf alles naar een Excel-bestand in memory
output = BytesIO()
with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
    df_input.to_excel(writer, index=False, sheet_name="Input")
    df_financial.to_excel(writer, index=False, sheet_name="Samenvatting_kosten")
    df_environmental.to_excel(writer, index=False, sheet_name="Samenvatting_CO2")


output = BytesIO()
with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
    df_input.to_excel(writer, index=False, sheet_name="Input")
    df_financial.to_excel(writer, index=False, sheet_name="Samenvatting_kosten")
    df_environmental.to_excel(writer, index=False, sheet_name="Samenvatting_CO2")

    workbook  = writer.book
    sheet_fig = workbook.add_worksheet("Grafieken")

    # Insert images at fixed positions
    sheet_fig.insert_image("A1", "fig_costs.png")
    sheet_fig.insert_image("A20", "fig_co2.png")
    sheet_fig.insert_image("A39", "fig_yearly.png")
    if vvu_ready: sheet_fig.insert_image("A58", "fig_vvu.png")
    sheet_fig.insert_image("A77", "fig_mki.png")
   


output.seek(0)

# 4) Download-knop onderaan de main pagina
st.markdown("<br><hr>", unsafe_allow_html=True)
st.download_button(
    label="Exporteer input en samenvatting naar Excel",
    data=output,
    file_name="asfaltcalculator_export.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)
