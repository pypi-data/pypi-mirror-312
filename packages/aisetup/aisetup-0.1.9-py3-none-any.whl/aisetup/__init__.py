import os
import random
import base64
import csv
import folium
import requests
import pandas as pd
import ipywidgets as widgets
import matplotlib.pyplot as plt
from openai import OpenAI, AzureOpenAI, DefaultHttpxClient
from dotenv import load_dotenv
from folium.plugins import BeautifyIcon
from IPython.display import display, HTML, Audio
from datetime import datetime as dt
from matplotlib.ticker import FuncFormatter


IN_COURSERA = os.getenv("IN_COURSERA_ENVIRON")

MODEL = "gpt-4o-mini"


def authenticate(api_key=None):
    global client

    if IN_COURSERA:
        try:
            client = AzureOpenAI(
                api_key="abcdefg",
                api_version="2024-02-01",
                azure_endpoint="https://cour-external-playground.openai.azure.com/",
                http_client=DefaultHttpxClient(verify=False),
            )
        except Exception as e:
            print(f"Exception encountered. Details:\n{e}")
    else:
        try:
            load_dotenv()
            openai_api_key = os.getenv("OPENAI_API_KEY")
            client = OpenAI(api_key=openai_api_key)
        except:
            if api_key is None:
                print(
                    "Warning: An OpenAI API key is required to use AI model functions. Please provide the key by calling `authenticate(openai_api_key)` or ensure it is specified in the `.env` file as 'OPENAI_API_KEY'. If you set it in the `.env` file, call `authenticate()` or reload the package to proceed."
                )
                return
            else:
                client = OpenAI(api_key=api_key)
                return client

    return client


client = authenticate()


def print_llm_response(prompt):
    """This function takes as input a prompt, which must be a string enclosed in quotation marks,
    and passes it to OpenAI's GPT3.5 model. The function then prints the response of the model.
    """
    llm_response = get_llm_response(prompt)
    print(llm_response)


def get_llm_response(prompt):
    """This function takes as input a prompt, which must be a string enclosed in quotation marks,
    and passes it to OpenAI's GPT3.5 model. The function then saves the response of the model as
    a string.
    """
    try:
        if not isinstance(prompt, str):
            raise ValueError("Input must be a string enclosed in quotes.")
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful but terse AI assistant who gets straight to the point.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
        )
        response = completion.choices[0].message.content
        return response
    except TypeError as e:
        print("Error:", str(e))


def get_chat_completion(prompt, history):
    history_string = "\n\n".join(["\n".join(turn) for turn in history])
    prompt_with_history = f"{history_string}\n\n{prompt}"
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful but terse AI assistant who gets straight to the point.",
            },
            {"role": "user", "content": prompt_with_history},
        ],
        temperature=0.0,
    )
    response = completion.choices[0].message.content
    return response


def get_dog_age(human_age):
    """This function takes one parameter: a person's age as an integer and returns their age if
    they were a dog, which is their age divided by 7."""
    return human_age / 7


def get_goldfish_age(human_age):
    """This function takes one parameter: a person's age as an integer and returns their age if
    they were a dog, which is their age divided by 5."""
    return human_age / 5


def get_cat_age(human_age):
    if human_age <= 14:
        # For the first 14 human years, we consider the age as if it's within the first two cat years.
        cat_age = human_age / 7
    else:
        # For human ages beyond 14 years:
        cat_age = 2 + (human_age - 14) / 4
    return cat_age


def get_random_ingredient():
    """
    Returns a random ingredient from a list of 20 smoothie ingredients.

    The ingredients are a bit wacky but not gross, making for an interesting smoothie combination.

    Returns:
        str: A randomly selected smoothie ingredient.
    """
    ingredients = [
        "rainbow kale",
        "glitter berries",
        "unicorn tears",
        "coconut",
        "starlight honey",
        "lunar lemon",
        "blueberries",
        "mermaid mint",
        "dragon fruit",
        "pixie dust",
        "butterfly pea flower",
        "phoenix feather",
        "chocolate protein powder",
        "grapes",
        "hot peppers",
        "fairy floss",
        "avocado",
        "wizard's beard",
        "pineapple",
        "rosemary",
    ]

    return random.choice(ingredients)


def get_random_number(x, y):
    """
    Returns a random integer between x and y, inclusive.

    Args:
        x (int): The lower bound (inclusive) of the random number range.
        y (int): The upper bound (inclusive) of the random number range.

    Returns:
        int: A randomly generated integer between x and y, inclusive.

    """
    return random.randint(x, y)


def calculate_llm_cost(characters, price_per_1000_tokens=0.015):
    tokens = characters / 4
    cost = (tokens / 1000) * price_per_1000_tokens
    return f"${cost:.4f}"


