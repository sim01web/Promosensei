import streamlit as st
from rag_query import retrieve_offers, generate_response_with_gemini

st.set_page_config(page_title="PromoSensei", layout="centered")
st.title("PromoSensei: Only the Best Deals")

query = st.text_input("Ask a question like 'haircare discounts under ₹500':")

if st.button("Search"):
    if query:
        with st.spinner("Searching offers..."):
            offers = retrieve_offers(query)
            if not offers:
                st.warning("No matching offers found.")
            else:
                response = generate_response_with_gemini(query, offers)
                st.success("Responding to your query...")
                st.markdown(f"**PromoSensei:**\n\n{response}")
    else:
        st.warning("Please enter a query to get started.")
