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
    "Delimiter Pattern": "Please summarise the following text 'There is a growing interest in understanding the role of genetics in explaining heterogeneity in behaviors, including those related to information systems (IS). The majority of the recent genetics research focuses on searching the entire genome in genome-wide association studies (GWASs) to link DNA to human traits. The results of GWASs can be used on datasets to compute a measure of genetic propensity known as a polygenic score, or PGS. PGSs are widely viewed as the future of genetics research. We conducted an exploratory study, in the context of information technology (IT) use, to examine if the PGS approach can be used to better understand the role of genetics in IS research. Consistent with our hypotheses, genetic endowments associated with Educational Attainment and General Cognition positively predict technology use, and genetic endowments associated with Neuroticism, Depressive Symptoms, Myocardial Infarction, and Coronary Artery Disease negatively predict technology use more than half a century later (genetic endowments are established at conception and our sample consists of individuals aged 50 to 80). Many of the characteristics known to be associated with heterogeneity in IT use (e.g., trust, education) appear to be mediators linking PGSs to IT use. Nonetheless, a number of PGSs maintain meaningful direct effects.'",
    "Assignment 1": "",
    "Few-Shot Pattern": """You are a Text Classifier indetifying 5 Propaganda Techniques within News Paper Articles. These are the 5 propaganda techniques you classify with definitions and examples:
    Loaded_Language - Uses specific phrases and words that carry strong emotional impact to affect the audience, e.g. 'a lone lawmaker’s childish shouting.'
    Exaggeration,Minimisation - Either representing something in an excessive manner or making something seem less important than it actually is, e.g. 'I was not fighting with her; we were just playing.'
    Appeal_to_Authority - Supposes that a claim is true because a valid authority or expert on the issue supports it, 'The World Health Organisation stated, the new medicine is the most effective treatment for the disease.'
    Slogans - A brief and striking phrase that contains labeling and stereotyping, e.g.  “Make America great again!”
    Doubt - Questioning the credibility of someone or something, e.g. 'Is he ready to be the Mayor?
    """,
    "Chain of Thought Pattern": "We are creating a online learning platform for students. We currently don't know how to design the platform. Please propose a initial design for the platform. Reason about your design and explain why each feature is important and which tech stack we could use.",
    "ReAct Pattern": "",
    "Assignment 2": "",
    "Condition Pattern": "We created a survey to collect feedback from our users of our prototype. We will pass the results of a survey to you. Please return only concrete improvement suggestions for our prototype and else return 'no suggestions'.",
    "Refinement Pattern": "We are designing a interview process. We will give you information about the interview process and then we will show you questions asked by the interviewer. Please give feedback on the questions, suggest improvements and propose a better version of the pattern.",
    "Interactive Problem Solving Pattern": "", #difference to prior pattern?
    "Assignment 3": "",
    "Structured Data Pattern": "Looking at the given transcripts please extract name, age, profession and location of the interviewee. Please return the extracted information in a structured format I prefer .csv.", 
    "Assignment 4": "",
    "Recipe Pattern": "Could you outline the steps for conducting a systematic literature review?",
    "Outline Expansion Pattern": "You are an outline expander please give bullet points about the 'The Impact of Large Language Models on Information Systems'. Please give 5 bullet points. I will then ask you to expand on one of the bullet points.",
    "Fact Check List Pattern": None, #TODO
    "Assignment 5": "",
    "Game Play + Meta Language + Semantic Filter Pattern": None
}

def init():
    # Load the OpenAI API key from the environment variable
    from dotenv import load_dotenv
    load_dotenv()
    
def main():
    init()

    # sidebar to choose prompt patterns
    with st.sidebar:
        prompt_type = st.selectbox("Choose Prompt Pattern", 
                                   prompt_patterns.keys(), 
                                    key="prompt_type")

        # Check if prompt type is changed
        if st.session_state.get('current_prompt_type') != prompt_type:
            # Clear chat history
            st.session_state.messages = []

        # Update current prompt type
        st.session_state.current_prompt_type = prompt_type

    chat = ChatOpenAI(temperature=0)

    st.header("The coolest Prompt Engineering Workshop in the World 🤖")

    user_input = st.text_area("Your message: ", value=prompt_patterns[prompt_type], key="user_input")

    # handle user input
    if st.button("Send"):
        print(user_input)
        if user_input:
            st.session_state.messages.append(HumanMessage(content=user_input))
            with st.spinner("Thinking..."):
                response = chat(st.session_state.messages)
            st.session_state.messages.append(
                AIMessage(content=response.content))

    # display message history
    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages):
        if i % 2 == 0:
            message(msg.content, is_user=True, key=str(i) + '_user')
        else:
            message(msg.content, is_user=False, key=str(i) + '_ai')


if __name__ == '__main__':
    main()
