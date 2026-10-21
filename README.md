# LAB 9 – KIỂM THỬ TỰ ĐỘNG BẰNG SELENIUM

- Sinh viên: **Bùi Quang Huy**.
- Website: **The Internet** — https://the-internet.herokuapp.com/.
- Công cụ: Python, Selenium WebDriver, pytest, pytest-html và Chrome.
- Repository: https://github.com/buiquanghuy2005/LAB9_DGKDCLPM.

## 1. Giới thiệu và mục tiêu

The Internet là website mẫu gồm các trang thực hành thao tác giao diện. Bài làm xây dựng **8 test case tự động** cho đăng nhập, đăng xuất, checkbox, dropdown và thêm/xóa phần tử. Phạm vi là kiểm thử chức năng giao diện theo phương pháp hộp đen; kết quả thực tế được kiểm tra bằng assertion.

Mỗi test dùng một phiên Chrome mới. `WebDriverWait` chờ phần tử hoặc URL theo điều kiện cụ thể, tránh chờ bằng `sleep`. Selenium tìm phần tử qua ID và CSS selector. Sau từng test, chương trình chụp trạng thái trang để làm minh chứng; pytest xuất báo cáo HTML và JUnit XML.

## 2. Tài liệu tự học

1. Selenium. *Getting started*. https://www.selenium.dev/documentation/webdriver/getting_started/
2. Selenium. *Waiting strategies*. https://www.selenium.dev/documentation/webdriver/waits/
3. Selenium. *Locators*. https://www.selenium.dev/documentation/webdriver/elements/locators/
4. Selenium. *Select lists*. https://www.selenium.dev/documentation/webdriver/support_features/select_lists/
5. pytest. *Fixtures*. https://docs.pytest.org/en/stable/how-to/fixtures.html
6. Website thực hành: https://the-internet.herokuapp.com/.

Nội dung áp dụng: khởi tạo và đóng WebDriver; điều hướng; tìm phần tử; nhập dữ liệu; nhấn nút; kiểm tra trạng thái checkbox; chọn dropdown; chờ kết quả; chụp ảnh; tổ chức test bằng fixture và assertion.

## 3. Môi trường và dữ liệu

- Python 3.12, Google Chrome và Internet.
- Các thư viện trong `requirements.txt`.
- Selenium Manager tìm/tải ChromeDriver khi khởi tạo Chrome.
- Tài khoản mẫu công khai: `tomsmith` / `SuperSecretPassword!` (được trang `/login` công bố).
- Username sai: `invalid_user_lab9`; mật khẩu sai: `WrongPassword123!`.
- Không cần cài website hoặc cơ sở dữ liệu trên máy.

## 4. Thiết kế test case

Điều kiện chung: website truy cập được và Chrome khởi tạo thành công. Mỗi test độc lập, tự mở trang và chuẩn bị dữ liệu cần thiết.

| Mã | Chức năng | Các bước / dữ liệu | Kết quả mong đợi |
|---|---|---|---|
| TC01 | Đăng nhập hợp lệ | Mở `/login` → nhập tomsmith / SuperSecretPassword! → Login | URL chứa /secure; tiêu đề Secure Area; thông báo đăng nhập thành công; có Logout |
| TC02 | Sai mật khẩu | Nhập tomsmith / WrongPassword123! → Login | Your password is invalid!; ở /login; còn ô password |
| TC03 | Sai username | Nhập invalid_user_lab9 / SuperSecretPassword! → Login | Your username is invalid!; ở /login |
| TC04 | Đăng xuất | Đăng nhập hợp lệ → Logout | You logged out of the secure area!; về /login; có ô username/password |
| TC05 | Checkbox | Mở `/checkboxes` → xác nhận ô 1 chưa chọn, ô 2 đã chọn → nhấn cả hai | Ô 1 được chọn, ô 2 bỏ chọn |
| TC06 | Dropdown | Mở `/dropdown` → chọn Option 1 → chọn Option 2 | Lựa chọn đầu là Option 1; lựa chọn cuối có value 2 và nhãn Option 2 |
| TC07 | Thêm phần tử | Mở `/add_remove_elements/` → xác nhận rỗng → nhấn Add Element 3 lần | Có đúng 3 nút Delete |
| TC08 | Xóa phần tử | Thêm 3 phần tử → lần lượt nhấn Delete | Số phần tử lần lượt 2, 1, 0 |

## 5. Tổ chức mã nguồn

```text
LAB9_DGKDCLPM/
├── .github/workflows/selenium.yml
├── tests/
│   ├── conftest.py
│   └── test_internet.py
├── evidence/
├── reports/
├── requirements.txt
├── pytest.ini
├── .gitignore
└── README.md
```

`conftest.py` tạo Chrome, đóng trình duyệt sau test và chụp ảnh cuối test. `test_internet.py` chứa 8 test cùng các hàm điều hướng/đăng nhập dùng chung. Mỗi test kiểm tra kết quả bằng assertion, không chỉ thực hiện thao tác.

## 6. Cài đặt và chạy

Clone repository:

```bash
git clone https://github.com/buiquanghuy2005/LAB9_DGKDCLPM.git
cd LAB9_DGKDCLPM
```

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest
```

Hiện cửa sổ Chrome:

```powershell
.\.venv\Scripts\python.exe -m pytest --headed
```

Chạy riêng TC05:

```powershell
.\.venv\Scripts\python.exe -m pytest -k TC05 --headed
```

Linux/macOS:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest
```

Mặc định Chrome chạy headless. Báo cáo: `reports/report.html`, `reports/results.xml`. Ảnh: `evidence/<tên-test>-<passed/failed>.png`. Tải HTML về mở bằng trình duyệt. Mỗi lần chạy ghi lại báo cáo; ảnh cũ cần được đối chiếu theo lần chạy, không dùng lẫn minh chứng.

## 7. Kết quả và minh chứng

Đang chờ lần chạy GitHub Actions cho website The Internet. Chưa ghi nhận Passed/Failed cho bộ test mới. Báo cáo và ảnh của website cũ đã được gỡ khỏi phiên bản hiện tại để tránh nhầm lẫn; các commit cũ vẫn giữ lịch sử.

## 8. GitHub Actions và nộp bài

Workflow `.github/workflows/selenium.yml` tự chạy khi push hoặc tạo pull request; có thể chạy thủ công bằng Run workflow. GitHub cài Chrome và thư viện, thực thi pytest rồi lưu artifact `selenium-results` gồm báo cáo và ảnh kể cả khi test thất bại.

Nộp link repository tại nơi giao bài và GSheet của lớp sau khi kiểm tra README và kết quả chạy.

## 9. Nhận xét

Bộ kiểm thử bao quát xác thực và các thao tác giao diện phổ biến, vượt mức tối thiểu 5 test case. Các test có thể chạy lại tự động và cung cấp kết quả đối chiếu được qua báo cáo, ảnh chụp. Phạm vi chưa gồm hiệu năng, bảo mật hoặc tương thích nhiều trình duyệt. Lỗi kết nối và lỗi khởi tạo Chrome cần phân biệt với lỗi chức năng; không ghi Passed khi chưa chạy thành công.
