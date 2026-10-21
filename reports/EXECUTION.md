# Kết quả thực thi

Ngày thực hiện: 21/10/2026 (giờ Việt Nam).

## Môi trường thực tế

- Linux x86_64; Python 3.12.14.
- Selenium 4.51.0; pytest 9.1.1; pytest-html 4.2.0.
- Chrome for Testing 156.0.8078.47 được Selenium Manager tải xuống.
- Lệnh: `SE_TIMEOUT=45 python3 -m pytest`.

## Kết quả

| Chỉ tiêu | Số lượng |
|---|---:|
| Test thu thập được | 8 |
| Passed | 0 |
| Failed tại assertion | 0 |
| Error tại setup | 8 |

Cả TC01–TC08 đều lỗi khởi tạo Chrome trước khi thực hiện thao tác trên website. Pytest báo `SessionNotCreatedException: Chrome instance exited`. Kiểm tra bằng cách mở Chrome trực tiếp ghi nhận:

```text
FATAL:chrome/browser/process_singleton_posix.cc:297
Check failed: . socket() failed: Operation not permitted (1)
```

Đây là giới hạn môi trường thực thi, chưa phải bằng chứng website có lỗi. Chưa xác nhận 8 test Passed. Không có ảnh minh chứng vì phiên trình duyệt chưa được tạo. Các tệp `report.html` và `results.xml` giữ nguyên kết quả thực tế lần chạy này (8 errors trong 64.92 giây).

## Kiểm tra mã và bước tiếp theo

Mã Python đã được kiểm tra cú pháp bằng `python3 -m compileall -q tests`; pytest đã thu thập đúng 8 test case.

Chạy lại trên Windows có Chrome theo README hoặc đẩy repo lên GitHub để workflow chạy. Sau đó kiểm tra báo cáo HTML, ảnh và cập nhật kết quả thực tế trước khi nộp. Không thay Error thành Passed nếu chưa chạy thành công.
