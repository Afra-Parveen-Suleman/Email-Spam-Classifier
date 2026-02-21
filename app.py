import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import nltk

# Download required NLTK data if not already present
nltk.download('punkt')
nltk.download('stopwords')

# Initialize stemmer
ps = PorterStemmer()

# Function to clean and transform email text
def transform_text(text):
    text = text.lower().split()

    # Keep only alphanumeric words
    text = [word for word in text if word.isalnum()]

    # Remove stopwords and punctuation
    text = [word for word in text if word not in stopwords.words('english') and word not in string.punctuation]

    # Apply stemming
    text = [ps.stem(word) for word in text]

    return " ".join(text)

# Load saved TF-IDF vectorizer and model
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl','rb'))

# Streamlit app title
st.title("Email Spam Classifier")

# Input email from user
input_email = st.text_area("Enter the Email")

# Predict button
if st.button('Predict'):
    transformed_email = transform_text(input_email)
    vector_input = tfidf.transform([transformed_email])
    result = model.predict(vector_input)[0]

    if result == 1:
        st.header("Spam")
    else:
        st.header("Not Spam")