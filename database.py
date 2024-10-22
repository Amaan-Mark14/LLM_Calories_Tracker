from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship

# Define the SQLite database URI
DATABASE_URI = 'sqlite:///calories.db'

# Create the engine, allowing the option to turn echo (SQL logs) on/off
def get_engine(echo=False):
    return create_engine(DATABASE_URI, echo=echo)

engine = get_engine(echo=False)  # Change echo to True to enable logging

# Base class for model declarations (modern style)
class Base(DeclarativeBase):
    pass

# Define the Users model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    bmr = Column(Integer, nullable=False)
    times = relationship('Time', backref='user', cascade="all, delete-orphan", lazy=True)

# Define the Time model
class Time(Base):
    __tablename__ = 'time'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Integer, nullable=False)  # date in yyyymmdd format
    diff_calories = Column(Float, nullable=False)  # diff_calories as positive/negative float
    weight = Column(Integer, nullable=False)  # weight in grams
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

# Create all tables in the database
Base.metadata.create_all(engine)

# Create a session factory bound to the engine
Session = sessionmaker(bind=engine)

# Add a new user
def add_user(name, bmr):
    with Session() as session:
        new_user = User(name=name, bmr=bmr)
        session.add(new_user)
        session.commit()
        return new_user.id

# Add or update a time entry for a specific user
def add_time(user_id, date, diff_calories, weight):
    with Session() as session:
        user = session.get(User, user_id)
        if not user:
            raise ValueError("User not found")
        
        # Check if a time entry with the same date already exists
        existing_time = session.query(Time).filter_by(user_id=user_id, date=date).first()

        # If an existing time entry is found, delete it
        if existing_time:
            session.delete(existing_time)
            session.commit()  # Commit the deletion before adding a new one
        
        # Add the new time entry
        new_time = Time(date=date, diff_calories=diff_calories, weight=weight, user_id=user_id)
        session.add(new_time)
        session.commit()
        return new_time.id

# Retrieve all users
def get_all_users():
    with Session() as session:
        users = session.query(User).all()
        return [{"id": user.id, "name": user.name, "bmr": user.bmr} for user in users]

# Retrieve all time entries for a specific user
def get_user_times(user_id):
    with Session() as session:
        user = session.get(User, user_id)
        if not user:
            raise ValueError("User not found")

        times = session.query(Time).filter_by(user_id=user_id).all()
        return [{"user_id": time.user_id, "time_id": time.id, "date": time.date, "diff_calories": time.diff_calories, "weight": time.weight} for time in times]

# Delete a user and their associated time entries
def delete_user(user_id):
    with Session() as session:
        user = session.get(User, user_id)
        if not user:
            raise ValueError("User not found")
        
        session.delete(user)
        session.commit()

# Delete a specific time entry
def delete_time(time_id):
    with Session() as session:
        time_entry = session.get(Time, time_id)
        if not time_entry:
            raise ValueError("Time entry not found")
        
        session.delete(time_entry)
        session.commit()

# Example usage
if __name__ == '__main__':
    # Example adding a user and a time entry
    # add_user('John Doe', 1800)
    # i = 20241017
    # y = 1
    # while i < 20241025:
    #     i += 1 
    #     y += 1
    #     add_time(1, i, -300, 70000-(y*50))
    print(get_user_times(1))
