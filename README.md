# BÀI THỰC HÀNH KIỂM THỬ TỰ ĐỘNG BẰNG SELENIUM

- Sinh viên: **Bùi Quang Huy**
- Website kiểm thử: **SauceDemo** — https://www.saucedemo.com/
- Công cụ: Python, Selenium WebDriver, pytest, pytest-html, Google Chrome.
- Phạm vi: kiểm thử giao diện theo phương pháp hộp đen, gồm xác thực, giỏ hàng và danh sách sản phẩm.

## 1. Mục tiêu và website được lựa chọn

Bài thực hành xây dựng 8 test case tự động để kiểm tra các thao tác phổ biến trên website bán hàng mẫu SauceDemo. Đây là website demo; dữ liệu đăng nhập trong mã là tài khoản thử nghiệm công khai, không phải tài khoản cá nhân. Bộ kiểm thử không thực hiện thanh toán.

Mỗi test mở một phiên Chrome mới để tránh ảnh hưởng trạng thái giữa các trường hợp. Selenium tìm phần tử bằng `data-test`, CSS selector và ID; `WebDriverWait` chờ điều kiện cụ thể thay cho thời gian ngủ cố định. Các assertion kiểm tra kết quả hiển thị, URL, số lượng và nội dung sản phẩm.

## 2. Tài liệu tự học

1. Selenium. *Getting started with WebDriver*. https://www.selenium.dev/documentation/webdriver/getting_started/
2. Selenium. *Waiting strategies*. https://www.selenium.dev/documentation/webdriver/waits/
3. Selenium. *Locators*. https://www.selenium.dev/documentation/webdriver/elements/locators/
4. pytest. *How to use fixtures*. https://docs.pytest.org/en/stable/how-to/fixtures.html

Nội dung cần nắm: khởi tạo WebDriver, tìm phần tử, nhập dữ liệu, nhấn nút, chờ điều kiện, kiểm tra kết quả và giải phóng trình duyệt. Fixture phụ trách mở/đóng Chrome; mỗi hàm `test_...` mô tả một tình huống kiểm thử độc lập.

## 3. Môi trường và dữ liệu

- Khuyến nghị Python 3.12 và Google Chrome bản ổn định.
- Kết nối Internet tới SauceDemo và máy chủ tải ChromeDriver.
- Selenium Manager tự tìm/tải driver khi khởi tạo `webdriver.Chrome`.
- Tài khoản đúng: `standard_user` / `secret_sauce`.
- Tài khoản khóa: `locked_out_user` / `secret_sauce`.
- Mật khẩu sai: `wrong_password`.

## 4. Danh sách test case

Điều kiện chung: truy cập được website; mỗi test bắt đầu tại trang đăng nhập với phiên trình duyệt mới.

| Mã | Nội dung | Dữ liệu / bước thực hiện | Kết quả mong đợi |
|---|---|---|---|
| TC01 | Đăng nhập hợp lệ | Nhập standard_user và secret_sauce → Login | URL chứa /inventory.html; tiêu đề Products; có 6 sản phẩm |
| TC02 | Sai mật khẩu | Nhập standard_user và wrong_password → Login | Thông báo Username and password do not match; không vào inventory |
| TC03 | Tài khoản bị khóa | Nhập locked_out_user và secret_sauce → Login | Thông báo Sorry, this user has been locked out.; không vào inventory |
| TC04 | Bỏ trống username | Để trống username, nhập secret_sauce → Login | Thông báo Username is required |
| TC05 | Thêm sản phẩm | Đăng nhập → thêm Sauce Labs Backpack → mở giỏ | Badge bằng 1; giỏ có đúng một sản phẩm Backpack, số lượng 1 |
| TC06 | Xóa sản phẩm | Đăng nhập → thêm Backpack → mở giỏ → Remove | Không còn dòng sản phẩm và badge giỏ hàng |
| TC07 | Sắp xếp giá tăng | Đăng nhập → chọn Price (low to high) | Có 6 giá và dãy giá tăng không giảm |
| TC08 | Đăng xuất | Đăng nhập → mở menu → Logout → truy cập lại inventory | Hiện trang đăng nhập; truy cập inventory bị chặn với thông báo You can only access |

## 5. Cấu trúc mã nguồn

