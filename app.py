import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(layout="wide", page_title="Đánh giá TTCS Sán Chỉ")
st.title("📊 Ứng Dụng Đánh Giá Hiệu Quả Truyền Thông Chính Sách")

# === HÀM HỖ TRỢ HIỂN THỊ CẢNH BÁO ===
def kiem_tra_logic(tu_so, mau_so, nhan):
    if tu_so > mau_so:
        st.error(f"⚠️ Lỗi ở {nhan}: Số lượng thực tế không được lớn hơn tổng số!")
        return False
    return True

# === 1. CHỈ SỐ NĂNG LỰC NỀN TẢNG THỰC THI (X1) ===
st.header("1. Chỉ số Năng lực nền tảng thực thi (X1)")
loai_x1 = st.radio("Chọn đặc thù địa phương:", ("Trường hợp 1: Vùng sử dụng Smartphone", "Trường hợp 2: Vùng hạn chế Smartphone"))

x1 = 0.0
hop_le_x1 = True

if "Trường hợp 1" in loai_x1:
    col1, col2, col3 = st.columns(3)
    with col1:
        tong_thon = st.number_input("Tổng số thôn", min_value=1, value=5)
        thon_co_song = st.number_input("Số thôn có sóng", min_value=0, value=5)
    with col2:
        tong_ho = st.number_input("Tổng số hộ (X1)", min_value=1, value=500)
        ho_co_thiet_bi = st.number_input("Số hộ có thiết bị", min_value=0, value=400)
    with col3:
        ho_tai_app = st.number_input("Số hộ tải App", min_value=0, value=200)

    # Kiểm tra logic từng phần [cite: 142, 144, 146]
    c1_logic = kiem_tra_logic(thon_co_song, tong_thon, "Chỉ số Tiếp cận (A1)")
    c2_logic = kiem_tra_logic(ho_co_thiet_bi, tong_ho, "Chỉ số Thiết bị (B1)")
    c3_logic = kiem_tra_logic(ho_tai_app, ho_co_thiet_bi, "Chỉ số Công dân số (C1)")
    
    if c1_logic and c2_logic and c3_logic:
        a1 = (thon_co_song / tong_thon) * 10
        b1 = (ho_co_thiet_bi / tong_ho) * 10
        c1 = (ho_tai_app / ho_co_thiet_bi) * 10 if ho_co_thiet_bi > 0 else 0
        x1 = (a1 * 0.5) + (b1 * 0.3) + (c1 * 0.2) # [cite: 147]
    else:
        hop_le_x1 = False
else:
    col1, col2 = st.columns(2)
    with col1:
        tong_ho_th2 = st.number_input("Tổng số hộ địa bàn", min_value=1, value=100)
        ho_co_can_bo = st.number_input("Số hộ có cán bộ phụ trách", min_value=0, value=100)
    with col2:
        buoi_ke_hoach = st.number_input("Số buổi kế hoạch", min_value=1, value=10)
        buoi_tiep_xuc = st.number_input("Số buổi tiếp xúc thực tế", min_value=0, value=8)
    
    c1_off_logic = kiem_tra_logic(ho_co_can_bo, tong_ho_th2, "Chỉ số Bao phủ (A1)")
    c2_off_logic = kiem_tra_logic(buoi_tiep_xuc, buoi_ke_hoach, "Tần số hiện diện (B1)")
    
    if c1_off_logic and c2_off_logic:
        a1 = (ho_co_can_bo / tong_ho_th2) * 10
        b1 = (buoi_tiep_xuc / buoi_ke_hoach) * 10
        x1 = (a1 * 0.5) + (b1 * 0.5) # [cite: 157]
    else:
        hop_le_x1 = False

if hop_le_x1:
    st.success(f"📌 Điểm X1: {x1:.2f}")

st.markdown("---")

# === 2. CHỈ SỐ THẤU HIỂU VÀ CHUYỂN ĐỔI (X2) ===
st.header("2. Chỉ số Thấu hiểu và chuyển đổi (X2)")
w_online = st.number_input("Trọng số Online (Wonline)", min_value=0.0, max_value=1.0, value=0.4)
w_offline = round(1.0 - w_online, 2)
st.write(f"Trọng số Offline (Woffline) tự động: **{w_offline}**")

