import streamlit as st
import random
import time

#hiermee genereer je een random waarde, afgerond op 2 decimalen
def waardegenerator():
    
    a = 1 
    b = 100
    getal = random.uniform(a, b)
    afgerond = round(getal, 2)
    return afgerond

def opdracht_waarde(): # voor de random opdrachtkeuze
    a = 1
    b = 3
    getal = str(random.randint(a, b))
    return getal

def eenheid_waarde(): # voor de random opdrachtkeuze
    a = 1
    b = 2
    getal = str(random.randint(a, b))
    return getal

def genereer_random_eenheden():
    #"""Bepaalt willekeurige eenheden voor de 'Alles door elkaar' (mix) optie."""
    
    # Random vgem eenheid
    eenheid_waarde_vgem_index = eenheid_waarde()
    eenheid_waarde_vgem = "m/s" if eenheid_waarde_vgem_index == "1" else "km/h"
                
    # Random afstand eenheid
    eenheid_waarde_s_index = eenheid_waarde()
    eenheid_waarde_s = "m" if eenheid_waarde_s_index == "1" else "km"
        
    # Random tijd eenheid
    eenheid_waarde_t_index = eenheid_waarde()
    eenheid_waarde_t = "s" if eenheid_waarde_t_index == "1" else "h"
        
    return eenheid_waarde_vgem, eenheid_waarde_s, eenheid_waarde_t

def opdracht(vraagtype, eenheid_waarde_vgem, eenheid_waarde_s, eenheid_waarde_t):

    # hier kan je de eenheden instellen
    gem_snelheid_eenheid = eenheid_waarde_vgem
    afstand_eenheid = eenheid_waarde_s
    tijd_eenheid = eenheid_waarde_t

    afstand_waarde = waardegenerator()
    tijd_waarde = waardegenerator()
    gem_snelheid_waarde = waardegenerator()

    # tijdelijke waarden om later om te rekenen 
    afstand_waarde_temp = afstand_waarde
    tijd_waarde_temp = tijd_waarde
    gem_snelheid_waarde_temp = gem_snelheid_waarde

    if vraagtype == "1": # voor gemmiddelde snelheid berekenen

        if afstand_eenheid == "km":
            afstand_waarde_temp *= 1000
            
        if tijd_eenheid == "h":
            tijd_waarde_temp *= 3600
        
        antwoord_ms = afstand_waarde_temp/tijd_waarde_temp

        if gem_snelheid_eenheid == "km/h":
            antwoord = round(3.6*antwoord_ms, 2)
        else:
            antwoord = round(antwoord_ms, 2)
        
        gevraagde_eenheid = gem_snelheid_eenheid
        opdracht_tekst = f"""
        Een voorwerp legt {afstand_waarde} {afstand_eenheid} af in {tijd_waarde} {tijd_eenheid}. 
        Bereken de gemiddelde snelheid in {gem_snelheid_eenheid}. 
        Rond je antwoord af op 2 decimalen."""
        

    elif vraagtype == "2": # voor afstand berekenen
        
        if gem_snelheid_eenheid == "km/h":
            gem_snelheid_waarde_temp /= 3.6
        if tijd_eenheid == "h":
            tijd_waarde_temp *= 3600
        
        antwoord_m = gem_snelheid_waarde_temp * tijd_waarde_temp

        if afstand_eenheid == "km":
            antwoord = round(antwoord_m/1000 , 2)
        else:
            antwoord = round(antwoord_m, 2)

        gevraagde_eenheid = afstand_eenheid
        opdracht_tekst = f"""
        Een voorwerp beweegt {tijd_waarde} {tijd_eenheid} met een snelheid van {gem_snelheid_waarde} {gem_snelheid_eenheid}. 
        Bereken de afstand die het voorwerp aflegt in {afstand_eenheid}. 
        Rond je antwoord af op 2 decimalen."""

    elif vraagtype == "3": # voor tijd berekenen

        
        if gem_snelheid_eenheid == "km/h":
            gem_snelheid_waarde_temp /= 3.6
        if afstand_eenheid == "km":
            afstand_waarde_temp *= 1000

        antwoord_s = afstand_waarde_temp/gem_snelheid_waarde_temp

        if tijd_eenheid == "h":
            antwoord = round(antwoord_s/3600, 2)    
        else:
            antwoord = round(antwoord_s, 2)

        
        gevraagde_eenheid = tijd_eenheid
        opdracht_tekst = f"""
        Een voorwerp legt {afstand_waarde} {afstand_eenheid} af met een gemiddelde snelheid van {gem_snelheid_waarde} {gem_snelheid_eenheid}.
        Bereken de tijd die het voorwerp hierover gedaan heeft in {tijd_eenheid}.
        Rond je antwoord af op 2 decimalen."""

    return opdracht_tekst, antwoord, gevraagde_eenheid

