import streamlit as st
import pandas as pd
import random
 
# ==========================================
# PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(page_title="Woom Circular Economy Simulator", layout="wide", initial_sidebar_state="expanded")
 
st.markdown("""
    <style>
    .metric-card { background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 5px solid #e1251b; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; border-bottom: 2px solid #f0f2f6; }
    .stTabs [data-baseweb="tab"] { height: 50px; font-weight: 600; font-size: 16px; }
    div[data-testid="stMetricValue"] { font-size: 28px; }
    </style>
""", unsafe_allow_html=True)
 
st.title("Woom 3: Circular Economy & Remanufacturing Simulator")
st.markdown("Enterprise-grade scenario modeling for reverse logistics, operational triage, component-level recovery, and environmental impact.")
 
# ==========================================
# SIDEBAR: EXECUTIVE INPUTS
# ==========================================
with st.sidebar:
    st.markdown("### Executive Parameters")
    
    with st.expander("1. Product & Sales Data", expanded=True):
        msrp = st.number_input("Woom 3 MSRP (€)", value=449, step=10)
        cogs = st.number_input("Manufacturing COGS (€)", value=185, step=5)
        annual_volume = st.number_input("Annual Sales Volume (Units)", value=5000, step=500)
 
    with st.expander("2. Reverse Logistics & Trade-in", expanded=True):
        upcycle_return_rate = st.slider("Trade-in Return Rate (%)", 0, 100, 35)
        upcycle_voucher_pct = st.slider("Customer Voucher (% of MSRP)", 10, 50, 30)
        core_cost = msrp * (upcycle_voucher_pct / 100)
        logistics_cost = st.number_input("Reverse Shipping/Unit (€)", value=18, step=1)
        triage_cost = st.number_input("Triage & Unboxing/Unit (€)", value=8, step=1)
 
    with st.expander("3. Operational Overheads", expanded=False):
        labor_rate = st.number_input("Mechanic Base Rate (€/h)", value=45, step=1)
        overhead_pct = st.slider("Facility Overhead (%)", 0, 50, 15)
        true_labor_rate = labor_rate * (1 + (overhead_pct/100))
        cannibalization_rate = st.slider("Cannibalization Rate (%)", 0, 30, 10)
 
# --- CORE BASELINE CALCULATIONS ---
new_margin_unit = msrp - cogs
returned_units = int(annual_volume * (upcycle_return_rate / 100))
total_triage_cost = returned_units * (logistics_cost + triage_cost)
 
# ==========================================
# INITIALIZE TABS
# ==========================================
tab1, tab2, tab3, tab_ideas, tab4, tab5, tab6 = st.tabs([
    "Executive Dashboard", 
    "Operational Triage", 
    "Component Recovery", 
    "Idea Bank: 350 Scenarios",
    "Scenario Simulation",
    "ESG & Impact", 
    "DfRem Audit"
])
 
