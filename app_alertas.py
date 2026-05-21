import streamlit as st
from datetime import datetime
import re
import pytz

# ---------------------------
# PAGE CONFIG
# ---------------------------

st.set_page_config(
    page_title="Sistema de Alertas",
    page_icon="🔔",
    layout="centered"
)

# ---------------------------
# DATOS
# ---------------------------

cgm_opciones = [
    "Banfield", "Ingeniero Budge", "Llavallol", "Lomas de Zamora",
    "Parque Barón", "San José", "Santa Catalina", "Santa Marta",
    "Temperley", "Turdera", "Villa Albertina", "Villa Centenario",
    "Villa Fiorito", "Villa Lamadrid"
]

categorias = ["Sirena", "Policía", "Bomberos", "Violencia de Género", "Ambulancia"]

tipo_iconos = {
    "Whatsapp":  "💬",
    "Botmarket": "🤖",
    "Sistema":   "🖥️"
}

# ---------------------------
# GLOBAL STYLES
# ---------------------------

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">

<style>

/* ── RESET & BASE ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
.main, .block-container {
    background-color: #0e0b07 !important;
    font-family: 'Syne', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background-image:
        radial-gradient(ellipse 70% 45% at 50% -5%, rgba(245,158,11,0.10) 0%, transparent 65%),
        radial-gradient(ellipse 40% 30% at 85% 90%, rgba(220,100,0,0.06) 0%, transparent 60%),
        linear-gradient(180deg, #0e0b07 0%, #110d08 100%) !important;
    min-height: 100vh;
}

/* ── HIDE STREAMLIT CHROME ── */
header[data-testid="stHeader"],
footer,
#MainMenu,
[data-testid="stBottomBlockContainer"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="appCreatorAvatar"],
[class*="_profileContainer"],
[class*="_profilePreview"],
[class*="_viewerBadge"],
[class*="viewerBadge"],
[class*="ProfilePreview"],
[class*="styles_viewerBadge__"],
[class*="_imageMove"],
.stDeployButton,
.stAppDeployButton {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

/* ── BLOCK CONTAINER ── */
.block-container {
    max-width: 760px !important;
    padding: 2.5rem 2rem 4rem !important;
}

/* ── TYPOGRAPHY ── */
p, label, .stMarkdown p {
    font-family: 'Syne', sans-serif !important;
    color: #c4a97d !important;
    font-size: 0.875rem !important;
}

/* ── LABELS ── */
.stSelectbox label,
.stTextInput label,
.stDateInput label {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #b8905a !important;
    margin-bottom: 4px !important;
}

/* ── INPUTS ── */
.stTextInput input,
.stDateInput input {
    background-color: #17110a !important;
    border: 1px solid #2a1f12 !important;
    border-radius: 8px !important;
    color: #e8d5b0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.875rem !important;
    padding: 0.6rem 0.875rem !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    height: 44px !important;
}

.stTextInput input:focus,
.stDateInput input:focus {
    border-color: #f59e0b !important;
    box-shadow: 0 0 0 3px rgba(245,158,11,0.12) !important;
    outline: none !important;
}

.stTextInput input::placeholder {
    color: #3b2e1e !important;
    font-family: 'IBM Plex Mono', monospace !important;
}

/* ── SELECTBOX ── */
.stSelectbox > div > div {
    background-color: #17110a !important;
    border: 1px solid #2a1f12 !important;
    border-radius: 8px !important;
    color: #e8d5b0 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.875rem !important;
    min-height: 44px !important;
    transition: border-color 0.2s ease !important;
}

.stSelectbox > div > div:hover {
    border-color: #3d2d18 !important;
}

.stSelectbox > div > div:focus-within {
    border-color: #f59e0b !important;
    box-shadow: 0 0 0 3px rgba(245,158,11,0.12) !important;
}

.stSelectbox [data-baseweb="select"] span {
    color: #e8d5b0 !important;
    font-family: 'Syne', sans-serif !important;
}

/* Dropdown */
[data-baseweb="popover"],
[data-baseweb="menu"],
[data-baseweb="select"] ul {
    background-color: #1c1409 !important;
    border: 1px solid #2a1f12 !important;
    border-radius: 8px !important;
}

[data-baseweb="option"] {
    background-color: transparent !important;
    color: #c4a97d !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.875rem !important;
}

[data-baseweb="option"]:hover,
[data-baseweb="option"][aria-selected="true"] {
    background-color: rgba(245,158,11,0.12) !important;
    color: #f59e0b !important;
}

.stSelectbox svg { color: #4a3520 !important; }

/* ── DATE PICKER ── */
[data-baseweb="calendar"] {
    background-color: #1c1409 !important;
    border: 1px solid #2a1f12 !important;
    border-radius: 12px !important;
}

[data-baseweb="calendar"] * { color: #c4a97d !important; }

/* ── HR ── */
hr {
    border: none !important;
    border-top: 1px solid #1e1508 !important;
    margin: 1.5rem 0 !important;
}

/* ── CARD ── */
[data-testid="stVerticalBlockBorderWrapper"] > div {
    background: linear-gradient(150deg, #17110a 0%, #130f08 100%) !important;
    border: 1px solid #261b0e !important;
    border-radius: 16px !important;
    padding: 2rem !important;
    box-shadow: 0 4px 48px rgba(0,0,0,0.6), 0 1px 0 rgba(255,200,80,0.04) inset !important;
    position: relative !important;
    overflow: hidden !important;
}

[data-testid="stVerticalBlockBorderWrapper"] > div::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(245,158,11,0.35), transparent);
}

/* ── BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, #b45309 0%, #f59e0b 100%) !important;
    color: #0e0b07 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.05em !important;
    height: 50px !important;
    min-height: 50px !important;
    max-height: 50px !important;
    padding: 0 1rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 24px rgba(245,158,11,0.25) !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    line-height: 1 !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 32px rgba(245,158,11,0.40) !important;
    background: linear-gradient(135deg, #c96b12 0%, #fbbf24 100%) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── ALERTS ── */
div[class*="stSuccess"] > div {
    background-color: rgba(245,158,11,0.10) !important;
    border-left: 3px solid #f59e0b !important;
    color: #fbbf24 !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
}

div[class*="stError"] > div {
    background-color: rgba(239,68,68,0.08) !important;
    border-left: 3px solid #ef4444 !important;
    color: #fca5a5 !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
}

/* ── COLUMNS ── */
[data-testid="stHorizontalBlock"] { gap: 1.25rem !important; }

/* ── CUSTOM CLASSES ── */
.badge-header {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.2);
    border-radius: 100px;
    padding: 5px 14px 5px 10px;
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #f59e0b;
    margin-bottom: 1.25rem;
}

.badge-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #f59e0b;
    box-shadow: 0 0 6px #f59e0b;
    animation: pulse-dot 2s infinite;
}

