import streamlit as st
import random

# تنظیمات کلی صفحه
st.set_page_config(page_title="شبیه‌ساز اوروک", layout="wide")

# --- بخش داشبورد و هسته مرکزی (نوار کناری) ---
st.sidebar.title("🏛️ دولت‌شهر باستانی اوروک")
st.sidebar.markdown("به شبیه‌ساز اقتصادی و استراتژیک جهان باستان خوش آمدید.")

# مقداردهی اولیه خزانه‌داری بازیکن
if 'balance' not in st.session_state:
    st.session_state['balance'] = 1000  # موجودی پیش‌فرض 1000 شکیل

st.sidebar.header("وضعیت دارایی")
st.sidebar.success(f"موجودی فعلی: {st.session_state['balance']:,.0f} شکیل")

# --- بخش بازی ارزش فعلی خالص (محتوای اصلی صفحه) ---
st.title("⚖️ خزانه‌داری معبد و پروژه‌های سرمایه‌گذاری")
st.markdown("---")

# ۱. تنظیمات معبد (نرخ بهره تصادفی)
if 'interest_rate' not in st.session_state:
    st.session_state['interest_rate'] = random.uniform(0.05, 0.25) # بین ۵ تا ۲۵ درصد

r = st.session_state['interest_rate']
st.info(f"📜 **اعلامیه کاهن اعظم:** نرخ سود سپرده‌گذاری در خزانه‌داری معبد در حال حاضر **{r*100:.1f}%** است.")

# ۲. ایجاد پروژه تصادفی
if st.button("🔍 جستجوی یک پروژه جدید در شهر"):
    st.session_state['project'] = {
        'C0': random.randint(100, 800),               # هزینه اولیه
        'C1': random.randint(200, 1500),              # بازدهی آینده
        't': random.randint(1, 5),                    # مدت زمان پروژه (سال)
        'name': random.choice(["احداث تاکستان", "حفر کانال آب", "کاروان تجاری به عیلام", "توسعه کوره آجرپزی"])
    }

if 'project' in st.session_state:
    proj = st.session_state['project']
    C0 = proj['C0']
    C1 = proj['C1']
    t = proj['t']
    
    st.subheader(f"🛠️ پروژه پیشنهادی: {proj['name']}")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("هزینه احداث ($C_0$)", f"{C0} شکیل")
    col2.metric("بازدهی نهایی ($C_1$)", f"{C1} شکیل")
    col3.metric("مدت زمان ($t$)", f"{t} سال")
    
    # ۳. محاسبات ریاضی
    # پولی که معبد بابت همین هزینه پس از t سال می‌دهد
    temple_return = C0 * ((1 + r) ** t)
    
    # ارزش فعلی بازدهی آینده (مقدار وامی که معبد امروز بابت وثیقه C1 می‌دهد)
    loan_amount = C1 / ((1 + r) ** t)
    
    st.markdown("### 📊 تحلیل مالی")
    st.write(f"اگر شما **{C0} شکیل** را به جای این پروژه، در خزانه‌داری معبد بگذارید، پس از {t} سال مبلغ **{temple_return:,.2f} شکیل** خواهید داشت.")
    
    if C1 > temple_return:
        st.success(f"✅ **سودآور:** بازدهی این پروژه ({C1}) از سود معبد ({temple_return:,.2f}) بیشتر است. پروژه ارزش سرمایه‌گذاری دارد.")
    else:
        st.error(f"❌ **زیان‌ده:** بازدهی این پروژه ({C1}) از سود معبد ({temple_return:,.2f}) کمتر است. بهتر است پول را در معبد نگه دارید.")
        
    st.markdown("### 🏛️ تسهیلات وثیقه معبد (قضیه تفکیک)")
    st.write(f"اگر پروژه را اجرا کنید و بازدهی قطعی **{C1} شکیل** را در معبد وثیقه بگذارید، کاهن اعظم ارزش فعلی آن را حساب کرده و امروز به شما وام می‌دهد:")
    
    st.latex(rf"PV = \frac{{{C1}}}{{(1 + {r:.2f})^{t}}} = {loan_amount:,.2f}")
    
    st.info(f"💰 معبد همین امروز مبلغ **{loan_amount:,.2f} شکیل** به شما وام پرداخت می‌کند.")
    
    st.markdown("---")
    
    # ۴. دکمه تصمیم‌گیری
    if st.button("✅ سرمایه‌گذاری در این پروژه"):
        if st.session_state['balance'] >= C0:
            st.session_state['balance'] -= C0
            # اضافه شدن مبلغ وام به موجودی امروزی (چون C1 وثیقه شده است)
            st.session_state['balance'] += loan_amount
            st.success("سرمایه‌گذاری با موفقیت انجام شد! موجودی جدید شما بروزرسانی گردید.")
            del st.session_state['project']
            st.rerun()
        else:
            st.error("موجودی شما برای احداث این پروژه کافی نیست!")
