import streamlit as st
import pandas as pd
import json
import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="Automotive Budget Estimator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INIZIALIZZAZIONE SESSION STATE ---
# Popoliamo lo stato con alcuni dati di esempio iniziali per facilitare i test immediati
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.portfolio_ecu = ["ECU_Engine", "ECU_Gateway", "ECU_Infotainment"]
    st.session_state.model_lines = ["Line_Alpha", "Line_Beta", "Line_Gamma"]
    st.session_state.veicoli = ["SUV_Segment_C", "Sedan_Electric", "Compact_Hybrid"]
    
    # Stato del progetto corrente
    st.session_state.project = {
        "tipo_budget": "Nuovo veicolo",
        "hc": 10.0,
        "zbb": 5.0,
        "hrHC": 60.0,
        "hrZBB": 45.0,
        "css": 2000.0,
        "pm_date": datetime.date.today(),
        "sop_date": datetime.date.today() + datetime.timedelta(days=365),
        "model_line": "Line_Alpha",
        "veicolo": "SUV_Segment_C",
        "selected_ecus": ["ECU_Engine"],
        "premesse": "",
        "ecu_data": {}  # Conterrà i dati inseriti per ogni singola ECU
    }

# --- FUNZIONI DI UTILITÀ: EXPORT / IMPORT JSON ---
def export_project_json():
    # Prepariamo un dizionario serializzabile (convertendo le date in stringhe)
    export_data = {
        "portfolio_ecu": st.session_state.portfolio_ecu,
        "model_lines": st.session_state.model_lines,
        "veicoli": st.session_state.veicoli,
        "project": {**st.session_state.project}
    }
    # Gestione delle date per il formato JSON
    export_data["project"]["pm_date"] = export_data["project"]["pm_date"].isoformat()
    export_data["project"]["sop_date"] = export_data["project"]["sop_date"].isoformat()
    return json.dumps(export_data, indent=4)

def import_project_json(uploaded_file):
    try:
        data = json.load(uploaded_file)
        st.session_state.portfolio_ecu = data.get("portfolio_ecu", [])
        st.session_state.model_lines = data.get("model_lines", [])
        st.session_state.veicoli = data.get("veicoli", [])
        
        # Ripristino dati di progetto e conversione stringhe -> date
        proj = data.get("project", {})
        if "pm_date" in proj:
            proj["pm_date"] = datetime.date.fromisoformat(proj["pm_date"])
        if "sop_date" in proj:
            proj["sop_date"] = datetime.date.fromisoformat(proj["sop_date"])
            
        st.session_state.project = proj
        st.success("Progetto caricato con successo!")
        st.rerun()
    except Exception as e:
        st.error(f"Errore durante il caricamento del file JSON: {e}")