@keyframes pulse-dot {
    0%, 100% { opacity: 1; box-shadow: 0 0 6px #f59e0b; }
    50% { opacity: 0.5; box-shadow: 0 0 14px #f59e0b; }
}

.main-title {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #f0dbb8;
    margin: 0 0 0.3rem;
    letter-spacing: -0.02em;
    line-height: 1.15;
}

.main-subtitle {
    font-family: 'Syne', sans-serif;
    font-size: 0.83rem;
    font-weight: 400;
    color: #4a3520;
    margin: 0 0 2rem;
}

.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #9a7a50;
    margin: 1.5rem 0 0.85rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #2a1f12;
}

.field-hint {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #7a6040;
    margin-top: 3px;
}

/* ── TIPO SLICER ── */
.tipo-grid {
    display: flex;
    gap: 12px;
    margin-bottom: 0.25rem;
}

.tipo-btn {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    padding: 14px 10px;
    background: #17110a;
    border: 1px solid #2a1f12;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: center;
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    font-weight: 600;
    color: #a08060;
    letter-spacing: 0.04em;
}

.tipo-btn:hover {
    border-color: #4a3520;
    color: #d4b07d;
    background: #1c1409;
}

.tipo-btn.selected {
    border-color: #f59e0b;
    background: rgba(245,158,11,0.10);
    color: #f59e0b;
    box-shadow: 0 0 0 1px rgba(245,158,11,0.3), 0 4px 16px rgba(245,158,11,0.10);
}

.tipo-icon {
    font-size: 1.5rem;
    line-height: 1;
}

/* ── CAT GRID ── */
.cat-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 4px;
}

