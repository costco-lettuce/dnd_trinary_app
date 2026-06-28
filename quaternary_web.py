import streamlit as st
import string

def generate_dictionaries(base):
    eng_to_cipher = {}
    cipher_to_eng = {}
    
    symbols = {0: '?', 1: '.', 2: '!', 3: ','}
    
    # Base-3 mathematically holds 27 items (0-26). Base-4 holds 64 items (0-63).
    if base == 3:
        char_set = string.ascii_uppercase + " "
    else:
        # A perfectly padded 64-character string to capture all Base-4 combinations
        # A-Z (26) + a-z (26) + 0-9 (10) + two symbols (2) = 64
        char_set = string.ascii_uppercase + string.ascii_lowercase + string.digits + "-+"
        
    # THE FIX: Changing start=1 to start=0 aligns the cipher with the DM's math
    for i, char in enumerate(char_set, start=0):
        val = i
        base_str = ""
        
        for _ in range(3):
            digit = val % base
            base_str = symbols[digit] + base_str
            val //= base
            
        eng_to_cipher[char] = base_str
        cipher_to_eng[base_str] = char
        
    return eng_to_cipher, cipher_to_eng

# --- 2. CONVERSION FUNCTIONS ---
def encode_english(text, eng_to_cipher):
    words = text.split()
    coded_lines = []
    
    for word in words:
        coded_letters = [eng_to_cipher[char.upper()] for char in word if char.upper() in eng_to_cipher]
        if coded_letters: # Ensures we don't add blank lines for pure punctuation
            coded_lines.append(" ".join(coded_letters))
            
    return "\n".join(coded_lines)


def decode_cipher(text, cipher_to_eng):
    coded_words = text.strip().split('\n')
    decoded_sentence = []
    
    for coded_word in coded_words:
        if not coded_word.strip():
            continue
            
        triplets = coded_word.split()
        current_word = ""
        
        for triplet in triplets:
            if triplet in cipher_to_eng:
                current_word += cipher_to_eng[triplet]
            else:
                current_word += "[?]" 
                
        decoded_sentence.append(current_word)
        
    return " ".join(decoded_sentence)


# --- 3. STREAMLIT WEB UI ---

# Configure the browser tab
st.set_page_config(page_title="Multi-Base Cipher", page_icon="🕵️")

st.title("Secret Cipher Converter")
st.write("Translate plain English into a secret Base-3 or Base-4 code, and vice versa!")

# Dropdown menu to govern the translation base
cipher_mode = st.selectbox(
    "Select Cipher Base:",
    ("Base-3 (Trinary)", "Base-4 (Quaternary)")
)

# Determine which base number to use based on the dropdown choice
base_num = 3 if cipher_mode == "Base-3 (Trinary)" else 4

# Generate the appropriate dictionaries instantly
eng_to_cipher, cipher_to_eng = generate_dictionaries(base_num)

tab1, tab2 = st.tabs(["English to Cipher", "Cipher to English"])

with tab1:
    st.subheader(f"Encode to {cipher_mode}")
    eng_text = st.text_area("Enter an English sentence:", height=100)
    
    if st.button("Convert to Cipher"):
        if eng_text:
            # Pass the dynamically generated dictionary to the function
            result = encode_english(eng_text, eng_to_cipher)
            st.code(result, language=None)
        else:
            st.warning("Please enter some text first.")

with tab2:
    st.subheader("Decode to Plain English")
    cipher_text = st.text_area("Enter Cipher code:", height=100)
    
    if st.button("Convert to English"):
        if cipher_text:
            # Pass the dynamically generated dictionary to the function
            result = decode_cipher(cipher_text, cipher_to_eng)
            st.code(result, language=None)
        else:
            st.warning("Please enter some code first.")
