# Dàn ý đề xuất cho báo cáo Survey và EDA

Ngày 25/11/2026. Trạng thái đề xuất để duyệt. Đây là dàn ý cho hai đầu ra riêng, gắn với [Define](project_define.md), [Design](project_design.md) và [hai form](../reference/forms/README.md).

Tên dự kiến là `docs/survey_report.md` và `docs/eda_report.md`. Markdown thuận tiện lưu lịch sử trong Git. Nếu cần bản Word để nộp, định dạng xuất bản sẽ được chốt khi nghiệm thu. Notebook dự kiến là `notebooks/ait_lds_eda.ipynb`.

## Báo cáo Survey

Phần mở đầu ghi phạm vi tám archive no-pcaps, phiên bản tài liệu, ngày truy cập nguồn và tình trạng kiểm chứng. Phần chính giữ 11 nhóm của form.

| Mục | Nội dung cần trình bày | Bằng chứng và phần cần kiểm chứng |
|---|---|---|
| 1. Thông tin định danh | Tên, viết tắt, phiên bản, tác giả, nhà phát hành, năm công bố, DOI, URL và citation | Trang phát hành và bài báo gốc. Phân biệt năm phát hành với lịch mô phỏng. |
| 2. Mục đích tạo dataset | Bài toán tác giả hướng đến, mục tiêu sử dụng của lab | Trích nguồn cho mục đích ban đầu, ghi riêng câu hỏi nghiên cứu của lab. |
| 3. Tổ chức phát sinh log | Tổ chức được tái hiện, loại hình, ngành, người dùng, địa lý và múi giờ | Nêu rõ điều nguồn có công bố và phần chưa rõ. |
| 4. Hệ thống sinh dữ liệu | Host, dịch vụ, phần mềm, nguồn log, phạm vi quan sát của từng nguồn | Đối chiếu danh mục nguồn log với manifest sau khi có dữ liệu. |
| 5. Môi trường phát sinh | Testbed, cách tạo hoạt động người dùng và tấn công | Đọc kiến trúc và quy trình tác giả trước khi phân loại. |
| 6. Tính xác thực | Thành phần hoạt động thật, được giả lập, được biến đổi hoặc sinh ngẫu nhiên | Ghi hệ quả đối với tính đại diện của hành vi tài khoản. |
| 7. Bối cảnh thời gian | Lịch mô phỏng từng dataset, biểu diễn và độ phân giải thời gian | Sau này đối chiếu `dataset.yml`, timestamp nguồn và căn cứ múi giờ. |
| 8. Thành phần dữ liệu | Tám archive, cấu trúc thư mục, định dạng và đơn vị bản ghi | Phân biệt dòng vật lý và sự kiện logic. Kiểm chứng cấu trúc, kích thước, số đếm. |
| 9. Thu thập và xử lý trước công bố | Collector, tiêu chí giữ/bỏ, ẩn danh, tính nhất quán định danh, lỗi và khoảng trống công bố | Ghi giới hạn của bản no-pcaps và ảnh hưởng của việc chọn log tới câu hỏi hành vi. |
| 10. Nhãn | Cách tạo, đơn vị nhãn, loại nhãn, quy tắc đường dẫn và số dòng, thời điểm nhãn khả dụng | Kiểm chứng phép ghép `labels/` với `gather/`. Dẫn cách tác giả diễn giải dòng thiếu annotation và giới hạn xác minh của cách diễn giải đó. |
| 11. Hướng dẫn sử dụng | Mục đích được tác giả khuyến nghị, hạn chế đã công bố, mức phù hợp sơ bộ cho HKDN | Kết luận sơ bộ được cập nhật bằng dẫn chiếu kết quả EDA. |

Phụ lục gồm danh mục nguồn, bảng tóm tắt riêng cho từng archive và ma trận bằng chứng. Mỗi claim có mã, nội dung, nguồn cụ thể, phép kiểm dự kiến, artifact hoặc `run_id`, trạng thái và kết luận sau kiểm chứng. Phần chưa có nguồn ghi “Không rõ”.

## Báo cáo EDA

Phần mở đầu ghi phạm vi thực sự đã đọc, đầu vào/checksum, phiên bản code, môi trường, cấu hình và `run_id`. Các mục bám theo bước 1–18 trong form để dễ đối chiếu với notebook.

