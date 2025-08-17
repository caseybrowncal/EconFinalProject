import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Australia vs USA Environmental Analysis",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("Australia vs USA Environmental Analysis")
st.markdown("**Comparative Analysis of Environmental Trends, CO2 Emissions, Temperature Changes, and Climate Impacts**")

# Load data
@st.cache_data
def load_data():
    try:
        # Australia data
        aus_co2 = pd.read_csv('group_project/co2_pcap_cons.csv')
        aus_temp = pd.read_csv('group_project/aus_temp.csv')
        aus_energy = pd.read_csv('group_project/energy_use_per_person.csv')
        aus_gdp = pd.read_csv('group_project/gdp_total_yearly_growth.csv')
        aus_sea_level = pd.read_csv('group_project/global_sea_levels.csv')
        
        # USA data
        us_co2 = pd.read_csv('individual_project/co2_pcap_cons.csv')
        us_temp = pd.read_csv('individual_project/data (2).csv', comment='#')  # US temperature data in Fahrenheit
        us_energy = pd.read_csv('individual_project/energy_use_per_person.csv')
        us_gdp = pd.read_csv('individual_project/gdp_total_yearly_growth.csv')
        us_disasters = pd.read_csv('individual_project/US_natural_disasters_cost.csv', comment='#')
        
        return aus_co2, aus_temp, aus_energy, aus_gdp, aus_sea_level, us_co2, us_temp, us_energy, us_gdp, us_disasters
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None, None, None, None, None, None, None

# Load data
data = load_data()
if data[0] is None:
    st.error("Failed to load data. Please check file paths and try again.")
    st.stop()

aus_co2, aus_temp, aus_energy, aus_gdp, aus_sea_level, us_co2, us_temp, us_energy, us_gdp, us_disasters = data

# Project Overview
st.header("Project Overview")
st.markdown("""
This analysis compares environmental trends between Australia and the United States, examining:
- CO2 emissions per capita trends
- Temperature variations and climate patterns
- Energy consumption patterns
- Economic growth correlations
- Environmental impact assessments
""")

# Australia Environmental Analysis
st.header("Australia Environmental Analysis")

# CO2 Emissions Analysis
st.subheader("CO2 Emissions Per Capita (1751-2022)")
if not aus_co2.empty:
    try:
        aus_co2_filtered = aus_co2[aus_co2['country'] == 'Australia'].copy()
        if not aus_co2_filtered.empty:
            # Melt the data to get year and emissions columns
            aus_co2_melted = aus_co2_filtered.melt(id_vars=['country'], var_name='Year', value_name='Emissions (Metric Tons Per Person)')
            aus_co2_melted['Year'] = pd.to_numeric(aus_co2_melted['Year'], errors='coerce')
            aus_co2_melted['Emissions (Metric Tons Per Person)'] = pd.to_numeric(aus_co2_melted['Emissions (Metric Tons Per Person)'], errors='coerce')
            aus_co2_melted = aus_co2_melted.dropna(subset=['Year', 'Emissions (Metric Tons Per Person)'])
            
            if not aus_co2_melted.empty:
                fig_aus_co2 = px.line(aus_co2_melted, x='Year', y='Emissions (Metric Tons Per Person)',
                                     title="Australia CO2 Emissions Per Capita Over Time")
                fig_aus_co2.update_layout(height=500)
                st.plotly_chart(fig_aus_co2, use_container_width=True)
                
                # Summary statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    max_emissions = aus_co2_melted['Emissions (Metric Tons Per Person)'].max()
                    st.metric("Peak Emissions", f"{max_emissions:.2f}", "Metric Tons Per Person")
                with col2:
                    current_emissions = aus_co2_melted[aus_co2_melted['Year'] == 2022]['Emissions (Metric Tons Per Person)']
                    if not current_emissions.empty:
                        st.metric("Current Emissions (2022)", f"{current_emissions.iloc[0]:.2f}", "Metric Tons Per Person")
                    else:
                        st.metric("Current Emissions (2022)", "N/A", "Data not available")
                with col3:
                    min_emissions = aus_co2_melted['Emissions (Metric Tons Per Person)'].min()
                    st.metric("Total Change", f"{max_emissions - min_emissions:.2f}", "Metric Tons Per Person")
            else:
                st.warning("No valid CO2 emissions data found for Australia")
        else:
            st.warning("Australia data not found in CO2 dataset")
    except Exception as e:
        st.error(f"Error processing Australia CO2 data: {e}")

# Temperature Analysis
st.subheader("Temperature Trends")
if not aus_temp.empty:
    try:
        aus_temp_filtered = aus_temp.copy()
        aus_temp_filtered['Year'] = pd.to_numeric(aus_temp_filtered['Year'], errors='coerce')
        aus_temp_filtered['Temperature'] = pd.to_numeric(aus_temp_filtered['Annual'], errors='coerce')  # Fixed: use 'Annual' column
        aus_temp_filtered = aus_temp_filtered.dropna(subset=['Year', 'Temperature'])
        
        if not aus_temp_filtered.empty:
            fig_aus_temp = px.line(aus_temp_filtered, x='Year', y='Temperature',
                                  title="Australia Temperature Trends Over Time")
            fig_aus_temp.update_layout(height=500)
            st.plotly_chart(fig_aus_temp, use_container_width=True)
        else:
            st.warning("No valid temperature data found for Australia")
    except Exception as e:
        st.error(f"Error processing Australia temperature data: {e}")

