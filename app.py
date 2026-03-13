import streamlit as st

st.set_page_config(layout="wide", page_title="Đánh giá TTCS Sán Chỉ")
st.title("📊 Ứng Dụng Đánh Giá Hiệu Quả Truyền Thông Chính Sách")
st.info("Lưu ý: Hệ thống đã tự động khóa giới hạn để đảm bảo điểm số không vượt quá 10.")

# === 1. CHỈ SỐ NĂNG LỰC NỀN TẢNG THỰC THI (X1) ===
st.header("1. Chỉ số Năng lực nền tảng thực thi (X1)")
loai_x1 = st.radio("Chọn đặc thù địa phương:", ("Trường hợp 1: Vùng sử dụng Smartphone", "Trường hợp 2: Vùng hạn chế Smartphone"))

x1 = 0.0
if "Trường hợp 1" in loai_x1:
    col1, col2, col3 = st.columns(3)
    with col1:
        tong_thon = st.number_input("Tổng số thôn", min_value=1, value=5)
        thon_co_song = st.number_input("Số thôn có sóng", min_value=0, max_value=tong_thon, value=5)
    with col2:
        tong_ho = st.number_input("Tổng số hộ (X1)", min_value=1, value=500)
        ho_co_thiet_bi = st.number_input("Số hộ có thiết bị", min_value=0, max_value=tong_ho, value=400)
    with col3:
        ho_tai_app = st.number_input("Số hộ tải App", min_value=0, max_value=max(1, ho_co_thiet_bi), value=200)

    a1 = (thon_co_song / tong_thon) * 10
    b1 = (ho_co_thiet_bi / tong_ho) * 10
    c1 = (ho_tai_app / ho_co_thiet_bi) * 10 if ho_co_thiet_bi > 0 else 0
    x1 = (a1 * 0.5) + (b1 * 0.3) + (c1 * 0.2)
else:
    col1, col2 = st.columns(2)
    with col1:
        tong_ho_th2 = st.number_input("Tổng số hộ địa bàn", min_value=1, value=100)
        ho_co_can_bo = st.number_input("Số hộ có cán bộ phụ trách", min_value=0, max_value=tong_ho_th2, value=100)
    with col2:
        buoi_ke_hoach = st.number_input("Số buổi kế hoạch", min_value=1, value=10)
        buoi_tiep_xuc = st.number_input("Số buổi tiếp xúc thực tế", min_value=0, max_value=buoi_ke_hoach, value=8)
        
    a1 = (ho_co_can_bo / tong_ho_th2) * 10
    b1 = (buoi_tiep_xuc / buoi_ke_hoach) * 10
    x1 = (a1 * 0.5) + (b1 * 0.5)

st.success(f"📌 Điểm X1: {x1:.2f}")

# === 2. CHỈ SỐ THẤU HIỂU VÀ CHUYỂN ĐỔI (X2) ===
st.header("2. Chỉ số Thấu hiểu và chuyển đổi (X2)")
st.subheader("Trọng số dân cư")
w_on, w_off = st.columns(2)
w_online = st.number_input("Trọng số Online (Wonline)", min_value=0.0, max_value=1.0, value=0.4)
w_offline = 1.0 - w_online
st.write(f"Trọng số Offline (Woffline) tự động tính: **{w_offline:.1f}**")

col_on, col_off = st.columns(2)
with col_on:
    st.markdown("**Kênh Trực tuyến (Online)**")
    tong_tiep_can = st.number_input("Tổng lượt tiếp cận", min_value=1, value=1000)
    tt_tren_120s = st.number_input("Lượt tương tác >120s", min_value=0, max_value=tong_tiep_can, value=600)
    tong_cau_hoi = st.number_input("Tổng câu hỏi trắc nghiệm", min_value=1, value=100)
    tl_dung_on = st.number_input("Câu trả lời đúng (Online)", min_value=0, max_value=tong_cau_hoi, value=80)
    tong_thiet_bi_x2 = st.number_input("Tổng thiết bị di động (X2)", min_value=1, value=400)
    thiet_bi_cai_app = st.number_input("Thiết bị cài App (X2)", min_value=0, max_value=tong_thiet_bi_x2, value=200)
    
    a2_on = (tt_tren_120s / tong_tiep_can) * 10
    b2_on = (tl_dung_on / tong_cau_hoi) * 10
    x2_online = (a2_on * b2_on) * 0.1 * (thiet_bi_cai_app / tong_thiet_bi_x2)

with col_off:
    st.markdown("**Kênh Trực tiếp (Offline)**")
    muc_tieu_hop = st.number_input("Mục tiêu người dự họp", min_value=1, value=300)
    nguoi_du_hop = st.number_input("Số người thực tế dự họp", min_value=0, max_value=muc_tieu_hop, value=250)
    nguoi_tuong_tac = st.number_input("Số người tương tác/phát biểu", min_value=0, max_value=max(1, nguoi_du_hop), value=150)
    nguoi_duoc_hoi = st.number_input("Số người được hỏi nội dung", min_value=1, value=50)
    tl_dung_off = st.number_input("Số người trả lời đúng (Offline)", min_value=0, max_value=nguoi_duoc_hoi, value=35)
    
    a2_off = (nguoi_tuong_tac / nguoi_du_hop) * 10 if nguoi_du_hop > 0 else 0
    b2_off = (tl_dung_off / nguoi_duoc_hoi) * 10
    x2_offline = (a2_off * b2_off) * 0.1 * (nguoi_du_hop / muc_tieu_hop)

