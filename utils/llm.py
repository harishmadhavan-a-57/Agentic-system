from transformers import pipeline
from loguru import logger

# Load ONCE when the app starts — not on every request
# This is important: loading a model takes 5-10 seconds
_generator = None

def get_generator():
    global _generator
    if _generator is None:
        logger.info("Loading Flan-T5 model...")
        _generator = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",
            max_length=512
        )
        logger.info("Model loaded.")
    return _generator

def ask_llm(prompt: str) -> str:
    """
    Send a prompt to Flan-T5 and get a response.
    We wrap it here so if we ever switch models,
    we only change this one file.
    """
    try:
        gen = get_generator()
        result = gen(prompt, max_length=512, do_sample=False)
        return result[0]["generated_text"].strip()
    except Exception as e:
        logger.error(f"LLM error: {e}")
        return "I could not process that request."