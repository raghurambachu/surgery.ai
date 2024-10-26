import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
import logging


from chains import Chain
from utils import clean_text

def load_documents(urls):
    documents = []
    for url in urls:
        try:
            loader = WebBaseLoader([url])
            document = loader.load()
            cleaned_text = clean_text(document.pop().page_content)
            documents.append(cleaned_text)
        except Exception as e:
            logging.error(f"Error processing URL {url}: {str(e)}")
    return documents

def create_streamlit_app(llm):
    if "previous_queries" not in st.session_state:
        st.session_state["previous_queries"] = []

    if "query" not in st.session_state:
        st.session_state["query"] = ""

    previous_queries = st.session_state["previous_queries"]
    query = st.session_state["query"]

    st.title("orthoassist.ai (Roa)")
    body_part = st.selectbox("Select Body Part", ("Hip", "Knee","Shoulder","Ankle"))

    # Clear the query input and chat history when body part changes
    if body_part != st.session_state.get('last_body_part', None):
        st.session_state['previous_queries'] = []
        st.session_state['query'] = ""

    st.session_state['last_body_part'] = body_part

    query = st.text_input("Ask your query:", value=st.session_state["query"], key="query_input")
    submit_button = st.button("Submit")

    if body_part == "Hip":
        url_input = ["https://www.hss.edu/article_hip-replacement-recovery.asp"]
    elif body_part == "Knee":
        url_input = [
            "https://orthop.washington.edu/patient-care/articles/knee/total-knee-replacement-a-patients-guide.html"]
    elif body_part == "Shoulder":
        url_input = ["https://my.clevelandclinic.org/health/treatments/8290-shoulder-replacement"]
    elif body_part == "Ankle":
        url_input = ["https://www.hss.edu/condition-list_ankle-replacement-arthroplasty.asp"]
    else:
        url_input = []

    if submit_button:
        previous_queries.append({"is_user": True, "message": query})
        st.session_state["query"] = ""  # Clear the query input

        try:
            data = load_documents(url_input)
            response = llm.extract_patient_guide(data, query)
            previous_queries.append({"is_user": False, "message": response})
        except Exception as e:
            st.error(f"An Error Occurred: {e}")

    for query_data in previous_queries:
        is_user = query_data["is_user"]

        with st.container():
            col1, col2 = st.columns([1, 1])
            with col1:
                if is_user:
                    st.markdown(f"""
                        <div style="background-color: #333; border-radius: 10px; padding: 10px 20px; margin-bottom: 20px; position: relative;">
                            <div style="background-color: #333; position: absolute; top: 0; right: 0; width: 0; height: 0; border-top: 10px solid transparent; border-bottom: 10px solid transparent; border-left:   
 10px solid #333;"></div>
                            **You:** {query_data["message"]}
                        </div>
                    """, unsafe_allow_html=True)
            with col2:
                if not is_user:
                    st.markdown(f"""
                                            <div style="background-color: #333; border-radius: 10px; padding: 10px 20px; margin-bottom: 20px; position: relative;">
                                                <div style="background-color: #333; position: absolute; top: 0; left: 0; width: 0; height: 0; border-top: 10px solid transparent; border-bottom: 10px solid transparent; border-right:   
                     10px solid #333;"></div>
                                                **Roa:**  {query_data["message"]}
                                            </div>
                                        """, unsafe_allow_html=True)







if __name__ == "__main__":
    chain = Chain()
    st.set_page_config(layout="wide", page_title="orthoassist.ai ", page_icon="")
    create_streamlit_app(chain)




# import streamlit as st
# from langchain_community.document_loaders import WebBaseLoader
# import logging
#
#
# from chains import Chain
# from utils import clean_text
#
# def load_documents(urls):
#     documents = []
#     for url in urls:
#         try:
#             loader = WebBaseLoader([url])
#             document = loader.load()
#             cleaned_text = clean_text(document.pop().page_content)
#             documents.append(cleaned_text)
#         except Exception as e:
#             logging.error(f"Error processing URL {url}: {str(e)}")
#     return documents
#
# def create_streamlit_app(llm):
#     previous_queries = []
#
#     st.title("📔Surgery.ai ")
#     body_part = st.selectbox("Select Body Part", ("Hip", "Knee","Shoulder","Ankle"))
#     query = st.text_input("Ask your query:", value="")
#     submit_button = st.button("Submit")
#
#
#
#     if body_part == "Hip":
#         url_input = ["https://www.hss.edu/article_hip-replacement-recovery.asp"]
#     elif body_part == "Knee":
#         url_input = [
#             "https://orthop.washington.edu/patient-care/articles/knee/total-knee-replacement-a-patients-guide.html"]
#     elif body_part == "Shoulder":
#         url_input = ["https://my.clevelandclinic.org/health/treatments/8290-shoulder-replacement"]
#     elif body_part == "Ankle":
#         url_input = ["https://www.hss.edu/condition-list_ankle-replacement-arthroplasty.asp"]
#     else:
#         url_input = []
#
#     if submit_button:
#         previous_queries.append({"is_user": True, "message": query})
#         print(url_input)
#         try:
#             data = load_documents(url_input)
#             # print(data)
#             response = llm.extract_patient_guide(data, query)
#             # previous_queries.append({"is_user": False, "message": response})
#             #
#             st.write(response)
#
#             #
#             # for query_data in previous_queries:
#             #     is_user = query_data["is_user"]
#             #     if is_user:
#             #         st.write(f"""
#             #                     <div style="text-align: left;">
#             #                         **You:** {query_data["message"]}
#             #                     </div>
#             #                 """, unsafe_allow_html=True)
#             #     else:
#             #         st.write(f"""
#             #                     <div style="text-align: right;">
#             #                         **AI:** {query_data["message"]}
#             #                     </div>
#             #                 """, unsafe_allow_html=True)
#
#
#         except Exception as e:
#             st.error(f"An Error Occurred: {e}")
#
#
# if __name__ == "__main__":
#     chain = Chain()
#     st.set_page_config(layout="wide", page_title="Patient Guide", page_icon="📔")
#     create_streamlit_app(chain)