# ==========================================
# TAB 2: OPERATIONAL TRIAGE & ROUTING
# ==========================================
with tab2:
    st.header("Condition-Based Quality Routing (Triage)")
    st.markdown("Define how incoming trade-in bikes are distributed into different remanufacturing pipelines.")
    
    col_r1, col_r2, col_r3 = st.columns(3)
    
    with col_r1:
        st.markdown("#### Light Refurbish (A-Grade)")
        pct_ref = st.number_input("Routing Volume (%)", value=55, key="pct_ref", step=5)
        cost_parts_ref = st.number_input("Parts Cost (€)", value=15, key="pr")
        time_ref = st.number_input("Labor Time (h)", value=0.75, step=0.1, key="tr")
        price_ref = st.number_input("Target Resale Price (€)", value=329, key="rr")
        margin_ref = price_ref - (core_cost + cost_parts_ref + (time_ref * true_labor_rate))
        st.metric("Unit Margin", f"€{margin_ref:.2f}")
        
    with col_r2:
        st.markdown("#### Full Remanufacture (B-Grade)")
        pct_rem = st.number_input("Routing Volume (%)", value=35, key="pct_rem", step=5)
        cost_parts_rem = st.number_input("Parts Cost (€)", value=60, key="pm")
        time_rem = st.number_input("Labor Time (h)", value=1.75, step=0.1, key="tm")
        price_rem = st.number_input("Target Resale Price (€)", value=389, key="rm")
        margin_rem = price_rem - (core_cost + cost_parts_rem + (time_rem * true_labor_rate))
        st.metric("Unit Margin", f"€{margin_rem:.2f}")
        
    with col_r3:
        st.markdown("#### Component Harvest (C-Grade)")
        pct_harv = st.number_input("Routing Volume (%)", value=10, key="pct_harv", step=5)
        time_harv = st.number_input("Tear-down Time (h)", value=0.4, step=0.1, key="th")
        st.info("Revenues for Harvesting are calculated dynamically in the Component Recovery tab.")
 
    if (pct_ref + pct_rem + pct_harv) != 100:
        st.error(f"Error: Routing percentages must equal 100%. Currently at {pct_ref + pct_rem + pct_harv}%.")
        st.stop()
 
# Volume calculations
vol_ref = int(returned_units * (pct_ref / 100))
vol_rem = int(returned_units * (pct_rem / 100))
vol_harv = int(returned_units * (pct_harv / 100))
vol_resold = vol_ref + vol_rem
 
# ==========================================
# TAB 3: COMPONENT RECOVERY SCENARIOS
# ==========================================
with tab3:
    st.header("Component-Level Material Flow (C-Grade Bikes)")
    st.markdown("For bikes routed to 'Component Harvest', determine the destiny of the dismantled parts.")
    
    col_c1, col_c2, col_c3, col_c4 = st.columns(4)
    with col_c1:
        comp_reuse_pct = st.number_input("Internal Reuse (%)", value=50, step=5)
    with col_c2:
        comp_reman_pct = st.number_input("Component Remanufacturing (%)", value=20, step=5)
    with col_c3:
        comp_b2b_pct = st.number_input("B2B Secondary Market (%)", value=20, step=5)
    with col_c4:
        comp_scrap_pct = st.number_input("Material Recycling (%)", value=10, step=5)
 
    if (comp_reuse_pct + comp_reman_pct + comp_b2b_pct + comp_scrap_pct) != 100:
        st.error("Component flow percentages must equal 100%.")
        st.stop()
 
    new_parts_value = 85  
    val_reuse = new_parts_value * 0.95   
    val_reman = new_parts_value * 0.60   
    val_b2b = new_parts_value * 0.25     
    val_scrap = 2                        
    
    qty_reuse = int(vol_harv * (comp_reuse_pct/100))
    qty_reman = int(vol_harv * (comp_reman_pct/100))
    qty_b2b = int(vol_harv * (comp_b2b_pct/100))
    qty_scrap = int(vol_harv * (comp_scrap_pct/100))
    
    total_recovery_value = (qty_reuse * val_reuse) + (qty_reman * val_reman) + (qty_b2b * val_b2b) + (qty_scrap * val_scrap)
    margin_harv = (total_recovery_value / max(1, vol_harv)) - (core_cost + (time_harv * true_labor_rate)) if vol_harv > 0 else 0
 
    col_s1, col_s2 = st.columns([2, 1])
    with col_s1:
        df_flow = pd.DataFrame({
            "Destination": ["Internal Reuse", "Remanufactured", "B2B Sales", "Scrap Metal"],
            "Quantity (Units)": [qty_reuse, qty_reman, qty_b2b, qty_scrap]
        })
        st.bar_chart(df_flow.set_index("Destination"), height=250)
 
    with col_s2:
        st.metric("Total Component Value Recovered", f"€{total_recovery_value:,.0f}")
        st.metric("Net Margin per Scrapped Bike", f"€{margin_harv:.2f}")
 
