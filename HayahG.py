import streamlit as st
import pandas as pd
import gspread
from google.oauth2 import service_account

# تهيئة الصفحة
if 'page' not in st.session_state:
    st.session_state.page = "main"

# إعداد بيانات الاعتماد من Streamlit Secrets
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ],
)

# تفويض بيانات الاعتماد
client = gspread.authorize(credentials)

try:
    # فتح ورقة العمل باستخدام المعرف
    sheet = client.open_by_key("1SUmVNpYKX2lk4d--XKUymevdJOJZdQa1MrNxAGL9s0A").worksheet("Sheet1")

    # قراءة البيانات وتحويلها إلى DataFrame
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    # عنوان التطبيق
    st.title("Alhayah Developments Offers")

    # زر البحث
    if st.button("البحث"):
        st.session_state.page = "search"
    else:
        st.session_state.page = "main"

    if st.session_state.page == "main":
        # عرض جدول منسق بكافة البيانات
        st.dataframe(df, height=len(df) * 35 + 35)  # ضبط ارتفاع الجدول

    elif st.session_state.page == "search":
        # صفحة البحث
        st.subheader("البحث عن عروض")
        area = st.selectbox("المنطقة", df['Area'].unique())
        project = st.selectbox("اسم المشروع", df['اسم المشروع'].unique())

        filtered_df = df[(df['Area'] == area) & (df['اسم المشروع'] == project)]

        # عرض نتائج البحث
        st.dataframe(filtered_df, height=len(filtered_df) * 35 + 35)  # ضبط ارتفاع الجدول

        # زر العودة إلى الصفحة الرئيسية
        if st.button("العودة إلى الصفحة الرئيسية"):
            st.session_state.page = "main"

except Exception as e:
    st.write(f"حدث خطأ: {e}")
