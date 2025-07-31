# 🧠 Multi-Persona Chatbot with LLMs

This project is an academic implementation of a **multi-persona chatbot** developed for the course **Organizational Learning / Decision Support Systems**, part of the **Bachelor’s Degree in Computer Engineering** (ESTG | IPVC). It utilizes **free Large Language Model (LLM) APIs** to create **domain-specific chatbots**.

## 📌 Project Goals

- Develop and implement **specialized chatbots** using **free LLM APIs**.
- Explore **prompt engineering** to define different personas:
  - 🎬 Movie Expert
  - 🌍 Travel Assistant
  - 🛠️ Technical Assistant
- Demonstrate the real-world value of LLMs in everyday interactions.
- Build a **visually appealing solution**, deployed using **Render**.

## 🧩 Technologies Used

- **Python** with **Flask**
- LLM API integration via:
  - [Together.ai](https://docs.together.ai/)
  - [Groq](https://console.groq.com/docs/)
  - [OpenRouter](https://openrouter.ai/docs)
- **Render** for web deployment
- **.env** file for managing API keys and environment variables

## 🧠 Implemented Personas

| Persona              | Platform Used         | Description                                                       |
|----------------------|-----------------------|-------------------------------------------------------------------|
| 🎬 Movie Expert       | Together.ai           | Answers questions about films, actors, and provides recommendations |
| 🌍 Travel Assistant   | Groq                  | Assists with travel planning, destinations, and budgets          |
| 🛠️ Technical Assistant| OpenRouter            | Offers technical support and explanations on computing topics     |

## 🚀 How to Run Locally

1. Clone this repository:
   ```bash
   git clone https://github.com/ruvensix/Chatbot-bend
   cd Chatbot-bend
   ```

2. Create a `.env` file with your API keys:
   ```env
   TOGETHER_API_KEY=your_together_api_key
   GROQ_API_KEY=your_groq_api_key
   OPENROUTER_API_KEY=your_openrouter_api_key
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask server:
   ```bash
   python app.py
   ```

## 🌐 Deployment

The project is deployed on [Render](https://render.com), with environment variables configured in the dashboard.

## 📸 Sample Results

- **Movie Expert**: Contextual responses and tailored recommendations about cinema.
- **Travel Assistant**: Custom destination suggestions and itinerary generation.
- **Technical Assistant**: Real-time technical support with clear explanations.

## 📚 References

- [OpenAI API](https://platform.openai.com/docs/)
- [Together.ai Docs](https://docs.together.ai/)
- [Groq Console Docs](https://console.groq.com/docs/)
- [OpenRouter Docs](https://openrouter.ai/docs/)
- Academic and technical references included in the original project PDF.

## 👨‍💻 Author

- **Ruben Eduardo Gramoso Ferreira** (ID: 21617)  
  [reduardoferreira@ipvc.pt](mailto:reduardoferreira@ipvc.pt)
