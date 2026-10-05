import os
from dotenv import load_dotenv
from langchain_core.language_models import BaseChatModel

load_dotenv()

def get_llm() -> BaseChatModel:
    """
    Initializes and returns the appropriate LLM instance based on environment variables.
    
    Supported Providers:
    - openai (uses OPENAI_API_KEY, OPENAI_MODEL or MODEL_NAME)
    - groq   (uses GROQ_API_KEY, GROQ_MODEL or MODEL_NAME)
    
    Defaults to 'openai' if OPENAI_API_KEY is present, or 'groq' if GROQ_API_KEY is present.
    """
    provider = os.getenv("LLM_PROVIDER", "").lower().strip()
    
    # Auto-detect provider if not explicitly specified
    if not provider:
        if os.getenv("OPENAI_API_KEY"):
            provider = "openai"
        elif os.getenv("GROQ_API_KEY"):
            provider = "groq"
        else:
            provider = "openai"  # Default fallback

    temperature = float(os.getenv("TEMPERATURE", "0.1"))

    if provider == "openai":
        from langchain_openai import ChatOpenAI
        model_name = os.getenv("OPENAI_MODEL") or os.getenv("MODEL_NAME") or "gpt-4o-mini"
        api_key = os.getenv("OPENAI_API_KEY")
        
        kwargs = {
            "model": model_name,
            "temperature": temperature,
        }
        if api_key:
            kwargs["api_key"] = api_key
            
        return ChatOpenAI(**kwargs)
        
    elif provider == "groq":
        from langchain_groq import ChatGroq
        model_name = os.getenv("GROQ_MODEL") or os.getenv("MODEL_NAME") or "llama-3.3-70b-versatile"
        api_key = os.getenv("GROQ_API_KEY")
        
        kwargs = {
            "model": model_name,
            "temperature": temperature,
        }
        if api_key:
            kwargs["groq_api_key"] = api_key
            
        return ChatGroq(**kwargs)
        
    else:
        raise ValueError(
            f"Unsupported LLM_PROVIDER: '{provider}'. Supported providers are 'openai' and 'groq'."
        )

llm = get_llm()