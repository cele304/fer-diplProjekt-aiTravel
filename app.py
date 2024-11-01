#ovo mislim da je okej, sada to mozes deployat na render kako bi ti dali feedback
#i kad zavrsis sa kartom spojit sve na bazu da se user mora loginat kako bi sve koristio





import streamlit as st
from typing import Generator
from groq import Groq
from dotenv import load_dotenv
import os





# Učitavanje okruženja iz .env fajla
load_dotenv()
api_key = os.getenv('GROQ_API_KEY')
weather_api_key = os.getenv('WEATHER_API_KEY')



# Provjeri je li API ključ postavljen
if not api_key or not weather_api_key:
    st.error("API key not set. Check your .env file.")
    st.stop()

client = Groq(api_key=api_key)

st.set_page_config(page_icon="✈️", layout="centered",
                   page_title="AI Travel Planner")









import requests
from datetime import timedelta, date

def get_weather_forecast(location: str, travel_dates: list):
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": location,
        "appid": weather_api_key,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        weather_data = response.json()
        forecasts = []
        for forecast in weather_data["list"]:
            forecast_date = date.fromtimestamp(forecast["dt"])
            if forecast_date in travel_dates:
                forecasts.append({
                    "date": forecast_date,
                    "time": forecast["dt_txt"].split(" ")[1][:2] + " h",
                    "temperature": round(forecast["main"]["temp"]),  # Rounded to nearest integer
                    "description": forecast["weather"][0]["description"],
                    "icon": forecast["weather"][0]["icon"]
                })
        return forecasts
    else:
        st.error("Could not retrieve weather data.")
        return []
















# Dodavanje prilagođenog CSS-a
st.markdown("""
    <style>

    /* Globalno postavljanje boje pozadine i fontova */
    html, body {
        background-color: #3A003D;
        color: #FFFFFF;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        height: 100%;
    }
            
   
    
    /* Glavni sadržaj - zaobljeni rubovi, pozadinska boja, sjene */
    .stApp {
        background-color: #2A2A3D;
        border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.4);
        padding: 10px;
            
    }

    /* Stil za naslove */
    .stApp h1, .stApp h2, .stApp h3 {
        color: #FFD700; /* Zlatna boja */
        font-weight: 600;
    }

    /* Sidebar stil - animirani efekti */
    .css-1lcbmhc {
        background-color: #3A3A5D;
        border-radius: 10px;
        padding: 20px;
        transition: all 0.2s ease-in-out;
    }
    .css-1lcbmhc:hover {
        background-color: #454575;
        transform: scale(1.02);
    }

    /* Boje za sve button elemente */
    .stButton > button {
        background-color: #00ADB5;
        color: #FFFFFF;
        border-radius: 12px;
        border: none;
        padding: 10px 20px;
        font-size: 1rem;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #00FFC6;
        box-shadow: 0 8px 15px rgba(0, 255, 198, 0.4);
    }

    /* Stil za inpute i selektovane opcije */
    .stTextInput > div, .stSelectbox > div, .stMultiselect > div, .stSlider > div, .stDateInput > div {
        background-color: #333354;
        color: #E0E0E0;
        border-radius: 8px;
        padding: 5px;
    }
    
    /* Promjena stila input placeholdera */
    ::placeholder {
        color: #B0B0B0;
        opacity: 0.7;
    }

    /* Stil za chat poruke */
    .css-1kh9p2p {
        background-color: #414161;
        border-radius: 15px;
        color: #FFFFFF;
        margin: 10px 0;
        padding: 15px;
    }

    /* Poruke korisnika - plava pozadina */
    .css-1kh9p2p.user {
        background-color: #2A9D8F;
    }

    /* Poruke asistenta - ljubičasta pozadina */
    .css-1kh9p2p.assistant {
        background-color: #9D2AA6;
    }

    /* Glavne ikone i avatar */
    .css-1hy0qcd {
        font-size: 2rem;
        color: #FFD700;
    }
    
    /* Stil za 'Start New Chat' gumb */
    .css-10trblm {
        background-color: #FF00D9;
        color: white;
        font-size: 1rem;
        border-radius: 12px;
        padding: 12px 20px;
        transition: transform 0.2s ease-in-out;
    }
    .css-10trblm:hover {
        background-color: #FF0079;
        transform: scale(1.05);
        box-shadow: 0px 8px 16px rgba(255, 0, 217, 0.4);
    }
            
    .main .block-container {
        max-width: 60%; /* Postavi širinu glavnog sadržaja na 90% ekrana */
        padding-left: 20%; /* Razmak s lijeve strane */
        padding-right: 20%; /* Razmak s desne strane */
    }

            

    
        /* Weather forecast card styling */
    .forecast-card {
        background-color: #3A3A5D;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        display: flex;
        align-items: center;
        animation: fadeIn 0.5s ease-in-out;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    }

    /* Icon styling with animation */
    .forecast-icon {
        width: 50px;
        height: 50px;
        margin-right: 10px;
        animation: iconBounce 1s ease-in-out infinite;
    }

    /* Weather info text styling */
    .forecast-info {
        color: #E0E0E0;
        font-size: 1.1rem;
        font-weight: 500;
    }

    /* Fade-in animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Bounce animation for icon */
    @keyframes iconBounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }


    </style>
""", unsafe_allow_html=True)









