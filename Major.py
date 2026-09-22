import streamlit as st
import random

st.set_page_config(page_title="شبیه‌ساز اوروک", layout="wide")

# --- تنظیمات سایدبار و دارایی ---
st.sidebar.title("🏛️ دولت‌شهر باستانی اوروک")

# فرم تنظیم دارایی اولیه توسط کاربر
with st.sidebar.expander("💰 تنظیم دارایی اولیه"):
    input_balance = st.number_input("دارایی خود را وارد کنید (شکیل):", min_value=100.0, value=1000.0, step=100.0)
    if st.button("ثبت دارایی"):
        st.session_state['balance'] = input_balance
        if 'project' in st.session_state:
            del st.session_state['project'] # حذف پروژه قبلی برای جلوگیری از ناهماهنگی با دارایی جدید
        st.rerun()

if 'balance' not in st.session_state:
    st.session_state['balance'] = 1000.0

balance = st.session_state['balance']
st.sidebar.success(f"موجودی فعلی: **{balance:,.0f} شکیل**")

# --- تنظیمات نرخ بهره ---
if 'interest_rate' not in st.session_state:
    st.session_state['interest_rate'] = random.uniform(0.05, 0.25)

r = st.session_state['interest_rate']

st.title("⚖️ خزانه‌داری معبد و تصمیم‌گیری سرمایه‌گذاری")
st.info(f"📜 **اعلامیه کاهن اعظم:** نرخ سود سپرده‌گذاری و استقراض در معبد **{r*100:.1f}%** در سال است.")
st.markdown("---")

# --- تولید پروژه متناسب با دارایی ---
if st.button("🔍 جستجوی یک پروژه جدید"):
    t = random.randint(1, 5)
    # هزینه پروژه ضریبی تصادفی (بین ۲۰ تا ۸۰ درصد) از دارایی کل بازیکن است
    C0 = int(balance * random.uniform(0.2, 0.8))
    
    # محاسبه نقطه سربه‌سر برای بانک
    break_even = C0 * ((1 + r) ** t)
    
    # بازدهی پروژه ضریبی تصادفی (بین ۷۰ تا ۱۵۰ درصد) از نقطه سربه‌سر است تا پروژه‌های سودآور و زیان‌ده تولید شود
    C1 = int(break_even * random.uniform(0.7, 1.5))
    
    st.session_state['project'] = {
        'C0': C0, 'C1': C1, 't': t,
        'name': random.choice(["احداث تاکستان", "حفر کانال آب", "کاروان تجاری به عیلام", "توسعه کوره آجرپزی"])
    }

# --- نمایش و تحلیل پروژه ---
if 'project' in st.session_state:
    proj = st.session_state['project']
    C0, C1, t = proj['C0'], proj['C1'], proj['t']
    
    st.subheader(f"🛠️ پروژه پیشنهادی: {proj['name']}")
    
    # مقایسه شفاف: پروژه در برابر خزانه‌داری
    temple_return = C0 * ((1 + r) ** t)
    
    st.markdown("### 🔍 مقایسه بازدهی (چرا سرمایه‌گذاری کنیم؟)")
    st.write(f"شما **{C0:,.0f} شکیل** پول نقد دارید که باید برای آن تصمیم بگیرید:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"🏦 **گزینه اول: سپرده در معبد**\n\nاگر این پول را به معبد بدهید، پس از {t} سال مبلغ **{temple_return:,.0f} شکیل** دریافت می‌کنید.")
    with col2:
        st.warning(f"🏗️ **گزینه دوم: احداث پروژه**\n\nاگر این پروژه را بسازید، پس از {t} سال مبلغ **{C1:,.0f} شکیل** به دست می‌آورید.")

    if C1 > temple_return:
        st.success(f"✅ **نتیجه:** پروژه سودآور است! بازدهی پروژه **{(C1 - temple_return):,.0f} شکیل** بیشتر از سود معبد است.")
    else:
        st.error(f"❌ **نتیجه:** پروژه زیان‌ده است! با سپرده‌گذاری در معبد **{(temple_return - C1):,.0f} شکیل** سود بیشتری کسب می‌کنید.")

    # تحلیل مصرف امروزی و وام
    loan_amount = C1 / ((1 + r) ** t)
    cash_left = balance - C0
    total_consumption_today = cash_left + loan_amount

    st.markdown("---")
    st.markdown("### 💰 قدرت مصرف امروزی (با استفاده از وام وثیقه‌ای)")
    st.write("اگر پروژه را اجرا کنید و محصول آینده را پیش‌فروش (وثیقه) کنید، وضعیت مالی امروز شما به این شکل خواهد بود:")
    
    col3, col4, col5 = st.columns(3)
    col3.metric("۱. نقدینگی باقیمانده (پس از احداث)", f"{cash_left:,.0f} شکیل")
    col4.metric("۲. وام دریافتی از معبد (ارزش فعلی وثیقه)", f"{loan_amount:,.0f} شکیل")
    col5.metric("۳. کل قدرت مصرف امروز (۱ + ۲)", f"{total_consumption_today:,.0f} شکیل")

    st.caption(f"*نکته: در سال {t}، معبد تمام {C1:,.0f} شکیل محصول شما را برمی‌دارد و وام به طور کامل تسویه می‌شود.*")

    # دکمه سرمایه‌گذاری
    if st.button("✅ تأیید سرمایه‌گذاری و اخذ وام"):
        # موجودی جدید = قدرت مصرف امروزی
        st.session_state['balance'] = total_consumption_today
        st.success("پروژه احداث شد، وام دریافت گردید و نقدینگی شما بروزرسانی شد!")
        del st.session_state['project']
        st.rerun()
