# Virtual Assistant Application

A Python-based virtual assistant that uses voice recognition and text-to-speech to perform various tasks, including setting reminders, timers, alarms, getting weather updates, and performing web searches. The assistant features a simple graphical user interface (GUI) for easier interaction.

## Features

- **Voice Commands**: Set reminders, timers, alarms, fetch weather data, and search the web.
- **Text-to-Speech**: Provides responses using pyttsx3 for speech output.
- **Weather Information**: Fetches current weather data using OpenWeather API.
- **Web Search**: Initiates Google search based on user queries.
- **Timers and Alarms**: Set countdown timers and alarms with audio alerts.
- **Graphical User Interface (GUI)**: Simple interface with input fields and buttons for voice commands.

## Technologies Used

- **Python**: The core language for the application.
- **SpeechRecognition**: For converting speech to text.
- **pyttsx3**: For converting text to speech.
- **Pygame**: For playing alarm sounds.
- **Requests**: To fetch weather data from OpenWeather API.
- **Tkinter**: For the graphical user interface.
- **Pillow**: To manipulate images for the GUI.

## Requirements

Before you begin, ensure you have the following installed:

- Python 3.x
- pip (Python package installer)

### Dependencies

Install the required dependencies using the following command:

```bash
pip install speechrecognition pyttsx3 pygame requests tkinter pillow
