import math
from datetime import datetime, timedelta

# Function to apply exponential scaling to a list of numbers
def exponential_scaling(values, alpha=0.9):
    scaled_values = []
    for i, value in enumerate(reversed(values)):
        weight = alpha ** i  # Exponential weight decreases as i increases
        scaled_values.append(weight * value)
    return sum(scaled_values) / sum(alpha ** i for i in range(len(values)))  # Weighted average

# Function to predict future weight changes based on past user data
def predict_weight_change(user_data, alpha=0.9):
    # Sort data by date and consider only the last 30 days (or fewer if less data is available)
    user_data_sorted = sorted(user_data, key=lambda x: x['date'], reverse=True)[:30]
    
    if not user_data_sorted:
        raise ValueError("Not enough data to make a prediction.")
    
    # Extract diff_calories and weight for the last 30 days
    diff_calories = [entry['diff_calories'] for entry in user_data_sorted]
    latest_weight = user_data_sorted[0]['weight']  # Current weight is the most recent weight
    last_date_str = str(user_data_sorted[0]['date'])  # Get the most recent date (in yyyymmdd format)
    last_date = datetime.strptime(last_date_str, '%Y%m%d')  # Convert it to datetime object
    
    # Apply exponential scaling to diff_calories
    scaled_avg_calories = exponential_scaling(diff_calories, alpha)
    
    # Predict weight change for the next 30 days
    # 1000 grams = 7700 calories, so weight change = (average daily net calories / 7700) * 1000
    weight_change_per_day = (scaled_avg_calories / 7700) * 1000  # in grams
    
    # Project weight over the next 30 days
    future_weights = []
    current_weight = latest_weight
    for day in range(1, 31):
        current_weight += weight_change_per_day  # Add predicted daily weight change
        future_date = last_date + timedelta(days=day)  # Increment the date by 1 day
        future_weights.append({
            "date": future_date.strftime('%Y%m%d'),  # Store the date in 'yyyymmdd' format
            "predicted_weight": math.ceil(current_weight)  # Round up weight to nearest gram
        })
    
    # Return the list of dictionaries, each with 'date' and 'predicted_weight'
    return future_weights

# Example usage of predict_weight_change
if __name__ == '__main__':
    # Example data input from get_user_times()
    example_data = [
        {'user_id': 1, 'time_id': 1, 'date': 20241001, 'diff_calories': -500.0, 'weight': 70000},
        {'user_id': 1, 'time_id': 2, 'date': 20241002, 'diff_calories': -400.0, 'weight': 69950},
        {'user_id': 1, 'time_id': 3, 'date': 20241003, 'diff_calories': 100.0, 'weight': 69900},
        {'user_id': 1, 'time_id': 4, 'date': 20241004, 'diff_calories': 200.0, 'weight': 69880},
        {'user_id': 1, 'time_id': 5, 'date': 20241005, 'diff_calories': 150.0, 'weight': 69890},
        {'user_id': 1, 'time_id': 6, 'date': 20241006, 'diff_calories': -100.0, 'weight': 69900},
        {'user_id': 1, 'time_id': 7, 'date': 20241007, 'diff_calories': 0.0, 'weight': 69900},
        {'user_id': 1, 'time_id': 8, 'date': 20241008, 'diff_calories': -300.0, 'weight': 69870},
        {'user_id': 1, 'time_id': 9, 'date': 20241009, 'diff_calories': -200.0, 'weight': 69860},
        {'user_id': 1, 'time_id': 10, 'date': 20241010, 'diff_calories': -100.0, 'weight': 69850},
    ]
    
    # Call the prediction function
    prediction = predict_weight_change(example_data)
    
    # Print the future predicted weights
    for entry in prediction:
        print(f"Date: {entry['date']}, Predicted Weight: {entry['predicted_weight']}g")
