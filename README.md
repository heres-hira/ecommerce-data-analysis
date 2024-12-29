# E-commerce Data Analysis

## Overview
This project involves an in-depth analysis of an e-commerce dataset to uncover valuable insights related to revenue trends, customer behavior, product categories, payment preferences, and delivery performance. The findings aim to support data-driven decision-making for improving sales, customer satisfaction, and operational efficiency.

This project is part of the "Belajar Analisis Data dengan Python" course by Dicoding.

## Objectives
The main objectives of this project include answering key business questions:
1. What are the monthly revenue trends from 2016 to 2018?
2. Which product categories are the best and worst performers in terms of sales revenue?
3. Which product categories receive the highest and lowest customer reviews?
4. What is the geographic distribution of our customers?
5. How are customers distributed based on their payment type? What is the average installment count for credit card users?
6. What is the distribution of order statuses, and what percentage is the cancellation rate?
7. What is the delivery time spread for delivered orders?

## Dataset
The dataset consists of several interconnected dataframes, each containing information crucial to the analysis:
1. [Customers Data](.data/customers_dataset.csv): Contains customer information, including unique IDs and location details.
2. [Orders Data](.data/orders_dataset.csv): Includes details about orders, such as status, purchase timestamps, and delivery timelines.
3. [Order Reviews Data](.data/order_reviews_dataset.csv): Provides customer reviews with scores, comments, and timestamps.
4. [Order Items Data](.data/order_items_dataset.csv): Contains details of each item in an order, including product IDs and pricing.
5. [Payments Data](.data/order_payments_dataset.csv): Describes payment details, including types and installment counts.
6. [Product Categories](.data/products_dataset.csv) and [Product Category Name Translation](.data/product_category_name_translation.csv): Includes category translations and detailed product attributes.

(Note: The dataset was provided by the course, and the original source is not specified.)

## Tools and Technologies
- **Programming Language:** Python
- **Libraries:**
  - Pandas: Data manipulation and analysis
  - Matplotlib & Seaborn: Data visualization
  - NumPy: Numerical computations

## Key Findings
1. **Revenue Trends:**
   - Revenue showed consistent growth, peaking sharply in November 2017, followed by a decline in December 2017 and fluctuating growth thereafter.

2. **Customer Reviews:**
   - The `cds_dvds_musicals` category received the highest average review score (4.6 stars), while `security_and_services` had the lowest (2.5 stars), suggesting potential quality or service issues.

3. **Product Categories:**
   - The `health_beauty` category generated the highest revenue, highlighting strong demand. Conversely, categories like `security_and_services` showed minimal sales, potentially influenced by pricing.

4. **Customer Demographics:**
   - São Paulo (SP) emerged as the dominant state for customers, with significantly lower distribution in other states.

5. **Payment Preferences:**
   - Most customers preferred credit cards (73.8% of transactions), with a majority opting for one-time payments. Debit cards were the least preferred, and only 18 customers selected the maximum of 24 installments.

6. **Order Status:**
   - Out of 116,290 total orders, 115,720 were successfully delivered, and 570 were canceled, resulting in a cancellation rate of 0.48%.

7. **Delivery Insights:**
   - The majority of orders were delivered within 8-14 days (46,013 orders), followed by 1-7 days, 15-21 days, and 13,667 orders taking more than 21 days.

## Visualizations
1. Monthly revenue trends from 2016 to 2018.
2. Average review scores by product category.
3. Payment type distribution and average installments for credit card users.
4. Geographic distribution of customers by state.
5. Order status counts and cancellation rate.
6. Delivery time spread for delivered orders.

## Challenges
- Handling missing or inconsistent data across multiple dataframes.
- Balancing detailed analysis with concise and interpretable visualizations.

## Future Improvements
1. Incorporate predictive modeling to forecast revenue trends.
2. Conduct sentiment analysis on customer reviews for deeper insights.
3. Investigate factors influencing delivery times across different regions.

## How to Run the Project
1. Clone this repository.
2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Jupyter Notebook or Python scripts to view the analysis and visualizations.

## Streamlit Demo
This project also showcases a Streamlit app. The live demo could be viewed here: [Streamlit Demo](https://dashboard-ecommerce-analysis.streamlit.app/)

## Author
Hanifa Mahira
**Contact:** hanifamahira.hm@gmail.com | www.linkedin.com/hanifa-mahira
