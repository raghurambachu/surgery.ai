import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain

from utils import clean_text

def create_streamlit_app(llm):
    previous_queries = []

    st.title("📔Surgery.ai ")
    body_part = st.selectbox("Select Body Part", ("Hip", "Knee","Shoulder"))
    query = st.text_input("Ask your query:", value="")
    submit_button = st.button("Submit")

    if body_part == "Hip":
        url_input = "https://www.hss.edu/article_hip-replacement-recovery.asp"
    if body_part == "Shoulder":
        url_input = "https://my.clevelandclinic.org/health/treatments/8290-shoulder-replacement"
    else:
        url_input = "https://orthop.washington.edu/patient-care/articles/knee/total-knee-replacement-a-patients-guide.html"

    if submit_button:
        previous_queries.append({"is_user": True, "message":query })
        try:
            loader = WebBaseLoader([url_input])
            data = loader.load().pop().page_content
            response = llm.extract_patient_guide(data,query)

            previous_queries.append({"is_user":False,"message" :response})

            st.write(response)

            #
            # for query_data in previous_queries:
            #     is_user = query_data["is_user"]
            #     if is_user:
            #         st.write(f"""
            #                     <div style="text-align: left;">
            #                         **You:** {query_data["message"]}
            #                     </div>
            #                 """, unsafe_allow_html=True)
            #     else:
            #         st.write(f"""
            #                     <div style="text-align: right;">
            #                         **AI:** {query_data["message"]}
            #                     </div>
            #                 """, unsafe_allow_html=True)


        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    st.set_page_config(layout="wide", page_title="Patient Guide", page_icon="📔")
    create_streamlit_app(chain)