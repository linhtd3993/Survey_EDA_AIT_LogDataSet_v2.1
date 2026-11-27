# Milestone đề xuất cho AI agent

Ngày 25/11/2026. Kế hoạch để sinh viên duyệt. M0 là công việc chuẩn bị của lượt này. Sinh viên đã giao thực hiện tuần tự M1–M8 và cập nhật khi hoàn thành từng mốc. Sau khi được giao một mốc, AI thực hiện đến khi đạt tiêu chí, xử lý lỗi trong phạm vi và báo cáo bằng artifact.

| Mốc và phụ thuộc | Công việc AI agent | Đầu ra dự kiến | Điều kiện nghiệm thu |
|---|---|---|---|
| M0. Chuẩn bị tài liệu | Gom hai form, ghi nguồn và hash, cập nhật bản đồ tài liệu, đề xuất dàn ý và kế hoạch | `reference/forms/`, dàn ý và tài liệu này | Hai PDF khớp SHA-256 nguồn, liên kết local hợp lệ. Trạng thái đề xuất hiển thị rõ. |
| M1. Survey tài liệu, sau M0 được duyệt | Đọc trang Zenodo và tài liệu tác giả, xác nhận phiên bản, tám no-pcaps, cấu trúc, thời gian, nhãn, giấy phép và điều chưa rõ | Survey sơ bộ, danh mục nguồn và ma trận claim–phép kiểm | Mỗi công bố có nguồn cụ thể. Danh sách bao phủ cả tám archive, các câu hỏi còn mở có cách kiểm tra hoặc lý do chưa thể kiểm. |
| M2. Chuẩn bị dữ liệu, sau M1 | Đo dung lượng trống, lập dự toán ZIP/cache/đầu ra và phương án stream. Tải tám no-pcaps, xác minh checksum, đọc danh mục và metadata | Manifest đầu vào, cấu hình, log tải/kiểm tra, cửa sổ mô phỏng từng dataset | Đủ tám archive đúng phiên bản/checksum, đọc được danh mục, có đủ tài nguyên cho phương án đã chọn. Thiếu đầu vào phải được ghi nhận và xử lý trước khi báo đủ độ phủ. |
| M3. Bộ đọc và ghép nhãn, sau M2 | Đặc tả rồi lập trình bộ đọc, khóa dòng gốc, parse thời gian và ghép nhãn. Thử một archive, so ví dụ nguồn. Test các trường hợp có nguy cơ sai số | Code, cấu hình, fixture/test và log pilot | Kiểm tra dòng trống/lỗi, newline và dòng cuối, rotation, nhiều host, nhiều nhãn, nhãn thiếu file/ngoài phạm vi, timestamp mơ hồ. Giải thích mọi chênh lệch pilot. |
| M4. Kiểm kê và chất lượng toàn bộ, sau M3 | Chạy cùng bộ đọc trên tám archive, phân loại lỗi/thời gian, tổng hợp số dòng và annotation, kiểm tra độ phủ | Manifest file, bảng tổng hợp, Data Quality Log và run manifest | Đối soát số dòng xử lý/bỏ có lý do/lỗi theo nhóm loại trừ nhau. Annotation có trạng thái phân giải. Đối soát riêng dòng có nhãn, lượt gán nhãn, sự kiện, bước và ca khi có ranh giới nguồn. |
| M5. Notebook EDA, sau M4 | Đo chất lượng, lượng log theo thời gian, nhãn, khoảng tấn công, khả năng nối tài khoản và leakage | Notebook, bảng, hình và Data Quality Log | Mỗi hình có phạm vi, mẫu số và nhận xét. Các mục chưa đo được có lý do. |
| M6. Hai báo cáo, sau M5 | Đối chiếu công bố với phép đo, đánh giá câu hỏi HKDN, cập nhật Survey và viết EDA | Hai báo cáo, ma trận bằng chứng | Kết luận truy được tới nguồn hoặc bảng/hình của lần chạy. |
| M7. Chạy lại, sau M6 | Chạy test, khởi động kernel mới, thực thi toàn bộ notebook, đối soát số đếm | Notebook đã chạy, log kiểm tra và đối soát | Tổng số dòng, annotation và các số đếm trong hình khớp bảng nguồn. |
| M8. Nghiệm thu, sau M7 | Kiểm tra phạm vi, privacy, hoàn chỉnh hướng dẫn tái lập và demo | Biên bản nghiệm thu và AI Usage cập nhật | Demo truy một phát hiện về bằng chứng, ghi độ phủ và các câu hỏi còn mở. |

