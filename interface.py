import streamlit as st
import time
import requests
import voicetotext
from datetime import datetime
import pytz

# Add custom CSS for improved UI
def add_custom_css():
    st.markdown("""
        <style>
            body {
            background: linear-gradient(135deg, #f2f2f2 0%, #cce0ff 100%);
            font-family: 'Poppins', sans-serif;
            color: #333;
        }
        .stApp {
            padding: 0;
        }
        .css-1v3fvcr {
            padding-top: 0 !important;
        }
        .chat-interface {
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            animation: slide-in 0.5s ease-out;
        }
        @keyframes slide-in {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .message-container {
            display: flex;
            align-items: flex-start;
            margin-bottom: 10px;
        }
        .message-user {
            background-color: #007bff;
            color: white;
            border-radius: 20px;
            padding: 10px;
            max-width: 60%;
            animation: fade-in 0.5s ease-in-out;
        }
        .message-assistant {
            background-color: #f2f2f2;
            color: #333;
            border-radius: 20px;
            padding: 10px;
            max-width: 60%;
            animation: fade-in 0.5s ease-in-out;
        }
        @keyframes fade-in {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .follow-up {
            font-size: 18px;
            font-weight: 600;
            margin-top: 20px;
            animation: followup-appear 1s ease-in-out;
        }
        @keyframes followup-appear {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
        .personalized-greeting {
            font-size: 24px;
            font-weight: bold;
            animation: greeting-slide 1s ease-in-out;
            margin-top: 20px;
            margin-bottom: 20px;
        }
        @keyframes greeting-slide {
            from { transform: translateX(-50px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        .stRadio > div {
            display: flex;
            justify-content: space-between;
        }
        .stButton > button {
            background: linear-gradient(135deg, #4B0082, #2C3E50); /* Same gradient as the assistant bubble */
            color: white;
            border-radius: 12px;
            padding: 10px 20px;
            transition: all 0.3s ease;
            border: none; /* Remove border for a cleaner look */
        }
        .stButton > button:hover {
            background: linear-gradient(135deg, #3B006B, #1F2A35); /* Darker gradient for hover effect */
        }
        /* InnerVerse Title aligned to the left */
        .innerverse-title {
            text-align: left;
            font-family: 'Poppins', sans-serif;
            font-weight: bold;
            font-size: 40px;
            background: linear-gradient(135deg, #6A82FB, #FC5C7D);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 2px;
            margin-bottom: 10px; /* Closer to tagline */
            margin-left: 0px; /* Aligned to the left */
            animation: title-slide 1s ease-out;
        }
        /* Tagline immediately below the title with minimal space */
        .innerverse-tagline {
            text-align: left;
            font-family: 'Poppins', sans-serif;
            font-size: 24px;  /* Slightly smaller size for balance */
            background: linear-gradient(135deg, #6A82FB, #FC5C7D);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 500;
            color: white;
            margin-top: 0px;   /* No extra space above tagline */
            margin-left: 0px;  /* Aligned to the left */
            animation: tagline-fade 1s ease-in-out;
        }
        /* Animation for the title and tagline */
        @keyframes title-slide {
            from { transform: translateY(-50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        @keyframes tagline-fade {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        /* Style for the name in personalized greeting */
        .personalized-name {
            background: linear-gradient(135deg, #6A82FB, #FC5C7D);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
        }
        /* The greeting text should be white except the name */
        .personalized-greeting {
            font-size: 24px;
            font-family: 'Poppins', sans-serif;
            color: white; /* White text */
            margin-top: 20px;
            animation: greeting-slide 1s ease-in-out;
        }
        /* Animation for the greeting */
        @keyframes greeting-slide {
            from { transform: translateX(-50px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        /* General chat styling */
        .chat-container {
            background-color: #000; /* Black background */
            padding: 20px;
            height: 500px;
            overflow-y: auto;  /* Scrollable if content exceeds */
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        .chat-bubble {
            background: white;  /* User chat bubble color */
            border: none;  /* Remove border */
            border-radius: 20px;  /* Rounded corners */
            padding: 10px 15px;  /* Padding for user bubble */
            margin: 5px;  /* Margin for spacing */
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);  /* Shadow effect */
            color: black;  /* Text color for user */
            max-width: 80%;  /* Max width for user bubble */
            position: relative;  /* To position the triangle */
            word-wrap: break-word;  /* Ensure text wraps */
        }
        .chat-bubble.assistant {
            background: linear-gradient(135deg, #4B0082, #2C3E50);  /* Darker gradient for assistant chat bubble */
            border: none;  /* Remove border */
            border-radius: 20px;  /* Rounded corners */
            padding: 10px 15px;  /* Padding for assistant bubble */
            margin: 5px;  /* Margin for spacing */
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);  /* Shadow effect */
            color: white;  /* Text color for assistant */
            max-width: 80%;  /* Max width for assistant bubble */
            position: relative;  /* To position the triangle */
            word-wrap: break-word;  /* Ensure text wraps */
        }
        .chat-bubble:after {
            border-top: 10px solid white;  /* Color of the user bubble */
            left: -10px;  /* Adjust to point towards user */
            top: 100%;  /* Position below the bubble */
        }
        .chat-bubble.assistant:after {
            border-top: 10px solid #4B0082;  /* Color of the assistant bubble */
            right: -10px;  /* Adjust to point towards assistant */
            top: 100%;  /* Position below the bubble */
        }
        .follow-up {
            margin-top: 10px;  /* Space above follow-up text */
            font-weight: bold;  /* Bold font */
            color: white;  /* White text for follow-up */
            font-family: 'Arial', sans-serif;  /* Better font for follow-up text */
            text-align: left;  /* Align left */
        /* Sidebar style */
        .stSidebar {
            background-color: #f8f9fa; /* Off-white color */
            border-right: 1px solid #e0e0e0; /* Optional: light border for separation */
            box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1); /* Optional: slight shadow for depth */        
        }
        </style>
    """, unsafe_allow_html=True)