# ==========================================
# TAB IDEA BANK: 350 REPURPOSING SCENARIOS
# ==========================================
with tab_ideas:
    st.header("Component Repurposing Strategy Matrix (350 Scenarios)")
    st.markdown("This database provides **350 B2B strategic scenarios** for handling harvested components. Use this matrix to identify new revenue streams, ESG initiatives, and cost-saving internal processes.")
    
    # Base 50 manual handcrafted premium scenarios
    scenarios_data = [
        ["Frame", "Internal Reuse", "Re-powder coat in limited edition colors for premium CPO sales."],
        ["Frame", "B2B Secondary Market", "Sell raw, unpainted frames to custom bike builders or technical welding schools."],
        ["Frame", "Upcycling / Brand Asset", "Repurpose damaged frames into retail display racks for Woom flagship stores."],
        ["Frame", "Material Recycling", "Grind severely damaged AA 6061 frames into aluminum powder for 3D printing feed."],
        ["Frame", "B2B Secondary Market", "Wholesale slightly dented frames to budget balance-bike manufacturers."],
        ["Frame", "Upcycling / Brand Asset", "Cut frame tubing to manufacture custom shop tool handles for Woom mechanics."],
        ["Frame", "Internal Reuse", "Use heavily scratched but structurally sound frames for internal mechanic training."],
        ["Fork", "Internal Reuse", "Salvage straight forks to replace bent forks on otherwise A-Grade bikes."],
        ["Fork", "Upcycling / Brand Asset", "Weld salvaged forks into custom bicycle parking stands for schools."],
        ["Fork", "Material Recycling", "Melt down aluminum forks directly into molds for new Woom pedal bodies."],
        ["Wheelset", "Component Remanufacturing", "True slightly bent wheels in-house for use in B-Grade remanufactured bikes."],
        ["Wheelset", "Component Remanufacturing", "Dismantle wheels: reuse good hubs and lace them to brand new rims."],
        ["Wheelset", "Component Remanufacturing", "Dismantle wheels: reuse good rims and lace them to new hubs."],
        ["Hubs", "Internal Reuse", "Extract internal bearings and axles to create low-cost repair kits for service centers."],
        ["Spokes", "Component Remanufacturing", "Cut and re-thread undamaged spokes to be used in smaller wheels (e.g., Woom 1 or 2)."],
        ["Wheelset", "B2B Secondary Market", "Sell 16-inch wheelsets to pediatric wheelchair manufacturers."],
        ["Wheelset", "Upcycling / Brand Asset", "Supply bent wheel rims to industrial designers for upcycled lighting fixtures."],
        ["Wheelset", "Internal Reuse", "Utilize scrapped wheels as permanent practice units for shop truing stands."],
        ["Tires", "Internal Reuse", "Harvest tires with >60% tread life for B-Grade remanufactured units."],
        ["Tires", "Material Recycling", "Grind completely worn Schwalbe tires into crumb rubber for cycle path surfacing."],
        ["Crankset", "Component Remanufacturing", "Mechanically polish scratched cranks to restore finish for A-Grade remanufacturing."],
        ["Chain", "Component Remanufacturing", "Clean, measure for stretch, and remove links to reuse on smaller Woom models."],
        ["Chain", "Upcycling / Brand Asset", "Upcycle worn chains into Woom-branded merchandise (e.g., keychains, bracelets)."],
        ["Crankset", "Upcycling / Brand Asset", "Repurpose cranks as creative door handles for Woom retail partner stores."],
        ["Pedals", "Component Remanufacturing", "Extract and replace bearings in high-quality pedals for B-Grade reuse."],
        ["Pedals", "Internal Reuse", "Salvage intact pedal reflectors to replenish small-parts inventory."],
        ["Chainring", "Upcycling / Brand Asset", "Incorporate salvaged chainrings into kinetic window displays in bike shops."],
        ["Drivetrain", "B2B Secondary Market", "Wholesale mixed drivetrain components to community bike-kitchens for repairs."],
        ["Bottom Bracket", "Internal Reuse", "Salvage sealed bearings from bottom brackets for internal shop use."],
        ["Chain", "B2B Secondary Market", "Donate un-reusable chains to art schools for metalworking projects (ESG credit)."],
        ["Handlebars", "Component Remanufacturing", "Cut down scratched ends of handlebars to create narrower profiles for smaller models."],
        ["Stem", "Internal Reuse", "Clean and directly reuse undamaged stems in A-Grade remanufacturing."],
        ["Brake Levers", "Component Remanufacturing", "Refurbish brake levers by replacing tension springs and pivot bolts."],
        ["Brake Calipers", "Internal Reuse", "Dismantle calipers to harvest tension screws, noodles, and springs for repair kits."],
        ["Grips", "Material Recycling", "Grind down damaged rubber lock-on grips for playground safety flooring."],
        ["Brake Cables", "Material Recycling", "Strip inner steel brake cables from housings for high-grade steel recycling."],
        ["Handlebars", "Upcycling / Brand Asset", "Weld handlebars together to create unique clothing racks for Woom apparel."],
        ["Stem", "B2B Secondary Market", "Sell surplus stems to DIY cargo bike builders in the secondary market."],
        ["Brake Pads", "B2B Secondary Market", "Donate brake pads with >50% life to cycling charities and NGOs."],
        ["Cable Housing", "Internal Reuse", "Cut old cable housings into short segments to use as frame protectors during transit."],
        ["Saddle", "Component Remanufacturing", "Re-cover structurally sound but torn saddles with new Woom-branded fabric."],
        ["Seatpost", "Internal Reuse", "Polish scratched aluminum seatposts for reuse in B-Grade bikes."],
        ["Seatpost Clamp", "Internal Reuse", "Salvage quick-release clamps directly into active spare parts inventory."],
        ["Inner Tubes", "Internal Reuse", "Patch punctured inner tubes for use in B-Grade or rental-fleet bikes."],
        ["Inner Tubes", "Upcycling / Brand Asset", "Cut unpatchable inner tubes into heavy-duty bungee cords for warehouse logistics."],
        ["Saddle Foam", "Material Recycling", "Recycle degraded saddle foam into protective packaging material for shipping new bikes."],
        ["Seatpost", "Upcycling / Brand Asset", "Repurpose bent seatposts as leverage extensions (cheater bars) for shop tools."],
        ["Fasteners", "Internal Reuse", "Ultrasonic clean all harvested bolts and screws for bulk reuse in remanufacturing."],
        ["Reflectors", "B2B Secondary Market", "Bundle surplus wheel reflectors and sell to budget bicycle manufacturers."],
        ["Packaging", "Upcycling / Brand Asset", "Shred original cardboard shipping boxes for void-fill in spare parts shipments."]
    ]
    
    # Procedural generation of 300 additional professional B2B scenarios
    components_b2b = ["Frames", "Forks", "Wheelsets", "Cranksets", "Handlebars", "Stems", "Brake Calipers", "Saddles", "Seatposts", "Pedals"]
    b2b_partners = [
        "pediatric wheelchair manufacturers", "community bike kitchens", "vocational training schools", 
        "developing nation NGOs", "DIY cargo bike builders", "local bike rental fleets", 
        "industrial design studios", "scrap metal aggregators", "upcycled furniture brands", "discount spare parts wholesalers"
    ]
    actions = [
        ("B2B Secondary Market", "Wholesale surplus {comp} to {partner} to open new secondary revenue streams without diluting brand value."),
        ("B2B Secondary Market", "Establish recurring supply contracts of {comp} with {partner} to ensure consistent inventory clearing."),
        ("Upcycling / Brand Asset", "Collaborate with {partner} to transform unrepairable {comp} into branded functional art installations."),
        ("Material Recycling", "Route heavily damaged {comp} to {partner} for raw material recovery and certified ESG emissions reporting."),
        ("Component Remanufacturing", "Outsource the bulk refurbishment of {comp} to {partner} to significantly reduce internal labor overhead."),
        ("Internal Reuse", "Standardize stress-testing of {comp} utilizing feedback from {partner} to improve internal A-Grade yields.")
    ]
    
    generated_ideas = []
    for comp in components_b2b:
        for partner in b2b_partners:
            for strat, desc_temp in actions:
                if len(generated_ideas) < 300:
                    generated_ideas.append([
                        comp, 
                        strat, 
                        desc_temp.format(comp=comp.lower(), partner=partner)
                    ])
                    
    # Combine lists
    all_scenarios = scenarios_data + generated_ideas
    df_ideas = pd.DataFrame(all_scenarios, columns=["Component Type", "Strategic Category", "Scenario Description"])
    
    # Interactive filters
    st.markdown(f"**Total scenarios currently loaded:** {len(df_ideas)}")
    filter_category = st.selectbox("Filter by Strategic Category:", ["All Categories"] + list(df_ideas["Strategic Category"].unique()))
    
    if filter_category != "All Categories":
        df_filtered = df_ideas[df_ideas["Strategic Category"] == filter_category]
    else:
        df_filtered = df_ideas
        
    st.dataframe(df_filtered, use_container_width=True, height=500)
    
    st.info("Export capability: This entire matrix (all 350 ideas) can be exported directly to Excel via the download icon in the top right corner of the table.")
 