## Theo dõi tiến độ

Mỗi mốc ghi trạng thái đề xuất/đang làm/cần xử lý/đủ điều kiện nghiệm thu/đã nghiệm thu. Bản ghi gồm ngày, phiên bản code, cấu hình, `run_id` nếu có, artifact, kiểm tra đã chạy, vấn đề và tác động tới mốc tiếp theo. M0 hiện đã có sản phẩm chuẩn bị để sinh viên xem xét, trạng thái thực hiện M1–M8 được cập nhật ở cuối tài liệu.

Các mốc trên triển khai chi tiết bốn nhóm trong mục Milestone của Project Design. M1 tương ứng Survey tài liệu, M2–M3 tương ứng chuẩn bị và thử bộ đọc, M4 tương ứng kiểm kê toàn bộ, M5–M8 tương ứng EDA và nghiệm thu.

## Cách agent thực hiện một mốc

Agent kiểm tra Git và tài nguyên liên quan, đọc đặc tả đầu vào/đầu ra, thực hiện, chạy kiểm tra phù hợp rồi đối chiếu điều kiện nghiệm thu. Khi phải sửa logic làm thay đổi số đếm, chạy lại các đầu ra phụ thuộc và lưu lý do. Cuối mốc báo sản phẩm, kết quả kiểm tra, điều chưa xác minh và phụ thuộc tiếp theo.

Tải dữ liệu lỗi có thể tiếp tục tải lại theo checksum. Bộ đọc lỗi được sửa rồi kiểm thử hồi quy. Khi dung lượng thiếu, agent đánh giá cách stream hoặc giảm cache trước khi đề xuất thay đổi nơi lưu. Quyết định mở rộng phạm vi hoặc xóa dữ liệu cần sinh viên xử lý theo quyền đã giao.

Thời lượng sẽ được ước lượng sau M2–M3 từ kích thước thực tế và tốc độ pilot. Mỗi lần báo tiến độ ghi độ phủ đo được, tránh dùng phần trăm hoàn thành thiếu căn cứ.

## Triển khai theo yêu cầu M1–M8

M1 Survey, M2 chuẩn bị dữ liệu, M3 pilot, M4 kiểm kê toàn bộ, M5 notebook EDA, M6 hai báo cáo, M7 chạy lại và đối soát, M8 nghiệm thu và demo. Ngày 25/11/2026 sinh viên giao thực hiện tuần tự và cập nhật tại từng mốc. M1 đã có Survey sơ bộ và manifest công bố.
M2 đã hoàn tất. Cả tám ZIP khớp byte và MD5 công bố. Kết quả kiểm kê đầu vào nằm ở outputs/archive_manifest.json.
M3 đã hoàn tất. Pilot russellmitchell kiểm kê 503 file, đếm 26.263.657 dòng văn bản. Ba test đạt, gồm đối chiếu bốn dòng audit do tác giả công bố.
M4 hoàn tất. 5.483 file, 261.402.985 dòng văn bản và 2.096.892 annotation đã đối soát. M5 hoàn tất. Notebook đã chạy 19 ô code, xuất bốn hình và Data Quality Log.
M6 hoàn tất. docs/survey_report.md có bảng đối chiếu sau EDA. docs/eda_report.md có bảng riêng tám dataset, bốn hình, phân tích nhãn, thời gian và tài khoản.
M7 hoàn tất. 5 test đạt, kernel mới chạy đủ 19 ô code, 96 artifact ổn định, 4 hình và 8 hàng báo cáo đã đối soát. M8 hoàn tất ngày 26/11/2026. Hướng dẫn tái lập, demo và giới hạn nghiệm thu nằm trong [biên bản](final_acceptance.md).