.cat-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 16px;
    background: #17110a;
    border: 1px solid #2a1f12;
    border-radius: 100px;
    cursor: pointer;
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    font-weight: 600;
    color: #a08060;
    letter-spacing: 0.03em;
    transition: all 0.18s ease;
    white-space: nowrap;
}

.cat-pill:hover {
    border-color: #4a3520;
    color: #d4b07d;
}

.cat-pill.selected {
    border-color: #f59e0b;
    background: rgba(245,158,11,0.10);
    color: #f59e0b;
    box-shadow: 0 0 0 1px rgba(245,158,11,0.25);
}

</style>

<script>
function ocultarBadge() {
    const sels = ['[class*="viewerBadge"]','[class*="ProfilePreview"]',
                  '[class*="_profileContainer"]','a[href*="streamlit.io"]'];
    sels.forEach(s => {
        document.querySelectorAll(s).forEach(el => {
            for (let i=0,n=el; i<5; i++, n=n.parentElement||n)
                n.style.setProperty('display','none','important');
        });
    });
}
ocultarBadge();
setInterval(ocultarBadge, 500);
</script>
""", unsafe_allow_html=True)

# ---------------------------
# SESSION STATE
# ---------------------------

if "form_key" not in st.session_state:
    st.session_state.form_key = 0
if "tipo_alerta" not in st.session_state:
    st.session_state.tipo_alerta = None
if "categoria_sel" not in st.session_state:
    st.session_state.categoria_sel = None
if "success_msg" not in st.session_state:
    st.session_state.success_msg = None
if "error_msg" not in st.session_state:
    st.session_state.error_msg = None

# ---------------------------
# HEADER
# ---------------------------

col_logo, col_text = st.columns([1, 8])

with col_logo:
    st.image("logo_izquierda.png", width=64)

with col_text:
    st.markdown("""
    <div style="padding-top:6px;">
        <div class="badge-header">
            <span class="badge-dot"></span>
            Monitoreo activo
        </div>
        <div class="main-title">Carga de Alertas</div>
        <div class="main-subtitle">Registro de alertas entrantes — Partido de Lomas de Zamora</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------------------------
# MENSAJES DE ESTADO
# ---------------------------

if st.session_state.success_msg:
    st.success(st.session_state.success_msg)
    st.session_state.success_msg = None

if st.session_state.error_msg:
    st.error(st.session_state.error_msg)
    st.session_state.error_msg = None

# ---------------------------
# FORMULARIO
# ---------------------------

fk = st.session_state.form_key

