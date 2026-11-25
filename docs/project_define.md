# Định nghĩa dự án | Survey & EDA AIT-LDS v2.1

**Trạng thái:** Bản đặc tả để duyệt. **Người đọc:** Team 2 dùng kết quả để chọn nguồn dữ liệu cho Account Behavior Security Gateway. Người nghiệm thu cần truy được từ kết luận về tài khoản đến phép đo và phạm vi quan sát.

## 1. Project Name

Survey và EDA bộ AIT Log Data Set v2.1 cho nghiên cứu hành vi tài khoản. Phiên bản khảo sát gồm tám archive no-pcaps.

## 2. Problem

Một lần xác thực có thể sinh nhiều dòng ở nhiều host. Khi tổng log tăng trong khoảng tấn công, riêng mức tăng chưa cho biết tài khoản nào đã thực hiện hành động. Lab khảo sát bằng chứng cần để nối dòng log với thao tác, thực thể và lịch sử của thực thể đó. Phạm vi gồm Survey và EDA trên tám archive no-pcaps. Gateway, huấn luyện model, pcap và phân tích dataset khác nằm ngoài phạm vi.

## 3. Target User

Team 2 dùng báo cáo để xác định nguồn log nào cho phép nối một thao tác với tài khoản, host và thời gian. Người nghiệm thu dùng notebook cùng manifest để tái tạo số liệu đứng sau từng kết luận.

## 4. Input

Nguồn chuẩn là [bản phát hành Zenodo 19483937](https://zenodo.org/records/19483937) và bài báo của tác giả được dẫn trong đó. Chỉ tiếp nhận archive có hậu tố `_no-pcaps.zip` của fox, harrison, russellmitchell, santos, shaw, wardbeck, wheeler và wilson. Ghi phiên bản và checksum cho từng archive. Dùng contract và privacy của Team 2 để đánh giá khả năng ánh xạ dữ liệu. Việc tiếp nhận AIT vào hệ thống HKDN thuộc quyết định riêng của dự án lớn.

## 5. Output

| Câu hỏi | Đầu ra | Căn cứ nghiệm thu |
|---|---|---|
| Tác giả tạo log và nhãn trong điều kiện nào? | Báo cáo Survey riêng | Đủ 11 nhóm của form Survey, dẫn nguồn từng khẳng định, ghi rõ điều chưa biết và phép kiểm tra tương ứng. |
| Tệp và nhãn có đọc, ghép và truy vết được không? | Manifest và bảng kiểm tra nhãn | Kiểm kê đủ tám archive, giải trình mọi tệp bỏ qua, mọi tham chiếu sai file hoặc ngoài số dòng. |
| Có thể mô tả lịch sử tài khoản nào? | Notebook EDA và báo cáo EDA riêng | Đo độ phủ khóa tài khoản, thời gian và khả năng nối theo từng nguồn. Chỉ trình bày chuỗi khi xác định được thực thể và thứ tự. |
| Kết luận nào có thể dùng cho HKDN? | Bảng đối chiếu trong hai báo cáo | Từng câu hỏi nhận mức đủ bằng chứng, có điều kiện hoặc chưa đánh giá được, kèm số liệu, giới hạn và tham chiếu lần chạy. |

## 6. Core Features

- Kiểm kê từng archive, xác minh checksum và ghi số dòng theo đường dẫn nguồn.
- Ghép annotation theo dòng vật lý gốc, giữ đầy đủ nhãn khi một dòng có nhiều nhãn.
- Đo chất lượng timestamp và khóa liên kết trước khi lập chuỗi hành vi. Đối chiếu lượng log trước, trong và sau khoảng tấn công theo từng testbed.
- Liên kết phát hiện trong báo cáo với bảng, hình và lần chạy để người đọc kiểm tra lại.

### Nội dung Survey và EDA

Survey bao gồm định danh, mục đích ban đầu, tổ chức giả lập, hệ thống sinh log, môi trường, tính xác thực, thời gian, đơn vị bản ghi, thu thập và xử lý trước công bố, nhãn và hướng dẫn sử dụng. Lưu lời công bố cùng nguồn trước khi bổ sung kết quả kiểm chứng.

Notebook theo 18 mục của form EDA. Các bước 1–4 đặc tả phạm vi, kiểm kê, schema và liên kết. Bước 5–8 đo thiếu, lỗi, trùng, chất lượng thời gian và độ phủ. Bước 9–13 mô tả phân bố, thực thể, thời gian, phiên và hành vi nền. Bước 14–15 phân tích quan hệ và nhãn. Bước 16–17 đánh giá tín hiệu ứng viên và leakage. Bước 18 đối chiếu Survey, tổng hợp phát hiện và giới hạn. Giữ mục không áp dụng và giải thích bằng chứng còn thiếu.

## 7. Technology

Đề xuất Python để đọc ZIP theo luồng và tổng hợp theo khối, Jupyter để thực thi notebook, pytest để kiểm tra đánh số dòng và ghép nhãn. Khi chạy thử, ghi dung lượng trống, bộ nhớ cao nhất và thời gian đọc một archive để chọn kích thước khối và quyết định có cần cache. Ghi phiên bản thư viện vào manifest của lần chạy.

## 8. Evaluation

| Chỉ số | Cách tính theo từng dataset và nguồn log |
|---|---|
| Khả năng ghép nhãn | Số annotation phân giải đúng một dòng / tổng annotation trong phạm vi kiểm tra. |
| Độ phủ thời gian | Số bản ghi xác định được thời điểm và thuộc khoảng mô phỏng / tổng bản ghi cần phân tích thời gian. |
| Độ phủ tài khoản | Số sự kiện nối được với tài khoản có bằng chứng / số sự kiện thuộc loại có thể quy cho tài khoản. Ghi tiêu chí chọn mẫu số. |

Mỗi thống kê ghi dataset, nguồn log, cửa sổ thời gian, đơn vị đếm, tử số và mẫu số khi báo tỷ lệ. Báo cáo phân biệt số dòng, sự kiện logic, lượt gán nhãn, bước tấn công và sự cố. Một sự cố chỉ được đếm khi nguồn cung cấp căn cứ xác định ranh giới.

Lab hoàn tất khi cả tám archive đã được xử lý theo cùng quy tắc, notebook chạy từ kernel mới và các bảng, hình, tổng số, nhãn trong báo cáo khớp manifest. Công bố nguồn, số đo trực tiếp và diễn giải phải truy vết riêng. [Thiết kế và cách kiểm tra](project_design.md)
