import streamlit as st
from enigma.rotor import Rotor
from enigma.reflector import Reflector
from enigma.plugboard import Plugboard
from enigma.machine import EnigmaMachine


st.set_page_config(page_title="Enigma Machine", layout="centered")
st.title("🔐 Enigma Machine Simulator")

st.markdown("### Step 1: Enter Your Message")
message = st.text_area("Message to Encrypt/Decrypt", value="HELLO WORLD")

st.markdown("### Step 2: Plugboard Settings")
plugboard_input = st.text_input("Plugboard Pairs (e.g. A-G,M-N)", value="A-G,M-N")

st.markdown("### Step 3: Rotor Settings")
rotor_positions = st.text_input("Rotor Positions (e.g. A A A)", value="A A A")

rotor_choices = ["I", "II", "III", "IV", "V"]
r_right = st.selectbox("Right Rotor", rotor_choices, index=0)
r_middle = st.selectbox("Middle Rotor", rotor_choices, index=1)
r_left = st.selectbox("Left Rotor", rotor_choices, index=2)

if st.button("🔒 Encrypt / Decrypt"):
    try:
        rotor_pos = rotor_positions.strip().upper().split()
        plug_pairs = plugboard_input.upper().split(',')
        plugboard_pairs = [(p[0], p[2]) for p in plug_pairs if len(p) == 3 and p[1] == '-']

        # Rotor wiring definitions
        rotor_map = {
            "I": ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 'Q'),
            "II": ("AJDKSIRUXBLHWTMCQGZNPYFVOE", 'E'),
            "III": ("BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V'),
            "IV": ("ESOVPZJAYQUIRHXLNFTGKDCMWB", 'J'),
            "V": ("VZBRGITYUPSDNHLXAWMJQOFECK", 'Z')
        }

        # Initialize rotors
        rotor1 = Rotor(*rotor_map[r_right], position=rotor_pos[2])
        rotor2 = Rotor(*rotor_map[r_middle], position=rotor_pos[1])
        rotor3 = Rotor(*rotor_map[r_left], position=rotor_pos[0])
        reflector = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
        plugboard = Plugboard(plugboard_pairs)

        machine = EnigmaMachine([rotor3, rotor2, rotor1], reflector, plugboard)
        output = machine.encrypt_message(message.upper())

        st.success(f"🔓 Output: {output}")

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
