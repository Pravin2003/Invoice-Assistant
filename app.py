import os
from flask import Flask, request, jsonify
from flask import Flask, render_template, request, jsonify
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
import google.generativeai as genai
from langchain.schema.output_parser import StrOutputParser

app = Flask(__name__)

# Retrieve the Google API key from environment variables
google_api_key = os.getenv("GOOGLE_API_KEY")

# Check if the API key is set
if google_api_key is None:
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

# Load and process the PDF 
file_path = "sample/sample-invoice.pdf" #Upload your file here
loader = PyPDFLoader(file_path)
docs = loader.load()

# Set up the embeddings and vectorstore
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectorstore = Chroma.from_documents(documents=docs, embedding=embeddings)
retriever = vectorstore.as_retriever()

# Define the knowledge base with invoice-related information
knowledge_base = {
    "invoice_number": "A unique identifier assigned to each invoice for tracking and reference purposes.",
    "order_number": "A unique identifier assigned to the customer's order.",
    "order_date": "The date when the order was placed by the customer.",
    "invoice_date": "The date when the invoice was generated.",
    "seller": {
        "name": "The name of the business selling the product or service.",
        "pan_number": "The seller's Permanent Account Number (PAN) for tax purposes.",
        "gst_number": "The seller's Goods and Services Tax (GST) number.",
        "address": "The physical address of the seller."
    },
    "billing_address": "The address provided by the customer for billing purposes.",
    "shipping_address": "The address where the goods are to be delivered.",
    "place_of_supply": "The state or union territory where the goods are supplied.",
    "item_details": {
        "description": "The description of the item purchased.",
        "code_number": "The code number (HSN) associated with the item.",
        "hsn_number": "HSN stands for Harmonized System of Nomenclature. It is a globally standardized system of names and numbers used to classify traded products.",
        "unit_price": "The price per unit of the item.",
        "quantity": "The number of units purchased.",
        "total_price": "The total cost of the item before taxes.",
        "tax_rate": "The percentage of tax applied.",
        "tax_amount": "The amount of tax charged on the item.",
        "final_amount": "The final amount payable for the item including tax."
    },
    "shipping_charges": "The cost of shipping the item, after any discounts.",
    "reverse_charge": "Indicates whether tax is payable under reverse charge.",
    "amount_in_words": "The total amount due, expressed in words."
}

# Define the system prompt used for generating responses
system_prompt = """
Context: {context}

You are a document analysis assistant specializing in invoices. Your primary task is to extract accurate and relevant information directly from the provided invoice.

Focus solely on the invoice content to answer the user's question. 

If the information is not present in the invoice, inform the user that the requested information is not available.

**Provide answers in a clear and concise format. Use bullet points or numbered lists where appropriate.**

If the user's question requires calculations, comparisons, or summaries based on invoice data, provide a quantitative response.

If the user's question is vague or requests general information about invoices, provide definitions, explanations, or examples related to invoice components.

User Question: {question}
"""

# Function to generate answers using LLM
def llm_ans(chat_input, history, knowledge_base):
    global system_prompt
    prompt2 = f"""{system_prompt}\n {history}"""
    prompt = ChatPromptTemplate.from_template(prompt2)  

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
    chain = (
        {"context": retriever, "knowledge_base": lambda _: str(knowledge_base), "question": lambda x: x}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain.invoke(chat_input)

# Define the route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Define the route to handle user questions
@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get("question")
    history = data.get("history", [])
    
    try:
        response = llm_ans(question, history, knowledge_base)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
