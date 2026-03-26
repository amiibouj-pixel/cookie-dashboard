"""
╔══════════════════════════════════════════════════════════════════╗
║        THE COOKIE COMPANY — STRATEGIC INTELLIGENCE DASHBOARD    ║
║        Built with Streamlit · Plotly · Python                   ║
╚══════════════════════════════════════════════════════════════════╝

GUIDE DE DÉPLOIEMENT (Streamlit Community Cloud)
=================================================

ÉTAPE 1 — Créer un compte GitHub gratuit
─────────────────────────────────────────
1. Rendez-vous sur https://github.com
2. Cliquez sur "Sign up" (en haut à droite).
3. Entrez votre adresse e-mail, choisissez un mot de passe et un
   nom d'utilisateur (ex : the-cookie-co).
4. Confirmez votre e-mail via le lien reçu.

ÉTAPE 2 — Déposer app.py dans un Repository GitHub
────────────────────────────────────────────────────
1. Une fois connecté à GitHub, cliquez sur le bouton vert "New"
   (ou allez sur https://github.com/new).
2. Donnez un nom au repo : "cookie-dashboard" (tout en minuscule).
3. Laissez-le en "Public", cochez "Add a README file", cliquez
   sur "Create repository".
4. Dans votre repo, cliquez sur "Add file" → "Upload files".
5. Glissez-déposez votre fichier app.py ET votre fichier
   requirements.txt (contenu ci-dessous).
6. Cliquez sur "Commit changes" (bouton vert).

   Contenu du fichier requirements.txt :
   ───────────────────────────────────────
   streamlit>=1.32.0
   plotly>=5.18.0
   pandas>=2.0.0
   numpy>=1.24.0

ÉTAPE 3 — Héberger sur Streamlit Community Cloud (gratuit)
──────────────────────────────────────────────────────────
1. Rendez-vous sur https://share.streamlit.io
2. Cliquez sur "Sign in with GitHub" et autorisez l'accès.
3. Cliquez sur le bouton "New app" (en haut à droite).
4. Dans le formulaire :
   - Repository : sélectionnez "cookie-dashboard"
   - Branch : main
   - Main file path : app.py
5. Cliquez sur "Deploy!" et attendez ~2 minutes.
6. Votre URL de partage sera du type :
   https://the-cookie-co-dashboard.streamlit.app  🎉

IMPORTANT : Pour que le dashboard lise le CSV, déposez également
Cookie_Company.csv dans votre repository GitHub (même dossier).
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ─────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="The Cookie Company · Dashboard",
    page_icon="🍪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────
# DESIGN SYSTEM — CSS GLOBAL
# ─────────────────────────────────────────────────────────────────
ACCENT      = "#607D8B"   # Bleu acier mat
ACCENT_SOFT = "#B0BEC5"   # Bleu acier clair
BG          = "#F8F9FA"   # Blanc cassé
CARD_BG     = "#FFFFFF"
TEXT        = "#37474F"   # Gris ardoise
TEXT_LIGHT  = "#78909C"
POSITIVE    = "#81C784"   # Vert sauge
NEGATIVE    = "#EF9A9A"   # Rose pâle
GOLD        = "#FFD54F"

st.markdown(f"""
<style>
  /* ── Google Font ── */
  @import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@300;400;600;700&display=swap');

  /* ── Reset & base ── */
  *, *::before, *::after {{ box-sizing: border-box; }}
  html, body, [class*="css"] {{
    font-family: 'Comfortaa', sans-serif !important;
    background-color: {BG} !important;
    color: {TEXT} !important;
  }}

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {{
    background-color: {CARD_BG} !important;
    border-right: 1px solid #ECEFF1;
  }}
  [data-testid="stSidebar"] * {{ font-family: 'Comfortaa', sans-serif !important; }}

  /* ── Remove Streamlit chrome ── */
  #MainMenu, footer, header {{ visibility: hidden; }}
  .block-container {{ padding-top: 2rem; padding-bottom: 4rem; max-width: 1200px; }}

  /* ── Cards ── */
  .card {{
    background: {CARD_BG};
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    border: 1px solid #ECEFF1;
  }}

  /* ── Section titles ── */
  .section-tag {{
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: {ACCENT};
    margin-bottom: 6px;
  }}
  .section-title {{
    font-size: 22px;
    font-weight: 700;
    color: {TEXT};
    margin-bottom: 4px;
    line-height: 1.3;
  }}
  .section-sub {{
    font-size: 13px;
    color: {TEXT_LIGHT};
    margin-bottom: 24px;
  }}

  /* ── Hero ── */
  .hero-wrap {{
    background: {CARD_BG};
    border-radius: 20px;
    padding: 40px 44px 32px;
    margin-bottom: 28px;
    border: 1px solid #ECEFF1;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  }}
  .hero-logo {{
    font-size: 36px;
    font-weight: 700;
    color: {TEXT};
    letter-spacing: -0.5px;
  }}
  .hero-tagline {{
    font-size: 13px;
    color: {TEXT_LIGHT};
    margin-top: 4px;
    letter-spacing: 1px;
    text-transform: uppercase;
  }}
  .hero-divider {{
    height: 1px;
    background: linear-gradient(to right, {ACCENT}, transparent);
    margin: 20px 0;
    opacity: 0.3;
  }}

  /* ── KPI cards ── */
  .kpi-grid {{ display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 20px; }}
  .kpi-box {{
    flex: 1; min-width: 160px;
    background: {CARD_BG};
    border-radius: 14px;
    padding: 20px 24px;
    border: 1px solid #ECEFF1;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }}
  .kpi-label {{
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: {TEXT_LIGHT};
    margin-bottom: 8px;
  }}
  .kpi-value {{
    font-size: 28px;
    font-weight: 700;
    color: {TEXT};
    line-height: 1;
  }}
  .kpi-delta {{
    font-size: 12px;
    color: {TEXT_LIGHT};
    margin-top: 4px;
  }}
  .kpi-positive {{ color: #4CAF50; }}
  .kpi-negative {{ color: #E57373; }}

  /* ── COVID KPI géant ── */
  .covid-kpi-wrap {{
    text-align: center;
    padding: 40px 20px;
  }}
  .covid-kpi-number {{
    font-size: 96px;
    font-weight: 700;
    color: #E57373;
    line-height: 1;
    letter-spacing: -2px;
  }}
  .covid-kpi-label {{
    font-size: 16px;
    color: {TEXT_LIGHT};
    margin-top: 12px;
    letter-spacing: 1px;
  }}
  .covid-kpi-context {{
    font-size: 12px;
    color: {TEXT_LIGHT};
    margin-top: 8px;
    opacity: 0.7;
  }}

  /* ── BCG quadrant labels ── */
  .bcg-legend {{
    display: flex; gap: 20px; flex-wrap: wrap;
    margin-top: 12px; margin-bottom: 4px;
  }}
  .bcg-item {{
    display: flex; align-items: center; gap: 8px;
    font-size: 12px; color: {TEXT_LIGHT};
  }}
  .bcg-dot {{
    width: 10px; height: 10px;
    border-radius: 50%;
    display: inline-block;
  }}

  /* ── Social / HookStrike posts ── */
  .post-card {{
    background: {BG};
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 16px;
    border-left: 3px solid {ACCENT};
  }}
  .post-platform {{
    font-size: 10px; font-weight: 700;
    letter-spacing: 2px; text-transform: uppercase;
    color: {ACCENT}; margin-bottom: 10px;
  }}
  .post-hook {{
    font-size: 17px; font-weight: 700;
    color: {TEXT}; margin-bottom: 8px; line-height: 1.4;
  }}
  .post-strike {{
    font-size: 13px; color: {TEXT_LIGHT};
    line-height: 1.6;
  }}
  .post-tag {{
    font-size: 11px; color: {ACCENT_SOFT};
    margin-top: 10px;
  }}

  /* ── Segment cards ── */
  .segment-card {{
    background: {BG};
    border-radius: 14px;
    padding: 24px 28px;
    border: 1px solid #ECEFF1;
  }}
  .segment-title {{
    font-size: 15px; font-weight: 700;
    color: {TEXT}; margin-bottom: 8px;
  }}
  .segment-body {{
    font-size: 13px; color: {TEXT_LIGHT};
    line-height: 1.7;
  }}

  /* ── Deploy guide ── */
  .deploy-step {{
    display: flex; gap: 20px; margin-bottom: 20px;
    align-items: flex-start;
  }}
  .deploy-num {{
    width: 36px; height: 36px; border-radius: 50%;
    background: {ACCENT}; color: white;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 14px; flex-shrink: 0;
  }}
  .deploy-content {{ flex: 1; }}
  .deploy-title {{
    font-size: 14px; font-weight: 700;
    color: {TEXT}; margin-bottom: 4px;
  }}
  .deploy-body {{
    font-size: 12px; color: {TEXT_LIGHT};
    line-height: 1.6;
  }}
  .deploy-code {{
    background: #ECEFF1; border-radius: 8px;
    padding: 8px 12px; margin-top: 8px;
    font-family: monospace; font-size: 11px;
    color: {TEXT}; display: inline-block;
  }}

  /* ── Nav sidebar ── */
  .nav-title {{
    font-size: 10px; font-weight: 700;
    letter-spacing: 2px; text-transform: uppercase;
    color: {TEXT_LIGHT}; margin-bottom: 16px;
    padding-bottom: 8px; border-bottom: 1px solid #ECEFF1;
  }}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# DATA LOADING & SIMULATION (2019-2025)
# ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_and_simulate():
    df_raw = pd.read_csv("Cookie_Company.csv")
    df_raw["Country"] = df_raw["Country"].replace("états-unis", "USA")
    df_raw["Date"] = pd.to_datetime(df_raw["Date"])

    # Keep only complete years in raw (2018-2020)
    base = df_raw[df_raw["Year"].isin([2018, 2019, 2020])].copy()

    # Simulate 2021-2025 by extrapolating from 2019-2020 with realistic trends
    rng = np.random.default_rng(42)
    products       = base["Product"].unique()
    countries      = base["Country"].unique()
    month_names    = {1:"January",2:"February",3:"March",4:"April",5:"May",
                      6:"June",7:"July",8:"August",9:"September",
                      10:"October",11:"November",12:"December"}

    # Growth rates per product (post-COVID recovery + trends)
    growth = {
        "Chocolate Chip":               0.10,
        "White Chocolate Macadamia Nut":0.14,
        "Oatmeal Raisin":              0.06,
        "Snickerdoodle":               0.08,
        "Sugar":                       0.03,
        "Fortune Cookie":             -0.02,
    }

    price_map  = dict(zip(base["Product"], base["Revenue per cookie"]))
    cost_map   = dict(zip(base["Product"], base["Cost per cookie"]))

    rows = []
    for year in range(2021, 2026):
        for month in range(1, 13):
            for country in countries:
                for product in products:
                    base_sub = base[
                        (base["Product"] == product) &
                        (base["Country"] == country) &
                        (base["Month Number"] == month)
                    ]["Units Sold"]
                    if len(base_sub) == 0:
                        base_units = rng.uniform(400, 2000)
                    else:
                        base_units = base_sub.mean()

                    g = growth[product]
                    years_since_2020 = year - 2020
                    units = base_units * ((1 + g) ** years_since_2020)
                    units *= rng.uniform(0.88, 1.12)   # noise
                    # Q4 seasonality boost
                    if month in [11, 12]:
                        units *= rng.uniform(1.15, 1.35)
                    # Summer dip
                    if month in [7, 8]:
                        units *= rng.uniform(0.85, 0.98)

                    rev   = units * price_map.get(product, 4)
                    cost  = units * cost_map.get(product, 2)
                    profit = rev - cost

                    rows.append({
                        "Country":           country,
                        "Product":           product,
                        "Units Sold":        round(units, 1),
                        "Revenue per cookie":price_map.get(product, 4),
                        "Cost per cookie":   cost_map.get(product, 2),
                        "Revenue":           round(rev, 2),
                        "Cost":              round(cost, 2),
                        "Profit":            round(profit, 2),
                        "Date":              pd.Timestamp(year=year, month=month, day=1),
                        "Month Number":      month,
                        "Month Name":        month_names[month],
                        "Year":              year,
                    })

    df_sim = pd.DataFrame(rows)
    df_all = pd.concat([base, df_sim], ignore_index=True)
    df_all = df_all[df_all["Year"] >= 2019]   # 2019-2025
    return df_all, base


df, df_base = load_and_simulate()


# ─────────────────────────────────────────────────────────────────
# SIDEBAR — NAVIGATION
# ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:24px 0 8px; text-align:center;'>
      <div style='font-size:28px;'>🍪</div>
      <div style='font-size:13px;font-weight:700;color:#37474F;margin-top:6px;'>Cookie Company</div>
      <div style='font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#90A4AE;'>Dashboard BI</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<div class='nav-title'>Navigation</div>", unsafe_allow_html=True)

    sections = {
        "📊 Vue Globale":           "kpis",
        "🌍 Volume par Pays":       "pays",
        "🦠 Impact COVID-19":       "covid",
        "📅 Saisonnalité":          "saison",
        "⭐ Matrice BCG":           "bcg",
        "🎯 Stratégie Sociale":     "social",
        "🚀 Guide Déploiement":     "deploy",
    }
    for label, anchor in sections.items():
        st.markdown(
            f"<a href='#{anchor}' style='display:block;padding:8px 12px;border-radius:8px;"
            f"text-decoration:none;color:#37474F;font-size:13px;margin-bottom:2px;"
            f"transition:background 0.2s;'>{label}</a>",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    # Year filter
    st.markdown("<div class='nav-title'>Filtres</div>", unsafe_allow_html=True)
    years_available = sorted(df["Year"].unique())
    selected_years = st.multiselect(
        "Années",
        options=years_available,
        default=years_available,
        key="year_filter"
    )

df_f = df[df["Year"].isin(selected_years)] if selected_years else df


# ─────────────────────────────────────────────────────────────────
# PLOTLY THEME
# ─────────────────────────────────────────────────────────────────
PLOT_LAYOUT = dict(
    template="plotly_white",
    font=dict(family="Comfortaa, sans-serif", color=TEXT, size=12),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=16, r=16, t=32, b=16),
    hoverlabel=dict(
        bgcolor=CARD_BG,
        font=dict(family="Comfortaa, sans-serif", size=12, color=TEXT),
        bordercolor="#ECEFF1",
    ),
)


# ─────────────────────────────────────────────────────────────────
# SECTION 0 — HERO
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero-wrap'>
  <div style='display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:16px;'>
    <div>
      <div class='hero-logo'>🍪 The Cookie Company</div>
      <div class='hero-tagline'>Strategic Intelligence Dashboard · 2019 – 2025</div>
    </div>
    <div style='text-align:right;'>
      <div style='font-size:11px;color:#90A4AE;letter-spacing:1px;'>Dernière mise à jour</div>
      <div style='font-size:13px;font-weight:700;color:#607D8B;'>Données simulées 2019–2025</div>
    </div>
  </div>
  <div class='hero-divider'></div>
  <div style='font-size:13px;color:#78909C;line-height:1.7;max-width:700px;'>
    Ce tableau de bord regroupe l'ensemble des indicateurs clés de performance, l'analyse de portefeuille BCG
    et les recommandations stratégiques pour optimiser votre mix produits et vos campagnes réseaux sociaux.
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# SECTION 1 — KPIs GLOBAUX
# ─────────────────────────────────────────────────────────────────
st.markdown("<div id='kpis'></div>", unsafe_allow_html=True)
st.markdown("""
<div class='card'>
  <div class='section-tag'>Vue Globale</div>
  <div class='section-title'>Indicateurs Clés de Performance</div>
  <div class='section-sub'>Consolidé sur la période sélectionnée</div>
""", unsafe_allow_html=True)

total_rev    = df_f["Revenue"].sum()
total_profit = df_f["Profit"].sum()
total_units  = df_f["Units Sold"].sum()
margin_pct   = (total_profit / total_rev * 100) if total_rev > 0 else 0

# YoY comparison (last two years in selection)
sel_sorted = sorted(selected_years) if selected_years else sorted(df["Year"].unique())
if len(sel_sorted) >= 2:
    rev_last   = df[df["Year"] == sel_sorted[-1]]["Revenue"].sum()
    rev_prev   = df[df["Year"] == sel_sorted[-2]]["Revenue"].sum()
    yoy        = (rev_last - rev_prev) / rev_prev * 100 if rev_prev else 0
    yoy_str    = f"{'▲' if yoy >= 0 else '▼'} {abs(yoy):.1f}% vs {sel_sorted[-2]}"
    yoy_cls    = "kpi-positive" if yoy >= 0 else "kpi-negative"
else:
    yoy_str = "—"
    yoy_cls = ""

best_product = df_f.groupby("Product")["Revenue"].sum().idxmax()

st.markdown(f"""
<div class='kpi-grid'>
  <div class='kpi-box'>
    <div class='kpi-label'>Chiffre d'Affaires</div>
    <div class='kpi-value'>${total_rev/1e6:.1f}M</div>
    <div class='kpi-delta {yoy_cls}'>{yoy_str}</div>
  </div>
  <div class='kpi-box'>
    <div class='kpi-label'>Profit Total</div>
    <div class='kpi-value'>${total_profit/1e6:.1f}M</div>
    <div class='kpi-delta'>Marge nette {margin_pct:.1f}%</div>
  </div>
  <div class='kpi-box'>
    <div class='kpi-label'>Unités Vendues</div>
    <div class='kpi-value'>{total_units/1e6:.1f}M</div>
    <div class='kpi-delta'>Cookies écoulés</div>
  </div>
  <div class='kpi-box'>
    <div class='kpi-label'>Produit Vedette</div>
    <div class='kpi-value' style='font-size:18px;margin-top:4px;'>{best_product}</div>
    <div class='kpi-delta'>N°1 en revenus</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # close card


# ─────────────────────────────────────────────────────────────────
# SECTION 2 — VOLUME PAR PAYS
# ─────────────────────────────────────────────────────────────────
st.markdown("<div id='pays'></div>", unsafe_allow_html=True)
st.markdown("""
<div class='card'>
  <div class='section-tag'>Géographie · BI</div>
  <div class='section-title'>Volume des Ventes par Pays</div>
  <div class='section-sub'>Chiffre d'affaires consolidé — toutes périodes sélectionnées</div>
""", unsafe_allow_html=True)

rev_country = (
    df_f.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=True)
    .reset_index()
)
rev_country["Revenue_M"] = rev_country["Revenue"] / 1e6

fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(
    x=rev_country["Revenue_M"],
    y=rev_country["Country"],
    orientation="h",
    marker=dict(
        color=[ACCENT if i < len(rev_country) - 1 else ACCENT for i in range(len(rev_country))],
        opacity=[0.55 + 0.09 * i for i in range(len(rev_country))],
        line=dict(width=0),
    ),
    text=[f"${v:.1f}M" for v in rev_country["Revenue_M"]],
    textposition="outside",
    textfont=dict(size=12, color=TEXT),
    hovertemplate="<b>%{y}</b><br>CA : $%{x:.2f}M<extra></extra>",
))
fig_bar.update_layout(
    **PLOT_LAYOUT,
    xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
    yaxis=dict(showgrid=False, tickfont=dict(size=13)),
    bargap=0.4,
    height=280,
)
st.plotly_chart(fig_bar, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# SECTION 3 — IMPACT COVID-19
# ─────────────────────────────────────────────────────────────────
st.markdown("<div id='covid'></div>", unsafe_allow_html=True)
st.markdown("""
<div class='card'>
  <div class='section-tag'>Analyse de Crise · BI</div>
  <div class='section-title'>Impact COVID-19 sur le Chiffre d'Affaires</div>
  <div class='section-sub'>Vague 17 mars – 11 mai 2020 vs même période 2019</div>
""", unsafe_allow_html=True)

df_covid_raw = df_base.copy()
df_covid_raw["Date"] = pd.to_datetime(df_covid_raw["Date"])
rev_2020 = df_covid_raw[
    (df_covid_raw["Date"] >= "2020-03-17") & (df_covid_raw["Date"] <= "2020-05-11")
]["Revenue"].sum()
rev_2019 = df_covid_raw[
    (df_covid_raw["Date"] >= "2019-03-17") & (df_covid_raw["Date"] <= "2019-05-11")
]["Revenue"].sum()
covid_pct = (rev_2020 - rev_2019) / rev_2019 * 100

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown(f"""
    <div class='covid-kpi-wrap'>
      <div class='covid-kpi-number'>{covid_pct:.1f}%</div>
      <div class='covid-kpi-label'>Variation du CA mondial</div>
      <div class='covid-kpi-context'>
        2019 : ${rev_2019/1e6:.2f}M &nbsp;→&nbsp; 2020 : ${rev_2020/1e6:.2f}M<br>
        Période de confinement · 17 mars – 11 mai
      </div>
    </div>
    """, unsafe_allow_html=True)

# Mini bar comparaison
fig_covid = go.Figure()
fig_covid.add_trace(go.Bar(
    x=["Période 2019", "Période 2020 (COVID)"],
    y=[rev_2019 / 1e6, rev_2020 / 1e6],
    marker_color=[ACCENT_SOFT, "#EF9A9A"],
    marker_line_width=0,
    text=[f"${v:.2f}M" for v in [rev_2019 / 1e6, rev_2020 / 1e6]],
    textposition="outside",
    width=0.4,
    hovertemplate="%{x}<br>$%{y:.2f}M<extra></extra>",
))
fig_covid.update_layout(
    **PLOT_LAYOUT,
    height=220,
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
    showlegend=False,
)
st.plotly_chart(fig_covid, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# SECTION 4 — SAISONNALITÉ
# ─────────────────────────────────────────────────────────────────
st.markdown("<div id='saison'></div>", unsafe_allow_html=True)
st.markdown("""
<div class='card'>
  <div class='section-tag'>Tendances · BI</div>
  <div class='section-title'>Saisonnalité des Ventes</div>
  <div class='section-sub'>Évolution mensuelle du chiffre d'affaires — toutes périodes</div>
""", unsafe_allow_html=True)

monthly = (
    df_f.groupby(["Year", "Month Number", "Month Name"])["Revenue"]
    .sum()
    .reset_index()
    .sort_values(["Year", "Month Number"])
)
monthly["Period"] = monthly["Year"].astype(str) + "-" + monthly["Month Number"].astype(str).str.zfill(2)

# One line per year
years_for_area = sorted(monthly["Year"].unique())
color_scale = [
    "#B0BEC5", "#90A4AE", "#78909C",
    "#607D8B", "#546E7A", "#455A64", "#37474F"
]

fig_area = go.Figure()
for i, yr in enumerate(years_for_area):
    sub = monthly[monthly["Year"] == yr].sort_values("Month Number")
    color = color_scale[i % len(color_scale)]
    is_last = (yr == years_for_area[-1])
    fig_area.add_trace(go.Scatter(
        x=sub["Month Name"],
        y=sub["Revenue"] / 1e3,
        mode="lines",
        name=str(yr),
        line=dict(color=color, width=2.5 if is_last else 1.5),
        fill="tozeroy" if is_last else "none",
        fillcolor=f"rgba(96,125,139,0.06)" if is_last else None,
        opacity=1.0 if is_last else 0.55,
        hovertemplate=f"<b>{yr}</b><br>%{{x}} : $%{{y:.0f}}K<extra></extra>",
    ))

fig_area.update_layout(
    **PLOT_LAYOUT,
    height=320,
    xaxis=dict(showgrid=False, tickfont=dict(size=11)),
    yaxis=dict(showgrid=True, gridcolor="#ECEFF1", tickformat="$,.0f", ticksuffix="K"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                font=dict(size=11)),
    hovermode="x unified",
)
st.plotly_chart(fig_area, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# SECTION 5 — MATRICE BCG
# ─────────────────────────────────────────────────────────────────
st.markdown("<div id='bcg'></div>", unsafe_allow_html=True)
st.markdown("""
<div class='card'>
  <div class='section-tag'>Portefeuille Produits · Matrice BCG</div>
  <div class='section-title'>Positionnement Stratégique des Produits</div>
  <div class='section-sub'>Part de marché relative × Taux de croissance · Taille = Profit généré</div>
""", unsafe_allow_html=True)

# Compute BCG metrics per product
years_s = sorted(df["Year"].unique())
if len(years_s) >= 2:
    yr_last, yr_prev = years_s[-1], years_s[-2]
else:
    yr_last, yr_prev = years_s[-1], years_s[-1]

rev_by_prod_last = df[df["Year"] == yr_last].groupby("Product")["Revenue"].sum()
rev_by_prod_prev = df[df["Year"] == yr_prev].groupby("Product")["Revenue"].sum()

total_market_last = rev_by_prod_last.sum()
total_market_prev = rev_by_prod_prev.sum()

bcg_rows = []
for product in df["Product"].unique():
    rev_l = rev_by_prod_last.get(product, 0)
    rev_p = rev_by_prod_prev.get(product, 1)
    market_share = rev_l / total_market_last if total_market_last else 0
    growth_rate  = (rev_l - rev_p) / rev_p * 100 if rev_p else 0
    profit_total = df_f[df_f["Product"] == product]["Profit"].sum()
    # Relative market share: vs avg competitor
    avg_share = 1 / len(df["Product"].unique())
    rel_share = market_share / avg_share
    bcg_rows.append({
        "Product": product,
        "Market Share": market_share * 100,
        "Relative Share": rel_share,
        "Growth Rate": growth_rate,
        "Profit": profit_total,
    })

bcg_df = pd.DataFrame(bcg_rows)

# BCG quadrant classification
def classify_bcg(row):
    if row["Relative Share"] >= 1.0 and row["Growth Rate"] >= 8:
        return "⭐ Vedette"
    elif row["Relative Share"] >= 1.0 and row["Growth Rate"] < 8:
        return "🐄 Vache à lait"
    elif row["Relative Share"] < 1.0 and row["Growth Rate"] >= 8:
        return "❓ Dilemme"
    else:
        return "💀 Poids mort"

bcg_df["Quadrant"] = bcg_df.apply(classify_bcg, axis=1)

bcg_colors = {
    "⭐ Vedette":      ACCENT,
    "🐄 Vache à lait": "#81C784",
    "❓ Dilemme":      "#FFD54F",
    "💀 Poids mort":   "#EF9A9A",
}

fig_bcg = go.Figure()

# Quadrant background rectangles
growth_mid = bcg_df["Growth Rate"].median()
share_mid  = 1.0  # relative share = 1 is the natural split

# Background quadrants
q_colors = ["rgba(129,199,132,0.06)", "rgba(96,125,139,0.06)",
            "rgba(239,154,154,0.06)", "rgba(255,213,79,0.06)"]
for quad_name, color, x0, x1, y0, y1 in [
    ("Vaches à lait", "rgba(129,199,132,0.08)", 1, 4.5, -5, growth_mid),
    ("Vedettes",      "rgba(96,125,139,0.08)",  1, 4.5, growth_mid, 25),
    ("Poids morts",   "rgba(239,154,154,0.08)", 0, 1,   -5, growth_mid),
    ("Dilemmes",      "rgba(255,213,79,0.08)",  0, 1,   growth_mid, 25),
]:
    fig_bcg.add_shape(type="rect",
        x0=x0, x1=x1, y0=y0, y1=y1,
        fillcolor=color, line=dict(width=0), layer="below")

# Lines
fig_bcg.add_hline(y=growth_mid, line=dict(color="#ECEFF1", width=1.5))
fig_bcg.add_vline(x=1.0, line=dict(color="#ECEFF1", width=1.5))

# Bubbles per quadrant
for quad, color in bcg_colors.items():
    sub = bcg_df[bcg_df["Quadrant"] == quad]
    if sub.empty:
        continue
    fig_bcg.add_trace(go.Scatter(
        x=sub["Relative Share"],
        y=sub["Growth Rate"],
        mode="markers+text",
        name=quad,
        marker=dict(
            size=sub["Profit"].apply(lambda p: max(24, min(60, p / 1e6 * 7))),
            color=color,
            opacity=0.82,
            line=dict(color="white", width=2),
        ),
        text=sub["Product"].apply(lambda x: x.replace(" ", "<br>")),
        textposition="top center",
        textfont=dict(size=10, color=TEXT),
        hovertemplate=(
            "<b>%{text}</b><br>"
            "Part relative : %{x:.2f}x<br>"
            "Croissance : %{y:.1f}%<br>"
            "<extra></extra>"
        ),
    ))

# Quadrant labels
for label, x, y in [
    ("⭐ VEDETTES",      2.5, 22),
    ("🐄 VACHES À LAIT", 2.5, -3),
    ("💀 POIDS MORTS",   0.4, -3),
    ("❓ DILEMMES",      0.4, 22),
]:
    fig_bcg.add_annotation(
        x=x, y=y, text=f"<b>{label}</b>",
        showarrow=False,
        font=dict(size=10, color="#B0BEC5"),
        xanchor="center",
    )

fig_bcg.update_layout(
    **PLOT_LAYOUT,
    height=460,
    xaxis=dict(title="Part de marché relative", showgrid=False,
               range=[0, 4.5], zeroline=False),
    yaxis=dict(title="Taux de croissance (%)", showgrid=False,
               range=[-5, 25], zeroline=False),
    legend=dict(orientation="h", yanchor="bottom", y=1.02,
                xanchor="right", x=1, font=dict(size=11)),
)
st.plotly_chart(fig_bcg, use_container_width=True)

# BCG summary table
st.markdown("<div style='margin-top:8px;'>", unsafe_allow_html=True)
bcg_show = bcg_df[["Product", "Quadrant", "Market Share", "Growth Rate", "Profit"]].copy()
bcg_show["Market Share"] = bcg_show["Market Share"].map("{:.1f}%".format)
bcg_show["Growth Rate"]  = bcg_show["Growth Rate"].map("{:+.1f}%".format)
bcg_show["Profit"]       = bcg_show["Profit"].map("${:,.0f}".format)
bcg_show = bcg_show.rename(columns={
    "Product": "Produit",
    "Market Share": "Part de marché",
    "Growth Rate": "Croissance",
})
st.dataframe(bcg_show, hide_index=True, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# SECTION 6 — STRATÉGIE RÉSEAUX SOCIAUX
# ─────────────────────────────────────────────────────────────────
st.markdown("<div id='social'></div>", unsafe_allow_html=True)
st.markdown("""
<div class='card'>
  <div class='section-tag'>Recommandations Stratégiques</div>
  <div class='section-title'>Marketing · Réseaux Sociaux</div>
  <div class='section-sub'>
    Segmentation client · Campagne HOOKSTRIKE™ · Produit Vedette : Chocolate Chip
  </div>
""", unsafe_allow_html=True)

st.markdown("#### 🎯 Segments Clients Prioritaires", unsafe_allow_html=False)

col1, col2 = st.columns(2, gap="medium")
with col1:
    st.markdown("""
    <div class='segment-card'>
      <div class='segment-title'>Segment 1 · Jeunes Professionnels Urbains (25-38 ans)</div>
      <div class='segment-body'>
        Actifs, connectés, soucieux de la qualité et de l'authenticité.
        Sensibles aux récits de marque, à l'origine des ingrédients et au
        plaisir coupable assumé. Forte présence Instagram & LinkedIn.
        Panier moyen élevé. Achats impulsifs déclenchés par du contenu visuel soigné.
      </div>
      <div style='margin-top:12px;font-size:11px;color:#90A4AE;'>
        📍 Canaux prioritaires : Instagram · LinkedIn · TikTok
      </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='segment-card'>
      <div class='segment-title'>Segment 2 · Familles & Parents Soucieux de la Qualité (32-50 ans)</div>
      <div class='segment-body'>
        Acheteurs réguliers, fidèles à leurs marques de confiance.
        Attachés aux valeurs familiales, aux recettes traditionnelles et aux
        occasions de partage. Sensibles aux formats "gros volumes" et aux
        promotions saisonnières. Influence forte sur la fidélisation long terme.
      </div>
      <div style='margin-top:12px;font-size:11px;color:#90A4AE;'>
        📍 Canaux prioritaires : Facebook · Pinterest · Email Marketing
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>#### 🚀 Campagne HOOKSTRIKE™ — 3 Posts Vedettes", unsafe_allow_html=True)

posts = [
    {
        "platform": "Instagram · Segment Jeunes Professionnels",
        "hook": "Tu mérites une pause. Une vraie.",
        "strike": (
            "Notre Chocolate Chip original n'est pas juste un cookie — c'est le signal "
            "que ta journée a été assez longue. Fait avec du vrai chocolat, sans compromis. "
            "Parce que les meilleures décisions se prennent après une bouchée."
        ),
        "tags": "#ChocolateChip #CookieCompany #SelfCare #SlowDown #FoodLovers",
    },
    {
        "platform": "LinkedIn · Segment Professionnels & B2B",
        "hook": "87% des décisions importantes se prennent après une pause café. Et si c'était une pause cookie ?",
        "strike": (
            "The Cookie Company fournit aux entreprises un snacking premium pour leurs équipes. "
            "Notre Chocolate Chip est le N°1 en satisfaction collaborateur dans nos partenariats "
            "corporate. Livraison en bureau, packaging personnalisé, traçabilité ingrédients incluse. "
            "On parle de bien-être au travail — parlons-en."
        ),
        "tags": "#WellbeingAtWork #CorporateGifting #QVT #CookieCompany",
    },
    {
        "platform": "Instagram · Segment Familles · Post Saisonnier",
        "hook": "Le goût dont ils se souviendront dans 20 ans.",
        "strike": (
            "Les recettes changent. Pas les souvenirs. Notre Chocolate Chip — la même recette "
            "depuis le début — est fait pour être partagé, cassé en deux, dévoré encore chaud. "
            "Ce week-end, donnez-leur quelque chose à raconter."
        ),
        "tags": "#FamilyTime #HomeBaked #ChocolateChipCookie #WeekendVibes #CookieCompany",
    },
]

for post in posts:
    st.markdown(f"""
    <div class='post-card'>
      <div class='post-platform'>{post['platform']}</div>
      <div class='post-hook'>[ HOOK ] &nbsp;{post['hook']}</div>
      <div class='post-strike'>[ STRIKE ] &nbsp;{post['strike']}</div>
      <div class='post-tag'>{post['tags']}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# SECTION 7 — GUIDE DÉPLOIEMENT
# ─────────────────────────────────────────────────────────────────
st.markdown("<div id='deploy'></div>", unsafe_allow_html=True)
st.markdown("""
<div class='card'>
  <div class='section-tag'>Guide · Déploiement Gratuit</div>
  <div class='section-title'>Partager votre Dashboard en ligne</div>
  <div class='section-sub'>GitHub + Streamlit Community Cloud · 3 étapes · ~10 minutes</div>
""", unsafe_allow_html=True)

steps = [
    {
        "n": "1",
        "title": "Créer un compte GitHub gratuit",
        "body": "Rendez-vous sur github.com → cliquez 'Sign up' → entrez votre e-mail, un mot de passe et un nom d'utilisateur (ex : the-cookie-co). Confirmez via l'e-mail reçu.",
        "code": "https://github.com → Sign up",
    },
    {
        "n": "2",
        "title": "Créer un Repository et uploader vos fichiers",
        "body": "Depuis GitHub, cliquez sur 'New' → nommez-le 'cookie-dashboard' → cochez 'Add a README file' → 'Create repository'. Puis 'Add file' → 'Upload files' → glissez app.py, Cookie_Company.csv et requirements.txt → 'Commit changes'.",
        "code": "Repository : cookie-dashboard (Public)",
    },
    {
        "n": "3",
        "title": "Déployer sur Streamlit Community Cloud",
        "body": "Allez sur share.streamlit.io → 'Sign in with GitHub' → 'New app' → sélectionnez votre repo 'cookie-dashboard' → Branch : main → Main file : app.py → cliquez 'Deploy!'. Votre URL de partage sera prête en ~2 minutes.",
        "code": "https://the-cookie-co-dashboard.streamlit.app  🎉",
    },
]

for step in steps:
    st.markdown(f"""
    <div class='deploy-step'>
      <div class='deploy-num'>{step['n']}</div>
      <div class='deploy-content'>
        <div class='deploy-title'>{step['title']}</div>
        <div class='deploy-body'>{step['body']}</div>
        <div class='deploy-code'>{step['code']}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style='background:#F0F4F8;border-radius:12px;padding:16px 20px;margin-top:8px;'>
  <div style='font-size:11px;font-weight:700;letter-spacing:1.5px;color:#607D8B;
              text-transform:uppercase;margin-bottom:6px;'>💡 Contenu du fichier requirements.txt</div>
  <div style='font-family:monospace;font-size:12px;color:#37474F;line-height:1.8;'>
    streamlit&gt;=1.32.0<br>
    plotly&gt;=5.18.0<br>
    pandas&gt;=2.0.0<br>
    numpy&gt;=1.24.0
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────
st.markdown(f"""
<div style='text-align:center;padding:40px 20px 20px;
            font-size:11px;color:#B0BEC5;letter-spacing:1px;'>
  🍪 The Cookie Company · Strategic Intelligence Dashboard<br>
  Données simulées 2019–2025 · Built with Streamlit & Plotly
</div>
""", unsafe_allow_html=True)
