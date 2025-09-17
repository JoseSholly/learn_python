from django.core.management.base import BaseCommand
from lesson.models import Lesson 

class Command(BaseCommand):
    help = 'Creates or updates a set of lessons with friendly and easily translatable content.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--overwrite',
            action='store_true',
            help='Overwrite existing lessons with the same topic and subtopic.',
        )

    def handle(self, *args, **options):
        # Data for all difficulty levels
        lesson_data = {
            '1': [
                {
                    'topic': 'Introduction to Variables & Data Types',
                    'subtopic': 'Variables and basic data types',
                    'code_example': 'name = "Alice"\nage = 30\nis_student = True\n\nprint(f"My name is {name}, I am {age} years old.")',
                    'code_explanation': "Variables are used to store data in a program. Each variable has a name and a value. This lesson introduces three basic data types. A string is used for text, such as 'Alice', which can be any word or sentence. An integer is for whole numbers, like 30, used for counting or calculations. A boolean is for True or False values, often used for decisions. The f-string is a special way to combine variables into a sentence, making it easy to display information. In this example, we create a variable 'name' and set it to 'Alice'. We set 'age' to 30 and 'is_student' to True. Then, we use an f-string to print a sentence that includes the values of 'name' and 'age'. This helps beginners understand how to store and display data clearly. Example: Assign 'Alice' to 'name', 30 to 'age', and print a sentence with both."
                },
                {
                    'topic': 'Control Flow: If/Else Statements',
                    'subtopic': 'Making decisions in code',
                    'code_example': 'age = 17\n\nif age >= 18:\n    print("You are old enough to vote.")\nelse:\n    print("You are not old enough to vote.")',
                    'code_explanation': "This lesson explains how to make decisions in a program using 'if' and 'else' statements. The 'if' statement checks a condition, like whether a number meets a requirement. If the condition is true, the program runs the code inside the 'if' block. If the condition is false, the program runs the code inside the 'else' block. In this example, we check if a person’s age is 18 or more to decide if they can vote. We set the variable 'age' to 17. The condition 'age >= 18' is false, so the program prints 'You are not old enough to vote.' If 'age' were 18 or more, it would print 'You are old enough to vote.' This structure helps programs make decisions based on data. Example: Set 'age' to 17, check if it is at least 18, and print the correct message."
                },
                {
                    'topic': 'Data Structures: Lists and Loops',
                    'subtopic': 'Working with collections of data',
                    'code_example': 'fruits = ["apple", "banana", "cherry"]\n\nfor fruit in fruits:\n    print(f"I like {fruit}.")',
                    'code_explanation': "Lists are used to store multiple items in one variable, like a collection of names or numbers. A 'for' loop goes through each item in a list and runs code for each one. This lesson shows how to use a list and a loop together. In the example, we create a list called 'fruits' containing 'apple', 'banana', and 'cherry'. The 'for' loop takes each fruit one by one and prints a sentence saying 'I like' followed by the fruit’s name. This is useful for working with groups of data, such as processing multiple items in a program. The loop ensures every item is handled in order. Example: Create a list with 'apple', 'banana', and 'cherry', use a loop to go through each item, and print 'I like apple', 'I like banana', and 'I like cherry' for each fruit."
                },
            ],
            '2': [
                {
                    'topic': 'Object-Oriented Programming (OOP)',
                    'subtopic': 'Classes and Objects',
                    'code_example': "class Dog:\n    def __init__(self, name, breed):\n        self.name = name\n        self.breed = breed\n\n    def bark(self):\n        return f'{self.name} says woof!'\n\nmy_dog = Dog('Buddy', 'Golden Retriever')\nprint(my_dog.bark())",
                    'code_explanation': "Object-Oriented Programming organizes code using classes and objects. A class is a blueprint that defines what an object can do and what data it holds. An object is an instance of a class, like a real item made from the blueprint. In this lesson, we create a 'Dog' class that defines a dog’s name and breed as data, and an action called 'bark'. The '__init__' function sets up the object with a name and breed when it is created. The 'bark' function makes the dog say its name followed by 'woof!'. In the example, we create a dog object named 'Buddy' with the breed 'Golden Retriever'. We then call the 'bark' action to print 'Buddy says woof!'. This approach helps organize code for complex programs. Example: Create a Dog class, make a dog named 'Buddy', and print its bark message."
                },
                {
                    'topic': 'File Handling',
                    'subtopic': 'Reading and writing files',
                    'code_example': "with open('my_file.txt', 'w') as file:\n    file.write('Hello, world!\\n')\n    file.write('This is a new line.')\n\nwith open('my_file.txt', 'r') as file:\n    content = file.read()\n    print(content)",
                    'code_explanation': "File handling allows a program to read from or write to files on a computer. The 'with' statement is a safe way to open a file because it automatically closes the file when done. The 'w' mode is used to write text to a file, creating or overwriting it. The 'r' mode is used to read text from a file. In this example, we first open a file called 'my_file.txt' in write mode and write two lines: 'Hello, world!' and 'This is a new line.' Then, we open the same file in read mode, read all its content into a variable called 'content', and print it. This shows how to save and retrieve data from files. Example: Write 'Hello, world!' and another line to a file, then read the file and print its content."
                },
                {
                    'topic': 'List Comprehensions',
                    'subtopic': 'Concise list creation',
                    'code_example': "numbers = [1, 2, 3, 4, 5]\nsquared_numbers = [num ** 2 for num in numbers if num % 2 == 0]\n\nprint(squared_numbers)",
                    'code_explanation': "List comprehensions are a short way to create new lists from existing ones in a single line of code. They are faster and more concise than using a regular 'for' loop. In this lesson, we start with a list of numbers [1, 2, 3, 4, 5]. The list comprehension checks each number to see if it is even (using 'num % 2 == 0'). If a number is even, it squares the number (using 'num ** 2') and adds it to a new list. In this example, the even numbers are 2 and 4, so their squares, 4 and 16, are included in the new list. The result is [4, 16]. This method is efficient for transforming lists. Example: Start with numbers [1, 2, 3, 4, 5], select even numbers 2 and 4, square them to get [4, 16], and print the new list."
                },
            ],
            '3': [
                {
                    'topic': 'Decorators',
                    'subtopic': 'Modifying functions without changing code',
                    'code_example': "import time\n\ndef timer(func):\n    def wrapper(*args, **kwargs):\n        start_time = time.time()\n        result = func(*args, **kwargs)\n        end_time = time.time()\n        print(f'{func.__name__} took {end_time - start_time:.4f} seconds.')\n        return result\n    return wrapper\n\n@timer\ndef long_running_function():\n    time.sleep(2)\n    print('Function finished.')\n\nlong_running_function()",
                    'code_explanation': "Decorators are special functions that modify how another function works without changing its code. They are applied using the '@' symbol before a function. In this lesson, we create a 'timer' decorator that measures how long a function takes to run. The decorator records the start time, runs the function, records the end time, and prints the difference. In the example, we apply the 'timer' decorator to a function called 'long_running_function' that waits for 2 seconds and then prints a message. When we run the function, the decorator prints how many seconds it took, like 'long_running_function took 2.0023 seconds.' This is useful for tracking performance. Example: Create a timer decorator, apply it to a function that waits 2 seconds, run the function, and print its execution time."
                },
                {
                    'topic': 'Generators',
                    'subtopic': 'Creating iterators on the fly',
                    'code_example': "def fibonacci_generator(max):\n    a, b = 0, 1\n    while a < max:\n        yield a\n        a, b = b, a + b\n\nfor num in fibonacci_generator(10):\n    print(num, end=' ')\n\n# Output: 0 1 1 2 3 5 8",
                    'code_explanation': "Generators are functions that produce values one at a time, using 'yield' to pause and resume execution. This saves memory because they do not store all values at once. In this lesson, we create a generator for the Fibonacci sequence, where each number is the sum of the two previous ones. The generator starts with 0 and 1, then yields each number until it reaches a maximum value. In the example, we set the maximum to 10, so the generator produces 0, 1, 1, 2, 3, 5, 8. A 'for' loop prints each number. This is efficient for large sequences. Example: Create a generator for Fibonacci numbers less than 10, yield each number one by one, and print them as 0 1 1 2 3 5 8."
                },
                {
                    'topic': 'Asynchronous Programming',
                    'subtopic': 'Handling tasks at the same time',
                    'code_example': "import asyncio\n\nasync def fetch_data(delay):\n    await asyncio.sleep(delay)\n    print(f'Fetched data after {delay} seconds.')\n    return delay\n\nasync def main():\n    task1 = asyncio.create_task(fetch_data(3))\n    task2 = asyncio.create_task(fetch_data(1))\n\n    print('Starting tasks...')\n\n    results = await asyncio.gather(task1, task2)\n    print('All tasks finished.')\n\nif __name__ == '__main__':\n    asyncio.run(main())",
                    'code_explanation': "Asynchronous programming allows multiple tasks to run at the same time, making programs faster. It is useful when tasks need to wait, like for data from a network. In this lesson, we use 'async' and 'await' to manage tasks. The 'fetch_data' function waits for a given number of seconds and prints a message. We create two tasks: one waits 3 seconds, and another waits 1 second. Using 'asyncio.create_task', we start both tasks together. The 'asyncio.gather' function waits for both tasks to finish and collects their results. The program prints 'Starting tasks...', runs the tasks, and prints 'All tasks finished.' when done. This shows how to handle multiple waiting tasks efficiently. Example: Create two tasks, one waiting 3 seconds and one waiting 1 second, run them together, and print their results."
                },
            ]
        }
        
        overwrite = options['overwrite']
        created_count = 0
        updated_count = 0

        for difficulty, lessons in lesson_data.items():
            self.stdout.write(self.style.NOTICE(f'Processing {Lesson.DIFFICULTY_CHOICES[int(difficulty) - 1][1]} lessons...'))
            
            for lesson_info in lessons:
                try:
                    # Try to get the lesson first
                    lesson_obj = Lesson.objects.get(
                        topic=lesson_info['topic'],
                        subtopic=lesson_info['subtopic']
                    )
                    
                    if overwrite:
                        # Update the existing lesson if overwrite flag is set
                        for key, value in lesson_info.items():
                            setattr(lesson_obj, key, value)
                        lesson_obj.save()
                        updated_count += 1
                        self.stdout.write(self.style.SUCCESS(f'Updated lesson: {lesson_obj}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Skipping existing lesson: {lesson_obj}'))

                except Lesson.DoesNotExist:
                    # Create a new lesson if it does not exist
                    Lesson.objects.create(
                        topic=lesson_info['topic'],
                        subtopic=lesson_info['subtopic'],
                        code_example=lesson_info['code_example'],
                        code_explanation=lesson_info['code_explanation'],
                        difficulty_level=difficulty
                    )
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Created new lesson: {lesson_info["topic"]} - {lesson_info["subtopic"]}'))
        
        self.stdout.write(
            self.style.SUCCESS('\nFinished populating lessons.')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Summary: {created_count} lessons created, {updated_count} lessons updated.')
        )