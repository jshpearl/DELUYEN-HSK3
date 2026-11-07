# HSK3 Online Exam Web Application (v13) - Cô Bảo Ngọc (黄宝玉老师)

Phiên bản cập nhật v13 bổ sung hoàn chỉnh đề thi **H31219** chuẩn xác 100% theo tài liệu gốc Hanban/孔子学院. Hiện tại hệ thống có đầy đủ 4 bộ đề: **H31003, H31008, H31111, H31219**.

## Cấu trúc từng đề thi trong ứng dụng (Đầy đủ 70 câu/đề)
- **Phần Nghe (35 câu, STT 1–35)**:
  - 10 câu đầu: Phán đoán đúng/sai dựa theo lời thoại ngữ cảnh.
  - 10 câu tiếp: Phán đoán nội dung đúng/sai trực tiếp theo đề thi gốc.
  - 15 câu sau: Trắc nghiệm hội thoại (A/B/C) kèm câu hỏi.
  - Sau khi nộp bài: Hiển thị đầy đủ **Audio Script (听力材料)**.
- **Phần Đọc (25 câu, STT 41–65)**:
  - 10 câu ghép nối câu hội thoại tương ứng (41–50).
  - 10 câu điền từ ngữ thích hợp vào chỗ trống (51–60).
  - 5 câu đọc hiểu đoạn văn ngắn chọn đáp án đúng (61–65).
  - Sau khi nộp bài: Hiển thị đáp án đúng/sai và giải thích chi tiết.
- **Phần Viết (10 câu, STT 71–80)**:
  - 5 câu sắp xếp từ thành câu hoàn chỉnh (71–75). Chữ Hán to rõ 28px, chấm điểm nghiêm ngặt 100% đúng cả dấu câu (。, ？).
  - 5 câu điền chữ Hán vào chỗ trống theo phiên âm (76–80).

## Tóm tắt nội dung đề H31219 mới bổ sung:
- **Nghe (1–35)**: Đầy đủ 35 câu với Audio Script kèm theo.
- **Đọc (41–65)**:
  - 41–50: Ghép nối câu đối thoại chuẩn đề gốc H31219 (bánh kem, áo sơ mi, email, điểm thi toán, tắt đèn bếp, hộ chiếu, bài toán 5 hào, điện thoại mới, sĩ số học sinh, chỉ đường).
  - 51–60: Điền từ vào chỗ trống: 铅笔, 短, 国家, 复习, 应该, 担心, 放心, 重要, 又, 练习.
  - 61–65: Đoạn văn chọn đáp án đúng (Sự lựa chọn, Hàng xóm họ Nguyên, Khám chân ở bệnh viện, Nhờ gọi điện thoại, Chuẩn bị đón khách).
- **Viết (71–80)**:
  - 71: 蓝小姐对人非常热情。
  - 72: 邻居高兴地走了。
  - 73: 妹妹长得最像妈妈。
  - 74: 请根据要求回答问题。
  - 75: 街道被打扫干净了。
  - 76: 花 (huā)
  - 77: 水 (shuǐ)
  - 78: 也 (yě)
  - 79: 雨 (yǔ)
  - 80: 个 (ge)

## Tính năng hệ thống giữ nguyên chuẩn mực:
1. Giao diện trang chủ dạng Grid 4 khối hình vuông Pastel viền màu đậm.
2. Ẩn hoàn toàn header, menu, icon góc trên bên phải của Streamlit.
3. Đồng hồ đếm ngược iframe HTML/JS độc lập, chạy mượt mà từng giây, đổi màu đỏ nhấp nháy khi còn dưới 5 phút, tự động nộp bài khi về 00:00.
4. Tự động đồng bộ kết quả làm bài về Google Sheet cô Bảo Ngọc qua Webhook URL đã tích hợp.
5. Chân trang có dòng chữ thương hiệu: **黄宝玉老师**.