col_on, col_off = st.columns(2)
hop_le_x2 = True

with col_on:
    st.markdown("**Kênh Trực tuyến (Online)**")
    tong_tiep_can = st.number_input("Tổng lượt tiếp cận", min_value=1, value=1000)
    tt_tren_120s = st.number_input("Lượt tương tác >120s", min_value=0, value=600)
    tong_cau_hoi = st.number_input("Tổng câu hỏi trắc nghiệm", min_value=1, value=100)
    tl_dung_on = st.number_input("Câu trả lời đúng (Online)", min_value=0, value=80)
    tong_thiet_bi_x2 = st.number_input("Tổng thiết bị di động (X2)", min_value=1, value=400)
    thiet_bi_cai_app = st.number_input("Thiết bị cài App (X2)", min_value=0, value=200)
    
    on1 = kiem_tra_logic(tt_tren_120s, tong_tiep_can, "Tương tác Online")
    on2 = kiem_tra_logic(tl_dung_on, tong_cau_hoi, "Câu trả lời đúng Online")
    on3 = kiem_tra_logic(thiet_bi_cai_app, tong_thiet_bi_x2, "Cài đặt App X2")
    
    if on1 and on2 and on3:
        a2_on = (tt_tren_120s / tong_tiep_can) * 10
        b2_on = (tl_dung_on / tong_cau_hoi) * 10
        x2_online = (a2_on * b2_on) * 0.1 * (thiet_bi_cai_app / tong_thiet_bi_x2)
    else:
        hop_le_x2 = False

with col_off:
    st.markdown("**Kênh Trực tiếp (Offline)**")
    muc_tieu_hop = st.number_input("Mục tiêu người dự họp", min_value=1, value=300)
    nguoi_du_hop = st.number_input("Số người thực tế dự họp", min_value=0, value=250)
    nguoi_tuong_tac = st.number_input("Số người tương tác/phát biểu", min_value=0, value=150)
    nguoi_duoc_hoi = st.number_input("Số người được hỏi nội dung", min_value=1, value=50)
    tl_dung_off = st.number_input("Số người trả lời đúng (Offline)", min_value=0, value=35)
    
    off1 = kiem_tra_logic(nguoi_du_hop, muc_tieu_hop, "Người dự họp thực tế")
    off2 = kiem_tra_logic(nguoi_tuong_tac, max(1, nguoi_du_hop), "Người tương tác phát biểu")
    off3 = kiem_tra_logic(tl_dung_off, nguoi_duoc_hoi, "Câu trả lời đúng Offline")
    
    if off1 and off2 and off3:
        a2_off = (nguoi_tuong_tac / nguoi_du_hop) * 10 if nguoi_du_hop > 0 else 0
        b2_off = (tl_dung_off / nguoi_duoc_hoi) * 10
        x2_offline = (a2_off * b2_off) * 0.1 * (nguoi_du_hop / muc_tieu_hop)
    else:
        hop_le_x2 = False

if hop_le_x2:
    x2 = (x2_online * w_online) + (x2_offline * w_offline)
    st.success(f"📌 Điểm X2: {x2:.2f}")

st.markdown("---")

# === 3. CHỈ SỐ NIỀM TIN VÀ AN NINH (X3) ===
st.header("3. Chỉ số Niềm tin và an ninh (X3)")
tong_tuong_tac_x3 = st.number_input("Tổng tương tác (Tích cực + Tiêu cực)", min_value=1, value=1000)
tuong_tac_tich_cuc = st.number_input("Số lượt tương tác tích cực (A3)", min_value=0, value=800)
thoi_gian_xu_ly = st.number_input("Thời gian xử lý tin xấu (giờ)", min_value=0.0, value=2.0)

hop_le_x3 = kiem_tra_logic(tuong_tac_tich_cuc, tong_tuong_tac_x3, "Tương tác tích cực X3")
if hop_le_x3:
    a3 = (tuong_tac_tich_cuc / tong_tuong_tac_x3) * 10
    if thoi_gian_xu_ly <= 2: b3 = 10
    elif thoi_gian_xu_ly >= 48: b3 = 0
    else: b3 = 10 - ((thoi_gian_xu_ly - 2) * (10 / 46)) # [cite: 188]
    x3 = (a3 * 0.7) + (b3 * 0.3)
    st.success(f"📌 Điểm X3: {x3:.2f}")