# ==========================================
# AGGREGATE FINANCIAL CALCULATIONS
# ==========================================
profit_new_only = annual_volume * new_margin_unit
profit_new_base = (annual_volume - returned_units) * new_margin_unit 
upsell_profit = returned_units * ((msrp * 1.1) - (cogs * 1.1)) 
profit_ref_total = vol_ref * margin_ref
profit_rem_total = vol_rem * margin_rem
profit_harv_total = vol_harv * margin_harv
reman_gross_profit = profit_ref_total + profit_rem_total + profit_harv_total - total_triage_cost
cannibalization_loss = (vol_resold * (cannibalization_rate / 100)) * new_margin_unit
total_circular_profit = profit_new_base + upsell_profit + reman_gross_profit - cannibalization_loss
 
 
# ==========================================
# TAB 5: SCENARIO SIMULATION (100 SCENARIOS)
# ==========================================
with tab4:
    st.header("Monte Carlo Scenario Simulation")
    st.markdown("Instantly generate 100 potential business outcomes by applying market volatility to your baseline inputs. This requires zero manual data entry.")
    
    st.subheader("Define Market Volatility Boundaries")
    sim_col1, sim_col2, sim_col3 = st.columns(3)
    with sim_col1:
        vol_price = st.slider("Resale Price Volatility (± %)", 0, 30, 10)
    with sim_col2:
        vol_labor = st.slider("Processing Cost Volatility (± %)", 0, 50, 15)
    with sim_col3:
        vol_return = st.slider("Trade-in Volume Volatility (± %)", 0, 50, 20)
 
    if st.button("Generate 100 Market Scenarios"):
        scenarios = []
        
        for i in range(1, 101):
            f_price = 1 + random.uniform(-vol_price/100, vol_price/100)
            f_labor = 1 + random.uniform(-vol_labor/100, vol_labor/100)
            f_return = 1 + random.uniform(-vol_return/100, vol_return/100)
            
            sim_return_rate = upcycle_return_rate * f_return
            sim_returned_units = int(annual_volume * (sim_return_rate / 100))
            sim_triage_cost = sim_returned_units * (logistics_cost + triage_cost)
            
            sim_vol_ref = int(sim_returned_units * (pct_ref / 100))
            sim_vol_rem = int(sim_returned_units * (pct_rem / 100))
            sim_vol_harv = int(sim_returned_units * (pct_harv / 100))
            sim_vol_resold = sim_vol_ref + sim_vol_rem
            
            sim_margin_ref = (price_ref * f_price) - (core_cost + (cost_parts_ref * f_labor) + (time_ref * true_labor_rate * f_labor))
            sim_margin_rem = (price_rem * f_price) - (core_cost + (cost_parts_rem * f_labor) + (time_rem * true_labor_rate * f_labor))
            sim_margin_harv = (total_recovery_value / max(1, sim_vol_harv)) - (core_cost + (time_harv * true_labor_rate * f_labor)) if sim_vol_harv > 0 else 0
            
            sim_upsell = sim_returned_units * ((msrp * 1.1) - (cogs * 1.1))
            sim_gross = (sim_vol_ref * sim_margin_ref) + (sim_vol_rem * sim_margin_rem) + (sim_vol_harv * sim_margin_harv) - sim_triage_cost
            sim_cannibalization = (sim_vol_resold * (cannibalization_rate / 100)) * new_margin_unit
            
            sim_total_profit = profit_new_base + sim_upsell + sim_gross - sim_cannibalization
            
            scenarios.append({
                "Iteration": i,
                "Return Volume": sim_returned_units,
                "Avg Resale Factor": f"{int((f_price-1)*100)}%",
                "Cost Factor": f"{int((f_labor-1)*100)}%",
                "Total Circular Profit (€)": int(sim_total_profit)
            })
            
        df_sim = pd.DataFrame(scenarios)
        df_sim = df_sim.sort_values(by="Total Circular Profit (€)").reset_index(drop=True)
        
        st.markdown("---")
        st.subheader("Simulation Results: Profit Distribution")
        st.line_chart(df_sim["Total Circular Profit (€)"], height=300)
        
        res1, res2, res3 = st.columns(3)
        res1.metric("Worst Case Scenario", f"€{df_sim['Total Circular Profit (€)'].min():,.0f}")
        res2.metric("Median Scenario", f"€{df_sim['Total Circular Profit (€)'].median():,.0f}")
        res3.metric("Best Case Scenario", f"€{df_sim['Total Circular Profit (€)'].max():,.0f}")
 
