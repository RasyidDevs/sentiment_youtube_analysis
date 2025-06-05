### Demo Video 💻  
Link Video: [Youtube video](https://youtu.be/R5wiGC29Hng?si=eI7PgUgl8GQ989CP)

### Demo Youtube 💻 
Demo Web: [streamlit app](https://sentiment-youtube.streamlit.app/)

## Installation

1. Clone this repository  
```bash
git clone https://github.com/RasyidDevs/sentiment_youtube_analysis
```
2. Go to directory project
```bash
cd FUN_PROJECT_2_REAPYTHON1LVTXY
```
3. install all requirement
```bash
pip install -r requirements.txt
```
4. Create  api key on this link  [https://console.cloud.google.com/](https://console.cloud.google.com/) 
```bash
1. Go to https://console.cloud.google.com/  
2. Create a new project or select an existing one  
3. Enable YouTube Data API v3 from the API Library  
4. Go to Credentials → Create Credentials → API Key  
5. Copy the API key  
```
5. Rename file secrets.toml.example -> .secrets.toml (you can see this file on .steamlit folder)
6. Add your API Key to secrets.toml file
```bash
API_KEY = "YOUR_API_KEY " 
```  
7. run streamlit
```bash
streamlit run app.py
```
⚠️ If the command above doesn't work, try:
```bash
python -m streamlit run app.py
```
# 🤝 Contributing
If you want to contribute to this project, please open an issue, submit a pull request or contact me at
rasyidbomantoro@gmail.com
