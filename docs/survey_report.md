# Survey AIT Log Data Set v2.1

## Phạm vi và nguồn

Bản phát hành v2_1 ngày 09/04/2026 của Landauer và cộng sự, DOI 10.5281/zenodo.19483937, giấy phép CC BY-NC-SA 4.0. Danh mục tám ZIP no-pcaps, số byte và MD5 công bố nằm trong [manifest nguồn](../configs/archives.csv). Các thông tin dưới đây thuộc Survey tài liệu.

## Bối cảnh và khả năng quan sát

AIT dựng tám mạng doanh nghiệp nhỏ để đánh giá phát hiện xâm nhập. Dịch vụ thật sinh log khi các tác nhân mô phỏng người dùng tương tác theo kịch bản trong 4–6 ngày. Các testbed có mail, web, chia sẻ file, VPN và firewall. Log xác thực và audit là ứng viên để quan sát tài khoản. Mẫu người dùng được mô phỏng và lịch sử ngắn giới hạn suy luận về nhân viên thực hoặc thay đổi hành vi dài hạn. Ngành, địa lý và mức đại diện dân số tài khoản chưa rõ. [Bài báo về dataset](https://arxiv.org/abs/2203.08580) · [Phương pháp tạo testbed](https://www.skopik.at/ait/2020_trel.pdf)

## Thu thập, thời gian và nhãn

Log lấy từ các host. File có nhãn đã được cắt theo thời gian mô phỏng, các nguồn khác có thể chứa log dựng hoặc thu hồi testbed. Phải giữ số dòng vật lý trước lọc thời gian. Tác giả gán nhãn bằng quy tắc, một annotation có thể chỉ nhiều nhãn bước cho một dòng. Dòng thiếu annotation được tác giả coi là normal trong benchmark. Độ chính xác của cách gán này phụ thuộc độ bao phủ quy tắc và việc nối đúng file/dòng. Lịch tấn công, rule và nhãn là thông tin đối chiếu hồi cứu. Mức ẩn danh giữa nguồn chưa xác định. [Mô tả bản phát hành](https://zenodo.org/records/19483937)

## Các công bố cần kiểm tra trên ZIP

| Công bố | Kiểm tra | Bằng chứng cần lưu |
|---|---|---|
| Tám testbed có bản no-pcaps | So dung lượng, MD5 và danh mục ZIP với manifest | Bảng toàn vẹn từng ZIP |
| gather phân cấp theo host, labels phản chiếu đường dẫn | Ghép dataset, host, path và số dòng, ghi thiếu file/ngoài biên | Bảng kiểm nhãn và số dòng |
| russellmitchell có bốn annotation audit dòng 1860–1863 | So số dòng, loại sự kiện và hai nhãn với ví dụ tác giả | Kết quả pilot |
| dataset.yml ghi cửa sổ mô phỏng | Đo timestamp trong, ngoài và chưa rõ theo nguồn | Bảng coverage và timeline |
| Dấu vết phụ thuộc nguồn và testbed | Kiểm tra ngoại lệ shaw (DNS) và wheeler (thiếu bước dò mật khẩu), phân bố trước/trong/sau lịch công bố | Bảng nhãn riêng từng dataset |
| Log audit có thể hỗ trợ nghiên cứu tài khoản | Đo tỷ lệ có định danh hợp lệ, thời gian và khả năng nối sự kiện | Bảng khả năng trả lời câu hỏi HKDN |

Các phép kiểm trên được lập tại M1. Kết quả sau khi chạy nằm trong bảng đối chiếu cuối báo cáo. Dữ liệu hướng tới đánh giá IDS và liên kết dấu vết nhiều nguồn. Mức phù hợp riêng cho hành vi tài khoản cần kết quả EDA.

### Lịch công bố

[Lịch tám testbed](../configs/published_windows.csv) ghi thời điểm bắt đầu và kết thúc mô phỏng, cùng khoảng tấn công riêng từng testbed theo Zenodo. Độ phân giải được công bố trong bảng là phút. Chỉ so sánh với timestamp của log sau khi đối chiếu múi giờ từ metadata. Không gộp tám lịch thành một chuỗi người dùng liên tục.

Bài báo mô tả bản v2.0 và nêu rằng tác giả chọn các file có dấu vết đủ rõ để viết quy tắc. Một số dấu vết ở file khác nằm ngoài phạm vi gán nhãn (§4.4). Đây là căn cứ để trình bày riêng độ phủ của rule khi đánh giá v2.1. Các giá trị IP và tên người dùng được chọn khi khởi tạo từng testbed (§3.1), vì vậy cần giữ dataset trong khóa thực thể. [Phương pháp và phạm vi gán nhãn](https://arxiv.org/html/2203.08580)

## Đối chiếu sau EDA

| Nội dung nguồn | Đo trên tám archive | Kết luận |
|---|---|---|
| Danh mục bản no-pcaps | 8/8 khớp kích thước và MD5 | Đã xác minh đầu vào |
| Tên file và lịch mô phỏng | Cả tám dùng dataset.yaml. Hai biên trong từng file khớp lịch Zenodo | Lịch khớp, tên file khác mô tả dataset.yml |
| Nhãn tham chiếu file và số dòng | 2.096.892/2.096.892 annotation hợp lệ, ví dụ bốn dòng audit khớp nội dung | Xác minh tham chiếu toàn bộ, kiểm tra ngữ nghĩa trực tiếp ở ví dụ |
| Nhãn nhiều mức | 6.284.252 lượt gán trên 2.096.892 dòng | Giữ riêng lượt gán và dòng có nhãn |
| Dữ liệu ngoài mô phỏng | 28.077.729/225.191.589 dòng thuộc năm nhóm đã xét nằm ngoài | Xác minh trên phần có bộ đọc thời gian |
| Lịch tấn công | 364.768 dòng có nhãn trước và 6.123 sau cửa sổ công bố | Lịch cung cấp bối cảnh, diễn giải chi tiết cần nhãn và timestamp |
| Dấu vết DNS của shaw, bước password cracking của wheeler | Trong 1.006 lượt gán trên dnsmasq của shaw có 0 nhãn dnsteal hoặc dnsteal-received. Trong 491.082 annotation của wheeler có 0 lượt crack_passwords. Sự vắng mặt của hành vi trong mọi log chưa được xác minh | Chỉ kết luận trong phạm vi quan sát |
| Khả năng khảo sát tài khoản | 182.972/222.664 dòng audit trong mô phỏng có acct và loại sự kiện sử dụng được | Nguồn bổ trợ cho hành vi tài khoản trên từng host |

Tóm tắt riêng tám archive, phân bố nguồn và các hình nằm trong [báo cáo EDA](eda_report.md). Nguồn đo là [manifest lần chạy](../outputs/runs/ait-v21-01/manifest.json). Phần mô tả công bố phía trên ghi lại trạng thái Survey trước khi mở dữ liệu.