def reset_opdracht():
    """Reset de status zodat een nieuwe opdracht kan worden gegenereerd."""
    st.session_state.status = 'initial'
    st.session_state.antwoord_ingevuld = '' # Maak het invoerveld leeg
    # Forceer herlading om een nieuwe willekeurige opdracht te genereren

def toon_antwoord_callback():
    """Stelt de status in om het antwoord te tonen. Wordt gebruikt als on_click callback."""
    st.session_state.status = 'opgegeven'

def probeer_opnieuw_callback():
    """Reset het invoerveld en de status om de gebruiker opnieuw te laten proberen. Gebruikt als on_click callback."""
    # st.session_state.antwoord_ingevuld is de waarde die we gebruiken voor de 'value' parameter
    st.session_state.antwoord_ingevuld = ''
    
    # st.session_state["antwoord_input_field"] is de interne waarde van het widget, gekoppeld aan de key.
    # We resetten deze expliciet om te garanderen dat het veld leeg is na de callback.
    if "antwoord_input_field" in st.session_state:
        st.session_state["antwoord_input_field"] = ''
        
    st.session_state.status = 'waiting_for_input'
def controleer_antwoord(user_input):
    """Controleert het ingevoerde antwoord tegen het juiste antwoord (opgeslagen in state)."""
    try:
        # Vervang komma's door punten en converteer naar float
        ingevuld = float(user_input.replace(",", "."))
    except ValueError:
        st.session_state.status = 'ongeldige_invoer'
        return

    juist_antwoord = st.session_state.antwoord
    
    # Tolerantie van 0.01, rekening houdend met afronding
    if abs(ingevuld - juist_antwoord) < 0.01:
        st.session_state.status = 'correct'
    else:
        st.session_state.status = 'incorrect'


# 1. Initialisatie van alle sessie-status variabelen
if 'antwoord' not in st.session_state:
    st.session_state.antwoord = None
    st.session_state.gevraagde_eenheid = ''
    st.session_state.opdracht_tekst = "Maak een keuze in de zijbalk om een opdracht te starten." # FIX: Nieuwe variabele
    # Status: 'initial', 'waiting_for_input', 'correct', 'incorrect', 'ongeldige_invoer'
    st.session_state.status = 'initial' 
    st.session_state.antwoord_ingevuld = ''

# 1. Initialisatie van alle variabelen 
gecombineerde_eenheden = None    # Code van de Eenheden-selectbox
vraagtype_vast = None           # Code van de Vraagtype-selectbox (vast of None)
vraagtype = None                # De uiteindelijke code voor de opdracht-functie
vraagtype_label = ""
antwoord_type = ""

# Initialisatie van eenheden (neutraal)
eenheid_waarde_vgem = ""
eenheid_waarde_s = ""
eenheid_waarde_t = ""
opdracht_tekst = "Maak een keuze in de zijbalk om een opdracht te starten."

#st.sidebar.header("")
#st.sidebar.header("")
#st.sidebar.header("")
#st.sidebar.header("")
#st.sidebar.header("")
#st.sidebar.header("")
# ------------------------------
# sidebar selectie 1: eenheden
# ------------------------------


st.sidebar.subheader("Kies de eenheden")

