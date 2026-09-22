import streamlit as st
import random

st.title("⚖️ خزانه‌داری معبد و پروژه‌های سرمایه‌گذاری")

# دریافت موجودی از هسته مرکزی
balance = st.session_state.get('balance', 1000)
st.write(f"**دارایی شما:** {balance:,.0f} شکیل")

st.markdown("---")

# 1. تنظیمات معبد (نرخ بهره تصادفی)
if 'interest_rate' not in st.session_state:
    st.session_state['interest_rate'] = random.uniform(0.05, 0.25) # بین ۵ تا ۲۵ درصد

r = st.session_state['interest_rate']
st.info(f"📜 **اعلامیه کاهن اعظم:** نرخ سود سپرده‌گذاری در خزانه‌داری معبد در حال حاضر **{r*100:.1f}%** است.")

# 2. ایجاد پروژه تصادفی
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
    col1.metric("هزینه احداث (C0)", f"{C0} شکیل")
    col2.metric("بازدهی نهایی (C1)", f"{C1} شکیل")
    col3.metric("مدت زمان (t)", f"{t} سال")
    
    # 3. محاسبات ریاضی
    # پولی که معبد بابت همین هزینه پس از t سال می‌دهد
    temple_return = C0 * ((1 + r) ** t)
    
    # ارزش فعلی بازدهی آینده (مقدار وامی که معبد امروز بابت وثیقه C1 می‌دهد)
    loan_amount = C1 / ((1 + r) ** t)
    
    # NPV خالص
    npv = -C0 + loan_amount
    
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
    # 4. دکمه تصمیم‌گیری
    if st.button("✅ سرمایه‌گذاری در این پروژه"):
        if balance >= C0:
            st.session_state['balance'] -= C0
            # اضافه شدن مبلغ وام به موجودی امروزی (چون C1 وثیقه شده است)
            st.session_state['balance'] += loan_amount
            st.success("سرمایه‌گذاری با موفقیت انجام شد! موجودی جدید شما بروزرسانی گردید.")
            del st.session_state['project']
            st.rerun()
        else:
            st.error("موجودی شما برای احداث این پروژه کافی نیست!")