def get_greeting():
    # Get current time in IST
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist).hour

    # Determine the greeting based on the hour
    if 5 <= current_time < 12:
        return "Good Morning"
    elif 12 <= current_time < 17:
        return "Good Afternoon"
    else:
        return "Good Evening"

def generate_response(message, value):
    new_data = {
        "Question": message,
        "User_Name": st.session_state.user_name,
        "User_Phone": st.session_state.user_phone,
        "Pincode": st.session_state.pincode,
        "Language": st.session_state.language,
        "UserID":st.session_state.user_name
    }
    if value == 0:
        url_post = "http://localhost:8088/askquery"
    else:
        url_post = "http://localhost:8088/askvector"
    post_response = requests.post(url_post, json=new_data)
    response_json = post_response.json()
    return response_json

def msendpin(pincode):
    new_data = {
        "Pincode": st.session_state.pincode
    }
    url_post = "http://localhost:8088/maps"
    post_response = requests.post(url_post, json=new_data)
    response_json = post_response.json()
    return response_json

def senddetail(user_name, user_phone, pincode, language):
    new_data = {
        "User_Name": user_name,
        "User_Phone": user_phone,
        "Pincode": pincode,
        "Language": language
    }
    url_post = "http://localhost:8088/askd"
    post_response = requests.post(url_post, json=new_data)
    response_json = post_response.json()
    return response_json

def getdetail():
    # Input fields for user details
    user_name = st.text_input("Enter your Name: ")
    user_phone = st.text_input("Enter your phone number: ")
    user_email = st.text_input("Enter your email: ")
    pincode = st.text_input("Enter your pincode: ")
    language = st.selectbox("Select a language...", ("English", "Hindi", "Kannada", "Tamil"))

    # Validation flags
    is_valid = True
    error_message = ""

    # Validate name (only alphabets, at least 3 characters)
    if user_name and not user_name.isalpha():
        is_valid = False
        error_message += "Name should only contain alphabets.\n"

    # Validate phone number (10 digits, numeric only)
    if user_phone and (not user_phone.isdigit() or len(user_phone) != 10):
        is_valid = False
        error_message += "Phone number should be 10 digits long.\n"

    # Validate email using regex
    import re
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if user_email and not re.match(email_pattern, user_email):
        is_valid = False
        error_message += "Please enter a valid email address.\n"

    # Validate pincode (6 digits, numeric only)
    if pincode and (not pincode.isdigit() or len(pincode) != 6):
        is_valid = False
        error_message += "Pincode should be 6 digits long.\n"

    # Display error messages if validation fails
    if not is_valid:
        st.error(error_message)

    # Submit button
    if st.button("Submit", icon="✅"):
        if user_name and user_phone and user_email and pincode and language and is_valid:
            response = senddetail(user_name, user_phone, pincode, language)
            if response['status'] == 1:
                st.success("Successfully sent data")
            else:
                st.error("Error in sending data")
        else:
            st.error("Please ensure all fields are correctly filled.")

    return user_name, user_phone, pincode, language


