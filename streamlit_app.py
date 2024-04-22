import json
import time
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

def generate_question(prompt):
    url = f'{host_api}/{main_engine}/{instance_id}/invoke'
    json_data = {
        "input": prompt,
        "config": {},
        "kwargs": {}
    }
    response = requests.post(url, json=json_data, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {tokens}"
    })
    print(url)
    if response.status_code == 200:
        return response


def main_app():
    generated_list = []

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
    selected_bloom = None
    selected_creative = None
    #----------------------------------------------------------
    for jenis in data:
        list_jenis.append(jenis['jenis'])
    list_jenis = list(set(list_jenis))

    jenis_option = st.selectbox(
        "Jenis Materi",
        list_jenis,
        index=None,
        placeholder="Pilih Jenis Materi"
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
            "Jenis Bidang",
            list_bidang,
            index=None,
            placeholder="Pilih Jenis Bidang"
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
            "Jenis Sub",
            list_sub,
            index=None,
            placeholder="Pilih Sub"
        )

        st.session_state["selected_sub"] = sub_option
        selected_sub = sub_option
    #----------------------------------------------------------
    if selected_sub is not None:
        bloom_option = st.selectbox(
            "Bloom",
            [
                "Mengingat (C1)",
                "Memahami (C2)",
                "Menerapkan (C3)",
                "Menganalisis (C4)",
                "Mengevaluasi (C5)",
                "Menciptakan (C6)"
            ],
            index=None,
            placeholder="Pilh Level Bloom"
        )
        st.session_state["select_bloom"] = bloom_option
        selected_bloom = bloom_option
    #----------------------------------------------------------
    if selected_bloom is not None:
        creative_option = st.radio(
            "Studi Kasus",
            ["Iya", "Tidak"],
            index=1
        )
        
        st.session_state["selected_creative"] = creative_option
        selected_creative = creative_option
    #----------------------------------------------------------
    if selected_creative is not None:
        if st.button(":robot_face: Generate Soal :robot_face:"):
            if st.session_state["selected_sub"] != None:
                
                generated_question = None
                
                if selected_creative == "Iya":
                    add_ons = " Buat soal menggunakan studi kasus nyata tanpa mempertanyakan secara langsung bloom yang ditanyakan."
                else:
                    add_ons = ""
                
                prompt = f"""Saya akan membuat soal {selected_jenis} untuk jabatan {selected_jabatan}. Soal yang dibuat harus terstruktur secara lengkap dan jelas. Soal tersebut disusun berdasarkan kemampuan {selected_kategori} pada bidang {selected_bidang}. Buatlah soal tentang {selected_sub} yang setara dengan Level Bloom {selected_bloom} tetapi sebagai pengecoh jangan gunakan kata yang sama dengan level bloom yang digunakan pada soal, termasuk tidak mengandung kata-kata level bloom. Soal tidak boleh mengandung kata-kata "{selected_bidang}" atau "{selected_sub}" di dalamnya.{add_ons}"""
                
                st.write(f"**{json.dumps(prompt, indent=4)}**")
                
                while True:
                    
                    res = generate_question(prompt)
                    
                    if res.status_code == 200:
                        try:
                            res_data = json.loads(res.text)
                            output_data = res_data.get('output')
                            
                            if output_data:
                                if output_data is not None:
                                    
                                    st.write("**Soal**")
                                    st.write(output_data['question'])
                                    
                                    answer_text = []
                                    for answer in output_data['answers']:
                                        answer_text.append(f"{answer['answer']} - {answer['score']}")
                                    
                                    answer_option = st.radio(
                                        "Pilihan",
                                        answer_text,
                                        disabled=True,
                                        index=None
                                    )
                                    st.write("**Pembahasan**")
                                    st.write(output_data['explanation'])
                                    
                                    print(json.dumps(output_data))
                                    print('-'*150)
                                    
                                    
                                    output_structure = {
                                        "jenis": selected_jenis,
                                        "jabatan": selected_jabatan,
                                        "kategori": selected_kategori,
                                        "bidang": selected_bidang,
                                        "sub": selected_sub,
                                        "bloom": selected_bloom,
                                        "studi_kasus": selected_creative,
                                        "question": output_data['question'],
                                        "option_a_text": output_data['answers'][0]['answer'],
                                        "option_a_value": output_data['answers'][0]['score'],
                                        "option_b_text": output_data['answers'][1]['answer'],
                                        "option_b_value": output_data['answers'][1]['score'],
                                        "option_c_text": output_data['answers'][2]['answer'],
                                        "option_c_value": output_data['answers'][2]['score'],
                                        "option_d_text": output_data['answers'][3]['answer'],
                                        "option_d_value": output_data['answers'][3]['score'],
                                        "option_e_text": output_data['answers'][4]['answer'],
                                        "option_e_value": output_data['answers'][4]['score'],
                                        "explanation": output_data['explanation']
                                    }
                                    break
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
      