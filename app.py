import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Heat Exchanger Visualizer", layout="centered")

st.title("🌡️ Heat Exchanger Performance Visualizer")
st.markdown("Analyze and compare performance of **Parallel** vs **Counter Flow** heat exchangers.")

# --- Inputs ---
st.sidebar.header("🔧 Input Parameters")

# Hot fluid
m_hot = st.sidebar.number_input("Hot Fluid Mass Flow Rate (kg/s)", value=1.5)
Cp_hot = st.sidebar.number_input("Hot Fluid Cp (kJ/kg·K)", value=4.2)
T_hot_in = st.sidebar.number_input("Hot Fluid Inlet Temp (°C)", value=140.0)
T_hot_out = st.sidebar.number_input("Hot Fluid Outlet Temp (°C)", value=90.0)

# Cold fluid
m_cold = st.sidebar.number_input("Cold Fluid Mass Flow Rate (kg/s)", value=2.0)
Cp_cold = st.sidebar.number_input("Cold Fluid Cp (kJ/kg·K)", value=4.18)
T_cold_in = st.sidebar.number_input("Cold Fluid Inlet Temp (°C)", value=30.0)
T_cold_out = st.sidebar.number_input("Cold Fluid Outlet Temp (°C)", value=70.0)

# Heat Exchanger Specs
U = st.sidebar.number_input("Overall Heat Transfer Coefficient, U (W/m²·K)", value=600.0)
A = st.sidebar.number_input("Heat Transfer Area, A (m²)", value=25.0)

flow_type = st.selectbox("Flow Configuration", ["Parallel Flow", "Counter Flow"])

# --- Calculations ---
Q_hot = m_hot * Cp_hot * (T_hot_in - T_hot_out) * 1000  # W
Q_cold = m_cold * Cp_cold * (T_cold_out - T_cold_in) * 1000  # W
Q = min(Q_hot, Q_cold)

# LMTD calculation
if flow_type == "Parallel Flow":
    delta_T1 = T_hot_in - T_cold_in
    delta_T2 = T_hot_out - T_cold_out
else:  # Counter Flow
    delta_T1 = T_hot_in - T_cold_out
    delta_T2 = T_hot_out - T_cold_in

if delta_T1 != delta_T2:
    LMTD = (delta_T1 - delta_T2) / np.log(delta_T1 / delta_T2)
else:
    LMTD = delta_T1

Q_lmtd = U * A * LMTD

C_min = min(m_hot * Cp_hot, m_cold * Cp_cold)
Q_max = C_min * (T_hot_in - T_cold_in) * 1000
effectiveness = Q / Q_max

# --- Output Results ---
st.subheader("📊 Results")
col1, col2 = st.columns(2)
col1.metric("Heat Duty (Q)", f"{Q/1000:.2f} kW")
col2.metric("Effectiveness (ε)", f"{effectiveness:.2f}")

st.write(f"**LMTD**: {LMTD:.2f} °C")
st.write(f"**Estimated Heat Duty via LMTD**: {Q_lmtd/1000:.2f} kW")

# --- Plot Temperature Profiles ---
st.subheader("📈 Temperature Profile")

x = np.linspace(0, 1, 50)

if flow_type == "Parallel Flow":
    T_hot_profile = T_hot_in - (T_hot_in - T_hot_out) * x
    T_cold_profile = T_cold_in + (T_cold_out - T_cold_in) * x
else:
    T_hot_profile = T_hot_in - (T_hot_in - T_hot_out) * x
    T_cold_profile = T_cold_out - (T_cold_out - T_cold_in) * x[::-1]

plt.figure(figsize=(7, 4))
plt.plot(x, T_hot_profile, label="Hot Fluid", color="red")
plt.plot(x, T_cold_profile, label="Cold Fluid", color="blue")
plt.xlabel("Exchanger Length (normalized)")
plt.ylabel("Temperature (°C)")
plt.title(f"Temperature Profile - {flow_type}")
plt.grid(True)
plt.legend()
st.pyplot(plt.gcf())
