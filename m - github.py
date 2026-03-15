import os
import sys
from typing import List, Dict

import requests

try:
    from groq import Groq
except ImportError:
    Groq = None  


DEFAULT_MODEL = "llama-3.3-70b-versatile"


GROQ_API_KEY: str = "secretaf"


def ensure_groq_client() -> "Groq":
    """
    Groq istemcisini hazırlar.
    - pip: pip install groq
    - Tercihen: Bu dosyadaki GROQ_API_KEY sabitine anahtarı yaz
    """
    if Groq is None:
        print(
            "Hata: 'groq' paketi yüklü değil.\n"
            "Kurmak için:\n"
            "  pip install groq\n",
            file=sys.stderr,
        )
        sys.exit(1)

    
    api_key = GROQ_API_KEY or os.environ.get("GROQ_API_KEY")
    if not api_key:
        print(
            "Hata: Groq API anahtarı bulunamadı.\n"
            "Bu dosyada yukarıdaki GROQ_API_KEY değişkenine anahtarını yazman yeterli.",
            file=sys.stderr,
        )
        sys.exit(1)

    return Groq(api_key=api_key)


def web_search(query: str) -> str:
    """
    Wikipedia tabanlı basit web araması.
    Önce Türkçe Wikipedia'da, sonuç yoksa İngilizce'de dener.
    """
    def search_on_lang(lang: str):
        url = f"https://{lang}.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "srlimit": 3,
        }
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data.get("query", {}).get("search", [])

    try:
        results = search_on_lang("tr")
        lang_used = "tr"
        if not results:
            results = search_on_lang("en")
            lang_used = "en"
    except Exception as e:
        return f"Wikipedia arama hatası: {e}"

    if not results:
        return "Wikipedia'da uygun bir sonuç bulunamadı."

    lines: List[str] = []
    for r in results:
        title = r.get("title", "")
        snippet = r.get("snippet", "")
        page_url = f"https://{lang_used}.wikipedia.org/wiki/{title.replace(' ', '_')}"
       
        lines.append(f"- {title}\n  {snippet}\n  {page_url}")

    return "\n".join(lines)


def chat_once(
    client: "Groq",
    messages: List[Dict[str, str]],
    model: str = DEFAULT_MODEL,
) -> str:
    """
    Groq ile tek bir tamamlanma isteği atar.
    """
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return completion.choices[0].message.content


def interactive_chat(model: str = DEFAULT_MODEL) -> None:
    """
    Terminal üzerinden basit etkileşimli sohbet.
    """
    client = ensure_groq_client()

    print(
        f"Groq sohbeti başlıyor. Model: {model}\n"
        "Türkçe veya İngilizce soru sorabilirsin.\n"
        "Çıkmak için: /exit\n"
    )

    system_prompt = (
        "Sen yardımcı bir asistansın. "
        "2024 civarına kadar olan genel bilgilerle eğitilmiş bir Groq modelisin. "
        "Güncel olaylarda emin değilsen bunu açıkça söyle. "
        "Kullanıcı Türkçe konuşursa Türkçe, başka dilde konuşursa o dilde cevap ver."
    )

    messages: List[Dict[str, str]] = [
        {"role": "system", "content": system_prompt},
    ]

    while True:
        try:
            user_input = input("Sen: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGörüşürüz!")
            break

        if user_input.lower() in {"/exit", "exit", "quit", "/quit"}:
            print("Görüşürüz!")
            break

        if not user_input:
            continue

       
        if user_input.startswith("/web "):
            search_query = user_input[5:].strip()
            if not search_query:
                print("Kullanım: /web <arama metni>\n")
                continue

            print("Web'den bilgi alınıyor...\n")
            web_info = web_search(search_query)

            messages.append(
                {
                    "role": "system",
                    "content": (
                        "Aşağıda internette bulunan daha güncel bilgiler var. "
                        "Bu bilgileri kullanarak soruyu güncel olarak yanıtla:\n\n"
                        f"{web_info}"
                    ),
                }
            )
            messages.append({"role": "user", "content": search_query})
        else:
            messages.append({"role": "user", "content": user_input})

        try:
            answer = chat_once(client, messages, model=model)
        except Exception as e:
            print(f"Hata oluştu: {e}", file=sys.stderr)
           
            messages.pop()
            continue

        messages.append({"role": "assistant", "content": answer})
        print(f"AI: {answer}\n")


def main():

    model = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODEL
    interactive_chat(model=model)


if __name__ == "__main__":
    main()

