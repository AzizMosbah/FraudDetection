# Fraud Detection

This project is an investigative work on detecting fraudulent transactions and fraudulent accounts in a transactions dataset

---
## Part One: Exploratory Analysis

The file named `task1_transport_data.csv` consists of data from a fictional transportation company. It details the number of orders that customers of this company make on any given day, with some additional variables. You should:

• Provide exploratory analysis of the dataset.

• Summarise and explain the key trends in the data, providing visualisations and tabular representations as necessary.

• Construct a model or models to predict the number of jobs that this transportation company will complete on any given day.

• Explain what factors you think are significant and insignificant in contributing to the number of jobs completed, and any other information about your model that you think is important.

---

## Part Two: Network Analysis
The file name `task2_customers_devices_cards.csv` is a fictional list of fraudulent users of a smartphone app that takes payments. Each line represents a user, a device and a credit card. Your task is to detect networks in this file.

• Provide a visualisation of any networks found.

• Detect and hypothesise two different types of fraudulent behaviour from the data provided.

---

## Part Three: Location Analysis
The file name `task3_fraudulent_orders_locations.csv` is data from a fictional e-commerce company. It contains a month's worth of fraudulent orders.

• Provide exploratory analysis of the dataset.

• Where should the fraud detection team concentrate their efforts?

• Where is the worst hotspot in terms of number of orders? And in terms of combined order values?

• Identify any limitations you think apply to this dataset.

---

### Part Four: Data extraction / simple SQL database queries
Go to `https://www.w3schools.com/sql/trysql.asp?filename=trysql_op_in` and familiarise yourself with the database.

• Write an SQL query to count how many orders were made by customers in London with a "W" postcode.

• Following on from the previous query, write a table that generates a table with the following headers:
'CustomerName', 'City', 'PostalCode', 'OrderID', 'ProductID', 'Quantity', 'Price', 'TotalOrderValue'. (Hint: 'TotalOrderValue' should be derived from Quantity times Price.)

• Following on again, write a simplified query that simply returns the total (sum) value of all orders from customers in London with a 'W' postcode.

---

END
