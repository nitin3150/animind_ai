import os
import time
import logging
from litellm import completion,RateLimitError,APIConnectionError,TimeoutError
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

retry_delay = [2,4,6]

def llm(system_prompt:str, user_input:str) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("MODEL","openrouter/stepfun/step-3.5-flash:free")
    last_err = None

    for attempt, delay in enumerate(retry_delay,1):
        try:
            response = completion(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": user_input},
                ],
                api_key=api_key,
                timeout = 45
            )
            return response.choices[0].message.content
        except (RateLimitError,TimeoutError,APIConnectionError) as e:
            last_err = e
            logger.warning(f"LLM attempt {attempt} failed: {e} retrying in {delay} seconds")
            time.sleep(delay)
        except Exception as e:
            logger.error(f"LLM attempt error {e}")
            raise RuntimeError(f"LLM failed after {len(retry_delay)} attempts")
    
    raise RuntimeError(f"LLM failed after {len(retry_delay)} attempts")
            