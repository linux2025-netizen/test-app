import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Streamlit app
st.title("Jumia Product Scraper")
st.write("Enter a Jumia page URL to extract product details, including seller names.")

# Input field for URL
jumia_url = st.text_input("Enter Jumia Page URL:", placeholder="https://www.jumia.co.ke/category-example")

# Button to start scraping
if st.button("Scrape Products"):
    if not jumia_url.startswith("https://www.jumia.co.ke"):
        st.error("Please enter a valid Jumia Kenya URL.")
    else:
        try:
            # Fetch the page content
            st.info("Fetching data from the provided URL...")
            headers = {"User-Agent": "Mozilla/5.0 (compatible; Bot/1.0; +http://example.com/bot)"}
            response = requests.get(jumia_url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")

            # Find product cards
            products = soup.find_all("article", class_="prd _fb col c-prd")
            product_data = []

            for product in products:
                # Get product name and link
                product_name = product.find("h3", class_="name").get_text(strip=True)
                product_link = product.find("a", href=True)["href"]
                product_url = f"https://www.jumia.co.ke{product_link}"

                # Open product page to extract seller name
                product_response = requests.get(product_url, headers=headers)
                product_soup = BeautifulSoup(product_response.content, "html.parser")

                seller_name = product_soup.find("a", class_="btn _def _we _gray -mts")
                seller_name = seller_name.get_text(strip=True) if seller_name else "Unknown Seller"

                # Get price
                price = product.find("div", class_="prc").get_text(strip=True)

                # Append product details
                product_data.append({
                    "Product Name": product_name,
                    "Price": price,
                    "Product URL": product_url,
                    "Seller Name": seller_name
                })

            # Convert to DataFrame
            df = pd.DataFrame(product_data)

            if not df.empty:
                st.success(f"Scraped {len(df)} products successfully!")
                st.dataframe(df)

                # Allow download of results
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="jumia_products.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No products found on the page. Please check the URL.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

