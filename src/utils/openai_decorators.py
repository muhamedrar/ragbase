import logging
from functools import wraps
import openai

logger = logging.getLogger("uvicorn.error")

def handle_openai_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except openai.RateLimitError as e:
            logger.error(
                f"Background Task Failed] OpenAI API Rate Limit Exceeded in {func.__name__}.\n"
                f"Details: {e.message}\n"
                f"Action Required: Check your trial tier thresholds or upgrade keys."
            )
            return None  
            
        except openai.AuthenticationError as e:
            logger.critical(f"[Background Task Failed] OpenAI Authentication Broken: {e}")
            return None
            
        except openai.BadRequestError as e:
            logger.error(f"[Background Task Failed] Invalid payload formatting sent to OpenAI: {e.message}")
            return None
            
        except (openai.APIConnectionError, openai.APIError) as e:
            logger.error(f"[Background Task Failed] OpenAI Network / API connectivity dropped: {e}")
            return None
            
        except Exception as e:
            logger.exception(f"[Background Task Failed] Unexpected failure inside background processor: {e}")
            return None
            
    return wrapper