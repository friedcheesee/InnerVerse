import streamlit as st
import time
import requests
import voicetotext
def generate_response(message, value):
    new_data = {
        "Question": message,
        "User_Name" : st.session_state.user_name,
        "User_Phone" : st.session_state.user_phone,
        "Pincode" : st.session_state.pincode,
        "Language":st.session_state.language
    }
    if value == 0:
        url_post = "http://localhost:8088/askquery"
        post_response = requests.post(url_post, json=new_data)
        response_json = post_response.json()
        return response_json
    else:
        url_post = "http://localhost:8088/askvector"
        post_response = requests.post(url_post, json=new_data)
        response_json = post_response.json()
        return response_json

def msendpin(pincode):
    new_data={
        "Pincode":st.session_state.pincode
    }
    url_post = "http://localhost:8088/maps"
    post_response = requests.post(url_post, json=new_data)
    response_json = post_response.json()
    return response_json

def senddetail(user_name,user_phone,pincode,language):
    new_data = {
        "User_Name" : user_name,
        "User_Phone" : user_phone,
        "Pincode" : pincode,
        "Language":language
    }
    url_post = "http://localhost:8088/askd"
    post_response = requests.post(url_post, json=new_data)
    response_json = post_response.json()
    return response_json

def getdetail(): 
    user_name = st.text_input("Enter your Name: ", type="default")
    user_phone = st.text_input("Enter your phone number: ", type="default")
    user_email = st.text_input("Enter your email: ", type="default")
    pincode = st.text_input("Enter your pincode: ", type="default")
    language=st.selectbox("Select a language...",("English","Hindi","Kannada","tamil"))

    
    if st.button("Submit"):
        if (user_name and user_phone and pincode and language):
            response = senddetail(user_name,user_phone,pincode,language)
            print(response)
            if (response['status']==1):
                st.success("Successfully sent data")
            else:
                st.error("Error in sending data")
        else:
            st.error("Please enter all the details")
    return user_name,user_phone,pincode,language

def createside():
    with st.sidebar:
        v1 = st.checkbox("Search Trusted Sources")
        if v1 not in st.session_state:
            st.session_state.v1 = v1
        if(int(st.session_state.v1)==0):
            st.session_state.img="./assets/red.png"
        else:
            st.session_state.img="./assets/blue.png"
        #st.button("Flag Content",on_click=flag())
        pages = ["User info", "Chat","Services"]
        page = st.radio("Select a page:", pages)
        
        return page


def services_page():
    maps= st.button("Find nearest hospitals")
    if maps:
        hospital_info = msendpin(st.session_state.pincode)
        st.markdown("<h3 style='text-align: left;'>Hospital 1 details </h3>", unsafe_allow_html=True)
        st.markdown("Name: "+hospital_info['data']['hospital1'][0])
        st.markdown("Address: "+hospital_info['data']['hospital1'][1]+" Phone Number:"+hospital_info['data']['hospital1'][2])
        st.markdown("<h3 style='text-align: left;'>Hospital 2 details </h3>", unsafe_allow_html=True)
        st.markdown("Name: "+hospital_info['data']['hospital2'][0])
        st.markdown("Address: "+hospital_info['data']['hospital2'][1]+" Phone Number:"+hospital_info['data']['hospital2'][2])
        st.markdown("<h3 style='text-align: left;'>Hospital 3 details </h3>", unsafe_allow_html=True)   
        st.markdown("Name: "+hospital_info['data']['hospital3'][0])
        st.markdown("Address: "+hospital_info['data']['hospital3'][1]+" Phone Number:"+hospital_info['data']['hospital3'][2])
    ssession= st.button("Book a session")
    if ssession:
        sendm()
        #mailer.sendem("name","chathistory")
        #mailer.sendem()
        #if res==1:
        st.success("Successfully booked a session, please check your email for further details")
    
def sendm():
    new_data={
        "User_name":st.session_state.user_name,
    }
    print("sendm called")
    url_post = "http://localhost:8088/maill"
    post_response = requests.post(url_post, json=new_data)
    #response_json = post_response.json()
   # return #response_json
    
def sendinput(question,avatar):
    with st.chat_message("user",avatar=st.session_state.userimg):
        st.markdown(question)
    st.session_state.messages.append({"role": "user", "content": question,"avatar":st.session_state.userimg})  
    response = generate_response(question, int(st.session_state.v1))
    answer = response['data']['Answer']
    full_response = ""
    with st.chat_message("assistant",avatar=avatar):
        message_placeholder = st.empty()
        for chunk in answer.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    if(response['data']['Source1']!=""):
        st.info(response['data']['Source1'])
        st.info(response['data']['Source2'])

    follow = response['data']['Followup']
    #follow="Follow up question:"+follow
    st.success("**Follow up question:**")
    st.success(follow)
    st.session_state.messages.append({"role": "assistant", "content": answer,"avatar":st.session_state.img})

    
def chat_page():
    # Create messages list in sessionstate
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "help" not in st.session_state:
        st.session_state.help = []
    ## Print messages from chat history on rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"],avatar=message["avatar"]):
            st.markdown(message["content"])
    
    if st.sidebar.button("Start Audio Input"):
        with st.spinner("Listening..."):
            recognized_text = voicetotext.listen()
        sendinput(recognized_text,st.session_state.img)

    var = "Ask a mental health question..."

    if a := st.chat_input(var):
        sendinput(a,st.session_state.img)

def main():
    st.title("InnerVerse")
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""
    if "user_phone" not in st.session_state:
        st.session_state.user_phone = ""
    if "pincode" not in st.session_state:
        st.session_state.pincode = ""
    if "userimg" not in st.session_state:
        st.session_state.userimg="./assets/img.png"
    if "language" not in st.session_state:
        st.session_state.language="English"
    page=createside()
    st.sidebar.button("Flag content")
    if page == "User info":
        user_detail = getdetail()
        if (user_detail[0] and user_detail[1] and user_detail[2] and user_detail[3]):  
            st.session_state.user_name = user_detail[0]
            st.session_state.user_phone = user_detail[1]
            st.session_state.pincode = user_detail[2]
            st.session_state.language=user_detail[3]
            
    
    elif page == "Chat":
        if (st.session_state.user_phone!=""):
            chat_page()
        else:
            st.warning("Please enter your details first on the 'User info' page.")
    elif page == "Services":  # Add a new condition for "Help Services"
            services_page()
    
if __name__ == "__main__":
    main()