# --- SIDEBAR & NAVIGAZIONE ---
st.sidebar.title("🚗 Automotive Budgeting")
navigation = st.sidebar.radio(
    "Navigazione Sezioni",
    ["Sezione Admin (Configurazione)", "Sezione Progetto (Stima Budget)"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("💾 Gestione Dati Progetto")

# Pulsante di Esportazione
json_string = export_project_json()
st.sidebar.download_button(
    label="📤 Esporta Progetto (JSON)",
    data=json_string,
    file_name=f"budget_project_{datetime.date.today()}.json",
    mime="application/json",
    use_container_width=True
)

# Pulsante di Importazione
uploaded_file = st.sidebar.file_uploader("📥 Importa Progetto (JSON)", type=["json"])
if uploaded_file is not None:
    if st.sidebar.button("Conferma Importazione", use_container_width=True):
        import_project_json(uploaded_file)


# ==============================================================================
# 2. SEZIONE ADMIN (CONFIGURAZIONE DI BASE)
# ==============================================================================
if navigation == "Sezione Admin (Configurazione)":
    st.title("⚙️ Sezione Admin")
    st.subheader("Configurazione delle anagrafiche di base")
    st.write("Inserisci o rimuovi gli elementi che popoleranno i selettori della sezione di stima budget.")
    
    col1, col2, col3 = st.columns(3)
    
    # Gestione Portfolio ECU
    with col1:
        st.card = st.container(border=True)
        with st.card:
            st.markdown("### 🎛️ Portfolio ECU")
            new_ecu = st.text_input("Aggiungi nuova ECU:", key="add_ecu_input")
            if st.button("Aggiungi ECU", use_container_width=True) and new_ecu:
                if new_ecu not in st.session_state.portfolio_ecu:
                    st.session_state.portfolio_ecu.append(new_ecu)
                    st.rerun()
            
            st.markdown("**ECU correnti:**")
            for ecu in st.session_state.portfolio_ecu:
                c1, c2 = st.columns([4, 1])
                c1.write(f"- {ecu}")
                if c2.button("❌", key=f"del_ecu_{ecu}"):
                    st.session_state.portfolio_ecu.remove(ecu)
                    st.rerun()

    # Gestione Model Line
    with col2:
        st.card = st.container(border=True)
        with st.card:
            st.markdown("### 📐 Model Line")
            new_ml = st.text_input("Aggiungi Model Line:", key="add_ml_input")
            if st.button("Aggiungi Linea", use_container_width=True) and new_ml:
                if new_ml not in st.session_state.model_lines:
                    st.session_state.model_lines.append(new_ml)
                    st.rerun()
            
            st.markdown("**Linee correnti:**")
            for ml in st.session_state.model_lines:
                c1, c2 = st.columns([4, 1])
                c1.write(f"- {ml}")
                if c2.button("❌", key=f"del_ml_{ml}"):
                    st.session_state.model_lines.remove(ml)
                    st.rerun()

    # Gestione Veicoli
    with col3:
        st.card = st.container(border=True)
        with st.card:
            st.markdown("### 🚘 Veicoli")
            new_v = st.text_input("Aggiungi Veicolo:", key="add_v_input")
            if st.button("Aggiungi Veicolo", use_container_width=True) and new_v:
                if new_v not in st.session_state.veicoli:
                    st.session_state.veicoli.append(new_v)
                    st.rerun()
            
            st.markdown("**Veicoli correnti:**")
            for v in st.session_state.veicoli:
                c1, c2 = st.columns([4, 1])
                c1.write(f"- {v}")
                if c2.button("❌", key=f"del_v_{v}"):
                    st.session_state.veicoli.remove(v)
                    st.rerun()


# ==============================================================================
# 3. SEZIONE PROGETTO (STIMA BUDGET)
# ==============================================================================
else:
    st.title("📊 Sezione Progetto & Stima Budget")
    
    # --------------------------------------------------------------------------
    # CONFIGURAZIONE INIZIALE
    # --------------------------------------------------------------------------
    with st.expander("📝 1. Configurazione Iniziale e Parametri di Progetto", expanded=True):
        p_col1, p_col2, p_col3 = st.columns(3)
        
        with p_col1:
            st.session_state.project["tipo_budget"] = st.selectbox(
                "Tipo di Budget", ["Nuovo veicolo", "Change request"],
                index=["Nuovo veicolo", "Change request"].index(st.session_state.project["tipo_budget"])
            )
            
            # Contesto da Admin
            ml_options = st.session_state.model_lines if st.session_state.model_lines else ["Nessuna linea definita"]
            v_options = st.session_state.veicoli if st.session_state.veicoli else ["Nessun veicolo definito"]
            
            st.session_state.project["model_line"] = st.selectbox(
                "Model Line", ml_options,
                index=ml_options.index(st.session_state.project["model_line"]) if st.session_state.project["model_line"] in ml_options else 0
            )
            st.session_state.project["veicolo"] = st.selectbox(
                "Veicolo", v_options,
                index=v_options.index(st.session_state.project["veicolo"]) if st.session_state.project["veicolo"] in v_options else 0
            )

        with p_col2:
            st.session_state.project["hc"] = st.number_input("Numero Interni (HC)", min_value=0.0, value=st.session_state.project["hc"], step=1.0)
            st.session_state.project["zbb"] = st.number_input("Numero Esterni (ZBB)", min_value=0.0, value=st.session_state.project["zbb"], step=1.0)
            
            # Calcolo automatico RIE
            hc_val = st.session_state.project["hc"]
            zbb_val = st.session_state.project["zbb"]
            if zbb_val > 0:
                rie = hc_val / zbb_val
                st.metric("Rapporto RIE (HC / ZBB)", f"{rie:.2f}")
            else:
                rie = 0.0
                st.metric("Rapporto RIE (HC / ZBB)", "N/A (ZBB = 0)")
                
            st.session_state.project["css"] = st.number_input("Costo Sessione Sviluppo (CSS) [€]", min_value=0.0, value=st.session_state.project["css"], step=100.0)

        with p_col3:
            st.session_state.project["hrHC"] = st.number_input("Costo Orario Interni hrHC [€/h]", min_value=0.0, value=st.session_state.project["hrHC"], step=5.0)
            st.session_state.project["hrZBB"] = st.number_input("Costo Orario Esterni hrZBB [€/h]", min_value=0.0, value=st.session_state.project["hrZBB"], step=5.0)
            
            # Date e calcolo durata
            st.session_state.project["pm_date"] = st.date_input("Data Inizio (Milestone PM)", st.session_state.project["pm_date"])
            st.session_state.project["sop_date"] = st.date_input("Data Fine (Milestone SOP)", st.session_state.project["sop_date"])
            
            delta_giorni = (st.session_state.project["sop_date"] - st.session_state.project["pm_date"]).days
            settimane = max(0.0, delta_giorni / 7.0)
            frazione_anno = max(0.0, delta_giorni / 365.25)
            
            st.write(f"⏱️ **Durata Progetto:** {settimane:.1f} settimane ({frazione_anno:.2f} anni)")

        st.markdown("---")
        
       # Filtriamo i default per assicurarci che contengano solo ECU ancora esistenti nel portfolio
disponibili_e_selezionate = [
    ecu for ecu in st.session_state.project["selected_ecus"] 
    if ecu in st.session_state.portfolio_ecu
]

st.session_state.project["selected_ecus"] = st.multiselect(
    "Centraline Coinvolte nel Progetto",
    options=st.session_state.portfolio_ecu,
    default=disponibili_e_selezionate
)
        
        st.session_state.project["premesse"] = st.text_area("Premesse di Progetto / Note operative", value=st.session_state.project["premesse"])

    # --------------------------------------------------------------------------
    # STIMA COSTI PER SINGOLA CENTRALINA
    # --------------------------------------------------------------------------
    st.subheader("🎛️ 4. Stima Costi per Singola Centralina")
    
    ecu_summary_list = [] # Lista per raccogliere i dati di riepilogo da visualizzare nell'overview finale
    
    if not st.session_state.project["selected_ecus"]:
        st.info("Seleziona almeno una centralina nella Configurazione Iniziale per inserire i costi dettagliati.")
    else:
        # Creiamo un tab grafico dinamico per ogni centralina selezionata
        tabs = st.tabs(st.session_state.project["selected_ecus"])
        
        for idx, ecu_name in enumerate(st.session_state.project["selected_ecus"]):
            with tabs[idx]:
                st.markdown(f"### Dettaglio Stima: **{ecu_name}**")
                
                # Inizializziamo la struttura dati locale per la ECU se non esiste nello stato
                if ecu_name not in st.session_state.project["ecu_data"]:
                    st.session_state.project["ecu_data"][ecu_name] = {
                        "nSS": 0.0, "supplier_cost": 0.0, "pm_h": 0.0, "sw_zdc_h": 0.0,
                        "req_m_h": 0.0, "sw_dev_h": 0.0, "mil_h": 0.0, "bugfix_h": 0.0,
                        "hil_test_ext": 0.0, "hil_setup_ext": 0.0, "parts_ext": 0.0
                    }
                
                ecu_store = st.session_state.project["ecu_data"][ecu_name]
                
                # Input dei Parametri Locali della ECU
                ec_col1, ec_col2 = st.columns(2)
                with ec_col1:
                    ecu_store["nSS"] = st.number_input(
                        f"Settimane di sviluppo e in pista (nSS) - {ecu_name}", 
                        min_value=0.0, value=float(ecu_store["nSS"]), step=1.0, key=f"{ecu_name}_nSS"
                    )
                with ec_col2:
                    ecu_store["supplier_cost"] = st.number_input(
                        f"ECU supplier cost [€] - {ecu_name}", 
                        min_value=0.0, value=float(ecu_store["supplier_cost"]), step=1000.0, key=f"{ecu_name}_sup"
                    )
                
                # Calcoli Automatici Voci Fisse legati ad nSS
                calc_veh_testing_h = ecu_store["nSS"] * 40.0
                calc_veh_testing_ext = ecu_store["nSS"] * st.session_state.project["css"]
                
                st.markdown("#### Inserimento Voci di Costo")
                
                # Layout per l'inserimento delle altre voci di costo
                form_col1, form_col2 = st.columns(2)
                
                with form_col1:
                    st.caption("**Voci espresse in ORE (h):**")
                    ecu_store["pm_h"] = st.number_input("Project management [h]", min_value=0.0, value=float(ecu_store["pm_h"]), step=10.0, key=f"{ecu_name}_pm")
                    ecu_store["sw_zdc_h"] = st.number_input("SW & ZDC management [h]", min_value=0.0, value=float(ecu_store["sw_zdc_h"]), step=10.0, key=f"{ecu_name}_sw_zdc")
                    ecu_store["req_m_h"] = st.number_input("Requirement management [h]", min_value=0.0, value=float(ecu_store["req_m_h"]), step=10.0, key=f"{ecu_name}_req")
                    ecu_store["sw_dev_h"] = st.number_input("SW development [h]", min_value=0.0, value=float(ecu_store["sw_dev_h"]), step=10.0, key=f"{ecu_name}_sw_dev")
                    ecu_store["mil_h"] = st.number_input("SW testing (MIL) [h]", min_value=0.0, value=float(ecu_store["mil_h"]), step=10.0, key=f"{ecu_name}_mil")
                    ecu_store["bugfix_h"] = st.number_input("Issue analysis & Bugfix [h]", min_value=0.0, value=float(ecu_store["bugfix_h"]), step=10.0, key=f"{ecu_name}_bugfix")
                    
                    # Voce bloccata / calcolata automaticamente
                    st.text_input("Vehicle testing [Ore - h] (Autocalcolato)", value=f"{calc_veh_testing_h} h", disabled=True, key=f"{ecu_name}_vt_h_dis")
                    
                with form_col2:
                    st.caption("**Voci esterne espresse in EURO (ext cost):**")
                    ecu_store["hil_test_ext"] = st.number_input("HIL testing [€]", min_value=0.0, value=float(ecu_store["hil_test_ext"]), step=500.0, key=f"{ecu_name}_hil_t")
                    ecu_store["hil_setup_ext"] = st.number_input("HIL Set-up (HW) [€]", min_value=0.0, value=float(ecu_store["hil_setup_ext"]), step=500.0, key=f"{ecu_name}_hil_s")
                    
                    # Voce bloccata / calcolata automaticamente
                    st.text_input("Vehicle testing [€ - ext cost] (Autocalcolato)", value=f"{calc_veh_testing_ext:,.2f} €", disabled=True, key=f"{ecu_name}_vt_e_dis")
                    
                    ecu_store["parts_ext"] = st.number_input("Parts [€]", min_value=0.0, value=float(ecu_store["parts_ext"]), step=500.0, key=f"{ecu_name}_parts")
                
                # --- LOGICA DI RIPARTIZIONE ORARIA (RIE) ---
                # Raccogliamo tutte le voci orarie per applicare la formula di split
                ore_voci = [
                    ecu_store["pm_h"], ecu_store["sw_zdc_h"], ecu_store["req_m_h"],
                    ecu_store["sw_dev_h"], ecu_store["mil_h"], ecu_store["bugfix_h"],
                    calc_veh_testing_h
                ]
                ore_totali_ecu = sum(ore_voci)
                
                # Calcolo split HC / ZBB sulla singola ECU basato sul pool complessivo del progetto
                if zbb_val == 0 and hc_val == 0:
                    ore_zbb_ecu = 0.0
                    ore_hc_ecu = 0.0
                elif zbb_val == 0:
                    ore_zbb_ecu = 0.0
                    ore_hc_ecu = ore_totali_ecu
                else:
                    # Formula basata sulle specifiche fornite: Ore_ZBB = Ore_totali / (1 + RIE)
                    ore_zbb_ecu = ore_totali_ecu / (1 + rie)
                    ore_hc_ecu = ore_totali_ecu - ore_zbb_ecu
                
                # Calcolo monetario dei costi orari della ECU
                costo_hc_ecu = ore_hc_ecu * st.session_state.project["hrHC"]
                costo_zbb_ecu = ore_zbb_ecu * st.session_state.project["hrZBB"]
                costo_orario_totale = costo_hc_ecu + costo_zbb_ecu
                
                # Somma Ext Cost legati alla ECU
                tot_ext_cost_ecu = (
                    ecu_store["hil_test_ext"] + 
                    ecu_store["hil_setup_ext"] + 
                    calc_veh_testing_ext + 
                    ecu_store["parts_ext"]
                )
                
                # Costo Totale ECU
                costo_totale_ecu = costo_orario_totale + ecu_store["supplier_cost"] + tot_ext_cost_ecu
                
                # Calcolo FTE Anno (Convenzione 1600h per anno su quota frazione anno progetto)
                quota_ore_fte = 1600.0 * frazione_anno
                fte_ecu = ore_totali_ecu / quota_ore_fte if quota_ore_fte > 0 else 0.0
                
                # Salvo i dati elaborati in una lista per l'Overview comparativa finale
                ecu_summary_list.append({
                    "Centralina": ecu_name,
                    "Ore HC (Interni)": round(ore_hc_ecu, 1),
                    "Ore ZBB (Esterni)": round(ore_zbb_ecu, 1),
                    "Costo Interni HC (€)": round(costo_hc_ecu, 2),
                    "Costo Esterni ZBB (€)": round(costo_zbb_ecu, 2),
                    "Supplier Cost (€)": round(ecu_store["supplier_cost"], 2),
                    "Ext Cost (€)": round(tot_ext_cost_ecu, 2),
                    "Costo Totale (€)": round(costo_totale_ecu, 2),
                    "FTE/Anno equivalenti": round(fte_ecu, 2)
                })
                
                # --- FINESTRA DI SUM_UP SINGOLA ECU ---
                st.markdown("---")
                st.markdown(f"#### 📊 Riepilogo Economico (SUM_UP): {ecu_name}")
                
                sum_col1, sum_col2, sum_col3, sum_col4 = st.columns(4)
                sum_col1.metric("Ore Totali HC (Interni)", f"{ore_hc_ecu:.1f} h", f"Costo: {costo_hc_ecu:,.2f} €", delta_color="off")
                sum_col2.metric("Ore Totali ZBB (Esterni)", f"{ore_zbb_ecu:.1f} h", f"Costo: {costo_zbb_ecu:,.2f} €", delta_color="off")
                sum_col3.metric("FTE Annuali Richiesti", f"{fte_ecu:.2f} FTE")
                sum_col4.metric("BUDGET TOTALE ECU", f"{costo_totale_ecu:,.2f} €")
                
                # Visualizzazione tabellare veloce per la singola ECU
                df_local_sum = pd.DataFrame([{
                    "HC (Ore)": ore_hc_ecu,
                    "ZBB (Ore)": ore_zbb_ecu,
                    "Costo Sviluppo Interno/Esterno (€)": costo_orario_totale,
                    "Costo Fornitore (€)": ecu_store["supplier_cost"],
                    "Costi Esterni / Materiali (€)": tot_ext_cost_ecu,
                }])
                st.dataframe(df_local_sum, hide_index=True, use_container_width=True)

    # --------------------------------------------------------------------------
    # OVERVIEW FINALE DEL PROGETTO
    # --------------------------------------------------------------------------
    st.markdown("---")
    st.header("🏁 5. Overview Finale del Progetto")
    
    if ecu_summary_list:
        df_summary = pd.DataFrame(ecu_summary_list)
        
        # Calcolo delle aggregazioni per il SUM UP globale del progetto
        tot_hc_ore = df_summary["Ore HC (Interni)"].sum()
        tot_zbb_ore = df_summary["Ore ZBB (Esterni)"].sum()
        tot_supplier = df_summary["Supplier Cost (€)"].sum()
        tot_ext_cost = df_summary["Ext Cost (€)"].sum()
        tot_fte = df_summary["FTE/Anno equivalenti"].sum()
        grand_total_budget = df_summary["Costo Totale (€)"].sum()
        
        # Visualizzazione Metriche Globali di Progetto
        ov_col1, ov_col2, ov_col3 = st.columns(3)
        with ov_col1:
            st.container(border=True).metric("Totale Ore Interni (HC)", f"{tot_hc_ore:,.1f} h", f"Equivalenti a {tot_fte:.2f} FTE Totali")
            st.container(border=True).metric("Totale Costi Supplier", f"{tot_supplier:,.2f} €")
        with ov_col2:
            st.container(border=True).metric("Totale Ore Esterni (ZBB)", f"{tot_zbb_ore:,.1f} h")
            st.container(border=True).metric("Totale Altri Costi Esterni (Ext Cost)", f"{tot_ext_cost:,.2f} €")
        with ov_col3:
            st.container(border=True).metric(
                "💰 BUDGET TOTALIZZATO PROGETTO", 
                f"{grand_total_budget:,.2f} €", 
                help="Include costi orari interni/esterni, costi fornitore e costi piste/materiali di tutte le ECU coinvolte."
            )
            
        # Tabella di dettaglio e comparazione tra le centraline coinvolte
        st.markdown("#### Tabella Comparativa Dettaglio Centraline")
        st.dataframe(df_summary, hide_index=True, use_container_width=True)
    else:
        st.warning("Nessun dato di sintesi disponibile. Assicurati di aver configurato il contesto e selezionato le relative ECU.")
