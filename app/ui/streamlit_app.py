from __future__ import annotations

import pandas as pd
import streamlit as st

from app.portfolio.construction import build_portfolio
from app.research.orchestrator import BiotechResearchOrchestrator

st.set_page_config(page_title='Biotech Scout', layout='wide')
st.title('Biotech Scout Dashboard')

orch = BiotechResearchOrchestrator()

ticker = st.sidebar.text_input('Ticker', value='NBIX').upper()
strategy = st.sidebar.selectbox('Strategy', list(orch.settings.strategy_profiles.keys()))

if st.sidebar.button('Run Research'):
    dossier = orch.run_ticker(ticker, strategy)
    tab1, tab2, tab3, tab4, tab5 = st.tabs(['Dossier', 'Catalyst Timeline', 'Financing', 'Analogs', 'Portfolio'])

    with tab1:
        st.subheader('Executive Summary')
        st.json({'score': dossier.score_breakdown.final_opportunity_score, 'archetype': dossier.archetype, 'changes': dossier.what_changed})
        st.subheader('Clinical Trial Cards')
        st.dataframe(pd.DataFrame(dossier.clinical_assessment))

    with tab2:
        st.subheader('Canonical Catalyst Timeline')
        st.dataframe(pd.DataFrame(dossier.canonical_catalysts))

    with tab3:
        st.subheader('Financing History / Risk')
        st.dataframe(pd.DataFrame(dossier.financing_events))
        st.json(dossier.financing_risk)

    with tab4:
        st.subheader('Historical Analogs')
        st.dataframe(pd.DataFrame(dossier.historical_analogs))

    with tab5:
        suggestions = build_portfolio([
            {'ticker': dossier.company.ticker, 'score': dossier.score_breakdown.final_opportunity_score, 'archetype': dossier.archetype.get('archetype', ''), 'liquidity_score': 0.7}
        ])
        st.dataframe(pd.DataFrame(suggestions))
