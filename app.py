import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Hospital Vaccination Impact Simulation", layout="wide")

# -------------------- TITLE --------------------
st.title("Hospital Vaccination Impact Simulation")

# -------------------- SIDEBAR INPUTS --------------------
st.sidebar.header("Simulation Parameters")

population = st.sidebar.slider("Total Population", 100, 10000, 1000)
initial_infected = st.sidebar.slider("Initial Infected", 1, 200, 10)
vaccination_rate = st.sidebar.slider("Vaccination Rate (per day)", 0.0, 0.5, 0.05)
beta = st.sidebar.slider("Infection Rate (β)", 0.1, 1.0, 0.3)
gamma = st.sidebar.slider("Recovery Rate (γ)", 0.05, 0.5, 0.1)
days = st.sidebar.slider("Simulation Days", 10, 200, 100)

# -------------------- SIR + VACCINATION MODEL --------------------
def simulate(population, I0, beta, gamma, vaccination_rate, days):
    S = population - I0
    I = I0
    R = 0
    V = 0

    S_list, I_list, R_list, V_list = [], [], [], []

    for _ in range(days):
        vaccinated = vaccination_rate * S
        new_infections = beta * S * I / population
        recoveries = gamma * I

        S = S - new_infections - vaccinated
        I = I + new_infections - recoveries
        R = R + recoveries
        V = V + vaccinated

        S_list.append(S)
        I_list.append(I)
        R_list.append(R)
        V_list.append(V)

    return np.array(S_list), np.array(I_list), np.array(R_list), np.array(V_list)

S, I, R, V = simulate(population, initial_infected, beta, gamma, vaccination_rate, days)

# -------------------- PLOTS --------------------
st.subheader("Population Dynamics")

col1, col2 = st.columns(2)

# --- Graph 1: SIR ---
with col1:
    st.markdown("**SIR Model**")

    fig1, ax1 = plt.subplots(figsize=(4, 2.5))

    ax1.plot(S, label="Susceptible")
    ax1.plot(I, label="Infected")
    ax1.plot(R, label="Recovered")

    ax1.set_xlabel("Days")
    ax1.set_ylabel("Population")
    ax1.legend(fontsize=8)

    st.pyplot(fig1, use_container_width=False)

# --- Graph 2: Vaccination ---
with col2:
    st.markdown("**Vaccination Dynamics**")

    non_vaccinated = S + I + R  # everyone not vaccinated

    fig2, ax2 = plt.subplots(figsize=(4, 2.5))

    ax2.plot(V, label="Vaccinated")
    ax2.plot(non_vaccinated, label="Non-Vaccinated")

    ax2.set_xlabel("Days")
    ax2.set_ylabel("Population")
    ax2.legend(fontsize=8)

    st.pyplot(fig2, use_container_width=False)

# -------------------- METRICS --------------------
st.subheader("Key Metrics")

peak_infected = np.max(I)
final_infected = I[-1]
final_vaccinated = V[-1]
herd_immunity_threshold = 1 - (1 / beta)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Peak Infected", int(peak_infected))
col2.metric("Final Infected", int(final_infected))
col3.metric("Total Vaccinated", int(final_vaccinated))
col4.metric("Herd Immunity Threshold", f"{herd_immunity_threshold:.2f}")

# -------------------- THEORY + MATH --------------------
st.subheader("Theory and Mathematical Model")

st.markdown("""
### SIR Model with Vaccination

We extend the classical SIR model by adding vaccination:

- **S**: Susceptible
- **I**: Infected
- **R**: Recovered
- **V**: Vaccinated

#### Differential Equations:

dS/dt = -βSI/N - vS  
dI/dt = βSI/N - γI  
dR/dt = γI  
dV/dt = vS  

Where:
- β = infection rate
- γ = recovery rate
- v = vaccination rate
- N = total population

#### Key Concepts:

- Infection spreads based on contact between susceptible and infected.
- Vaccination reduces susceptible pool directly.
- Recovery builds immunity.
- Herd immunity threshold ≈ 1 - (1/β)

#### Interpretation:

- Higher vaccination rate → lower peak infections  
- Higher β → faster spread  
- Higher γ → faster recovery  

This simulation models how intervention (vaccination) changes infection dynamics in a hospital setting.
""")