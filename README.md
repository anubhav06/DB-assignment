# Drone-Base Assignment

A Python CLI application, built for the Drone Base assignment for SWE Intern.  
Features:
1. User Authentication  
  -> Login, Logout, Hashed password storage  
2. User Management  
  -> Create, Update, Delete and Read users  
3. Weather Information  
  -> Get live weather information about a place from lat/lon  

<hr>
<img src="https://i.ibb.co/LPr4Hnr/db-assignment-pic.png" alt="db-assignment-pic" border="0">

## Installation

1. Run `pip install requirements.txt` to install the dependencies.
2. Rename `example.env` to `.env`
3. Get a [OpenWeather](https://openweathermap.org/appid) API key and add in `.env` file:  
   `API_key=<your_api_key_here>`
5. Run `python app.py` to start the CLI
6. Optionally, you can run `python test_app.py` to run the tests.

