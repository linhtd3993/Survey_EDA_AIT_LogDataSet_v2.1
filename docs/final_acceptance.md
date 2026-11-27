# Nghiệm thu và demo AIT-LDS v2.1

Lần chạy `ait-v21-01` dùng tám ZIP no-pcaps trong manifest phát hành. Báo cáo nộp gồm [Survey](survey_report.md), [EDA](eda_report.md) và [notebook đã thực thi](../notebooks/ait_lds_eda.ipynb). Ngày nghiệm thu 26/11/2026.

| Điều kiện | Bằng chứng đã kiểm tra |
|---|---|
| Đủ và đúng đầu vào | 8/8 archive có kích thước và MD5 khớp. Tất cả có dataset.yaml và lịch mô phỏng khớp nguồn. |
| Bộ đọc và ghép nhãn | 5 test đạt, bao gồm ví dụ tác giả, biên dòng, annotation lỗi/lặp, timestamp thiếu múi giờ và timestamp có offset. |
| Đối soát số liệu | Kiểm tra danh mục file log và nhãn với ZIP, tổng annotation hợp lệ/lỗi, số dòng riêng và tổng lượt gán. Đối chiếu số dòng thời gian theo file, tổng theo giờ và khoảng tấn công. |
| Notebook và báo cáo | Kernel mới chạy đủ 19 ô code. 4 hình nhúng khớp byte với 4 PNG. 8 hàng số liệu báo cáo khớp manifest và bảng thời gian. 96 artifact có hash ổn định khi chạy lại notebook từ các bảng kiểm kê. |
| Phạm vi và privacy | Sản phẩm chia sẻ gồm số tổng hợp, loại nhãn, loại sự kiện và mã dataset. File kiểm kê cục bộ giữ đường dẫn gốc để truy vết. ZIP, bảng chi tiết, cache và reference được Git ignore. |

## Tái lập trên Windows

Từ thư mục gốc lab, dùng Python 3.12 và môi trường riêng. Lệnh tải chỉ đọc danh mục tám no-pcaps, xác minh MD5 trước khi dùng. Các lệnh dưới đây ghi kết quả vào thư mục run nêu trên.

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r configs/requirements.txt
.venv/Scripts/python scripts/download.py
.venv/Scripts/python scripts/archive_manifest.py
.venv/Scripts/python -m unittest discover -s tests -v
.venv/Scripts/python scripts/inventory.py
.venv/Scripts/python scripts/profile_events.py
.venv/Scripts/python scripts/extended_time.py
.venv/Scripts/python scripts/verify.py
.venv/Scripts/python scripts/run_notebook.py
```

Các script inventory/profile ghi số liệu từng dataset. Bảng thời gian dùng giờ UTC ở độ phân giải giờ. Tệp ZIP giữ nguyên khóa dataset–đường dẫn–dòng gốc. Test author example minh họa đọc lại timestamp trong dòng audit từ ZIP. Manifest lưu phiên bản Python, checksum đầu vào, tổng số và SHA-256 code/cấu hình. Bảng chi tiết xuất hiện lại khi chạy các lệnh trên. Notebook chứa sẵn hình và bảng để đọc ngay khi clone repo.

## Demo đề xuất

1. Mở Survey và chọn công bố về cách tham chiếu nhãn theo số dòng. Chạy test author example để truy bốn annotation tới bốn sự kiện audit.
2. Mở mục 15 của notebook. Chọn russellmitchell và so 46.346 dòng có annotation trước cửa sổ với 9.808 dòng trong cửa sổ. Dùng bảng theo nguồn để giải thích vì sao lịch tấn công chỉ hỗ trợ đối chiếu.
3. Mở mục 5 và 12. Dùng số dòng audit có acct và mã phiên để giải thích câu hỏi hành vi tài khoản nào trả lời được. Kết thúc bằng bảng câu hỏi HKDN trong EDA.

## Giới hạn nghiệm thu

Kiểm kê file và kiểm tra tham chiếu nhãn bao phủ cả tám archive. Phân tích chính theo giờ bao phủ năm nhóm nguồn. Tỷ lệ phù hợp của nhãn với nội dung sự kiện trên toàn tập, độ trùng nội dung toàn corpus và số sự cố chiếm tài khoản độc lập chưa được xác định. Đối soát nhãn ngoài cửa sổ ghi bằng chứng theo đồng hồ nguồn, chưa xác định nguyên nhân của chênh lệch DNS. Bản nghiệm thu kiểm tra chạy lại notebook trên bảng trung gian và đối chiếu với manifest của lần kiểm kê toàn bộ.
