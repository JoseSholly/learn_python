from django.core.management.base import BaseCommand
from lesson.models import Lesson 

class Command(BaseCommand):
    help = 'Creates a set of lessons with real-world Python topics for each difficulty level.'

    def handle(self, *args, **options):
        # Data to populate the lessons
        lesson_data = {
            '1': [
                {
                    'topic': 'Introduction to Variables & Data Types',
                    'subtopic': 'Variables and basic data types',
                    'code_example': 'name = "Alice"\nage = 30\nis_student = True\n\nprint(f"My name is {name}, I am {age} years old.")',
                    'code_explanation': "This lesson introduces variables and the most common data types in Python: strings (text), integers (whole numbers), and booleans (True/False). Variables are used to store data, and f-strings provide a simple way to embed variable values into a string for printing.",
                },
                {
                    'topic': 'Control Flow: If/Else Statements',
                    'subtopic': 'Making decisions in code',
                    'code_example': 'age = 17\n\nif age >= 18:\n    print("You are old enough to vote.")\nelse:\n    print("You are not old enough to vote.")',
                    'code_explanation': "Control flow statements like `if`, `elif`, and `else` allow your program to make decisions and execute different blocks of code based on conditions. This example checks if a user's age is greater than or equal to 18.",
                },
                {
                    'topic': 'Data Structures: Lists and Loops',
                    'subtopic': 'Working with collections of data',
                    'code_example': 'fruits = ["apple", "banana", "cherry"]\n\nfor fruit in fruits:\n    print(f"I like {fruit}.")',
                    'code_explanation': "Lists are an ordered collection of items. The `for` loop is a powerful tool used to iterate over items in a list, performing an action on each one. This is a fundamental concept for handling collections of data.",
                },
            ],
            '2': [
                {
                    'topic': 'Object-Oriented Programming (OOP)',
                    'subtopic': 'Classes and Objects',
                    'code_example': "class Dog:\n    def __init__(self, name, breed):\n        self.name = name\n        self.breed = breed\n\n    def bark(self):\n        return f'{self.name} says woof!'\n\nmy_dog = Dog('Buddy', 'Golden Retriever')\nprint(my_dog.bark())",
                    'code_explanation': "This lesson covers the basics of OOP, including how to define a class with its attributes and methods. Objects are instances of a class. This allows you to model real-world concepts in your code, making it more organized and reusable.",
                },
                {
                    'topic': 'File Handling',
                    'subtopic': 'Reading and writing files',
                    'code_example': "with open('my_file.txt', 'w') as file:\n    file.write('Hello, world!\\n')\n    file.write('This is a new line.')\n\nwith open('my_file.txt', 'r') as file:\n    content = file.read()\n    print(content)",
                    'code_explanation': "File handling is a crucial skill for reading data from or writing data to files. The `with` statement ensures that the file is automatically closed, even if errors occur, which is a best practice for managing resources.",
                },
                {
                    'topic': 'List Comprehensions',
                    'subtopic': 'Concise list creation',
                    'code_example': "numbers = [1, 2, 3, 4, 5]\nsquared_numbers = [num ** 2 for num in numbers if num % 2 == 0]\n\nprint(squared_numbers)",
                    'code_explanation': "List comprehensions provide a compact way to create a new list from an existing one. They are more readable and often faster than traditional `for` loops for simple list creation. The example creates a list of squared numbers for all even numbers in the original list.",
                },
            ],
            '3': [
                {
                    'topic': 'Decorators',
                    'subtopic': 'Modifying functions without changing code',
                    'code_example': "import time\n\ndef timer(func):\n    def wrapper(*args, **kwargs):\n        start_time = time.time()\n        result = func(*args, **kwargs)\n        end_time = time.time()\n        print(f'{func.__name__} took {end_time - start_time:.4f} seconds.')\n        return result\n    return wrapper\n\n@timer\ndef long_running_function():\n    time.sleep(2)\n    print('Function finished.')\n\nlong_running_function()",
                    'code_explanation': "Decorators are a powerful Python feature that allows you to wrap a function with additional functionality. This example demonstrates a `timer` decorator that measures the execution time of any function it decorates, without changing the decorated function's code.",
                },
                {
                    'topic': 'Generators',
                    'subtopic': 'Creating iterators on the fly',
                    'code_example': "def fibonacci_generator(max):\n    a, b = 0, 1\n    while a < max:\n        yield a\n        a, b = b, a + b\n\nfor num in fibonacci_generator(10):\n    print(num, end=' ')\n\n# Output: 0 1 1 2 3 5 8",
                    'code_explanation': "Generators are a memory-efficient way to create iterators. Unlike a function that returns a list, a generator 'yields' values one at a time, allowing you to work with very large or even infinite sequences of data without loading them all into memory at once.",
                },
                {
                    'topic': 'Asynchronous Programming',
                    'subtopic': 'Handling I/O-bound tasks concurrently',
                    'code_example': "import asyncio\n\nasync def fetch_data(delay):\n    await asyncio.sleep(delay)\n    print(f'Fetched data after {delay} seconds.')\n    return delay\n\nasync def main():\n    task1 = asyncio.create_task(fetch_data(3))\n    task2 = asyncio.create_task(fetch_data(1))\n\n    print('Starting tasks...')\n\n    results = await asyncio.gather(task1, task2)\n    print('All tasks finished.')\n\nif __name__ == '__main__':\n    asyncio.run(main())",
                    'code_explanation': "Asynchronous programming (AsyncIO) is used to handle multiple I/O-bound tasks (like network requests or database queries) concurrently without using threads. It's ideal for making your application more responsive and scalable, as it allows other tasks to run while waiting for an operation to complete.",
                },
            ]
        }
        
        for difficulty, lessons in lesson_data.items():
            self.stdout.write(self.style.NOTICE(f'Creating lessons for difficulty: {difficulty.upper()}...'))
            
            for lesson_info in lessons:
                lesson = Lesson.objects.create(
                    topic=lesson_info['topic'],
                    subtopic=lesson_info['subtopic'],
                    code_example=lesson_info['code_example'],
                    code_explanation=lesson_info['code_explanation'],
                    difficulty_level=difficulty
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created lesson: {lesson}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('\nAll lessons have been created.')
        )