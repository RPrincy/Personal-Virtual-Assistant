# importing all the required libraries
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests
import json
import tkinter as tk
from tkinter import ttk, PhotoImage
import threading
import time
import pygame
from PIL import Image, ImageTk

# creating class constructor to handle the collection of functions
class VirtualAssistant:
    
    # initializing the text to speech engine
    def __init__(self):
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self.reminders = []
        self.alarms = []
        self.timers = []
        pygame.mixer.init()
    
    # converting text to speech and repeating it
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    #listening to user input and converting that into text
    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                text = self.recognizer.recognize_google(audio)
                print(f"Recognized: {text}")
                return text.lower()
            except sr.UnknownValueError:
                print("Could not understand audio")
                return ""
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                return ""
            except Exception as e:
                print(f"An error occurred: {e}")
                return ""
            
    ## Open a Google search for the provided query in the default web browser
    def search_web(self, query):
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(search_url)
        self.speak(f"I've opened a web search for {query}")
            
    def process_command(self, command):
        if "search" in command:
            parts = command.split("search for")
            if len(parts) > 1:
                query = parts[1].strip()
                self.search_web(query)
            else:
                self.speak("Please specify what to search for.")
        else:
            self.speak("I'm sorry, I didn't understand that command")
            
class GUI:
    def __init__(self, assistant):
        # Initialize the GUI with the virtual assistant object
        self.assistant = assistant
        self.root = tk.Tk()
        self.root.title("Virtual Assistant")        

        # Load and set a semi-transparent background image
        self.background_image = Image.open("C:/Users/Princy/Downloads/voice1.png").convert("RGBA")
        width, height = self.background_image.size
        alpha = 200 
        self.background_image.putalpha(alpha)

        # Convert the image for Tkinter compatibility and add it to a canvas
        self.background_image_tk = ImageTk.PhotoImage(self.background_image)
        self.canvas = tk.Canvas(self.root, width=width, height=height)
        self.canvas.place(relwidth=1, relheight=1)
        self.canvas.create_image(0, 0, image=self.background_image_tk, anchor="nw")

        # Add a status label at the top of the window
        self.status_label = ttk.Label(self.root, text="Press 'Mic' to start/stop listening", background="lightblue", font=("Helvetica", 12))
        self.status_label.pack(pady=20)
        
        # Add a microphone button with an image to start/stop listening
        self.microphone_photo = PhotoImage(file="C:/Users/Princy/Downloads/imagee.png") 
        self.mic_button = ttk.Button(self.root, image=self.microphone_photo, command=self.toggle_listening)
        self.mic_button.pack(pady=10)
        
        # Add an entry field for text commands
        self.command_entry = ttk.Entry(self.root, width=50)
        self.command_entry.insert(0, "Enter command here (e.g. weather, reminder)")
        self.command_entry.bind("<FocusIn>", self.clear_placeholder)
        self.command_entry.bind("<FocusOut>", self.add_placeholder)
        self.command_entry.pack(pady=10)

        # Add a submit button to process the entered command
        self.submit_button = ttk.Button(self.root, text="Submit", command=self.submit_command, style="TButton")
        self.submit_button.pack(pady=10)

        # Add a text widget to display output or assistant responses
        self.output_text = tk.Text(self.root, height=10, width=50)
        self.output_text.pack(pady=10)

        style = ttk.Style()
        style.configure("TButton",
                        background="lightgreen",
                        foreground="black",
                        font=("Helvetica", 14, "bold"),
                        padding=10)
        style.map("TButton",
                  background=[("active", "lightgreen"), ("pressed", "darkgreen")])

    def submit_command(self):
        command = self.command_entry.get()
        if command:
            threading.Thread(target=self.assistant.process_command, args=(command,)).start()
            self.output_text.insert(tk.END, f"You said: {command}\n")
            self.command_entry.delete(0, tk.END)

    def toggle_listening(self):
        if not self.assistant.is_listening:
            threading.Thread(target=self.start_listening).start()
        else:
            print("Stopping listening...")
            self.assistant.is_listening = False

    def start_listening(self):
        print("Starting listening...")
        self.assistant.is_listening = True
        while self.assistant.is_listening:
            command = self.assistant.listen()
            if command:
                if "stop" in command:
                    break
                else:
                    print(f"Processing command: {command}")
                    self.output_text.insert(tk.END, f"You said: {command}\n")
                    threading.Thread(target=self.assistant.process_command, args=(command,)).start()

    def clear_placeholder(self, event):
        if self.command_entry.get() == "Enter command here (e.g. weather, reminder)":
            self.command_entry.delete(0, tk.END)

    def add_placeholder(self, event):
        if not self.command_entry.get():
            self.command_entry.insert(0, "Enter command here (e.g. weather, reminder)")

    def run(self):
        self.root.mainloop()

def main():
    assistant = VirtualAssistant()
    gui = GUI(assistant)
    gui.run()

if __name__ == "__main__":
    main()