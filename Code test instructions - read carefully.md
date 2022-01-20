# Ravelin Investigations Team Code Test

This code test is designed to test your technical aptitude and expertise with handling data. That said, we are just as interested in your approach to problem solving as the actual answers to your test.

Don't spend any longer than a couple of hours on each task. We acknowledge that you may be working and it may be difficult to find time to complete this test. The deadline for your report will take this into account and will be indicated on the email confirming your invitation to this code test.

Please submit your work in the form of a PDF. It is up to you to choose how to represent your findings. You should aim to make your work clear and explicable, using visualisations, tables, maps, etc as necessary. Think about "what", "when", "where", "how", and "why". Remember, you will be explaining your findings to clients and you need to choose the right balance of technical detail and narrative.

It doesn't matter what software or tools you use, as long as you can use them effectively to model your data and extract the information you need.

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
