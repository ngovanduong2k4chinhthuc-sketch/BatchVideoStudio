BATCH VIDEO STUDIO - PROJECT TẠO BẢN WINDOWS PORTABLE

Mình chưa thể biên dịch/kiểm thử file EXE Windows ngay trong môi trường hiện tại. Dự án có sẵn workflow GitHub Actions để build miễn phí trên máy Windows của GitHub; máy dùng ứng dụng không cần cài Python.

CÁCH TẠO ZIP PORTABLE:
1. Tạo repository GitHub mới.
2. Tải toàn bộ nội dung thư mục dự án này lên repository (bao gồm thư mục .github).
3. Mở tab Actions, chọn “Build Windows Portable ZIP”.
4. Bấm Run workflow.
5. Khi chạy xong, mở lần chạy thành công và tải Artifact “BatchVideoStudio_Portable_Windows”.
6. Giải nén ZIP, mở thư mục BatchVideoStudio, nhấp đúp BatchVideoStudio.exe.

CHỨC NĂNG BẢN ĐẦU:
- Ghép 1 video + 1 ảnh tĩnh + 1 SRT theo tên file trùng nhau.
- Ảnh giữ xuyên suốt video; scale/pad theo tỷ lệ video, không kéo méo.
- Giữ âm thanh nguồn, mã hóa AAC cho MP4.
- Chỉnh font, cỡ chữ, màu, viền, vị trí, lề phụ đề.
- Hiệu ứng khói dạng mây/nhiễu chuyển động, Radio/VHS, hoặc kết hợp.
- Xử lý tuần tự, bỏ qua bộ thiếu file, ghi nhật ký, dừng sau video hiện tại.
- Ưu tiên NVIDIA NVENC, tự thử CPU x264 nếu NVENC không chạy.

ĐẶT TÊN FILE:
clip001.mp4 + clip001.jpg + clip001.srt
clip002.mp4 + clip002.png + clip002.srt
Tên phần trước dấu chấm phải giống nhau.

LƯU Ý:
- Hiệu ứng khói hiện tại là lớp mây/nhiễu tạo bằng filter, chưa phải khói điện ảnh chân thực.
- Chưa có cửa sổ xem trước.
- Hãy thử 1–2 video ngắn trước khi xử lý hàng loạt.
- Chỉ dùng video, âm thanh và phụ đề mà bạn sở hữu hoặc được cấp phép. Thay hình ảnh hay thêm hiệu ứng không tạo ra quyền sử dụng nội dung hoặc bảo đảm đủ điều kiện kiếm tiền YouTube.
