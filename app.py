import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(layout="wide", page_title="Đánh giá TTCS Sán Chỉ")
st.title("📊 Ứng Dụng Đánh Giá Hiệu Quả Truyền Thông Chính Sách")

# === HÀM KIỂM TRA LOGIC (Chỉ bôi đỏ phần sai, không báo lỗi Xcode) ===
def check_logic(tu_so, mau_so, nhan):
    if tu_so > mau_so:
        st.error(f"❌ Sai sót tại {nhan}: Giá trị thực tế không được lớn hơn tổng số/mục tiêu!")
        return False
    return True

# === 1. CHỈ SỐ NĂNG LỰC NỀN TẢNG THỰC THI (X1) ===
st.header("1. Chỉ số Năng lực nền tảng thực thi (X1)")
loai_x1 = st.radio("Chọn vùng:", ("Smartphone", "Hạn chế Smartphone"))
x1, hop_le_x1 = 0.0, True

if loai_x1 == "Smartphone":
    col1, col2, col3 = st.columns(3)
    with col1:
        t_thon = st.number_input("Tổng số thôn", min_value=1, value=5)
        s_thon = st.number_input("Số thôn có sóng", min_value=0, value=5)
    with col2:
        t_ho = st.number_input("Tổng số hộ (X1)", min_value=1, value=500)
        s_ho_tb = st.number_input("Số hộ có thiết bị", min_value=0, value=400)
    with col3:
        s_ho_app = st.number_input("Số hộ tải App", min_value=0, value=200)

    if check_logic(s_thon, t_thon, "Chỉ số Tiếp cận (A1)") and \
       check_logic(s_ho_tb, t_ho, "Chỉ số Thiết bị (B1)") and \
       check_logic(s_ho_app, s_ho_tb, "Chỉ số Công dân số (C1)"):
        a1 = (s_thon / t_thon) * 10
        b1 = (s_ho_tb / t_ho) * 10
        c1 = (s_ho_app / s_ho_tb) * 10
        x1 = (a1 * 0.5) + (b1 * 0.3) + (c1 * 0.2)
    else: hop_le_x1 = False
else:
    col1, col2 = st.columns(2)
    with col1:
        t_ho_off = st.number_input("Tổng số hộ địa bàn", min_value=1, value=100)
        s_can_bo = st.number_input("Số hộ có cán bộ", min_value=0, value=100)
    with col2:
        b_kh = st.number_input("Số buổi kế hoạch", min_value=1, value=10)
        b_tt = st.number_input("Số buổi tiếp xúc thực tế", min_value=0, value=8)
    
    if check_logic(s_can_bo, t_ho_off, "Chỉ số Bao phủ (A1)") and \
       check_logic(b_tt, b_kh, "Tần số hiện diện (B1)"):
        x1 = ((s_can_bo/t_ho_off)*10*0.5) + ((b_tt/b_kh)*10*0.5)
    else: hop_le_x1 = False

if hop_le_x1: st.success(f"📌 Điểm X1: {x1:.2f}")

# === 2. CHỈ SỐ THẤU HIỂU VÀ CHUYỂN ĐỔI (X2) ===
st.header("2. Chỉ số Thấu hiểu và chuyển đổi (X2)")
w_on = st.number_input("Trọng số dân cư Online (Wonline)", 0.0, 1.0, 0.4)
w_off = round(1.0 - w_on, 2)
st.info(f"Trọng số dân cư Offline (Woffline): {w_off}")

col_on, col_off = st.columns(2)
x2_on, x2_off, hop_le_x2 = 0.0, 0.0, True

with col_on:
    st.markdown("**Kênh Online**")
    t_tc = st.number_input("Tổng lượt tiếp cận", 1, value=1000)
    s_tt = st.number_input("Lượt tương tác >120s", 0, value=600)
    t_ch = st.number_input("Tổng câu hỏi", 1, value=100)
    s_tl = st.number_input("Câu trả lời đúng (Online)", 0, value=80)
    t_tb = st.number_input("Tổng thiết bị X2", 1, value=400)
    s_app = st.number_input("Thiết bị cài App X2", 0, value=200)
    if check_logic(s_tt, t_tc, "Tương tác Online") and \
       check_logic(s_tl, t_ch, "Câu trả lời đúng Online") and \
       check_logic(s_app, t_tb, "Cài đặt App"):
        x2_on = ((s_tt/t_tc)*10 * (s_tl/t_ch)*10) * 0.1 * (s_app/t_tb)
    else: hop_le_x2 = False

with col_off:
    st.markdown("**Kênh Offline**")
    m_hop = st.number_input("Mục tiêu người dự", 1, value=300)
    s_hop = st.number_input("Người dự thực tế", 0, value=250)
    s_pb = st.number_input("Số người phát biểu", 0, value=150)
    t_hoi = st.number_input("Số người được hỏi", 1, value=50)
    s_dung_off = st.number_input("TL đúng (Offline)", 0, value=35)
    if check_logic(s_hop, m_hop, "Dự họp thực tế") and \
       check_logic(s_pb, max(1, s_hop), "Người phát biểu") and \
       check_logic(s_dung_off, t_hoi, "TL đúng Offline"):
        x2_off = ((s_pb/s_hop)*10 * (s_dung_off/t_hoi)*10) * 0.1 * (s_hop/m_hop)
    else: hop_le_x2 = False