def view_map():
    # Coordinates and flags of the cities
    itinerary = {
        "New York": {
            "coords": (40.7128, -74.0060),
            "arrival": "July-01",
            "departure": "July-08",
            "flag": "🇺🇸",
        },
        "Rio de Janeiro": {
            "coords": (-22.9068, -43.1729),
            "arrival": "July-09",
            "departure": "July-16",
            "flag": "🇧🇷",
        },
        "Cape Town": {
            "coords": (-33.9249, 18.4241),
            "arrival": "July-17",
            "departure": "July-24",
            "flag": "🇿🇦",
        },
        "Istanbul": {
            "coords": (41.0082, 28.9784),
            "arrival": "July-25",
            "departure": "August-01",
            "flag": "🇹🇷",
        },
        "Paris": {
            "coords": (48.8566, 2.3522),
            "arrival": "August-02",
            "departure": "August-09",
            "flag": "🇫🇷",
        },
        "Tokyo": {
            "coords": (35.6895, 139.6917),
            "arrival": "August-10",
            "departure": "August-17",
            "flag": "🇯🇵",
        },
        "Sydney": {
            "coords": (-33.8688, 151.2093),
            "arrival": "August-18",
            "departure": "August-25",
            "flag": "🇦🇺",
        },
    }

    # Create a map centered around the geographical center of all cities
    map_center = [20, 0]
    world_map = folium.Map(
        tiles="Cartodb Positron",
        location=map_center,
        zoom_start=2,
        max_bounds=True,
        control_scale=True,
        min_zoom=2,
        max_zoom=3,
    )

    # Add markers for each city with arrival and departure dates and flags
    for city, info in itinerary.items():
        popup_text = f"<h1>{city} {info['flag']}</h1><br><h4>Arrival: {info['arrival']}<br>Departure: {info['departure']}</h4>"
        if city == "New York":
            folium.Marker(
                location=info["coords"],
                popup=popup_text,
                icon=BeautifyIcon(
                    icon="flag", border_color="green", text_color="green"
                ),
            ).add_to(world_map)
        elif city == "Sydney":
            folium.Marker(
                location=info["coords"],
                popup=popup_text,
                icon=BeautifyIcon(icon="flag", border_color="red", text_color="red"),
            ).add_to(world_map)
        else:
            folium.Marker(
                location=info["coords"],
                popup=popup_text,
                icon=BeautifyIcon(icon="flag"),
            ).add_to(world_map)

    # Add lines between cities to represent travel path
    prev_coords = None
    for city, info in itinerary.items():
        if prev_coords:
            folium.PolyLine([prev_coords, info["coords"]], color="black").add_to(
                world_map
            )
        prev_coords = info["coords"]

    # Add custom legend
    legend_html = """
	<div style="
	position: fixed; 
	bottom: 50px; left: 50px; width: 150px; 
	border:2px solid grey; z-index:9999; font-size:18px;
	background-color:white;
	">
	&nbsp;<b>Legend</b><br>
	&nbsp;<i class="fa fa-flag" style="color:green"></i>&nbsp;Starting city<br>
	&nbsp;<i class="fa fa-flag" style="color:black"></i>&nbsp;Trip stop<br>
	&nbsp;<i class="fa fa-flag" style="color:red"></i>&nbsp;Ending city<br>
	</div>
	"""

    title_html = """
	<div style="
	display: flex;
	justify-content: center;
	align-items: center;
	width: 100%; 
	height: 50px; 
	border:0px solid grey; 
	z-index:9999; 
	font-size:30px;
	padding: 5px;
	background-color:white;
	text-align: center;
	">
	&nbsp;<b>Trip Around the World in One Short Course</b>
	</div>
	"""

    world_map.get_root().html.add_child(folium.Element(legend_html))
    world_map.get_root().html.add_child(folium.Element(title_html))

    return world_map


def download_map(
    file_path="trip_around_world_map.html", description="Click here to download the map"
):
    with open(file_path, "rb") as file:
        file_data = file.read()
        encoded_data = base64.b64encode(file_data).decode()
        href = f'<a href="data:text/html;base64,{encoded_data}" download="{file_path}">{description}</a>'
        return HTML(href)

    def read_csv_dict(csv_file_path):
        """This function takes a csv file and loads it as a dict."""

        # Initialize an empty list to store the data
        data_list = []

        # Open the CSV file
        with open(csv_file_path, mode="r") as file:
            # Create a CSV reader object
            csv_reader = csv.DictReader(file)

            # Iterate over each row in the CSV file
            for row in csv_reader:
                # Append the row to the data list
                data_list.append(row)

        # Convert the list to a dictionary
        data_dict = {i: data_list[i] for i in range(len(data_list))}
        return data_dict


def upload_txt_file():
    """
    Uploads a text file and saves it to the specified directory.

    Args:
        directory (str): The directory where the uploaded file will be saved.
        Defaults to the current working directory.
    """
    # Create the file upload widget
    upload_widget = widgets.FileUpload(
        accept=".txt",  # Accept text files only
        multiple=False,  # Do not allow multiple uploads
    )
    # Impose file size limit
    output = widgets.Output()

    # Function to handle file upload
    def handle_upload(change):
        with output:
            output.clear_output()
            # Read the file content
            content = upload_widget.value[0]["content"]
            name = "your_file.txt"
            size_in_kb = len(content) / 1024

            if size_in_kb > 3:
                print(
                    f"Your file is too large, please upload a file that doesn't exceed 3KB."
                )
                return

            # Save the file to the specified directory
            with open(name, "wb") as f:
                f.write(content)
            # Confirm the file has been saved
            print(f"File has been uploaded.")

    # Attach the file upload event to the handler function
    upload_widget.observe(handle_upload, names="value")

    display(upload_widget, output)


