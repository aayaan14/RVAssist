# **RVAssist**

A **Streamlit-based chatbot app** designed to assist users with information about **Rashtreeya Vidyalaya College of Engineering (RVCE)**. The app also includes a **Google Maps-powered campus navigation feature** to guide users to various locations on the campus.

---

## **Features**

1. **RVAssist Chatbot**  
   - Utilizes a custom Retrieval-Augmented Generation (RAG) model combining LlamaIndex and a language model.  
   - Provides accurate, campus-specific answers about RVCE, including departments, facilities, and more.

2. **Interactive Campus Navigation**  
   - Integrates Google Maps to highlight the RVCE campus.  
   - Offers walking directions based on current location or manual input.  
   - Features a dynamic dropdown of popular destinations for easy selection.

3. **Dynamic and User-Friendly Design**  
   - Built using Streamlit for an intuitive chatbot interface.  
   - Ensures a seamless navigation experience and accessibility for all users.

---

## **Technologies Used**

- **Beautiful Soup** for web scraping and extracting content. 
- **SQLite** for managing and storing retrieved data in a lightweight database.  
- **LlamaIndex** for vector indexing and querying.  
- **Llama3.2:1b** as the LLM model for generating responses.   
- **Google Maps API** for map rendering and navigation.  
- **Streamlit** for building the chatbot UI.   
- **HTML/CSS/JavaScript** for the navigation feature.

---

## **Installation and Set-up**

### **1. Clone the Repository**
```bash
git clone https://github.com/your-username/RVAssist.git
cd RVAssist 
```

### **2. Set Up Python Environment**
```bash
python -m venv venv
source venv/bin/activate  
# On Windows, use venv\Scripts\activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Set Up Database**
```bash
python create_db.py
```

### **5. Set Up Google Maps API Key**

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Enable the **Google Maps JavaScript API** for your project.
4. Obtain your **API key** from the credentials page.
5. Add the API key to the `map.html` file under the `<script>` tag:

```html
<script async defer src="https://maps.googleapis.com/maps/api/js?key=YOUR_GOOGLE_MAPS_API_KEY&libraries=places&callback=initMap"></script>
```

### **6. Configure LlamaIndex and LLM Model**

1. **Set Up Ollama**  
   If you are using **Ollama** to run the model locally, ensure you have Ollama installed on your machine.  
   You can download and install Ollama from the [official Ollama website](https://ollama.com/).

2. **Run llama3.2:1b Model**  
   ```bash
   ollama run llama3.2:1b
   ```

### **7. Run the App**
```bash
streamlit run app.py
```