```text
LAB9_DGKDCLPM/
├── .github/workflows/selenium.yml
├── tests/
│   ├── conftest.py
│   └── test_saucedemo.py
├── evidence/                 # Ảnh tự sinh khi chạy
├── reports/                  # Báo cáo HTML và JUnit XML
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

`conftest.py` cấu hình Chrome và chụp ảnh sau mỗi test; nếu lỗi xảy ra khi mở trang, chương trình cũng thử chụp ảnh. Nếu Chrome chưa khởi tạo được thì không thể có ảnh. `test_saucedemo.py` chứa 8 tình huống và các hàm thao tác dùng chung. Không sửa website để làm test thành công.

## 6. Cài đặt và chạy trên Windows PowerShell

Mở terminal trong thư mục chứa README này:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest
```

Chạy có cửa sổ Chrome để quan sát:

```powershell
.\.venv\Scripts\python.exe -m pytest --headed
```

Chạy riêng một test:

```powershell
.\.venv\Scripts\python.exe -m pytest -k TC05 --headed
```

Trên Linux/macOS:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest
```

Mở `reports/report.html` sau khi chạy. `reports/results.xml` chứa kết quả máy đọc được; ảnh nằm trong `evidence/` với tên test và kết quả. Mỗi lần chạy báo cáo được ghi lại; nên lưu bản cũ nếu cần so sánh. Ảnh cũ không tự xóa, do đó chỉ dùng ảnh tương ứng lần chạy đang báo cáo.

## 7. Kết quả thực nghiệm

Đã chạy thực tế trên GitHub Actions ngày **21/10/2026**, Ubuntu 24.04, Python 3.12.15, Selenium 4.51.0. Kết quả: **6 Passed, 2 Failed trong 43.18 giây**.

| Test | Kết quả |
|---|---|
| TC01 – Đăng nhập hợp lệ | Passed |
| TC02 – Sai mật khẩu | Passed |
| TC03 – Tài khoản bị khóa | Passed |
| TC04 – Bỏ trống username | Passed |
| TC05 – Thêm vào giỏ | Passed |
| TC06 – Xóa khỏi giỏ | Failed: chờ giỏ trống và badge biến mất quá 15 giây |
| TC07 – Sắp xếp giá tăng | Passed |
| TC08 – Đăng xuất | Failed: sau khi nhấn Logout, không tìm thấy nút đăng nhập trong 15 giây |

Hai lỗi trên chưa được xác định nguyên nhân gốc; không kết luận ngay là lỗi website vì cần đối chiếu ảnh, trạng thái trang và thao tác Selenium.

- [Lần chạy có kết quả kiểm chứng](https://github.com/buiquanghuy2005/LAB9_DGKDCLPM/actions/runs/39535739313).
- [Tải báo cáo HTML/XML và 8 ảnh minh chứng](https://github.com/buiquanghuy2005/LAB9_DGKDCLPM/actions/runs/39535739313/artifacts/12317715018) (GitHub có thể yêu cầu đăng nhập; artifact có thời hạn lưu).
- Các báo cáo HTML/XML đang lưu trong thư mục `reports/` của mã nguồn là **lần chạy cục bộ trước đó**, bị chặn Chrome (8 setup errors); xem `reports/EXECUTION.md`. Không nhầm chúng với kết quả CI ở trên.


## 8. Chạy trên GitHub Actions

Workflow tự chạy khi push, tạo pull request hoặc bấm Run workflow trong tab Actions. Sau mỗi lần chạy, tải artifact `selenium-results` để lấy báo cáo và ảnh. Workflow dùng Ubuntu, Python 3.12 và Chrome. Kết quả CI chỉ tồn tại sau khi đã tải mã lên GitHub và workflow thực sự chạy.

## 9. Repository và nộp bài

Repository: https://github.com/buiquanghuy2005/LAB9_DGKDCLPM

```bash
git clone https://github.com/buiquanghuy2005/LAB9_DGKDCLPM.git
cd LAB9_DGKDCLPM
```

Tiếp tục cài thư viện và chạy theo mục 6. Trong tab Actions, mở lần chạy mới nhất để kiểm tra trạng thái và tải artifact `selenium-results`. Kết quả chạy trên máy cục bộ bị giới hạn môi trường được giữ riêng trong `reports/EXECUTION.md`.

Nộp đường dẫn repository tại nơi giao bài và GSheet của lớp.

## 10. Nhận xét

Bộ kiểm thử bao quát 8 trường hợp, vượt mức tối thiểu 5 trường hợp của đề bài. Kiểm thử tự động giúp lặp lại thao tác và kiểm tra kết quả nhất quán. Tuy nhiên, bộ test chỉ kiểm tra những luồng đã mô tả, chưa đánh giá toàn bộ website, hiệu năng, bảo mật hoặc độ tương thích nhiều trình duyệt. Khi SauceDemo thay đổi giao diện hoặc dữ liệu, cần kiểm tra lại selector và kết quả mong đợi.
