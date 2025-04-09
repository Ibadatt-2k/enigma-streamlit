import streamlit as st
from enigma.rotor import Rotor
from enigma.reflector import Reflector
from enigma.plugboard import Plugboard
from enigma.machine import EnigmaMachine

import json
from firebase_admin import credentials

firebase_key = st.secrets["FIREBASE"]
cred = credentials.Certificate(json.loads(json.dumps(firebase_key)))
firebase_admin.initialize_app(cred)



db = firestore.client()



st.set_page_config(page_title="Enigma Machine", layout="centered")
st.title("🔐 Enigma Machine Simulator")

with st.sidebar:
    st.markdown("## 👤 Your Identity")
    username = st.text_input("Your username", key="sender_username")
    st.markdown("## 📤 Send Encrypted File")
    recipient = st.text_input("Friend's username", key="recipient_username")

with st.sidebar:
    st.title("📘 Enigma Info")
    st.markdown("""
    - Built by: **Ibadatt** , **Ekam** , **Shayne** , **Gagneet**
    - Based on WWII encryption
    - Symmetric key: Same settings decrypt what was encrypted
    - Supports 5 rotors, plugboard pairs, and classic reflector

    🔁 Encrypt again with same settings to decrypt!
    """)
st.markdown("### Step 1: Enter Your Message")
message = st.text_area("Message to Encrypt/Decrypt", value="HELLO WORLD")


#File Uploading section
st.markdown("---")
st.markdown("### 📂 Encrypt or Decrypt a File (.txt only)")

uploaded_file = st.file_uploader("Choose a .txt file", type=["txt"])

file_action = st.radio("What do you want to do?", ["Encrypt", "Decrypt"])

