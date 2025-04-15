import streamlit as st
import pandas as pd
import gspread
from google.oauth2 import service_account
import base64
from io import BytesIO

# تهيئة حالة الجلسة
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

# تعريف دالة لعرض الشعار
def add_logo():
    st.markdown(
        """
        <style>
        .logo-container {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }
        .logo-img {
            max-width: 300px;
            margin: 0 auto;
        }
        </style>
        <div class="logo-container">
            <img class="logo-img" src="https://raw.githubusercontent.com/AVIATOR7474/ARRAY/main/logo.jpg">
        </div>
        """,
        unsafe_allow_html=True
    )

# تعريف دالة لتحسين مظهر التطبيق
def set_custom_style():
    st.markdown(
        """
        <style>
        .main {
            background-color: #f5f5f5;
            padding: 20px;
        }
        h1 {
            color: #8B6B23;
            text-align: center;
            font-family: 'Arial', sans-serif;
            padding: 10px;
            margin-bottom: 30px;
        }
        h2, h3 {
            color: #8B6B23;
            font-family: 'Arial', sans-serif;
        }
        .stButton>button {
            background-color: #8B6B23;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-weight: bold;
            border: none;
            margin: 10px 0;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #6d5419;
        }
        .stSelectbox label, .stDataFrame {
            color: #333;
            font-weight: bold;
        }
        .stDataFrame {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            background-color: white;
        }
        .row-header {
            background-color: #8B6B23;
            color: white;
            font-weight: bold;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

try:
    # تطبيق التصميم المخصص
    set_custom_style()
    
    # إضافة الشعار
    add_logo()
    
    # عنوان التطبيق
    st.title("Alhayah Developments Offers")
    
    # فتح ورقة العمل باستخدام المعرف
    sheet = client.open_by_key("1SUmVNpYKX2lk4d--XKUymevdJOJZdQa1MrNxAGL9s0A").worksheet("Sheet1")

    # قراءة البيانات وتحويلها إلى DataFrame
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    
    # إنشاء قائمة بأزرار التنقل
    col1, col2 = st.columns(2)
    with col1:
        if st.button("عرض جميع العروض"):
            st.session_state.page = "main"
    with col2:
        if st.button("البحث عن عروض"):
            st.session_state.page = "search"

    # صفحة العرض الرئيسية
    if st.session_state.page == "main":
        # عرض جدول منسق بكافة البيانات
        st.subheader("جميع العروض المتاحة")
        
        # تعديل حجم الجدول ليعرض جميع البيانات
        st.dataframe(
            df,
            height=600,  # ارتفاع أكبر للجدول
            width=1000,  # عرض أكبر للجدول
            use_container_width=True  # استخدام عرض الحاوية بالكامل
        )

    # صفحة البحث
    elif st.session_state.page == "search":
        st.subheader("البحث عن عروض")
        
        # إنشاء 3 أعمدة للبحث
        col1, col2, col3 = st.columns(3)
        
        with col1:
            area = st.selectbox("المنطقة", ["الكل"] + sorted(df['Area'].unique().tolist()))
        
        with col2:
            project = st.selectbox("اسم المشروع", ["الكل"] + sorted(df['اسم المشروع'].unique().tolist()))
        
        with col3:
            # إضافة البحث باسم الشركة
            companies = ["الكل"]
            if 'اسم الشركة' in df.columns:
                companies += sorted(df['اسم الشركة'].unique().tolist())
            company = st.selectbox("اسم الشركة", companies)
        
        # تطبيق الفلترة
        filtered_df = df.copy()
        
        if area != "الكل":
            filtered_df = filtered_df[filtered_df['Area'] == area]
        
        if project != "الكل":
            filtered_df = filtered_df[filtered_df['اسم المشروع'] == project]
        
        if company != "الكل" and 'اسم الشركة' in df.columns:
            filtered_df = filtered_df[filtered_df['اسم الشركة'] == company]
        
        # عرض نتائج البحث
        st.subheader(f"نتائج البحث ({len(filtered_df)} عرض)")
        
        # تعديل حجم الجدول ليعرض جميع البيانات
        st.dataframe(
            filtered_df,
            height=600,  # ارتفاع أكبر للجدول
            width=1000,  # عرض أكبر للجدول
            use_container_width=True  # استخدام عرض الحاوية بالكامل
        )

except Exception as e:
    st.error(f"حدث خطأ: {e}")
    st.info("يرجى التحقق من اتصال البيانات والمحاولة مرة أخرى.")