if hop_le_x2:
    x2 = (x2_on * w_on) + (x2_off * w_off)
    st.success(f"📌 Điểm X2: {x2:.2f}")

# === 3. CHỈ SỐ NIỀM TIN VÀ AN NINH (X3) ===
st.header("3. Chỉ số Niềm tin và an ninh (X3)")
t_tt_x3 = st.number_input("Tổng tương tác X3", 1, value=1000)
s_tc_x3 = st.number_input("Tương tác tích cực", 0, value=800)
t_gian = st.number_input("Thời gian xử lý tin xấu (giờ)", 0.0, value=2.0)
x3, hop_le_x3 = 0.0, True

if check_logic(s_tc_x3, t_tt_x3, "Tương tác tích cực X3"):
    a3 = (s_tc_x3/t_tt_x3)*10
    b3 = 10 if t_gian <= 2 else (0 if t_gian >= 48 else 10 - ((t_gian-2)*(10/46)))
    x3 = (a3 * 0.7) + (b3 * 0.3)
    st.success(f"📌 Điểm X3: {x3:.2f}")
else: hop_le_x3 = False

# === 4. CHỈ SỐ HÀNH ĐỘNG VÀ SINH KẾ (X4) ===
st.header("4. Chỉ số Hành động và sinh kế (X4)")
t_thu_huong = st.number_input("Tổng hộ thụ hưởng", 1, value=200)
s_dk = st.number_input("Hộ chủ động đăng ký", 0, value=160)
s_xl = st.number_input("Hộ được xử lý thành công", 0, value=120)
m_tieu = st.number_input("Mục tiêu chính sách", 1, value=50)
s_tt_x4 = st.number_input("Giá trị/Mô hình thực tế", 0, value=40)
x4, hop_le_x4 = 0.0, True

if check_logic(s_dk, t_thu_huong, "Hộ đăng ký (A4)") and \
   check_logic(s_xl, max(1, s_dk), "Hộ xử lý (B4)") and \
   check_logic(s_tt_x4, m_tieu, "Mô hình thực tế (C4)"):
    x4 = ((s_dk/t_thu_huong)*10*0.4) + ((s_xl/s_dk)*10*0.3) + ((s_tt_x4/m_tieu)*10*0.3)
    st.success(f"📌 Điểm X4: {x4:.2f}")
else: hop_le_x4 = False

# === 5. TỔNG KẾT VÀ XẾP LOẠI ===
st.header("5. Tổng Chỉ Số Hiệu Quả (X)")
st.write("Thiết lập trọng số (Tổng w1 + w2 + w3 + w4 phải bằng 1.0)")
cw1, cw2, cw3, cw4 = st.columns(4)
with cw1: w1 = st.number_input("Trọng số w1", value=0.2)
with cw2: w2 = st.number_input("Trọng số w2", value=0.3)
with cw3: w3 = st.number_input("Trọng số w3", value=0.2)
with cw4: w4 = st.number_input("Trọng số w4", value=0.3)

tong_w = round(w1 + w2 + w3 + w4, 2)
if tong_w != 1.0:
    st.error(f"⚠️ LỖI: Tổng trọng số đang là {tong_w}. Vui lòng điều chỉnh để tổng bằng 1.0!")
else:
    if st.button("🚀 XUẤT KẾT QUẢ ĐỊNH LƯỢNG", use_container_width=True):
        if hop_le_x1 and hop_le_x2 and hop_le_x3 and hop_le_x4:
            x_tong = (x1*w1) + (x2*w2) + (x3*w3) + (x4*w4)
            
            if x_tong > 8.5: xl, mau = "🌟 RẤT HIỆU QUẢ", "green"
            elif x_tong > 6.5: xl, mau = "✅ HIỆU QUẢ", "blue"
            elif x_tong > 5.0: xl, mau = "⚠️ ÍT HIỆU QUẢ", "orange"
            else: xl, mau = "❌ CHƯA HIỆU QUẢ", "red"
            
            st.balloons()
            st.markdown(f"""
            <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center; border: 2px solid {mau};">
                <h2 style="color: black;">TỔNG ĐIỂM: {x_tong:.2f} / 10</h2>
                <h1 style="color: {mau};">{xl}</h1>
            </div>
            """, unsafe_allow_html=True)
            
            # Xuất Excel
            df = pd.DataFrame({
                "Chỉ số": ["Nền tảng (X1)", "Thấu hiểu (X2)", "Niềm tin (X3)", "Hành động (X4)", "TỔNG"],
                "Điểm số": [round(x1, 2), round(x2, 2), round(x3, 2), round(x4, 2), round(x_tong, 2)],
                "Trọng số": [w1, w2, w3, w4, 1.0]
            })
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            st.download_button("📥 Tải Báo Cáo Excel", output.getvalue(), "bao_cao_ttcs.xlsx")
        else:
            st.warning("Vui lòng sửa các thông số nhập sai (đang báo đỏ phía trên)!")
