import random
import time
import json

class Trainer:
    def __init__(self):
        self.data = []

    def add_data(self, meal, calories):
        self.data.append({"meal": meal, "calories": calories})

    def get_total_calories(self):
        return sum(item["calories"] for item in self.data)

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.data, f)

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            self.data = json.load(f)

    def display_meals(self):
        for item in self.data:
            print(f'Meal: {item["meal"]}, Calories: {item["calories"]}')

if __name__ == '__main__':
    trainer = Trainer()
    while True:
        action = input("Enter 'add' to add a meal, 'show' to display meals, 'exit' to quit: ")
        if action == 'add':
            meal = input("Enter meal name: ")
            calories = int(input("Enter calories: "))
            trainer.add_data(meal, calories)
            print(f'Added {meal} with {calories} calories.")
        elif action == 'show':
            trainer.display_meals()
            print(f'Total Calories: {trainer.get_total_calories()}')
        elif action == 'exit':
            break
        else:
            print('Invalid action!')
            time.sleep(1)
