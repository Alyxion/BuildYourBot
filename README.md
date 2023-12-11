# 🤖 BuildYourBot 🤖

This repository contains several very basic examples about how to build a basic chatbot 
using the OpenAI API which tracks your chat history, summarizes it if needed, restores 
the history, and then continues the conversation, tracks the costs and token usage etc.

In addition it provides a very basic console app which can be used to test the API and
behaves like a math teacher. Feel free to write your own prompts and experiment with
it.

![img.png](assets/console_screenshot.png)

---

## Installation

* Install Python 3.10 or above
* Install poetry: `pip install poetry`
* Install dependencies: `poetry install`

---

## Configuration

* Create an OpenAI account and get an API key
* Create a `.env` file in the root of the project and add the following:

### OpenAI

```
OPENAI_KEY=YOUR_KEY_HERE
OPENAI_API_VERSION=2023-05-15
OPENAI_BASE_MODEL=gpt-35-turbo
# GPT 3.5-Turbo as of 2023-12. The pricing if you want to track it
OPENAI_COSTS_PER_1K_IN=0.001
OPENAI_COSTS_PER_1K_OUT=0.002
```

### Azure

```
OPENAI_KEY=YOUR_KEY_HERE
OPENAI_AZURE_ENDPOINT=https://YOUR_ENDPOINT.openai.azure.com/
OPENAI_API_VERSION=2023-05-15
OPENAI_BASE_MODEL=YOUR_DEPLOYMENT_NAME_NOT_THE_MODEL
# GPT 3.5-Turbo as of 2023-12. The pricing if you want to track it
OPENAI_COSTS_PER_1K_IN=0.001
OPENAI_COSTS_PER_1K_OUT=0.002
```

## Demo Apps

### Console

* Run `poetry run python oaisamples/console_bot/console_bot.py`

## License

The code is licensed under the MIT license. See [LICENSE](LICENSE) for more information.