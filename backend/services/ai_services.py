from services.vector_services import search_similar_news
from services.llm_services import generate_response
from services.chat_services import save_chat




def get_ai_news(query, user_id):
    results = search_similar_news(query)

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    context = "\n\n".join(documents)

    try:
        answer = generate_response(context + "\n\n" + query)

        if "Error" in answer:
            raise Exception("LLM failed")

    except:
        return {
            "answer": "Here are the most relevant news articles:",
            "sources": metadatas
        }
    
    save_chat(user_id, query, answer)

    return {
        "answer": answer,
        "sources": metadatas
    }