gecombineerde_eenheden_codes = {
        "Alleen m/s, m en s": "1",
        "Alleen km/h, km en h": "2",
        "Alles door elkaar": "3"
    }

gecombineerde_eenheden_select = st.sidebar.selectbox(
        "Welke eenheden wil je mee oefenen?",
        list(gecombineerde_eenheden_codes.keys()),
        index = None,
        placeholder = "Maak een keuze..."
    )
# eenheden status




if gecombineerde_eenheden_select is not None:
    gecombineerde_eenheden = gecombineerde_eenheden_codes[gecombineerde_eenheden_select]

    if gecombineerde_eenheden == "1":
        eenheid_waarde_vgem = "m/s"
        eenheid_waarde_s = "m"
        eenheid_waarde_t = "s"

                
    elif gecombineerde_eenheden == "2":
        eenheid_waarde_vgem = "km/h"
        eenheid_waarde_s = "km"
        eenheid_waarde_t = "h"
                
    elif gecombineerde_eenheden == "3":
        eenheid_waarde_vgem = "mix"
        eenheid_waarde_s = "mix"
        eenheid_waarde_t = "mix"

    # st.sidebar.subheader("Geselecteerde eenheden:")
    # st.sidebar.markdown(f"**Snelheid** ($\mathbf{{v_{{gem}}}}$): {eenheid_waarde_vgem}")
    # st.sidebar.markdown(f"**Afstand** ($\mathbf{{s}}$): {eenheid_waarde_s}")
    # st.sidebar.markdown(f"**Tijd** ($\mathbf{{t}}$): {eenheid_waarde_t}")

    
    # Display de geselecteerde eenheden
st.sidebar.markdown("---")
# ------------------------------
# sidebar selectie 2: vraagtype
# ------------------------------
st.sidebar.subheader("Kies je vraagtype")

vraagtype_temp_codes = {
    "Snelheid": "1",
    "Afstand": "2",
    "Tijd": "3",
    "Alles door elkaar": "4"
} 

# vraagtype status
  


vraagtype_temp_select = st.sidebar.selectbox(
    "**Welke berekening wil je mee oefenen?**",
    list(vraagtype_temp_codes.keys()),
    index = None,
    placeholder = "Maak een keuze..."
)

if vraagtype_temp_select is not None:
    vraagtype_temp = vraagtype_temp_codes[vraagtype_temp_select]

    if vraagtype_temp == "4":
        vraagtype_vast = "4" #trigger random opdrachtkeuze
        vraagtype_label = "Alles door elkaar heen"
        antwoord_type = None
    else:
        vraagtype_vast = vraagtype_temp
        if vraagtype_temp == "1":
            vraagtype_vast = "1"
            vraagtype_label = "**Geselecteerd vraagtype:** alleen snelheid ($\mathbf{v_{gem}}$) berekenen"
            antwoord_type = "De gemiddelde snelheid is: "
        elif vraagtype_temp == "2":
            vraagtype_vast = "2"
            vraagtype_label = "**Geselecteerd vraagtype:** alleen afstand ($\mathbf{s}$) berekenen"
            antwoord_type = "De afstand is "
        elif vraagtype_temp == "3":
            vraagtype_vast = "3"
            vraagtype_label = "**Geselecteerd vraagtype:** alleen tijd ($\mathbf{t}$) berekenen"
            antwoord_type = "De tijd is "
        
 
# st.sidebar.write(vraagtype_label)



# ---------------------------------------------------------
# Bepaal de uiteindelijke vraagtype code (random of vast)
# ---------------------------------------------------------

if vraagtype_vast == "4":
    
    # genereren van een random opdrachtkeuze uit 3 en de intro van het eindantwoord
    vraagtype = opdracht_waarde()
    if vraagtype == "1":
            antwoord_type = "De gemiddelde snelheid is: "
    elif vraagtype == "2": 
            antwoord_type = "De afstand is "
    elif vraagtype == "3":
            antwoord_type = "De tijd is "    
else:
    # vast vraagtype
    vraagtype = vraagtype_vast    

