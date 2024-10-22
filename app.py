from flask import Flask, render_template, request, redirect, url_for
# Importing necessary external functions
from database import get_all_users, add_user, get_user_times, add_time
from prediction import predict_weight_change
from prompt import get_calories_from_llm

app = Flask(__name__)

# Route to display the list of users on the index page
@app.route('/')
def index():
    users = get_all_users()  # Fetch all users
    return render_template('index.html', users=users)  # Render index.html with users

# Route to create a new user using the form data from index.html
@app.route('/create_user', methods=['POST'])
def create_user():
    try:
        # Get form data
        name = request.form.get('name')
        age = int(request.form.get('age'))  # Convert age to integer
        height = float(request.form.get('height'))  # Convert height to float
        weight = float(request.form.get('weight')) * 1000  # Convert weight to grams
        gender = request.form.get('gender')
        bmr = int(request.form.get('bmr'))  # Convert BMR to integer

        # Validate required fields
        if not name or not age or not height or not weight or not gender or not bmr:
            raise ValueError("Missing required fields")
        
        # Add new user to the database
        user_id = add_user(name=name, bmr=bmr)

        # Redirect to the homepage to refresh the user list
        return redirect(url_for('index'))

    except ValueError as e:
        # Handle any validation or conversion errors
        return f"Error: {str(e)}", 400

# Route to display the diet entry page for a specific user
@app.route('/diet/<int:user_id>')
def diet(user_id):
    return render_template('diet.html', user_id=user_id)  # Render diet page with user_id

# Route to fetch the calories of a given food using an LLM function
@app.route('/get_calories/food', methods=['POST'])
def get_calories():
    food_item = request.form.get('food')  # Get the food name from the form
    calories = get_calories_from_llm(food_item)  # Use the LLM to get calories of the food
    return {'calories': calories}  # Return the calories as a JSON response

# Route to add a new diet entry for a specific user
@app.route('/add_diet', methods=['POST'])
def add_diet():
    try:
        # Get form data
        date = request.form.get('date')
        calories = float(request.form.get('calories'))  # Get total calories from form
        user_id = int(request.form.get('user_id'))  # Convert user_id to integer
        weight = float(request.form.get('weight'))  # Convert weight to float

        # Fetch user details to get BMR
        users = get_all_users()
        user = next((u for u in users if u['id'] == user_id), None)
        if not user:
            raise ValueError("User not found")

        bmr = user['bmr']  # Get BMR for the user

        # Calculate diff_calories as total calories minus BMR
        diff_calories = calories - bmr

        # Add the diet entry into the database with the calculated diff_calories
        add_time(user_id, date, diff_calories, weight)  # Use user's current weight

        # Redirect to the user's results page after adding the diet entry
        return redirect(url_for('show_results', user_id=user_id))
    
    except ValueError as e:
        return f"Error: {str(e)}", 400

# Route to show the prediction results for a specific user

@app.route('/results/<int:user_id>')
def show_results(user_id):
    # Fetch historical data (last 30 days of user entries)
    data = get_user_times(user_id)

    # Make weight predictions for the next 30 days
    prediction = predict_weight_change(data)
    
    # Prepare historical data for template
    historical_data = [
        {"date": str(entry['date']), "weight": entry['weight']} for entry in data[-30:]
    ]
    
    # Predicted data is already a list of dictionaries, no need to split strings
    predicted_data = [
        {"date": entry['date'], "weight": entry['predicted_weight']} for entry in prediction
    ]

    # Render the results page
    return render_template('results.html', user_id=user_id, historical_data=historical_data, predicted_data=predicted_data)

if __name__ == '__main__':
    app.run(debug=True)