# ==========================================
# TAB 1: EXECUTIVE DASHBOARD
# ==========================================
with tab1:
    st.header("Financial Performance Overview")
    
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Circular Profit", f"€{total_circular_profit:,.0f}", f"€{total_circular_profit - profit_new_base:,.0f} vs Linear Model")
    kpi2.metric("Avg. Margin / Resold Bike", f"€{(reman_gross_profit / max(1, vol_resold)):.2f}")
    kpi3.metric("Cost per Acquired Core", f"€{core_cost:.2f}")
    kpi4.metric("Cannibalization Cost", f"-€{cannibalization_loss:,.0f}")
 
    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns([2, 1])
    
    with col_chart1:
        st.subheader("Revenue & Profit Streams (€)")
        df_waterfall = pd.DataFrame({
            "Stream": ["1. Baseline Linear", "2. Trade-in Upsell", "3. Refurbished Sales", "4. Triage & Scrap", "5. Cannibalization Penalty"],
            "Value (€)": [profit_new_base, upsell_profit, (profit_ref_total + profit_rem_total), (profit_harv_total - total_triage_cost), -cannibalization_loss]
        })
        st.bar_chart(df_waterfall.set_index("Stream"), height=350)
    
    with col_chart2:
        st.subheader("Asset Routing Volume")
        df_routing = pd.DataFrame({
            "Pipeline": ['Light Refurbish', 'Full Remanufacture', 'Component Harvest'],
            "Units": [vol_ref, vol_rem, vol_harv]
        })
        st.bar_chart(df_routing.set_index("Pipeline"), height=350)
 
    st.markdown("### Export Financials")
    df_export = pd.DataFrame({
        "Metric": ["Linear Base Profit", "Core Acquisition Volume", "Unit Core Cost", "Trade-in Upsell Profit", "Remanufacturing Gross Profit", "Cannibalization Loss", "Total Circular Profit"],
        "Value (€/Units)": [profit_new_only, returned_units, core_cost, upsell_profit, reman_gross_profit, cannibalization_loss, total_circular_profit]
    })
    csv = df_export.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download Executive Report (CSV)", data=csv, file_name="woom_circular_report.csv", mime="text/csv")
 