# Energy Use Analysis
st.subheader("Energy Consumption Per Person")
if not aus_energy.empty:
    try:
        aus_energy_filtered = aus_energy[aus_energy['country'] == 'Australia'].copy()  # Fixed: filter by country first
        if not aus_energy_filtered.empty:
            # Melt the data to get year and energy columns (wide format)
            aus_energy_melted = aus_energy_filtered.melt(id_vars=['country'], var_name='Year', value_name='Energy')
            aus_energy_melted['Year'] = pd.to_numeric(aus_energy_melted['Year'], errors='coerce')
            aus_energy_melted['Energy'] = pd.to_numeric(aus_energy_melted['Energy'], errors='coerce')
            aus_energy_melted = aus_energy_melted.dropna(subset=['Year', 'Energy'])
            
            if not aus_energy_melted.empty:
                fig_aus_energy = px.line(aus_energy_melted, x='Year', y='Energy',
                                        title="Australia Energy Consumption Per Person Over Time")
                fig_aus_energy.update_layout(height=500)
                st.plotly_chart(fig_aus_energy, use_container_width=True)
            else:
                st.warning("No valid energy data found for Australia")
        else:
            st.warning("Australia data not found in energy dataset")
    except Exception as e:
        st.error(f"Error processing Australia energy data: {e}")

# USA Environmental Analysis
st.header("USA Environmental Analysis")

# CO2 Emissions Analysis
st.subheader("CO2 Emissions Per Capita (1751-2022)")
if not us_co2.empty:
    try:
        us_co2_filtered = us_co2[us_co2['country'] == 'USA'].copy()  # Fixed: use 'USA' not 'United States'
        if not us_co2_filtered.empty:
            # Melt the data to get year and emissions columns
            us_co2_melted = us_co2_filtered.melt(id_vars=['country'], var_name='Year', value_name='Emissions (Metric Tons Per Person)')
            us_co2_melted['Year'] = pd.to_numeric(us_co2_melted['Year'], errors='coerce')
            us_co2_melted['Emissions (Metric Tons Per Person)'] = pd.to_numeric(us_co2_melted['Emissions (Metric Tons Per Person)'], errors='coerce')
            us_co2_melted = us_co2_melted.dropna(subset=['Year', 'Emissions (Metric Tons Per Person)'])
            
            if not us_co2_melted.empty:
                fig_us_co2 = px.line(us_co2_melted, x='Year', y='Emissions (Metric Tons Per Person)',
                                    title="USA CO2 Emissions Per Capita Over Time")
                fig_us_co2.update_layout(height=500)
                st.plotly_chart(fig_us_co2, use_container_width=True)
                
                # Summary statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    max_emissions = us_co2_melted['Emissions (Metric Tons Per Person)'].max()
                    st.metric("Peak Emissions", f"{max_emissions:.2f}", "Metric Tons Per Person")
                with col2:
                    current_emissions = us_co2_melted[us_co2_melted['Year'] == 2022]['Emissions (Metric Tons Per Person)']
                    if not current_emissions.empty:
                        st.metric("Current Emissions (2022)", f"{current_emissions.iloc[0]:.2f}", "Metric Tons Per Person")
                    else:
                        st.metric("Current Emissions (2022)", "N/A", "Data not available")
                with col3:
                    min_emissions = us_co2_melted['Emissions (Metric Tons Per Person)'].min()
                    st.metric("Total Change", f"{max_emissions - min_emissions:.2f}", "Metric Tons Per Person")
            else:
                st.warning("No valid CO2 emissions data found for USA")
        else:
            st.warning("USA data not found in CO2 dataset")
    except Exception as e:
        st.error(f"Error processing USA CO2 data: {e}")

# Temperature Analysis
st.subheader("Temperature Trends")
st.info("Note: Temperature data structure may vary between projects. Using available data.")

if not us_temp.empty:
    try:
        # Clean and prepare US temperature data
        us_temp_filtered = us_temp.copy()
        # Extract year from Date column (format: YYYYMM)
        us_temp_filtered['Year'] = us_temp_filtered['Date'].astype(str).str[:4].astype(int)
        us_temp_filtered['Temperature_F'] = pd.to_numeric(us_temp_filtered['Value'], errors='coerce')
        us_temp_filtered = us_temp_filtered.dropna(subset=['Year', 'Temperature_F'])
        
        if not us_temp_filtered.empty:
            # Group by year and calculate average temperature
            us_temp_yearly = us_temp_filtered.groupby('Year')['Temperature_F'].mean().reset_index()
            
            fig_us_temp = px.line(us_temp_yearly, x='Year', y='Temperature_F',
                                 title="USA Temperature Trends Over Time (Fahrenheit)")
            fig_us_temp.update_layout(height=500)
            st.plotly_chart(fig_us_temp, use_container_width=True)
        else:
            st.warning("No valid temperature data found for USA")
    except Exception as e:
        st.error(f"Error processing USA temperature data: {e}")

