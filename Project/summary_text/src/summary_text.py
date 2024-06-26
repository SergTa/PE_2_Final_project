from base64 import b64encode

import streamlit as st
from chardet import detect
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    pipeline,
)


@st.cache_data
def get_base64(file: str) -> str:
    # загрузка файла в base64 для streamlit
    with open(file, "rb") as f:
        data = f.read()
    return b64encode(data).decode()


@st.cache_resource
def load_summary_model():
    # создание кэшированных объектов модели и токенайзера
    model_name = "csebuetnlp/mT5_multilingual_XLSum"
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name, legasy=False)

    # загружаем\получаем из кэша объект pipeline с моделью
    return pipeline("summarization", model=model, tokenizer=tokenizer)


@st.cache_resource
def detect_encoding(data: bytes) -> str:
    # определение кодировки символов
    return detect(data)["encoding"]


def main():
    # загружаем предварительно обученную модель summary
    summary_text = load_summary_model()
    # инициализируем переменные с текстом
    if "text" not in st.session_state:
        st.session_state["text"] = ""

    # вывод заголовка
    st.title("Краткое содержание текста")
    st.write(
        "Приложение возвращает краткое содержание текста"
    )

    # выбор источника данных
    source_button = st.radio(
        "Выберите источник данных",
        ["Ввод текста", "Загрузка файла"],
        captions=[
            "Вставить текст из буфера или ввести с клавиатуры",
            "Загрузить файл формата TXT",
        ],
    )

    # форма ввода текста
    if source_button == "Ввод текста":
        st.session_state["text"] = st.text_area("Введите текст")

    elif source_button == "Загрузка файла":
        # форма для загрузки файла
        uploaded_file = st.file_uploader(
            "Выберите файл",
            type=["txt"],
            accept_multiple_files=False,
        )

        if uploaded_file is not None:
            # чтение текста из файла
            file_bytes = uploaded_file.read()
            if uploaded_file.type == "text/plain":
                # определение кодировки
                encoding = detect_encoding(data=file_bytes)
                # декодирование и вывод превью
                st.session_state["text"] = file_bytes.decode(
                    encoding=encoding,
                    errors="ignore",
                )
        if st.session_state["text"]:
            st.session_state["text"] = st.text_area(
                label="Проверьте и отредактируйте текст:",
                value=st.session_state["text"],
            )

    # слайдер "Cтепень сжатия результата"
    brevity_level = st.slider(
        "Уровень сжатия результата (10 - кратко, 100 - подробно)",
        min_value=10,
        max_value=100,
        value=50
    )

    # кнопка "Создать"
    create_button = st.button("Создать")
    if create_button and st.session_state["text"]:
        try:
            with st.spinner("Пожалуйста, подождите..."):
                # выводим результат
                length = len(st.session_state["text"].split())
                st.markdown("**Результат: ** %s" % summary_text(
                    st.session_state["text"],
                    max_length=round(length * 1.5),
                    min_length=round(length * (brevity_level / 100))
                )[0]["summary_text"])
        except Exception as e:
            # выводим возникающие ошибки
            st.write(f"Ошибка: {e}")


if __name__ == "__main__":
    # запускаем приложение
    main()