def createside():
    with st.sidebar:
        # v1 = st.checkbox("Search Trusted Sources")
        # if v1 not in st.session_state:
        st.session_state.v1 = 0
        if int(st.session_state.v1) == 0:
            st.session_state.img = "./assets/red.png"
        else:
            st.session_state.img = "./assets/blue.png"
        pages = ["User info", "Chat", "Services"]
        page = st.radio("Select a page:", pages)
        return page


def services_page():
    maps = st.button("Find nearest hospitals",icon="🏥")
    if maps:
        hospital_info = msendpin(st.session_state.pincode)
        st.markdown("<h3>Hospital 1 details</h3>", unsafe_allow_html=True)
        st.markdown("Name: " + hospital_info['data']['hospital1'][0])
        st.markdown("Address: " + hospital_info['data']['hospital1'][1] + " Phone Number: " + hospital_info['data']['hospital1'][2])
        st.markdown("<h3>Hospital 2 details</h3>", unsafe_allow_html=True)
        st.markdown("Name: " + hospital_info['data']['hospital2'][0])
        st.markdown("Address: " + hospital_info['data']['hospital2'][1] + " Phone Number: " + hospital_info['data']['hospital2'][2])
        st.markdown("<h3>Hospital 3 details</h3>", unsafe_allow_html=True)
        st.markdown("Name: " + hospital_info['data']['hospital3'][0])
        st.markdown("Address: " + hospital_info['data']['hospital3'][1] + " Phone Number: " + hospital_info['data']['hospital3'][2])
    # if st.button("Book a session", icon="📅"):
    #     sendm()
    #     st.success("Successfully booked a session, please check your email for further details")
def sendm():
    new_data = {
        "User_name": st.session_state.user_name,
    }
    url_post = "http://localhost:8088/maill"
    requests.post(url_post, json=new_data)

def sendinput(question, avatar):
    with st.chat_message("user", avatar=st.session_state.userimg):
        st.markdown(f"<div class='chat-bubble'>{question}</div>", unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": question, "avatar": st.session_state.userimg})
    response = generate_response(question, int(st.session_state.v1))
    answer = response['data']['Answer']
    full_response = ""
    with st.chat_message("assistant", avatar=avatar):
        message_placeholder = st.empty()
        for chunk in answer.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(f"<div class='chat-bubble assistant'>{full_response}▌</div>", unsafe_allow_html=True)
        message_placeholder.markdown(f"<div class='chat-bubble assistant'>{full_response}</div>", unsafe_allow_html=True)
    # if response['data']['Source1'] != "":
    #     st.info(response['data']['Source1'])
    #     st.info(response['data']['Source2'])
    follow = response['data']['Followup']
    st.markdown(f"<div class='follow-up'>Follow up question: {follow}</div>", unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": answer, "avatar": st.session_state.img})
def chat_page():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        role = message["role"]
        avatar = message["avatar"]
        with st.chat_message(role, avatar=avatar):
            st.markdown(message["content"])

    if st.sidebar.button("Start Audio Input", icon="🎙️"):
        with st.spinner("Listening..."):
            try:
                recognized_text = voicetotext.listen()
                sendinput(recognized_text, st.session_state.img)
            except Exception as e:
                st.error("Sorry, did not get that. Please try again!")
    
    if a := st.chat_input("What's on your mind today?"):
        sendinput(a, st.session_state.img)


def main():
    # st.title("InnerVerse")
    add_custom_css()
    st.markdown(
        "<h1 class='innerverse-title'>InnerVerse-Your Gateway to Mental Wellness</h1>",
        unsafe_allow_html=True
    )

    # Tagline or phrase with consistent gradient and animation
    # st.markdown(
    #     "<h2 class='innerverse-tagline'>Your Gateway to Mental Wellness</h2>",
    #     unsafe_allow_html=True
    # )
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""
    if "user_phone" not in st.session_state:
        st.session_state.user_phone = ""
    if "pincode" not in st.session_state:
        st.session_state.pincode = ""
    if "userimg" not in st.session_state:
        st.session_state.userimg = "./assets/img.png"
    if "language" not in st.session_state:
        st.session_state.language = "English"

    st.markdown(
        f"<div class='personalized-greeting'>{get_greeting()} <span class='personalized-name'>{st.session_state.user_name}</span>, Welcome to your Mental Health Assistant</div>",
        unsafe_allow_html=True
    )

    page = createside()
    # st.sidebar.button("Flag content", icon="🚩")

    if page == "User info":
        user_detail = getdetail()
        st.session_state.user_name = user_detail[0]
        st.session_state.user_phone = user_detail[1]
        st.session_state.pincode = user_detail[2]
        st.session_state.language = user_detail[3]
    elif page == "Chat":
        chat_page()
    elif page == "Services":
        services_page()

if __name__ == "__main__":
    main()
