import streamlit as st
import streamlit.components.v1 as components

st.set_page_config( 
     page_title="EmissioNavi", 
     page_icon="💚", 
     layout="wide", 
     initial_sidebar_state="expanded", 
 ) 
hide_default_format = """ 
        <style> 
        #MainMenu {visibility: show; }         footer {visibility: hidden;} 
        </style> 
        """ 
st.markdown(hide_default_format, unsafe_allow_html=True) 

def gradient_text(text, color1, color2):
    gradient_css = f"""
        background: -webkit-linear-gradient(left, {color1}, {color2});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        font-size: 42px;
    """
    return f'<span style="{gradient_css}">{text}</span>'

color1 = "#0d3270"
color2 = "#0fab7b"
text = "GreenPath Navigator "
  
left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image("images/logo.png", width=250)

styled_text = gradient_text(text, color1, color2)
st.write(f"<div style='text-align: center;'>{styled_text}</div>", unsafe_allow_html=True)
  
st.markdown("""
#### Welcome to GreenPath Navigator  - Where Transportation Meets Environmental Responsibility 🌍🚀

At GreenPath Navigator , we bridge the gap between transportation and sustainability, empowering users with powerful insights to make eco-friendly decisions.

---

### Key Features and Innovations 🌱💡

1. **Commute Insight**:  
   Effortlessly calculate and reduce your carbon footprint for daily commutes using intuitive machine learning models. Input your travel details and discover how small changes in transportation choices can significantly reduce emissions.

2. **Trans Sustain - Sustainable Transportation & Shipment Impact Analysis**:  
   Track and log the environmental impact of personal and business transportation activities. This module integrates **Logistic Regression** models to predict and analyze CO₂ emissions, providing actionable suggestions for sustainable alternatives.

3. **Carbon Graph - Global Emission Visualization**:  
   Explore interactive, data-driven visualizations that shed light on carbon footprints worldwide. Compare different transportation options and shipment methods to identify greener choices with clear and engaging visual data.

4. **Dynamic Route Optimization**:  
   Using the TomTom API, we calculate optimal routes while integrating emission data and environmental parameters. See the most eco-friendly path between destinations, saving fuel and reducing your environmental impact.

---

### Why GreenPath Navigator  Stands Out 🌐🔍

- **Comprehensive Data Analytics**:  
  Empowering users with insights from **interactive maps**, **emission heatmaps**, and **comparative bar charts** for a detailed understanding of global and local emission patterns.

- **Eco-Friendly Guidance**:  
  Receive personalized recommendations for adopting green transportation methods, including walking, biking, carpooling, and EV (Electric Vehicle) transitions.

- **Advanced Supply Chain Tools**:  
  Optimize logistics with **shipment emission calculators**, helping businesses adopt sustainable practices that minimize carbon footprints while enhancing operational efficiency.

---

### Unlock the Benefits of GreenPath Navigator  🏆🌿

- **Raise Environmental Awareness**:  
  Understand the hidden environmental cost of everyday actions and inspire behavioral changes.

- **Drive Eco-Friendly Innovation**:  
  Use data-driven strategies to influence green policies and corporate responsibility initiatives.

- **Support Global Sustainability**:  
  Collaborate in creating a cleaner future by integrating carbon-conscious decisions into transportation and logistics.

---

### How It Works 🔧🚴‍♂️

1. **Input Locations or Coordinates**: Enter start and end points for route optimization.
2. **Select Mode of Transportation**: Choose between public transport, car, or bike.
3. **Visualize and Compare**: View optimized routes, carbon emissions, and alternative eco-friendly paths.
4. **Act and Reduce**: Follow actionable tips to cut down emissions, helping the planet and your wallet.

---

### Try GreenPath Navigator  Today and Navigate the Future Responsibly!  
**Together, let’s steer toward a sustainable tomorrow. 🌍💚**  
""")