st.markdown("---")

# === 4. CHỈ SỐ HÀNH ĐỘNG VÀ SINH KẾ (X4) ===
st.header("4. Chỉ số Hành động và sinh kế (X4)")
ho_thu_huong = st.number_input("Số hộ thụ hưởng chính sách", min_value=1, value=200)
ho_dang_ky = st.number_input("Số hộ chủ động đăng ký (A4)", min_value=0, value=160)
ho_xu_ly = st.number_input("Số hộ được xử lý thành công (B4)", min_value=0, value=120)
muc_tieu_de_ra = st.number_input("Mục tiêu chính sách", min_value=1, value=50)
gia_tri_thuc_te = st.number_input("Mô hình thực tế (C4)", min_value=0, value=40)

h1 = kiem_tra_logic(ho_dang_ky, ho_thu_huong, "Hộ đăng ký X4")
h2 = kiem_tra_logic(ho_xu_ly, max(1, ho_dang_ky), "Hộ xử lý X4")
h3 = kiem_tra_logic(gia_tri_thuc_te, muc_tieu_de_ra, "Mô hình thực tế X4")

if h1 and h2 and h3:
    a4 = (ho_dang_ky / ho_thu_huong) * 10
    b4 = (ho_xu_ly / ho_dang_ky) * 10 if ho_dang_ky > 0 else 0
    c4 = (gia_tri_thuc_te / muc_tieu_de_ra) * 10
    x4 = (a4 * 0.4) + (b4 * 0.3) + (c4 * 0.3) # [cite: 198]
    st.success(f"📌 Điểm X4: {x4:.2f}")
else:
    hop_le_x4 = False

st.markdown("---")

# === 5. TỔNG KẾT VÀ XUẤT FILE ===
st.header("5. Tổng Kết Hiệu Quả")
col_w1, col_w2, col_w3, col_w4 = st.columns(4)
with col_w1: w1 = st.number_input("Trọng số w1", value=0.2)
with col_w2: w2 = st.number_input("Trọng số w2", value=0.3)
with col_w3: w3 = st.number_input("Trọng số w3", value=0.2)
with col_w4: w4 = st.number_input("Trọng số w4", value=0.3)

if st.button("🚀 TÍNH TOÁN KẾT LUẬN", use_container_width=True):
    if hop_le_x1 and hop_le_x2 and hop_le_x3 and h1 and h2 and h3:
        tong_x = (x1 * w1) + (x2 * w2) + (x3 * w3) + (x4 * w4) # 
        
        # Xếp loại chuẩn tài liệu [cite: 212, 213, 214, 215]
        if tong_x > 8.5: xep_loai, mau = "RẤT HIỆU QUẢ", "green"
        elif tong_x > 6.5: xep_loai, mau = "HIỆU QUẢ", "blue"
        elif tong_x > 5.0: xep_loai, mau = "ÍT HIỆU QUẢ", "orange"
        else: xep_loai, mau = "CHƯA HIỆU QUẢ", "red"

        st.balloons()
        st.markdown(f"### Kết quả: <span style='color:{mau}'>{xep_loai} ({tong_x:.2f} điểm)</span>", unsafe_allow_html=True)

        data = {
            "Chỉ số": ["Năng lực thực thi (X1)", "Thấu hiểu chuyển đổi (X2)", "Niềm tin an ninh (X3)", "Hành động sinh kế (X4)", "TỔNG ĐIỂM (X)"],
            "Điểm số": [round(x1, 2), round(x2, 2), round(x3, 2), round(x4, 2), round(tong_x, 2)],
            "Xếp loại": ["-", "-", "-", "-", xep_loai]
        }
        df = pd.DataFrame(data)

        def to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='BaoCao')
            return output.getvalue()

        st.download_button(
            label="📥 Tải Báo Cáo Kết Quả Excel",
            data=to_excel(df),
            file_name="bao_cao_truyen_thong_sanchi.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error("Vui lòng kiểm tra lại các thông số bị báo đỏ ở trên trước khi tính tổng điểm!")
