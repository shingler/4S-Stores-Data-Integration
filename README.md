# platform20200916

This project was developed for multinational 4S automotive retail stores of BMW and Porsche groups. This project streamlines daily financial data aggregation, integrity verification, and dynamic storage in a database after converting the data to required formats and standards. The system then utilizes SOAP technology to send the formatted data to the Navision system for data integration.

Technical points of this project
1. Developed in Python, the project accesses SQL Server through SQLAlchemy.
2. Source data can be either multiple XML files located at specified paths or JSON data read from network interfaces.
3. To accommodate non-scheduled tasks, the program uses Flask to build a simple API interface, allowing management backend staff to manually trigger data processing functions as needed.

The challenges of this project
1. To facilitate statistics and archiving, all data must be stored in different database tables based on the store, which cannot be pre-enumerated. This means the program must have the capability to dynamically create database tables.
2. The variety and number of data fields are extensive, requiring the program to perform complex format validation and have error compatibility. Additionally, the program must process data quickly to avoid backlogs that could delay business operations. Therefore, the application employs a multi-threading framework to accelerate the processing.

The highlight of this project
The highlight of this project is the use of Test-Driven Development (TDD), which anticipates extreme data and network anomalies in advance. When there are changes in requirements or unexpected extreme data, the system can quickly identify areas needing adjustment and maintain the code through logs and pre-accumulated test cases, earning high praise from the client.
