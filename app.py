import streamlit as st

st.set_page_config(page_title="شبیه‌ساز اوروک", layout="wide")

st.title("🏛️ دولت‌شهر باستانی اوروک")
st.markdown("به شبیه‌ساز اقتصادی و استراتژیک جهان باستان خوش آمدید.")

# مقداردهی اولیه خزانه‌داری بازیکن
if 'balance' not in st.session_state:
    st.session_state['balance'] = 1000  # موجودی پیش‌فرض 1000 شکیل

st.sidebar.header("وضعیت دارایی")
st.sidebar.success(f"موجودی فعلی: {st.session_state['balance']} شکیل")

st.write("لطفاً از منوی سمت چپ، وارد بخش **بازی NPV** شوید تا پروژه‌های سرمایه‌گذاری را بررسی کنید.")