with st.container(border=True):

    # ── BLOQUE 0: Tipo de alerta ──
    st.markdown('<div class="section-label">① Tipo de alerta</div>', unsafe_allow_html=True)

    tipo_cols = st.columns(3)
    tipos = list(tipo_iconos.keys())

    for i, tipo in enumerate(tipos):
        with tipo_cols[i]:
            selected_class = "selected" if st.session_state.tipo_alerta == tipo else ""
            st.markdown(f"""
            <div class="tipo-btn {selected_class}" id="tipo-{tipo}">
                <span class="tipo-icon">{tipo_iconos[tipo]}</span>
                {tipo}
            </div>
            """, unsafe_allow_html=True)
            if st.button(tipo, key=f"tipo_btn_{tipo}_{fk}", use_container_width=True):
                st.session_state.tipo_alerta = tipo
                st.rerun()

    # Mostrar selección actual debajo (feedback visual)
    if st.session_state.tipo_alerta:
        st.markdown(
            f'<div style="font-family:\'Syne\',sans-serif; font-size:0.75rem; '
            f'color:#f59e0b; margin-top:2px; letter-spacing:0.06em;">'
            f'✓ &nbsp; {st.session_state.tipo_alerta} seleccionado</div>',
            unsafe_allow_html=True
        )

    # ── BLOQUE 1: Temporalidad ──
    st.markdown('<div class="section-label">② Temporalidad</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        fecha = st.date_input(
            "Fecha del evento",
            datetime.today(),
            key=f"fecha_{fk}"
        )
    with col2:
        horario = st.text_input(
            "Horario",
            value="",
            placeholder="HH:MM",
            key=f"horario_{fk}"
        )
        st.markdown(
            '<div class="field-hint">Formato 24 h — ej: 08:30 / 21:45</div>',
            unsafe_allow_html=True
        )

    # ── BLOQUE 2: Jurisdicción ──
    st.markdown('<div class="section-label">③ CGM</div>', unsafe_allow_html=True)

    cgm = st.selectbox(
        "Centro de Gestión Municipal",
        options=["Seleccione"] + cgm_opciones,
        index=0,
        key=f"cgm_{fk}"
    )

    # ── BLOQUE 3: Categoría ──
    st.markdown('<div class="section-label">④ Categoría</div>', unsafe_allow_html=True)

    cat_icons = {
        "Sirena":             "🚨",
        "Policía":            "👮",
        "Bomberos":           "🚒",
        "Violencia de Género":"🛡️",
        "Ambulancia":         "🚑"
    }

    cat_cols = st.columns(len(categorias))
    for i, cat in enumerate(categorias):
        with cat_cols[i]:
            is_sel = st.session_state.categoria_sel == cat
            # Reduce font for long labels
            font_size = "0.72rem" if len(cat) > 10 else "0.85rem"
            btn_style = f"""
            <style>
            div[data-testid="column"]:nth-child({i+1}) .stButton > button {{
                font-size: {font_size} !important;
                padding: 0 0.4rem !important;
                letter-spacing: 0.02em !important;
            }}
            </style>
            """
            st.markdown(btn_style, unsafe_allow_html=True)
            label = f"{cat_icons[cat]} {cat}"
            if st.button(label, key=f"cat_{cat}_{fk}", use_container_width=True):
                st.session_state.categoria_sel = cat
                st.rerun()

    if st.session_state.categoria_sel:
        st.markdown(
            f'<div style="font-family:\'Syne\',sans-serif; font-size:0.75rem; '
            f'color:#f59e0b; margin-top:4px; letter-spacing:0.06em;">'
            f'✓ &nbsp; {st.session_state.categoria_sel} seleccionada</div>',
            unsafe_allow_html=True
        )

# ── BOTÓN GUARDAR ──
st.markdown("<div style='height:1.25rem'></div>", unsafe_allow_html=True)
submitted = st.button(
    "Registrar Alerta  →",
    use_container_width=True,
    key=f"submit_{fk}"
)

# ---------------------------
# VALIDACIÓN (sin backend)
# ---------------------------

if submitted:

    horario_input = st.session_state.get(f"horario_{fk}", "").strip()
    cgm_val       = st.session_state.get(f"cgm_{fk}", "Seleccione")
    tipo_val      = st.session_state.tipo_alerta
    cat_val       = st.session_state.categoria_sel

    errores = []
    horario_valido = re.match(r"^([01]\d|2[0-3]):([0-5]\d)$", horario_input)

    if not tipo_val:
        errores.append("Debe seleccionar el Tipo de alerta")
    if not horario_valido:
        errores.append("Horario inválido — usar formato HH:MM")
    if cgm_val == "Seleccione":
        errores.append("Debe seleccionar un CGM")
    if not cat_val:
        errores.append("Debe seleccionar una Categoría")

    if errores:
        st.session_state.error_msg = "  ·  ".join(errores)
        st.rerun()
    else:
        # ── BACKEND PLACEHOLDER ──
        # Aquí irá la lógica de guardado una vez definido el back
        # Ejemplo:
        # sheet.append_row([...])
        # requests.post(api_url, json={...})

        st.session_state.success_msg = "Alerta registrada correctamente."
        st.session_state.form_key += 1
        st.session_state.tipo_alerta = None
        st.session_state.categoria_sel = None
        st.rerun()