| Mục | Nội dung và đầu ra dự kiến |
|---|---|
| 1. Phạm vi và câu hỏi | Câu hỏi tài khoản có thể kiểm chứng, thực thể, đơn vị phân tích, phạm vi toàn bộ và mẫu. |
| 2. Nạp và kiểm kê | Bảng archive/file/host/nguồn, kích thước, số dòng, trạng thái đọc, độ phủ tám archive. |
| 3. Schema và ý nghĩa trường | Từ điển trường thực tế theo nguồn, định dạng, parse status và đối chiếu Survey. |
| 4. Thực thể và liên kết | Khóa tài khoản, host, IP, phiên, quan hệ nối có căn cứ và tỷ lệ nối được. |
| 5. Dữ liệu thiếu | Bảng thiếu theo trường và nguồn với mẫu số bản ghi mà trường áp dụng. |
| 6. Hợp lệ, nhất quán và trùng | Lỗi định dạng, miền giá trị, rotation, trùng dòng hoặc sự kiện và quyết định xử lý. |
| 7. Toàn vẹn thời gian | Thiếu/lỗi timestamp, múi giờ, đảo thứ tự, độ phân giải và trong/ngoài/chưa xác định so với `dataset.yml`. |
| 8. Độ bao phủ | Heatmap nguồn–host–thời gian, khoảng thiếu quan sát, tỷ lệ nguồn đã parse được. Khoảng không có log cần căn cứ trước khi diễn giải thành mất dữ liệu. |
| 9. Phân bố từng trường | Tần suất, độ đa dạng, phân vị cho trường phù hợp, kèm tỷ lệ phần chưa parse được. |
| 10. Hồ sơ thực thể | Số sự kiện, nguồn, máy và thời gian hoạt động theo tài khoản trên phần định danh được. |
| 11. Mẫu hình thời gian | Lượng log theo dataset/host/nguồn, nhịp hoạt động trên thời gian đã xác minh. |
| 12. Phiên và chuỗi | Quy tắc dựng phiên, tỷ lệ nối, phiên thiếu biên, độ dài và chuyển tiếp. Kiểm tra độ nhạy ngưỡng nếu phải suy ra phiên. |
| 13. Hành vi nền và tính mới | Độ dài lịch sử, cold start, tỷ lệ giá trị mới chỉ dựa trên lịch sử trước sự kiện. |
| 14. Quan hệ đa nguồn | Bảng liên kết và độ phủ, lệch thời gian, quan hệ tài khoản–host và giả thuyết có căn cứ. |
| 15. Nhãn và khoảng tấn công | Lỗi ghép, annotation mồ côi/trùng/nhiều nhãn, phân bố theo từng đơn vị đếm, timeline trước–trong–sau tấn công. Báo rõ nguồn xác định ranh giới bước và ca. |
| 16. Tín hiệu hành vi khả thi | Bảng trường/chuỗi ứng viên, căn cứ EDA, độ phủ, thời điểm khả dụng, giới hạn và khả năng giải thích. |
| 17. Leakage và khả năng đánh giá | Metadata, lịch tấn công, nhãn hậu nghiệm, trùng giữa nhóm hoặc thời gian, Test và nguy cơ dùng tương lai. Đánh giá khả năng tách dữ liệu có căn cứ ở mức dữ liệu/nhãn. |
| 18. Tổng hợp và kết luận | Phát hiện, bằng chứng, diễn giải, hạn chế, hệ quả, hành động. Ma trận câu hỏi HKDN trả lời được/một phần/chưa đủ dữ liệu, đối chiếu Survey và Data Quality Log. |

Notebook có mục 0 thiết lập và các mục tương ứng 1–18. Mỗi mục gồm câu hỏi, code, bảng/hình và nhận xét. Phần chưa áp dụng vẫn ghi lý do và bằng chứng giới hạn. Mục 16–17 dừng ở đánh giá dữ liệu theo phạm vi được giao.

## Viết báo cáo trong khi kiểm tra

1. Survey sơ bộ ghi công bố có dẫn nguồn và danh sách claim còn cần đo. Mỗi claim giữ mã xuyên suốt lab.
2. Mỗi lần chạy tạo manifest và `run_id`. Kết quả đo cập nhật EDA và ma trận bằng chứng, kèm số lượng ngoại lệ. Khi thay đổi bộ đọc, đánh dấu các kết quả phụ thuộc cần chạy lại.
3. Survey giữ nội dung nguồn công bố, thêm ghi chú đối chiếu và liên kết đến mục EDA tương ứng. Nếu khác nhau, ghi cả hai cùng phạm vi và căn cứ.
4. Báo cáo cuối và notebook dùng cùng lần chạy đã nghiệm thu. Mỗi số liệu có dataset, host/nguồn liên quan, thời gian, đơn vị, mẫu số, phạm vi mẫu/toàn bộ và artifact. Phân biệt kết quả đo, diễn giải và giả thuyết.

Tổng số dòng và tỷ lệ nhãn tính trên toàn bộ phần dữ liệu tương ứng. Nếu giới hạn tài nguyên buộc dùng mẫu để khảo sát chuỗi, ghi quy tắc lấy mẫu theo thực thể hoặc cửa sổ liên tục và độ phủ. Báo cáo chia sẻ chỉ trình bày số tổng hợp hoặc định danh đã bảo vệ theo privacy.
