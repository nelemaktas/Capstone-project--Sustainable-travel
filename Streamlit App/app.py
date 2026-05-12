## streamlit run "Streamlit App\app.py"
## cd "C:\Users\Nutzer\Documents\Practical-Data-Science-Course-Professor\Streamlit App"
## FOR TROUBELSHOOT
# st.write("Current working directory:", os.getcwd())
# st.write("Files in this folder:")
# st.write(os.listdir("."))
import streamlit as st

st.title("Sustainable Travel in Europe")
st.subheader("Train :train2: vs. Air:airplane:")
st.write("")

# Beautiful box
st.markdown("""
<div style="
    background-color:#f2f2f2;
    padding:16px 18px;
    border-radius:10px;
    color:#444;
    line-height:1.5;
">
<b>The idea behind this app</b><br><br>
When travelling in Europe, trains are often the most sustainable option. But high prices, long travel times, and airport overheads make the comparison less obvious.<br><br>
<b>Generalised cost</b> combines time, price, and carbon emissions to compare air and rail more realistically. What means of transport wins under more realistic assumptions? By what margin?
            <br><br><b>Social cost of carbon</b> approximates the future economic damage of emissions, it's the cost society bears. It has been estimated around 185 USD/ton or 166 EUR (1).
</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

st.caption("(1) See: *A new way to price carbon: Understanding the social cost of carbon* by Christoph Hambel Ton van den Bremer Frederick van der Ploeg, 2024, CEPR].")