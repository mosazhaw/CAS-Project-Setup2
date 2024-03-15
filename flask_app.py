import os
from flask import Flask, jsonify, render_template, request, send_file

from chatbot.chatbot import Chatbot

PYTHONANYWHERE_USERNAME = "carvice"
PYTHONANYWHERE_WEBAPPNAME = "mysite"

app = Flask(__name__)

my_type_role = """
   As your dedicated digital assistant, I'm here to facilitate the ordering of products and services necessary for your daily activities and duties at work. My role is to guide you towards making the best choices for smartphones and IT hardware through the ServiceNow platform. For needs outside these categories, I will direct you to your assigned purchaser.

Available Products:

Smartphones (Policy: One smartphone every two years, simulate a function call to retrieve user's status):
- Samsung S23
- iPhone 15
- Google Pixel 7 5G
IT Hardware:
- Privacy screens for laptops
- Mice
- External keyboards for laptops
Guidelines:
- My assistance is strictly for business-related needs. I cannot facilitate orders for personal products or services.
- Please make your selection carefully, keeping in mind our company's policies and your specific needs.
- Always be mindful of our core values: Responsibility and Respect.
- Always answer in user prompt language and use the Du-form.
- Never ask for personal details, only employee number. 
"""

my_instance_context = """
      The user is an assistant and often order Workplace Hardware and software package for new employees.
   Always enforce the following rules: 
   In category Mouse, the current employee can only orders 3 mouses: Mex Master, Micro Ergomaus, Dello Standard Maus
   In category Software: the current logged in employee can only order Visio
   In category Laptop, The current logged in employee can only order 2 laptop: 14 inch and 16 inch laptop.
"""

my_instance_starter = """
 greet the user. in german.
"""

bot = Chatbot(
    database_file="database/chatbot.db", 
    type_id="demo",
    user_id="demo",
    type_name="Health Coach",
    type_role=my_type_role,
    instance_context=my_instance_context,
    instance_starter=my_instance_starter
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/mockups.pdf', methods=['GET'])
def get_first_pdf():
    script_directory = os.path.dirname(os.path.realpath(__file__))
    files = [f for f in os.listdir(script_directory) if os.path.isfile(os.path.join(script_directory, f))]
    pdf_files = [f for f in files if f.lower().endswith('.pdf')]
    if pdf_files:
        # Get the path to the first PDF file
        pdf_path = os.path.join(script_directory, pdf_files[0])

        # Send the PDF file as a response
        return send_file(pdf_path, as_attachment=True)

    return "No PDF file found in the root folder."

@app.route("/<type_id>/<user_id>/chat")
def chatbot(type_id: str, user_id: str):
    return render_template("chat.html")


@app.route("/<type_id>/<user_id>/info")
def info_retrieve(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    response: dict[str, str] = bot.info_retrieve()
    return jsonify(response)


@app.route("/<type_id>/<user_id>/conversation")
def conversation_retrieve(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    response: list[dict[str, str]] = bot.conversation_retrieve()
    return jsonify(response)


@app.route("/<type_id>/<user_id>/response_for", methods=["POST"])
def response_for(type_id: str, user_id: str):
    user_says = None
    # content_type = request.headers.get('Content-Type')
    # if (content_type == 'application/json; charset=utf-8'):
    user_says = request.json
    # else:
    #    return jsonify('/response_for request must have content_type == application/json')

    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    assistant_says_list: list[str] = bot.respond(user_says)
    response: dict[str, str] = {
        "user_says": user_says,
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)


@app.route("/<type_id>/<user_id>/reset", methods=["DELETE"])
def reset(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    bot.reset()
    assistant_says_list: list[str] = bot.start()
    response: dict[str, str] = {
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)
