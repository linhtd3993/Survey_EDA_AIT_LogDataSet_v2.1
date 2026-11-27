# Sử dụng AI trong lab Survey và EDA AIT Log Data Set v2.1

**Cập nhật ngày 25/11/2026.** Bản ghi hiện bao phủ công việc chuẩn bị tài liệu. Các mục về kiểm tra dữ liệu bên dưới là tiêu chí cho giai đoạn sau.

## 1. AI Tools Used — Công cụ

Sinh viên sử dụng ChatGPT/Codex để đọc tài liệu trong workspace, đối chiếu yêu cầu giữa các nguồn, soạn Markdown và rà soát cấu trúc tài liệu. Repo riêng của lab là nơi lưu sản phẩm. Bản sao trong `reference/` cung cấp ngữ cảnh HKDN và quy trình Lab 2.

## 2. Main Workflow & Progress — Công việc đã thực hiện

| Yêu cầu của sinh viên | Phần AI hỗ trợ | Minh chứng |
| --- | --- | --- |
| Xác định phạm vi lab độc lập | Tổng hợp mục tiêu, nguồn dữ liệu và đầu ra | [README](../README.md) |
| Định nghĩa bài toán và tiêu chí đánh giá | Soạn tài liệu theo thứ tự tám mục sinh viên yêu cầu | [Project Define](project_define.md) |
| Thiết kế cách thực hiện và nghiệm thu | Mô tả module, luồng dữ liệu, giao diện, tiến độ và rủi ro | [Project Design](project_design.md) |
| Làm rõ vai trò của AI | Đối chiếu mẫu AI Usage của Lab 2 và kiểm kê tài liệu hiện có | Bản ghi này và danh mục vị trí trả cho sinh viên |

## 3. Student Contributions — Đóng góp của sinh viên

Sinh viên chọn AIT Log Data Set v2.1, giới hạn đầu vào ở tám archive `*_no-pcaps.zip`, cung cấp nguồn và tạo repo riêng. Sinh viên yêu cầu hai báo cáo độc lập cho Survey và EDA, chỉ định thứ tự các mục Define/Design, yêu cầu phân biệt thông tin tác giả công bố với kết quả đo, và giữ quyền duyệt thời điểm bắt đầu xử lý dữ liệu.

## 4. Prompt Engineering & Proposals — Cách giao việc và điều chỉnh

| Chỉ dẫn của sinh viên (tóm lược) | Ảnh hưởng tới sản phẩm |
| --- | --- |
| Tham khảo Lab 2 về tổ chức công việc, báo cáo và demo | Dùng cấu trúc đặc tả và tiêu chí nghiệm thu phù hợp với log |
| Tách phần có nguồn công bố khỏi phần cần dùng code kiểm chứng | Báo cáo Survey dự kiến dẫn tài liệu tác giả cho mô tả nguồn và dẫn manifest cho số đo thực tế |
| Đánh giá bộ dữ liệu phục vụ câu hỏi hành vi tài khoản đến đâu | Báo cáo EDA dự kiến nêu nguồn log, trường, độ bao phủ và giới hạn cho từng câu hỏi |

## 5. Verification & Quality Control — Kiểm chứng

Ở bước tài liệu, vị trí và nội dung được đối chiếu trên file cục bộ. Khi được duyệt chạy, mỗi kết luận về dữ liệu cần có nguồn tương ứng. Mô tả của tác giả dẫn về [bản phát hành AIT](https://zenodo.org/records/19483937). Số đo phải truy được về manifest, phiên chạy, dataset, host hoặc nguồn log, khoảng thời gian, đơn vị đếm và mẫu số.

Với phép ghép nhãn, cần lưu kết quả kiểm tra đường dẫn, số dòng, tham chiếu ngoài phạm vi và các dòng mang nhiều nhãn. Khi nghiệm thu EDA, cần chạy notebook từ đầu đến cuối và đối chiếu số liệu trong bảng, hình với manifest. Chỉ ghi các bước này là hoàn tất khi có đầu ra để kiểm tra.

## 6. Limitations & Manual Adjustments — Giới hạn và hiệu chỉnh

Cập nhật chuẩn bị ngày 25/11/2026 theo yêu cầu sinh viên, Codex đã sao chép hai form vào `reference/forms/`, đối chiếu SHA-256 với nguồn, thêm bản đồ tài liệu trong README, soạn [dàn ý báo cáo](report_outlines.md) và [milestone cho agent](milestones.md). Đây là sản phẩm lập kế hoạch để duyệt.

Tài liệu HKDN mô tả nhu cầu của Team 2. Việc một trường xuất hiện trong contract chưa chứng minh trường đó có trong log AIT. Sinh viên sẽ xem xét bằng chứng ghép nhãn, ý nghĩa của dòng thiếu nhãn, rủi ro dùng thông tin xuất hiện sau sự kiện và giới hạn suy luận về tài khoản trước khi duyệt kết luận.

Khi cập nhật bản ghi, ghi ngày, yêu cầu, phần AI đề xuất, phần sinh viên sửa hoặc quyết định, cùng đường dẫn tới bằng chứng kiểm tra. Chỉ đưa ví dụ log đã xử lý theo quy định privacy vào tài liệu chia sẻ.
Ngày 26/11/2026, theo chỉ định thực hiện M1–M8, Codex đọc nguồn tác giả, tải và xác minh tám ZIP, viết bộ kiểm kê, chạy pilot và test, đo toàn bộ tập, chạy notebook và viết hai báo cáo. Sinh viên giao phạm vi và yêu cầu cập nhật từng mốc. Kết quả thực thi của agent và giới hạn nằm trong [biên bản nghiệm thu](final_acceptance.md). Việc sinh viên hoặc mentor duyệt nội dung học thuật là bước riêng.
