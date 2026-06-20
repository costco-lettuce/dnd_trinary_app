import streamlit as st
import string

# set up dictionaries
eng_to_tri = {}
tri_to_eng = {}

for i, char in enumerate(string.ascii_uppercase, start=1):
    val = i
    base3 = ""
    for _ in range(3):
        base3 = str(val % 3) + base3
        val //= 3
        
    trinary_code = base3.replace('0', '?').replace('1', '.').replace('2', '!')
    eng_to_tri[char] = trinary_code
    tri_to_eng[trinary_code] = char


# conversion functions
def encode_english(text):
    words = text.split()
    coded_lines = []
    for word in words:
        coded_letters = [eng_to_tri[char.upper()] for char in word if char.upper() in eng_to_tri]
        coded_lines.append(" ".join(coded_letters))
    return "\n".join(coded_lines)

def decode_trinary(text):
    triplets = text.split()
    decoded_word = ""
    for triplet in triplets:
        if triplet in tri_to_eng:
            decoded_word += tri_to_eng[triplet]
        else:
            decoded_word += "[?]" 
    return decoded_word


# web ui for ease of use

# configure the browser tab
st.set_page_config(page_title="Trinary Converter", page_icon="🕵️")

# add headers and instructions
st.title("Trinary Cipher Converter")
st.write("Translate plain English into a secret Base-3 cipher, and vice versa!")

# create two clean tabs for the user to switch between
tab1, tab2 = st.tabs(["English to Trinary", "Trinary to English"])

with tab1:
    st.subheader("Encode to Trinary")
    # large text box for input
    eng_text = st.text_area("Enter an English sentence:", height=100)
    
    # clickable button
    if st.button("Convert to Trinary"):
        if eng_text:
            result = encode_english(eng_text)
            # display the result in a green success box
            st.success(result)
        else:
            # error handling if they click without typing
            st.warning("Please enter some text first.")

with tab2:
    st.subheader("Decode to Plain English")
    tri_text = st.text_area("Enter Trinary code (e.g., ?!! .??):", height=100)
    
    if st.button("Convert to English"):
        if tri_text:
            result = decode_trinary(tri_text)
            st.success(result)
        else:
            st.warning("Please enter some code first.")