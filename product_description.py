import streamlit as st
from openai import OpenAI

# Set up API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- Streamlit UI ---
st.title("🛍️ AI Product Description Generator")
st.markdown("Describe your product, and let GPT-4 generate compelling copy for you.")

with st.form("input_form"):
    product_name = st.text_input("Product Name", placeholder="e.g. Solar-Powered Smartwatch")
    features = st.text_area("Key Features / Benefits", placeholder="Long battery life, fitness tracking, waterproof...")
    audience = st.text_input("Target Audience", placeholder="e.g. outdoor enthusiasts, tech lovers")
    tone = st.selectbox("Tone", ["Friendly", "Professional", "Salesy", "Creative"], index=0)
    submitted = st.form_submit_button("Generate Description")

# --- GPT-4 Call ---
if submitted:
    with st.spinner("Generating description..."):
        prompt = f"""
        Write a persuasive product description for the following product.

        Product Name: {product_name}
        Key Features: {features}
        Target Audience: {audience}
        Tone: {tone}

        Make it engaging and clear. Avoid fluff. Use bullet points where appropriate.
        """
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        description = response.choices[0].message.content

        st.subheader("📝 Generated Product Description")
        st.text_area("Description", value=description, height=300)
        st.download_button("Download as .txt", description, file_name="product_description.txt")