def list_files_in_directory(directory="."):
    """
    Lists all non-hidden files in the specified directory.

    Args:
        directory (str): The directory to list files from. Defaults to the current working directory.
    """
    try:
        files = [
            f
            for f in os.listdir(directory)
            if (not f.startswith(".") and not f.startswith("_"))
        ]
        for file in files:
            print(file)
    except Exception as e:
        print(f"An error occurred: {e}")


def display_table(data):
    df = pd.DataFrame(data)

    # Display the DataFrame as an HTML table
    display(HTML(df.to_html(index=False)))


def get_current_time():
    now = dt.now()
    return now.strftime("%m/%d/%Y, %H:%M:%S")


def celsius_to_fahrenheit(celsius):
    fahrenheit = celsius * 9 / 5 + 32
    print(f"{celsius}°C is equivalent to {fahrenheit:.2f}°F")


def beautiful_barh(labels, values):
    # Create the bar chart
    plt.figure(figsize=(9, 5))
    bars = plt.barh(labels, values, color=plt.cm.tab20.colors)

    for bar in bars:
        plt.text(
            bar.get_width() / 2,  # X coordinate
            bar.get_y() + bar.get_height() / 2,  # Y coordinate
            f"${bar.get_width() / 1e9:.1f}B",  # Text label
            ha="center",
            va="center",
            color="w",
            fontsize=10,
            fontweight="bold",
        )

    # Customizing the x-axis to display values in billions
    def billions(x, pos):
        """The two args are the value and tick position"""
        return f"${x * 1e-9:.1f}B"

    formatter = FuncFormatter(billions)
    plt.gca().xaxis.set_major_formatter(formatter)

    # Inverting the y-axis to have the highest value on top
    plt.gca().invert_yaxis()


def display_map():
    # Define the bounding box for the continental US
    us_bounds = [[24.396308, -125.0], [49.384358, -66.93457]]
    # Create the map centered on the US with limited zoom levels
    m = folium.Map(
        location=[
            37.0902,
            -95.7129,
        ],  # Center the map on the geographic center of the US
        zoom_start=5,  # Starting zoom level
        min_zoom=4,  # Minimum zoom level
        max_zoom=10,
        max_bounds=True,
        control_scale=True,  # Maximum zoom level
    )

    # Set the bounds to limit the map to the continental US
    m.fit_bounds(us_bounds)
    # Add a click event to capture the coordinates
    m.add_child(folium.LatLngPopup())
    title_html = """
	<div style="
	display: flex;
	justify-content: center;
	align-items: center;
	width: 100%; 
	height: 50px; 
	border:0px solid grey; 
	z-index:9999; 
	font-size:30px;
	padding: 5px;
	background-color:white;
	text-align: center;
	">
	&nbsp;<b>Click to view coordinates</b>
	</div>
	"""

    m.get_root().html.add_child(folium.Element(title_html))

    # Display the map
    return m


def get_forecast(lat, lon):
    url = f"https://api.weather.gov/points/{lat},{lon}"

    # Make the request to get the grid points
    response = requests.get(url)
    data = response.json()
    # Extract the forecast URL from the response
    forecast_url = data["properties"]["forecast"]

    # Make a request to the forecast URL for the selected location
    forecast_response = requests.get(forecast_url)
    forecast_data = forecast_response.json()

    daily_forecast = forecast_data["properties"]["periods"]
    return daily_forecast


def upload_audio_file():
    """
    Uploads an MP3 file, checks if it exceeds the specified size limit,
    and saves it to the specified directory. If the file is too large,
    it asks the user to upload a different file.
    """
    # Create the file upload widget
    upload_widget = widgets.FileUpload(
        accept=".mp3, .wav",  # Accept MP3 files only
        multiple=False,  # Do not allow multiple uploads
    )

    # Output widget to display messages
    output = widgets.Output()

    # Function to handle file upload
    def handle_upload(change):
        with output:
            output.clear_output()
            # Read the file content
            file_info = upload_widget.value[0]
            content = file_info["content"]
            name = file_info["name"]
            size = len(content) / (1024 * 1024)
            size_limit = 1  # Set the size limit to 1MB

            if size > size_limit:
                # If the file is too large, inform the user
                print(f"Your file '{name}' is too large ({size:.2f} MB).")
                print(f"Please upload a file that does not exceed {size_limit} MB.")
            else:
                # Save the file directly if within the size limit
                with open(name, "wb") as f:
                    f.write(content)
                print(f"The file '{name}' has been uploaded successfully.")
                display(Audio(filename=name, autoplay=False))

    # Attach the file upload event to the handler function
    upload_widget.observe(handle_upload, names="value")

    display(upload_widget, output)