def icon(emoji: str):
    """Prikazuje emoji kao Notion-style ikonu stranice."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


icon("✈️")

st.subheader("AI Travel Planner", divider="rainbow", anchor=False)


# Inicijalizacija povijesti chata i odabranog modela
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

# Definicija modela
models = {
    "gemma-7b-it": {"name": "Gemma-7b-it", "tokens": 8192, "developer": "Google"},
    "llama2-70b-4096": {"name": "LLaMA2-70b-chat", "tokens": 4096, "developer": "Meta"},
    "llama3-70b-8192": {"name": "LLaMA3-70b-8192", "tokens": 8192, "developer": "Meta"},
    "llama3-8b-8192": {"name": "LLaMA3-8b-8192", "tokens": 8192, "developer": "Meta"},
    "mixtral-8x7b-32768": {"name": "Mixtral-8x7b-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"},
}


# Sidebar za planiranje putovanja
st.sidebar.header("Plan Your Next Trip")
with st.sidebar.form(key="travel_form"):
    origin = st.text_input("Origin", placeholder="Enter a country or city")
    destination = st.text_input("Destination", placeholder="Enter a country or city")
    travel_type = st.selectbox("Travel Style", ["Adventure", "Relaxation", "Cultural", "Luxury", "Budget", "Family"])
    interests = st.multiselect("What are you interested in?", ["Beaches", "Hiking", "Museums", "Nightlife", "History", "Food", "Shopping", "Nature"])
    accommodation = st.selectbox("Preferred Accommodation", ["Hotel", "Hostel", "Airbnb", "Resort", "Camping"])
    budget_range = st.slider("Budget Per Person (EUR)", min_value=100, max_value=4000, value=(100, 500), help="Set the budget range per person")
    trip_duration = st.number_input("How many days?", min_value=1, max_value=60, step=1)
    travel_dates = st.date_input("Travel Dates", [])
    num_people = st.number_input("Number of People", min_value=1, max_value=20, step=1, help="Specify the total number of people traveling")
    transportation = st.selectbox("Preferred Local Transportation", ["Public Transport", "Car Rental", "Biking", "Walking", "Taxi/Ride-sharing"])

    submit_button = st.form_submit_button(label="Get Travel Suggestions")

# Layout za odabir modela i slider za max_tokens
col1, col2 = st.columns(2)

with col1:
    model_option = st.selectbox(
        "Choose model:",
        options=list(models.keys()),
        format_func=lambda x: models[x]["name"],
        index=0  # Zadani model je gemma
    )

# Provjera promjene modela i brisanje povijesti ako se model promijenio
if st.session_state.selected_model != model_option:
    st.session_state.messages = []
    st.session_state.selected_model = model_option

max_tokens_range = models[model_option]["tokens"]

with col2:
    max_tokens = st.slider(
        "Max Number Of Tokens:",
        min_value=512,  # Minimalna vrijednost za fleksibilnost
        max_value=max_tokens_range,
        value=min(32768, max_tokens_range),
        step=2,
        help=f"Set the maximum number of tokens (words) for the model's response. Maximum for the selected model: {max_tokens_range}"
    )

if submit_button:
    if destination:
        user_input = (
            f"I'm from {origin} and I want to go to {destination} for a {travel_type.lower()} trip. "
            f"I'm interested in {', '.join(interests)}, prefer {accommodation} accommodation, "
            f"for {trip_duration} days, with a budget per person of ${budget_range[0]} - ${budget_range[1]} EUR "
            f"for {num_people} people. Preferred transportation at the destination is {transportation}."
        )
        
        # Dodaj korisnički upit u chat povijest
        st.session_state.messages.append({"role": "user", "content": user_input})

        try:
            travel_response = client.chat.completions.create(
                model=st.session_state.selected_model,
                messages=[
                    {"role": "user", "content": user_input}
                ],
                max_tokens=2000,  # Postavljamo razuman limit tokena za putovanje
                stream=False
            )
            
            # Pristupamo odgovoru pomoću atributa 'content' iz objekta ChatCompletionMessage
            result = travel_response.choices[0].message.content


            # Generate weather forecast display
            weather = get_weather_forecast(destination, travel_dates)
            if weather:
                weather_content = f"**Weather forecast for {destination}:**\n\n"
                current_date = None
                for day in weather:
                    if day["date"] != current_date:
                        weather_content += f"\n**{day['date']}**\n"
                        current_date = day["date"]
                    weather_content += (
                        f"- {day['time']}: ![Weather icon](http://openweathermap.org/img/wn/{day['icon']}@2x.png) "
                        f"{day['temperature']}°C, {day['description'].capitalize()}\n"
                    )
            else:
                weather_content = f"Weather data for {destination} is unavailable. The weather forecast is only available for 5 days in advance."

            # Combine AI response with weather content
            combined_result = f"{result}\n\n{weather_content}"

            # Add combined response to chat history
            st.session_state.messages.append({"role": "assistant", "content": combined_result})






        except Exception as e:
            st.error(f"Error fetching travel plan: {e}")

# Prikaz povijesti chata na ponovnom pokretanju aplikacije
for message in st.session_state.messages:
    avatar = '🤖' if message["role"] == "assistant" else '👤'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])


def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield sadržaja odgovora iz Groq API odgovora."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content






if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar='👤'):
        st.markdown(prompt)

    # Dohvaćanje odgovora iz Groq API-ja
    try:
        chat_completion = client.chat.completions.create(
            model=model_option,
            messages=[
                {
                    "role": m["role"],
                    "content": m["content"]
                }
                for m in st.session_state.messages
            ],
            max_tokens=max_tokens,
            stream=True
        )

        # Korištenje generator funkcije s st.write
        with st.chat_message("assistant", avatar="🤖"):
            chat_responses_generator = generate_chat_responses(chat_completion)
            full_response = "".join(list(chat_responses_generator))
            st.write(full_response)
    except Exception as e:
        st.error(e)

    # Dodavanje punog odgovora u st.session_state.messages
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response})

# Dodavanje gumba za novi chat
if st.button("Start New Chat"):
    st.session_state.messages = []