if uploaded_file and st.button("🔐 Process File"):
    try:
        content = uploaded_file.read().decode("utf-8").strip()

        rotor_pos = rotor_positions.strip().upper().split()
        plug_pairs = plugboard_input.upper().split(',')
        plugboard_pairs = [(p[0], p[2]) for p in plug_pairs if len(p) == 3 and p[1] == '-']

        # Setup machine
        rotor1 = Rotor(*rotor_map[r_right], position=rotor_pos[2])
        rotor2 = Rotor(*rotor_map[r_middle], position=rotor_pos[1])
        rotor3 = Rotor(*rotor_map[r_left], position=rotor_pos[0])
        reflector = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
        plugboard = Plugboard(plugboard_pairs)
        machine = EnigmaMachine([rotor3, rotor2, rotor1], reflector, plugboard)

        output = machine.encrypt_message(content.upper())

        st.success("✅ File processed!")
        st.text_area("Output Preview:", value=output[:1000], height=150)

        # Provide download link
        st.download_button(
            label="📥 Download Result",
            data=output,
            file_name=f"{'encrypted' if file_action=='Encrypt' else 'decrypted'}_output.txt",
            mime="text/plain"
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")
st.markdown("---")
st.markdown("### 🔁 Send Encrypted File to a Friend")

uploaded_file_send = st.file_uploader("Choose a .txt file to send to friend", type=["txt"], key="file_send")


if uploaded_file and st.button("📤 Encrypt & Send File"):
    if not username or not recipient:
        st.error("Please enter both your username and your friend's username.")
    else:
        content = uploaded_file.read().decode("utf-8").strip()

        try:
            # Setup rotor/plugboard from current Streamlit UI
            rotor_pos = rotor_positions.strip().upper().split()
            plug_pairs = plugboard_input.upper().split(',')
            plugboard_pairs = [(p[0], p[2]) for p in plug_pairs if len(p) == 3 and p[1] == '-']

            rotor1 = Rotor(*rotor_map[r_right], position=rotor_pos[2])
            rotor2 = Rotor(*rotor_map[r_middle], position=rotor_pos[1])
            rotor3 = Rotor(*rotor_map[r_left], position=rotor_pos[0])
            reflector = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
            plugboard = Plugboard(plugboard_pairs)

            machine = EnigmaMachine([rotor3, rotor2, rotor1], reflector, plugboard)
            encrypted = machine.encrypt_message(content.upper())

            # Simulated message store: save to a local text file named by recipient
            # Save to Firebase Firestore
            message_data = {
                "from": username,
                "to": recipient,
                "encrypted": encrypted,
                "timestamp": firestore.SERVER_TIMESTAMP
            }
            db.collection("messages").add(message_data)

            st.success(f"✅ Message sent to {recipient} via Firestore!")


        except Exception as e:
            st.error(f"Error encrypting/sending: {e}")
st.markdown("### 📥 Check Your Inbox")

inbox_owner = st.text_input("Enter your username to check messages:", key="inbox_check")

if inbox_owner:
    try:
        messages = db.collection("messages").where("to", "==", inbox_owner).stream()
        inbox_display = ""

        for msg in messages:
            data = msg.to_dict()
            inbox_display += f"From: {data['from']}\nMessage:\n{data['encrypted']}\n---\n"

        if inbox_display:
            st.text_area("📬 Messages Received:", value=inbox_display, height=300)
        else:
            st.info("No messages yet.")

    except FileNotFoundError:
        st.info("No messages yet.")

st.markdown("### Step 2: Plugboard Settings")
plugboard_input = st.text_input("Plugboard Pairs (e.g. A-G,M-N)", value="A-G,M-N")

st.markdown("### Step 3: Rotor Settings")
rotor_positions = st.text_input("Rotor Positions (e.g. A A A)", value="A A A")

rotor_choices = ["I", "II", "III", "IV", "V"]
col1, col2, col3 = st.columns(3)
with col1:
    r_right = st.selectbox("Right Rotor", rotor_choices, index=0)
with col2:
    r_middle = st.selectbox("Middle Rotor", rotor_choices, index=1)
with col3:
    r_left = st.selectbox("Left Rotor", rotor_choices, index=2)

rotor_map = {
    "I": ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 'Q'),
    "II": ("AJDKSIRUXBLHWTMCQGZNPYFVOE", 'E'),
    "III": ("BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V'),
    "IV": ("ESOVPZJAYQUIRHXLNFTGKDCMWB", 'J'),
    "V": ("VZBRGITYUPSDNHLXAWMJQOFECK", 'Z')
}

st.markdown("---")
st.markdown("### 📂 Encrypt or Decrypt a File (.txt only)")

uploaded_file = st.file_uploader("Choose a .txt file to encrypt/decrypt", type=["txt"], key="file_encrypt_decrypt")

file_action = st.radio("What do you want to do?", ["Encrypt", "Decrypt"], key="file_action_radio")


if uploaded_file and st.button("🔐 Process File", key="process_file_button"):
    try:
        content = uploaded_file.read().decode("utf-8").strip()

        rotor_pos = rotor_positions.strip().upper().split()
        plug_pairs = plugboard_input.upper().split(',')
        plugboard_pairs = [(p[0], p[2]) for p in plug_pairs if len(p) == 3 and p[1] == '-']

        # Initialize Enigma components
        rotor1 = Rotor(*rotor_map[r_right], position=rotor_pos[2])
        rotor2 = Rotor(*rotor_map[r_middle], position=rotor_pos[1])
        rotor3 = Rotor(*rotor_map[r_left], position=rotor_pos[0])
        reflector = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
        plugboard = Plugboard(plugboard_pairs)
        machine = EnigmaMachine([rotor3, rotor2, rotor1], reflector, plugboard)

        output = machine.encrypt_message(content.upper())

        st.success("✅ File processed!")
        st.text_area("Output Preview:", value=output[:1000], height=150)

        st.download_button(
            label="📥 Download Result",
            data=output,
            file_name=f"{'encrypted' if file_action == 'Encrypt' else 'decrypted'}_output.txt",
            mime="text/plain"
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")