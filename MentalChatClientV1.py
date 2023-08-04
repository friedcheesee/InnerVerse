import tkinter as tk
from tkinter import *
import openai
import requests
import os
import tkinter as tk
import webbrowser

def send_message():
    message = entry.get()
    if message.strip() != "":
        chat_box.insert(tk.END, "User: " + message + "\n", "user")
        response = generate_response(message,v1.get())
        print(v1.get())
        print(response['data']['Answer'])
        print(response['data']['Followup'])
        followupbox.delete(0, tk.END)
        entry.delete(0, tk.END)
        chat_box.insert(tk.END, "BOT: " + str(response['data']['Answer']) + "\n","ai")
        followupbox.insert(tk.END, "Followup Question: " + str(response['data']['Followup']) + "\n")    
        
        if(str(response['data']['Source'])!=""):
            Citation_Text.insert(INSERT,response['data']['Source'][0]['Citation'], ("link", response['data']['Source'][0]['Citation']))
            Citation_Text.tag_config("link", foreground="blue", underline=1)
            Citation_Text.tag_bind("link", "<Button-1>", open_link)

            Citation_Text.insert(tk.END,"\n")
            Citation_Text.insert(INSERT,response['data']['Source'][0]['Text'].strip())
            Citation_Text.tag_config("link", foreground="blue", underline=1)
            Citation_Text.tag_bind("link", "<Button-1>", open_link)
            Citation_Text.insert(tk.END,"\n")
            Citation_Text.insert(INSERT,response['data']['Source'][1]['Citation'], ("link", response['data']['Source'][1]['Citation']))
            Citation_Text.insert(tk.END,"\n")
            Citation_Text.insert(INSERT,response['data']['Source'][1]['Text'].strip()) 
            Citation_Text.insert(tk.END,"\n")        


        # Add to History object yet to ve implemented.
        

# Function to generate a response using ChatGPT model
def generate_response(message, value):

    new_data = {
        "Question": message,
        "Chat_History" : [],
        "Page_Context": "Portfolio",
        "GPT_Val" : value
    }

    # The API endpoint
    url_post = "http://localhost:8088/askquery"

    # A POST request to the API
    post_response = requests.post(url_post, json=new_data)

    # Print the response
    response_json = post_response.json()
    return response_json

    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message,
        max_tokens=50,
        temperature=0.7
    )
    return response.choices[0].text.strip()
    """
# Create the main window

from tkinter import ttk



window = tk.Tk()
window.title("Mental Health Chat Bot")
window.geometry()
s= ttk.Style() 
s.theme_use("winnative")



# Create a chat box
chat_box = tk.Text(window, wrap = WORD, width=80, height=35,bg="#FAFAEB")
chat_box.grid(column=0, row=0, padx=2, pady=2, columnspan=10, rowspan= 10)


Citation_Text = tk.Text(window,wrap=WORD, width=80, height=35,bg="#CDCDC0")
Citation_Text.grid(column=10, row=0, padx=2, pady=2,columnspan=10, rowspan=10)



#give different colours for the messages.
chat_box.tag_configure("user", foreground="#000000", justify="right")
chat_box.tag_configure("ai", foreground="#4B4B00", justify = "left")

# Create an entry field for user input
entry = tk.Entry(window, width=100)
entry.grid(column=3, row=67, padx=10, pady=10)

followuplabel  = tk.Label(window,text = "Would like to consider this  Question?") 
followuplabel.grid(row = 68, column = 3)
   

followupbox = tk.Entry(window,width=100, bg="grey")
followupbox.grid(column=3, row=70, padx=10, pady=10)


v1 = tk.IntVar()
C1 = tk.Checkbutton(window, text = "Search Trusted Sources", variable = v1)
#C1.place(x=10, y=250)
C1.grid(column= 15, row=67, padx=10, pady=10)
# Create a button to send the message
button = tk.Button(window, text="Send", command=send_message)
button.grid(column=14, row=67, padx=2, pady=2)

flag_button = tk.Button(window, text="Flag Content", command=send_message)
flag_button.grid(column=17, row=67, padx=5, pady=5)

def open_link(link):
    print(f"Opening link: {link}")
    print(link)
    os.startfile(link)


# Start the GUI main loop
window.mainloop()
