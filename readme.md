# LLM Calories Tracker

## Project Description
LLM Calories Tracker is a Flask-based web application designed to help users track their daily caloric intake and forecast future weight changes. By utilizing a locally hosted open-source language model (LLM), this app provides a unique interface where users can input their meals, and the LLM estimates the calorie content. The app then logs the user's weight and calculates calorie balance using the Basal Metabolic Rate (BMR). With historical data, it predicts potential weight changes over the next 30 days.

## Features
- **Flask Interface**: The app provides a simple web interface for managing users and logging daily food intake and weight.
- **LLM-Based Calorie Estimation**: The app uses a locally hosted LLaMA 3.2 GGUF model to estimate the calorie content of food based on user input.
- **SQLite Database**: All user data, including food intake and weight records, are stored using SQLite.
- **Weight Forecasting**: The app uses the last 30 days of caloric data, applies simple exponential scaling, and predicts the user's weight trend for the next 30 days.

## Workflow
1. **User Management**: The app allows for the creation and management of user profiles.
2. **Daily Food Logging**: After selecting a user, you're redirected to a page where you can input the day's meals and receive calorie estimates from the LLM.
3. **Calorie Balance Calculation**: Once all meals and the user's weight for the day are logged, the backend computes the total calorie intake and compares it to the user's BMR.
4. **Weight Forecasting**: On the results page, the backend analyzes the past 30 days of data (or fewer if there isn't 30 days' worth of data) and predicts the user's weight change for the next 30 days using a basic exponential scaling method.

## Areas for Improvement
- **LLM Accuracy**: The LLaMA 3.2 GGUF model used for calorie estimation is not very accurate. With proper fine-tuning, the accuracy can be greatly improved.
- **Improved Prediction Model**: The current forecasting method is simplistic. It could be enhanced by incorporating more sophisticated models trained on larger datasets.

## Images

### Seting up new user
![Seting up new user](<screenshots/Screenshot 2024-10-22 at 21-04-43 User Registration.png>)

### Calculating BMR
![Calculating BMR](<screenshots/Screenshot 2024-10-22 at 21-04-51 User Registration.png>)

### Getting calories from llm
![Getting calories from llm](<screenshots/Screenshot 2024-10-22 210557.png>)

### Adding food to list
![Adding food to list](<screenshots/Screenshot 2024-10-22 210744.png>)

### Final list and adding date
![Final list and adding date](<screenshots/Screenshot 2024-10-22 at 21-08-08 User Diet.png>)

### Results page
![Results page](<screenshots/Screenshot 2024-10-22 at 21-08-16 User Weight Prediction.png>)

Feel free to recommend projects or improvments.
If you found this project helpful or interesting, please consider giving this repository a star ⭐! 