# ==========================================
# TAB 6: ESG & IMPACT
# ==========================================
with tab5:
    st.header("Scope 3 Emissions & Material Savings")
    st.markdown("Remanufacturing avoids the extraction of virgin materials, particularly aluminum, which is highly energy-intensive to produce.")
    
    bike_weight = 5.4 
    alu_pct = 0.75 
    alu_co2_per_kg = 11.5 
    
    co2_saved_per_bike = (bike_weight * alu_pct) * alu_co2_per_kg
    total_co2_saved = (vol_resold * co2_saved_per_bike) / 1000 
    virgin_alu_saved = (vol_resold * bike_weight * alu_pct) / 1000 
    
    esg1, esg2, esg3 = st.columns(3)
    esg1.metric("CO2e Saved per Resold Bike", f"{co2_saved_per_bike:.1f} kg")
    esg2.metric("Total Annual CO2e Avoided", f"{total_co2_saved:.1f} Tons")
    esg3.metric("Virgin Aluminum Kept in Loop", f"{virgin_alu_saved:.1f} Tons")
 
# ==========================================
# TAB 7: DFREM AUDIT TOOL
# ==========================================
with tab6:
    st.header("Product Assessment: Design for Remanufacturing (DfRem)")
    st.markdown("Evaluate the physical design of the Woom 3. Lower scores indicate high processing times in Triage & Refurbishment pipelines.")
 
    score = 0
    max_score = 40
    recs = []
    
    st.subheader("1. Standardized Tooling & Fasteners")
    a1 = st.radio("How are components fastened on the Woom 3?", [
        "Mix of standard and custom sizes, requires changing tools frequently (5 pts)", 
        "Fully standardized ISO/DIN hex and torx across the entire bike (10 pts)"
    ])
    if "10 pts" in a1: score += 10
    else: recs.append("**Tooling:** Standardize all bolt heads to one or two hex sizes.")
 
    st.subheader("2. Cosmetic Remediation (Frame)")
    a2 = st.radio("How is cosmetic damage (scratches) handled?", [
        "Requires chemical paint stripping and wet repainting (0 pts)", 
        "Thick branded decal kits are applied over common scratch zones (10 pts)"
    ])
    if "10 pts" in a2: score += 10
    else: recs.append("**Cosmetics:** Repainting destroys profit margins. Supply mechanics with exact-fit decal kits.")
 
    st.subheader("3. Component Disassembly (Harvesting)")
    a3 = st.radio("How easily can components be stripped during harvesting?", [
        "Internal cable routing and press-fit bearings slow down tear-down (0 pts)", 
        "External cables and threaded/bolted components allow rapid dismantling (10 pts)"
    ])
    if "10 pts" in a3: score += 10
    else: recs.append("**Disassembly:** Internal cable routing looks premium but drastically increases labor costs.")
 
    st.subheader("4. Lifecycle Data Management")
    a4 = st.radio("How do mechanics verify the bike's history and condition?", [
        "Visual inspection and guesswork (0 pts)", 
        "Digital Product Passport (NFC/QR) integrated into the frame (10 pts)"
    ])
    if "10 pts" in a4: score += 10
    else: recs.append("**Data:** A Digital Passport removes guesswork and saves spare part costs.")
 
    st.markdown("---")
    percentage = int((score / max_score) * 100)
    st.metric("Overall DfRem Readiness Score", f"{percentage}%")
    st.progress(percentage)
    
    if percentage < 100:
        st.markdown("### Actionable Design Improvements:")
        for r in recs:
            st.markdown(r)