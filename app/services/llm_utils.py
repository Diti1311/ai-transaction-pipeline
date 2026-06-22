import time


def retry_llm(fn, *args):

    delay = 1

    for attempt in range(3):

        try:

            return fn(*args)

        except Exception as e:

            print(
                f"LLM attempt {attempt + 1} failed: {e}"
            )

            time.sleep(delay)

            delay *= 2

    return None