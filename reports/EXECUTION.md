# Kết quả chạy thực tế trên GitHub Actions

- Ngày: 21/10/2026 (giờ Việt Nam).
- Run: https://github.com/buiquanghuy2005/LAB9_DGKDCLPM/actions/runs/39535739313
- Commit kiểm thử: e630117c9b1036fda041528172c75e5af67c3408.
- Ubuntu 24.04; Python 3.12.15; Selenium 4.51.0; pytest 9.1.1; pytest-html 4.2.0.
- Lệnh: `python -m pytest`.
- Kết quả: **6 passed, 2 failed trong 43.18 giây**, không có setup error.

TC01, TC02, TC03, TC04, TC05, TC07 Passed. TC06 hết thời gian chờ giỏ trống và badge biến mất; ảnh cuối còn sản phẩm và badge 1. TC08 hết thời gian chờ nút đăng nhập sau Logout; ảnh cuối vẫn ở trang sản phẩm với menu mở. Chưa xác định nguyên nhân gốc của hai trường hợp Failed.

`report.html`, `results.xml` và 8 ảnh trong `evidence/` được lấy nguyên bản từ artifact của lần chạy này. Chú thích ảnh có trong README chính. Các báo cáo cục bộ cũ (8 lỗi setup do môi trường chặn Chrome) đã được thay bằng báo cáo CI; kết quả cục bộ đó không dùng để đánh giá chức năng website.
