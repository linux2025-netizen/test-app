import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.chrome.options import Options

# Streamlit App
def main():
    st.title("Jumia Product Scraper")

    # Input URL
    url = st.text_input("Enter Jumia Product Page URL", "")

    # Button to scrape the page
    if st.button("Scrape Products"):
        if url.strip():
            with st.spinner("Scraping products..."):
                try:
                    products = scrape_jumia_products(url)
                    if products:
                        st.success(f"Scraped {len(products)} products successfully!")
                        df = pd.DataFrame(products)
                        st.dataframe(df)

                        # Allow user to download data as CSV
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name="jumia_products.csv",
                            mime="text/csv",
                        )
                    else:
                        st.error("No products found on the page. Please check the URL.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a valid URL.")

# Scraping Function
def scrape_jumia_products(url):
    # Set up Selenium
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = Service()  # Automatically uses chromedriver from PATH if installed
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(5)  # Wait for the page to load

        # Get page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        products = []

        # Extract product details
        product_elements = soup.find_all("article", class_="prd _fb col c-prd")
        for product in product_elements:
            name = product.find("h3", class_="name")
            price = product.find("div", class_="prc")
            seller = product.find("div", class_="-mhs _pns")  # Seller info (if available)

            # Extract data and handle missing fields
            products.append({
                "Product Name": name.text.strip() if name else "N/A",
                "Price": price.text.strip() if price else "N/A",
                "Seller": seller.text.strip() if seller else "N/A",
            })

        return products
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
