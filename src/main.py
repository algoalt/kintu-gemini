import openai
from .utils import get_static_file, throw_if_missing
import os
import google.generativeai as genai

def main(context):
    throw_if_missing(os.environ, ["OPENAI_API_KEY"])

    if context.req.method == "GET":
        return context.res.send(
            get_static_file("index.html"),
            200,
            {
                "content-type": "text/html; charset=utf-8"
            },
        )

    try:
        throw_if_missing(context.req.body, ["prompt"])
    except ValueError as err:
        return context.res.json({"ok": False, "error": err.message}, 400)

    gemini_key = os.environ["OPENAI_API_KEY"]

    try:
        #response = openai.ChatCompletion.create(
        #    model="gpt-3.5-turbo",
        #    max_tokens=int(os.environ.get("OPENAI_MAX_TOKENS", "512")),
        #    messages=[{"role": "user", "content": context.req.body["prompt"]}],
        #)
        #completion = response.choices[0].message.content
        genai.configure(api_key = gemini_key)
        gemini_model = genai.GenerativeModel("gemini-pro")
        chat = gemini_model.generate_content("who is Jesus")
        return context.res.json({"ok": True, "completion": chat.text}, 200)

    except Exception:
        return context.res.json({"ok": False, "error": "Failed to query model."}, 500)
