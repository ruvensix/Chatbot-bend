import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv # Para carregar variáveis de ambiente
import requests # Para fazer chamadas HTTP para as APIs dos LLMs
from flask_cors import CORS # Necessário para permitir requisições do frontend

# Carregar variáveis de ambiente do ficheiro .env
load_dotenv()

app = Flask(__name__)
CORS(app) # Habilitar CORS para permitir que o frontend (netlify/vercel) se conecte

# --- Configuração das API Keys (do .env) ---
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# --- Definição das Personas e seus Prompts ---
# Cada persona terá um "system message" que define o seu comportamento
PERSONAS = {
    "movie_expert": {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1", # Exemplo de modelo para Together.ai ou OpenRouter
        "base_url": "https://api.together.xyz/v1/chat/completions", # Together.ai URL
        "api_key": TOGETHER_API_KEY,
        "system_message": "Você é um perito em cinema, com conhecimento enciclopédico sobre filmes, atores, diretores, géneros, história do cinema e curiosidades. Responda de forma entusiasta e informativa, como se estivesse a partilhar a sua paixão pelo cinema. Seja conciso mas abrangente.",
        "headers": {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }
    },
    "travel_guide": {
        "model": "llama3-8b-8192", # Exemplo de modelo para Groq
        "base_url": "https://api.groq.com/openai/v1/chat/completions", # Groq URL
        "api_key": GROQ_API_KEY,
        "system_message": "Você é um guia de viagens experiente e amigável. Forneça conselhos práticos, sugestões de destinos, dicas culturais e informações úteis para viajantes. Use uma linguagem inspiradora e encorajadora. Foco em Portugal.",
        "headers": {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
    },
    "technical_assistant": {
        "model": "google/gemini-pro-1.5", # Exemplo de modelo para OpenRouter (ou pode ser Together/Groq)
        "base_url": "https://openrouter.ai/api/v1/chat/completions", # OpenRouter URL
        "api_key": OPENROUTER_API_KEY,
        "system_message": "Você é um assistente técnico preciso e conciso. Forneça explicações claras, instruções passo a passo e resolva problemas técnicos de forma lógica. Evite divagações e vá direto ao ponto.",
        "headers": {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://chatbot-backend-3xcv.onrender.com/", # Substitua pela URL do seu frontend (ex: https://your-chatbot.netlify.app)
            "X-Title": "My Awesome Chatbot"
        }
    }
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    persona_id = data.get("persona")

    if not user_message or not persona_id:
        return jsonify({"error": "Mensagem ou persona em falta."}), 400

    persona_config = PERSONAS.get(persona_id)
    if not persona_config:
        return jsonify({"error": "Persona inválida."}), 400

    # Adicionar o histórico de chat à mensagem para contexto (se existir)
    # Por simplicidade, neste exemplo, vamos apenas enviar a mensagem atual e a system_message.
    # Para um histórico real, o frontend precisaria enviar o array de mensagens anteriores.
    messages = [
        {"role": "system", "content": persona_config["system_message"]},
        {"role": "user", "content": user_message}
    ]

    payload = {
        "model": persona_config["model"],
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 500
    }

    try:
        response = requests.post(
            persona_config["base_url"],
            headers=persona_config["headers"],
            json=payload
        )
        response.raise_for_status() # Levanta um erro para bad status codes (4xx ou 5xx)
        llm_response = response.json()
        
        # Extrair a resposta do LLM, pode variar ligeiramente entre as APIs
        if llm_response and llm_response.get('choices') and llm_response['choices'][0].get('message'):
            return jsonify({"response": llm_response['choices'][0]['message']['content']})
        else:
            print(f"Erro: Resposta inesperada do LLM: {llm_response}")
            return jsonify({"error": "Resposta inesperada do LLM."}), 500

    except requests.exceptions.RequestException as e:
        print(f"Erro ao chamar a API do LLM ({persona_id}): {e}")
        return jsonify({"error": f"Erro ao comunicar com a API do LLM: {e}"}), 500
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return jsonify({"error": f"Ocorreu um erro interno: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)