# Energy Use Analysis
st.subheader("Energy Consumption Per Person")
if not us_energy.empty:
    try:
        us_energy_filtered = us_energy[us_energy['country'] == 'USA'].copy()  # Fixed: filter by country first
        if not us_energy_filtered.empty:
            # Melt the data to get year and energy columns (wide format)
            us_energy_melted = us_energy_filtered.melt(id_vars=['country'], var_name='Year', value_name='Energy')
            us_energy_melted['Year'] = pd.to_numeric(us_energy_melted['Year'], errors='coerce')
            us_energy_melted['Energy'] = pd.to_numeric(us_energy_melted['Energy'], errors='coerce')
            us_energy_melted = us_energy_melted.dropna(subset=['Year', 'Energy'])
            
            if not us_energy_melted.empty:
                fig_us_energy = px.line(us_energy_melted, x='Year', y='Energy',
                                       title="USA Energy Consumption Per Person Over Time")
                fig_us_energy.update_layout(height=500)
                st.plotly_chart(fig_us_energy, use_container_width=True)
            else:
                st.warning("No valid energy data found for USA")
        else:
            st.warning("USA data not found in energy dataset")
    except Exception as e:
        st.error(f"Error processing USA energy data: {e}")

# Natural Disasters Analysis
st.subheader("Natural Disaster Costs (1980-2024)")
if not us_disasters.empty:
    try:
        us_disasters_filtered = us_disasters.copy()
        us_disasters_filtered['Year'] = pd.to_numeric(us_disasters_filtered['Year'], errors='coerce')
        us_disasters_filtered['Cost'] = pd.to_numeric(us_disasters_filtered['All Disasters Cost'], errors='coerce')
        us_disasters_filtered = us_disasters_filtered.dropna(subset=['Year', 'Cost'])
        
        if not us_disasters_filtered.empty:
            fig_disasters = px.line(us_disasters_filtered, x='Year', y='Cost',
                                   title="US Natural Disaster Costs Over Time",
                                   labels={'Cost': 'Cost (Billions USD)'})
            fig_disasters.update_layout(height=500)
            st.plotly_chart(fig_disasters, use_container_width=True)
        else:
            st.warning("No valid natural disaster data found")
    except Exception as e:
        st.error(f"Error processing natural disaster data: {e}")

# Comparison Analysis
st.header("Comparative Analysis")

# Correlation comparison
st.subheader("Correlation Comparison")

# Hard-coded correlation values from notebook analysis
aus_correlation = 0.6476  # From Australia analysis
us_correlation = 0.1371   # From USA analysis

col1, col2 = st.columns(2)

with col1:
    st.metric("Australia", f"{aus_correlation:.4f}", "Temperature vs CO2 Correlation")
    st.info("Strong positive correlation indicating temperature and CO2 emissions are closely related in Australia")

with col2:
    st.metric("USA", f"{us_correlation:.4f}", "Temperature vs CO2 Correlation")
    st.info("Weak positive correlation suggesting less direct relationship between temperature and CO2 emissions in USA")

# Correlation interpretation
st.subheader("Correlation Analysis")
st.markdown("""
**Australia (0.6476):**
- Strong positive correlation between temperature and CO2 emissions
- Indicates that as CO2 emissions increase, temperatures also tend to increase
- Suggests Australia's climate is more directly impacted by its emissions

**USA (0.1371):**
- Weak positive correlation between temperature and CO2 emissions
- Indicates a much weaker relationship between emissions and temperature changes
- May be due to larger geographic area, diverse climate zones, or other environmental factors
""")

# Key differences
st.subheader("Key Differences")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Australia:**
    - Higher correlation between CO2 and temperature
    - Strong correlation with sea level rise (0.7856)
    - More recent decline in emissions
    - Focus on eco-tourism and biodiversity
    """)

with col2:
    st.markdown("""
    **USA:**
    - Different correlation pattern with CO2 emissions
    - Different emission patterns
    - Natural disaster cost tracking
    - Larger economy and population
    """)

# Data Sources
st.header("Data Sources and Methodology")
st.markdown("""
**Data Sources:**
- CO2 emissions per capita: Our World in Data
- Temperature data: Bureau of Meteorology (Australia), NOAA (USA)
- Energy consumption: World Bank
- GDP growth: World Bank
- Sea level data: NASA
- Natural disaster costs: NOAA

**Methodology:**
- Time series analysis of environmental indicators
- Correlation analysis between CO2 emissions and temperature
- Comparative analysis of trends between countries
- Statistical significance testing where applicable
""")