x2 = (x2_online * w_online) + (x2_offline * w_offline)
st.success(f"📌 Điểm X2: {x2:.2f}")

# === 3. CHỈ SỐ NIỀM TIN VÀ AN NINH (X3) ===
st.header("3. Chỉ số Niềm tin và an ninh (X3)")
c1, c2, c3 = st.columns(3)
with c1: 
    tong_tuong_tac_x3 = st.number_input("Tổng tương tác (Tích cực + Tiêu cực)", min_value=1, value=1000)
    tuong_tac_tich_cuc = st.number_input("Số lượt tương tác tích cực (A3)", min_value=0, max_value=tong_tuong_tac_x3, value=800)
with c3: 
    thoi_gian_xu_ly = st.number_input("Thời gian xử lý tin xấu (giờ)", min_value=0.0, value=2.0)

a3 = (tuong_tac_tich_cuc / tong_tuong_tac_x3) * 10
# Tính B3 theo quy chuẩn [cite: 188]
if thoi_gian_xu_ly <= 2: b3 = 10
elif thoi_gian_xu_ly >= 48: b3 = 0
else: b3 = 10 - ((thoi_gian_xu_ly - 2) * (10 / 46))
x3 = (a3 * 0.7) + (b3 * 0.3)
st.success(f"📌 Điểm X3: {x3:.2f}")

# === 4. CHỈ SỐ HÀNH ĐỘNG VÀ SINH KẾ (X4) ===
st.header("4. Chỉ số Hành động và sinh kế (X4)")
c1, c2, c3 = st.columns(3)
with c1:
    ho_thu_huong = st.number_input("Số hộ thuộc diện thụ hưởng chính sách", min_value=1, value=200)
    ho_dang_ky = st.number_input("Số hộ chủ động đăng ký (A4)", min_value=0, max_value=ho_thu_huong, value=160)
with c2: 
    ho_xu_ly = st.number_input("Số hộ được xử lý thành công (B4)", min_value=0, max_value=max(1, ho_dang_ky), value=120)
with c3:
    muc_tieu_de_ra = st.number_input("Mục tiêu chính sách đề ra", min_value=1, value=50)
    gia_tri_thuc_te = st.number_input("Giá trị/Mô hình thực tế đạt được (C4)", min_value=0, max_value=muc_tieu_de_ra, value=40)

a4 = (ho_dang_ky / ho_thu_huong) * 10
b4 = (ho_xu_ly / ho_dang_ky) * 10 if ho_dang_ky > 0 else 0
c4 = (gia_tri_thuc_te / muc_tieu_de_ra) * 10
x4 = (a4 * 0.4) + (b4 * 0.3) + (c4 * 0.3)
st.success(f"📌 Điểm X4: {x4:.2f}")

# === 5. TỔNG CHỈ SỐ VÀ XẾP LOẠI ===
st.header("5. Tổng Chỉ Số Hiệu Quả (X) và Xếp Loại")
st.write("Thiết lập trọng số (w1 + w2 + w3 + w4 = 1.0) [cite: 223]")
w1_col, w2_col, w3_col, w4_col = st.columns(4)
with w1_col: trong_so_1 = st.number_input("Trọng số w1", value=0.2)
with w2_col: trong_so_2 = st.number_input("Trọng số w2", value=0.3)
with w3_col: trong_so_3 = st.number_input("Trọng số w3", value=0.2)
with w4_col: trong_so_4 = st.number_input("Trọng số w4", value=0.3)

if st.button("🚀 TÍNH TOÁN KẾT LUẬN", use_container_width=True):
    tong_diem = (x1 * trong_so_1) + (x2 * trong_so_2) + (x3 * trong_so_3) + (x4 * trong_so_4)
    
    # Xếp loại theo thang điểm trong tài liệu [cite: 211, 212, 213, 214, 215]
    if tong_diem > 8.5: xep_loai, mau_sac = "🌟 RẤT HIỆU QUẢ", "green"
    elif tong_diem > 6.5: xep_loai, mau_sac = "✅ HIỆU QUẢ", "blue"
    elif tong_diem > 5.0: xep_loai, mau_sac = "⚠️ ÍT HIỆU QUẢ", "orange"
    else: xep_loai, mau_sac = "❌ CHƯA HIỆU QUẢ", "red"
        
    st.balloons()
    st.markdown(f"""
    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center; border: 2px solid {mau_sac};">
        <h2 style="color: black; margin-bottom: 0;">TỔNG ĐIỂM ĐỊNH LƯỢNG: {tong_diem:.2f} / 10</h2>
        <h1 style="color: {mau_sac}; margin-top: 10px;">{xep_loai}</h1>
    </div>
    """, unsafe_allow_html=True)
