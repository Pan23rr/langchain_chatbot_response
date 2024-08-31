import os
import getpass
from langchain_core.chat_history import(
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq


os.environ["GROQ_API_KEY"]='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'
model=ChatGroq(model="llama3-8b-8192")


store={}

def session_history(session_id:str)->BaseChatMessageHistory:
    if session_id not in store:
        store[session_id]=InMemoryChatMessageHistory()
    return store[session_id]

with_message_history=RunnableWithMessageHistory(model,session_history)

config={"configurable":{"session_id":"abc2"}}

prompt=ChatPromptTemplate.from_messages(
    [
    (
        "system",
        """Predefined Question-Answer Set:

Question: What is the process for changing a train ticket date?
Answer: To change the date of your train ticket, visit the official IRCTC website or app. Log in to your account, navigate to the "Booked Tickets" section, select the ticket you wish to modify, and choose the option to change the journey date. Please note that date changes are subject to availability and specific conditions, and additional charges may apply.

Question: How can I check the PNR status of my train ticket?
Answer: You can check the PNR status of your train ticket by visiting the IRCTC website, using the IRCTC mobile app, or sending an SMS with your PNR number to the designated railway inquiry number. Additionally, you can check the status at the railway station's inquiry counter or through various third-party apps and websites that offer PNR status checking services.

Question: What should I do if my train is delayed?
Answer: If your train is delayed, you can take the following steps: Stay informed by checking the live train status through the IRCTC website or mobile app. If the delay is significant and you wish to cancel your journey, you may be eligible for a full refund. Alternatively, if the delay is more than three hours, you can file for a refund even after the scheduled departure. Always keep your ticket and PNR number handy when seeking assistance.

Question: How do I get a refund for a canceled ticket?
Answer: To get a refund for a canceled train ticket, log in to your IRCTC account, go to the "Booked Tickets" section, and find the ticket you want to cancel. Follow the prompts to cancel the ticket. Refunds are processed according to the IRCTC refund policy, which depends on the time of cancellation relative to the train's departure. The refund amount will be credited back to the payment method used during booking.

Question: Can I modify the passenger details after booking?
Answer: Yes, you can modify certain passenger details after booking, such as the name or age of a passenger. To do this, visit a railway reservation office with a printout of the e-ticket and a valid ID proof of the passenger. Modifications must be made at least 24 hours before the train's scheduled departure. Note that only one modification per ticket is allowed, and certain conditions apply.User Query: Users will likely ask questions related to train ticket reservations, modifications, refunds, status checks, or issues they might encounter during their journey. These queries may vary in phrasing but should relate to the above predefined questions.

Question: What should I do if the food served on the train is of poor quality?
Answer: If you encounter poor-quality food on the train, you can file a complaint through the IRCTC app or website. Please provide a detailed description of the issue and attach an image of the food for verification. This will help us address the problem more effectively and ensure that appropriate actions are taken.

Question: How can I report unclean toilets or compartments during my journey?
Answer: To report unclean toilets or compartments, please use the IRCTC app or website's complaint section. Attach an image of the unclean area and provide a brief description of the issue. Our team will work to resolve the problem as soon as possible to ensure a more comfortable journey for all passengers.

Question: What steps should I take if I witness an accident or safety issue on the train?
Answer: If you witness an accident or any safety issue on the train, immediately inform the train staff or contact the railway helpline number. Additionally, you can report the incident through the IRCTC app or website. Please include a description of the event and attach any relevant images to help us respond quickly and appropriately.

Question: How do I complain about loud or disruptive passengers in my compartment?
Answer: To report loud or disruptive passengers, you can file a complaint using the IRCTC app or website. Please describe the situation in detail and, if possible, attach an image to support your complaint. The railway authorities will take the necessary actions to ensure a peaceful journey for all passengers.

Question: What can I do if I find pests or insects in my train compartment?
Answer: If you find pests or insects in your train compartment, report the issue immediately through the IRCTC app or website. Attach an image of the pests or insects and provide a brief description of the problem. This will help our cleaning staff take swift action to resolve the issue and maintain a hygienic environment on the train.

Response Template:

If the user's query directly relates to one of the predefined questions, generate a response using the relevant answer from the predefined set.
If the user's query does not relate to any of the predefined questions, respond with: "We can't handle this request."
Guidelines for Relevance:

The model should first attempt to match the user’s query to the closest predefined question. This match should consider synonyms, related terms, and common phrasing variations.
If the query matches sufficiently, generate a response using the associated answer.
If no match is found, or the query is outside the scope of the predefined questions, the model should output, "We can't handle this request.""",
    ),
    MessagesPlaceholder("messages"),
    ]
)


chain=prompt | model

response=chain.invoke(
    [HumanMessage(content="How can i book a ticket from delhi to bombay")],
    config=config,
)

print(response.content)

response=chain.invoke(
    [HumanMessage(content="what did i ask you earliar")],
    config=config,
)

print(response.content)