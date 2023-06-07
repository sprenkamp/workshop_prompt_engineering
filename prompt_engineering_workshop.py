import streamlit as st
from streamlit_chat import message
# from dotenv import load_dotenv
import os

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

prompt_patterns = {
    "Persona Pattern": "Imagine you are being interviewed by an Information Systems PhD doing research on the used-car market. Please respond in an authentic manner, please criticise the interview if you think the question asked are not senseful to you.",
    "Delimiter Pattern": "You are a student in a class. You are asked to write a report on the topic of 'How to write a good report'. Please write a report on this topic.",
    "Assignment 1": None,
    "Few-Shot Pattern": """You are a Text Classifier indetifying 14 Propaganda Techniques within News Paper Articles. These are the 14 propaganda techniques you classify with definitions and examples:
    Loaded_Language - Uses specific phrases and words that carry strong emotional impact to affect the audience, e.g. 'a lone lawmaker’s childish shouting.'
    Name_Calling,Labeling - Gives a label to the object of the propaganda campaign as either the audience hates or loves, e.g. 'Bush the Lesser.'
    Repetition -  Repeats the message over and over in the article so that the audience will accept it, e.g. 'Our great leader is the epitome of wisdom. Their decisions are always wise and just.'
    Exaggeration,Minimisation - Either representing something in an excessive manner or making something seem less important than it actually is, e.g. 'I was not fighting with her; we were just playing.'
    Appeal_to_fear-prejudice - Builds support for an idea by instilling anxiety and/or panic in the audience towards an alternative, e.g. 'stop those refugees; they are terrorists.'
    Flag-Waving; Playing on strong national feeling (or with respect to a group, e.g., race, gender, political preference) to justify or promote an action or idea, e.g. 'entering this war will make us have a better future in our country.'
    Causal_Oversimplification -  Assumes a single reason for an issue when there are multiple causes, e.g. 'If France had not declared war on Germany, World War II would have never happened.'
    Appeal_to_Authority - Supposes that a claim is true because a valid authority or expert on the issue supports it, 'The World Health Organisation stated, the new medicine is the most effective treatment for the disease.'
    Slogans - A brief and striking phrase that contains labeling and stereotyping, e.g.  “Make America great again!”
    Thought-terminating_Cliches -  Words or phrases that discourage critical thought and useful discussion about a given topic, e.g. “it is what it is”
    Whataboutism,Straw_Men,Red_Herring - Attempts to discredit an opponent’s position by charging them with hypocrisy without directly disproving their argument, e.g. 'They want to preserve the FBI’s reputation.'
    Black-and-White_Fallacy -  Gives two alternative options as the only possibilities, when actually more options exist, e.g. 'You must be a Republican or Democrat'
    Bandwagon,Reductio_ad_hitlerum - Justify actions or ideas because everyone else is doing it, or reject them because it's favored by groups despised by the target audience, e.ag. “Would you vote for Clinton as president? 57% say yes.
    Doubt - Questioning the credibility of someone or something, e.g. 'Is he ready to be the Mayor?
    """,
    "Chain of Thought Pattern": "We are creating a online learning platform for students. We currently don't know how to design the platform. Please propose a initial design for the platform. Reason about your design and explain why each feature is important and which tech stack we could use.",
    "ReAct Pattern": "",
    "Assignment 2": None,
    "Condition Pattern": "We created a survey to collect feedback from our users of our prototype. We will pass the results of a survey to you. Please return only concrete improvement suggestions for our prototype and else return 'no suggestions'.",
    "Refinement Pattern": "We are designing a interview process. We will give you information about the interview process and then we will show you questions asked by the interviewer. Please give feedback on the questions, suggest improvements and propose a better version of the pattern.",
    "Interactive Problem Solving Pattern": "", #difference to prior pattern?
    "Assignment 3": None,
    "Structured Data Pattern": "Looking at the given transcripts please extract name, age, profession and location of the interviewee. Please return the extracted information in a structured format I prefer .csv.", 
    "Assignment 4": None,
    "Recipe Pattern": "Could you outline the steps for conducting a systematic literature review?",
    "Outline Expansion Pattern": "You are an outline expander please give bullet points about the 'The Impact of Large Language Models on Information Systems'. Please give 5 bullet points. I will then ask you to expand on one of the bullet points.",
    "Fact Check List Pattern": None, #TODO
    "Assignment 5": None,
    "Game Play + Meta Language + Semantic Filter Pattern": None
}

def init():
    # Load the OpenAI API key from the environment variable
    from dotenv import load_dotenv

def main():
    # init()

    # sidebar to choose prompt patterns
    with st.sidebar:
        prompt_type = st.selectbox("Choose Prompt Pattern", 
                                   prompt_patterns.keys(), 
                                    key="prompt_type")

    chat = ChatOpenAI(temperature=0)

    # initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
        ]

    st.header("The coolest Prompt Engineering Workshop in the World 🤖")

    user_input = st.text_area("Your message: ", value=prompt_patterns[prompt_type], key="user_input")

    # handle user input
    if user_input:
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("Thinking..."):
            response = chat(st.session_state.messages)
        st.session_state.messages.append(
            AIMessage(content=response.content))

    # display message history
    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            message(msg.content, is_user=True, key=str(i) + '_user')
        else:
            message(msg.content, is_user=False, key=str(i) + '_ai')


if __name__ == '__main__':
    main()