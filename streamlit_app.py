import json
import time
import random
import requests
import pandas as pd
import streamlit as st

tokens = st.secrets["TOKENS"]
password = st.secrets["PASSWORD"]
host_api = st.secrets["HOST"]
main_engine = st.secrets["MAIN_ENGINE"]
instance_id = st.secrets["INSTANCE_ID"]
file_path = st.secrets["FILE_PATH"]


with open("./materi_teknis.json", 'r') as file:
    data = json.load(file)


if 'selected_option' not in st.session_state:
    st.session_state.selected_option = None
    
#----------------------------------------------------------

def generate_question(prompts):
    url = f'{host_api}/{main_engine}/{instance_id}/soal-pppk/batch'
    # "https://langchain-api-production.up.railway.app/vertex-ai/{instance_id}/soal-pppk/batch"
    json_data = {
        "inputs": prompts,
        "config": {},
        "kwargs": {}
    }
    response = requests.post(url, json=json_data, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {tokens}"
    })
    print(response.text)
    if response.status_code == 200:
        return response


def main_app():
    generated_list = []
    prompt_list = []

    list_jenis = []
    list_jabatan = []
    list_kategori = []
    list_bidang = []
    list_sub = []

    selected_jenis = None
    selected_jabatan = None
    selected_kategori = None
    selected_bidang = None
    selected_sub = None
    # selected_bloom = None
    selected_creative = None
    #----------------------------------------------------------
    for jenis in data:
        list_jenis.append(jenis['jenis'])
    list_jenis = list(set(list_jenis))

    jenis_option = st.selectbox(
        "Tipe Modul",
        list_jenis,
        index=None,
        placeholder="Pilih Tipe Modul"
    )

    st.session_state["selected_jenis"] = jenis_option
    selected_jenis = jenis_option
    #----------------------------------------------------------
    if selected_jenis is not None:
        for jabatan in data:
            if jabatan['jenis'] == selected_jenis:
                list_jabatan.append(jabatan['nama_jabatan'])
        list_jabatan = list(set(list_jabatan))

        jabatan_option = st.selectbox(
            "Jenis Jabatan",
            list_jabatan,
            index=None,
            placeholder="Pilih Jenis Jabatan"
        )

        st.session_state["selected_jabatan"] = jabatan_option
        selected_jabatan = jabatan_option
    #----------------------------------------------------------
    if selected_jabatan is not None:
        for kategori in data:
            if kategori['jenis'] == selected_jenis and kategori['nama_jabatan'] == selected_jabatan:
                list_kategori.append(kategori['kategori'])
        list_kategori = list(set(list_kategori))

        kategori_option = st.selectbox(
            "Jenis Kategori",
            list_kategori,
            index=None,
            placeholder="Pilih Jenis Kategori"
        )

        st.session_state["selected_kategori"] = kategori_option
        selected_kategori = kategori_option
    #----------------------------------------------------------
    if selected_kategori is not None:
        for bidang in data:
            if bidang['jenis'] == selected_jenis and bidang['nama_jabatan'] == selected_jabatan and bidang['kategori'] == selected_kategori:
                list_bidang.append(bidang['bidang'])
        list_bidang = list(set(list_bidang))

        bidang_option = st.selectbox(
            "Jenis Sub Kategori",
            list_bidang,
            index=None,
            placeholder="Pilih Sub Kategori"
        )

        st.session_state["selected_bidang"] = bidang_option
        selected_bidang = bidang_option
    #----------------------------------------------------------
    if selected_bidang is not None:
        for sub in data:
            if sub['jenis'] == selected_jenis and sub['nama_jabatan'] == selected_jabatan and sub['kategori'] == selected_kategori and sub['bidang'] == selected_bidang:
                list_sub.append(sub['sub'])
        list_sub = list(set(list_sub))

        sub_option = st.selectbox(
            "Jenis Materi",
            list_sub,
            index=None,
            placeholder="Pilih Materi"
        )

        st.session_state["selected_sub"] = sub_option
        selected_sub = sub_option
    #----------------------------------------------------------
    original_list = [
        "Mengingat (C1)",
        "Memahami (C2)",
        "Menerapkan (C3)",
        "Menganalisis (C4)",
        "Mengevaluasi (C5)"
    ]
    # if selected_sub is not None:
        # bloom_option = st.selectbox(
        #     "Bloom",
            # [
            #     "Mengingat (C1)",
            #     "Memahami (C2)",
            #     "Menerapkan (C3)",
            #     "Menganalisis (C4)",
            #     "Mengevaluasi (C5)",
            #     "Menciptakan (C6)"
            # ],
        #     index=None,
        #     placeholder="Pilh Level Bloom"
        # )
        # st.session_state["select_bloom"] = bloom_option
        # selected_bloom = bloom_option
    #----------------------------------------------------------
    # if selected_sub is not None:
    #     creative_option = st.radio(
    #         "Studi Kasus",
    #         ["Iya", "Tidak"],
    #         index=1
    #     )
        
    #     st.session_state["selected_creative"] = creative_option
    #     selected_creative = creative_option
    #----------------------------------------------------------
    question_length = st.number_input("Jumlah Soal", value=None, placeholder="Masukkan jumlah soal")
    #----------------------------------------------------------
    if selected_sub is not None and question_length != 0:
        if st.button(":robot_face: Generate Soal :robot_face:"):
            new_list = random.choices(original_list, k=round(question_length))
            
            for item in new_list:
                prompt = f"""Saya akan membuat soal {selected_jenis} untuk jabatan {selected_jabatan}. Soal yang dibuat harus terstruktur secara lengkap dan jelas. Soal tersebut disusun berdasarkan kemampuan {selected_kategori} pada bidang {selected_bidang}. Buatlah soal tentang {selected_sub} yang setara dengan Level Bloom {item} tetapi sebagai pengecoh jangan gunakan kata yang sama dengan level bloom yang digunakan pada soal, termasuk tidak mengandung kata-kata level bloom. Soal tidak boleh mengandung kata-kata "{selected_bidang}" atau "{selected_sub}" di dalamnya. Buat soal menggunakan studi kasus nyata tanpa mempertanyakan secara langsung bloom yang ditanyakan dengan memprioritaskan segi praktek lapangan sebagai abdi negara di bidang tersebut"""
                prompt_list.append(prompt)
            
            res = generate_question(prompt_list)
            
            if res.status_code == 200:
                try:
                    res_data = json.loads(res.text)
                    output_data = res_data.get('output')
                    
                    for question_data in output_data:
                        st.write("**Soal**")
                        st.write(question_data['question'])
                        
                        answer_text = []
                        for answer in question_data['answers']:
                            answer_text.append(f"{answer['answer']} - {answer['score']}")
                        
                        answer_option = st.radio(
                            "Pilihan",
                            answer_text,
                            disabled=True,
                            index=None
                        )
                        st.write("**Pembahasan**")
                        st.write(question_data['explanation'])
                    else:
                        print(json.dumps(output_data))
                        print('-'*150)
                        st.write("Failed to generate question. Retry...")
                except json.JSONDecodeError:
                    print(json.dumps(output_data))
                    print('-'*150)
                    st.write("Failed to decode JSON. Retry...")
            else:
                print(json.dumps(output_data))
                print('-'*150)
                st.write(f"Failed with status code: {res.status_code}. Retry...")
            
            time.sleep(1)


st.set_page_config(layout="wide")
if "password_entered" not in st.session_state:
    st.session_state.password_entered = False

if not st.session_state.password_entered:
    user_password = st.text_input("Enter password:", type="password")

    if user_password == password:
        st.session_state.password_entered = True
    elif user_password != "":
        st.error("Incorrect password. Please try again.")

if st.session_state.password_entered:
    main_app()
      