# ---------------------------------------------------------
# Als mix eenheden is gekozen, random eenheid genereren 
# ---------------------------------------------------------
if gecombineerde_eenheden == "3" and vraagtype_vast is not None:
    eenheid_waarde_vgem, eenheid_waarde_s, eenheid_waarde_t = genereer_random_eenheden()

# ---------------------------------------------------------
# Toon status en generereer opdracht
# ---------------------------------------------------------

# Header
st.header("Aron's fantastische oefenprogramma")
st.markdown("Hier kan je oefenen met het rekenen met gemiddelde snelheid")






# controle of opdracht kan starten

if gecombineerde_eenheden is not None and vraagtype is not None:
    
    # genereer de opdracht, maar ALLEEN als de status 'initial' is
    if st.session_state.status == 'initial': # FIX: Alleen initial
        # variabelen uit de functie halen
        opdracht_tekst, antwoord, gevraagde_eenheid = opdracht(
            vraagtype, eenheid_waarde_vgem, eenheid_waarde_s, eenheid_waarde_t
            ) 
        st.session_state.antwoord = antwoord
        st.session_state.gevraagde_eenheid = gevraagde_eenheid
        st.session_state.opdracht_tekst = opdracht_tekst # FIX: Sla de tekst op in state
        st.session_state.status = 'waiting_for_input'

    # toon de opdrachttekst
    st.markdown("---")
    st.subheader("De opdracht:")
    st.markdown(st.session_state.opdracht_tekst) # FIX: Toon opgeslagen tekst
    # st.write(f"Het antwoord is: {antwoord} {gevraagde_eenheid}") # Toon het antwoord (voor debugging)

    # input veld en correctie
    col_input, col_button = st.columns([3, 1])

    with col_input:
        # invoerveld voor de leerling. de key zorgt ervoor dat de waarde bewaard blijft totdat de gebruiker probeer opnieuw kiest.
        ingevuld = st.text_input(
            label = antwoord_type,
            value = st.session_state.antwoord_ingevuld,
            key = "antwoord_input_field",
            disabled = (st.session_state.status == 'correct' or st.session_state.status == 'opgegeven')

        ).replace(",", ".")
   
    
    with col_button:
        # extra ruimte om lager te plaatsen
        st.markdown('<br>', unsafe_allow_html=True)
        # gebruik de on_click om de controle direct uit te voeren
        if st.button(
            "Controleer Antwoord",
            key='controleer_butn',
            disabled=(st.session_state.status == 'correct' or st.session_state.status == 'opgegeven')
        ):
            st.session_state.antwoord_ingevuld = ingevuld  # update de ingevulde waarde in state
            controleer_antwoord(ingevuld)

    # feedback correctie en vervolgacties
    if st.session_state.status == 'correct':
        st.success("Juist!")
        if st.button("Volgende Opdracht", on_click = reset_opdracht):
            pass
    
    elif st.session_state.status == 'incorrect' or st.session_state.status == 'ongeldige_invoer':
        if st.session_state.status == 'incorrect':
            st.error('Onjuist...')
        elif st.session_state.status == 'ongeldige_invoer':
            st.warning('Ongeldige invoer. Voer alsjeblieft een getal in')

        col_retry, col_show = st.columns(2)

        with col_retry:
            # GEFIXED: Gebruik de on_click callback voor directe statuswijziging.
            st.button(
                "Probeer opnieuw", 
                key ='probeer_opnieuw',
                on_click = probeer_opnieuw_callback
            )

        
        with col_show:
            # GEFIXED: Gebruik de on_click callback voor directe statuswijziging.
            st.button("Toon antwoord", key = 'toon_antwoord_btn', on_click = toon_antwoord_callback)

    elif st.session_state.status == 'opgegeven':
        st.info(f"Het juiste antwoord is **{st.session_state.antwoord} {st.session_state.gevraagde_eenheid}**.")
        if st.button('Volgende opdracht', on_click = reset_opdracht):
            pass
else:
    # Toon de starttekst
    st.markdown("---")
    st.warning("Kies links in de zijbalk waarmee je wil oefenen (op je telefoon moet je op de pijltjes linksboven klikken)")


