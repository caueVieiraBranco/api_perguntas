import requests

# === CONFIGURAÇÕES ===
CLIENT_ID = '6439275970401699'
CLIENT_SECRET = 'Pw9VVyEx4Wj3iYSeNFVvCWSd44I1j7hZ'
REFRESH_TOKEN = 'TG-685eefa4befee4000139f1cc-162089212'

def obter_access_token():
    print("🔄 Atualizando access_token...")
    token_url = "https://api.mercadolibre.com/oauth/token"
    payload = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN
    }
    response = requests.post(token_url, data=payload)
    response.raise_for_status()
    return response.json()['access_token']

def buscar_perguntas_nao_respondidas(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Obter ID do usuário
    user_response = requests.get("https://api.mercadolibre.com/users/me", headers=headers)
    user_response.raise_for_status()
    user_id = user_response.json()['id']
    
    print(f"🔎 Buscando perguntas não respondidas para o usuário {user_id}...")
    
    url = f"https://api.mercadolibre.com/questions/search?seller_id={user_id}&status=UNANSWERED"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    perguntas = response.json().get("questions", [])
    
    if not perguntas:
        print("✅ Nenhuma pergunta pendente.")
        return
    
    for p in perguntas:
        print("\n🆕 Pergunta recebida:")
        print(f"➡️ Texto: {p['text']}")
        print(f"🆔 Pergunta ID: {p['id']}")
        print(f"📦 Anúncio ID: {p['item_id']}")

if __name__ == "__main__":
    try:
        token = obter_access_token()
        buscar_perguntas_nao_respondidas(token)
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
