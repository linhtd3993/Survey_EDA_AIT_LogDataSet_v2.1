# Survey & EDA — AIT Log Data Set v2.1

Lab độc lập khảo sát và phân tích khám phá **AIT Log Data Set v2.1**, chỉ sử dụng tám archive `*_no-pcaps.zip`. Lab tập trung vào nguồn gốc, cấu trúc, chất lượng, thời gian, nhãn và mức độ dữ liệu hỗ trợ nghiên cứu hành vi tài khoản trong bối cảnh bài tập lớn **Account Behavior Security Gateway (ABSG)**.

**Đã nghiệm thu ngày 26/11/2026.** Tám archive no-pcaps có 261.402.985 dòng văn bản theo bộ kiểm kê và 2.096.892 dòng có annotation. Toàn bộ tham chiếu nhãn hợp lệ theo file và số dòng. Phạm vi quan sát tài khoản và giới hạn về thời gian được nêu trong báo cáo.

- [Báo cáo Survey](docs/survey_report.md)
- [Báo cáo EDA](docs/eda_report.md)
- [Notebook đã chạy](notebooks/ait_lds_eda.ipynb)
- [Nghiệm thu, hướng dẫn tái lập và demo](docs/final_acceptance.md)

## Mục lục

- [Mục tiêu](#mục-tiêu)
- [Phạm vi](#phạm-vi)
- [Nguồn dữ liệu](#nguồn-dữ-liệu)
- [Câu hỏi của lab](#câu-hỏi-của-lab)
- [Bằng chứng và cách báo cáo](#bằng-chứng-và-cách-báo-cáo)
- [Đầu ra dự kiến](#đầu-ra-dự-kiến)
- [Nguyên tắc thực hiện](#nguyên-tắc-thực-hiện)
- [Trạng thái và nội dung còn mở](#trạng-thái-và-nội-dung-còn-mở)
- [Tài liệu tham khảo trong workspace](#tài-liệu-tham-khảo-trong-workspace)
- [Bản đồ tài liệu](#bản-đồ-tài-liệu)
- [Repository](#repository)

## Mục tiêu

Lab cần trả lời ba nhóm câu hỏi:

1. **Dataset là gì?** AIT-LDS v2.1 được tạo ra trong môi trường nào, gồm những hệ thống và nguồn log nào, nhãn được tạo và công bố ra sao?
2. **Dữ liệu thực tế có chất lượng thế nào?** Các archive có đầy đủ và đọc được không; timestamp, schema, độ bao phủ và quan hệ giữa `gather/` với `labels/` có nhất quán không?
3. **Dataset hỗ trợ nghiên cứu hành vi tài khoản tới mức nào?** Có nhận diện và nối được tài khoản, host, phiên hoặc chuỗi hành động không; câu hỏi nào có thể trả lời và câu hỏi nào còn thiếu dữ liệu?

Kết quả của lab nhằm tạo bằng chứng cho việc đánh giá dataset. Lab không mặc định rằng AIT-LDS phù hợp với ABSG trước khi hoàn tất kiểm chứng.

## Phạm vi

### Trong phạm vi

- Survey tài liệu chính thức, bài báo tác giả và mô tả phát hành AIT-LDS v2.1.
- Kiểm kê và EDA cả tám archive `*_no-pcaps.zip`.
- Kiểm tra cấu trúc archive, loại log, host, số dòng, timestamp và chất lượng dữ liệu.
- Kiểm tra phép ghép file và số dòng giữa `labels/` với `gather/`.
- Phân tích theo khoảng mô phỏng trong `dataset.yml`.
- Phân tích lượng log theo dataset, host, nguồn và thời gian.
- Đánh giá ngữ nghĩa, phân bố và giới hạn của nhãn.
- Khảo sát các trường và chuỗi sự kiện có thể hỗ trợ nghiên cứu hành vi tài khoản.
- Rà soát nguy cơ data leakage ở cấp dữ liệu và nhãn.

### Ngoài phạm vi

- Packet capture và các archive có pcap.
- Xây dựng hoặc triển khai Security Gateway.
- Huấn luyện, chọn hoặc đánh giá mô hình học máy.
- EDA các dataset khác.
- Thay đổi, commit hoặc push vào repository HKDN của Team 2.

## Nguồn dữ liệu

| Thuộc tính | Giá trị |
|---|---|
| Dataset | AIT Log Data Set v2.1 |
| Phiên bản | `v2_1` |
| Nhà phát hành | Austrian Institute of Technology và các tác giả |
| Phân phối chính thức | [Zenodo record 19483937](https://zenodo.org/records/19483937) |
| DOI | [10.5281/zenodo.19483937](https://doi.org/10.5281/zenodo.19483937) |
| Giấy phép công bố | CC BY-NC-SA 4.0 |
| Bản chất | Log sinh từ tám testbed mô phỏng mạng doanh nghiệp nhỏ |
| Phạm vi lab | Chỉ các archive `*_no-pcaps.zip` |

Tám archive thuộc phạm vi:

| Dataset | Archive |
|---|---|
| `fox` | `fox_no-pcaps.zip` |
| `harrison` | `harrison_no-pcaps.zip` |
| `russellmitchell` | `russellmitchell_no-pcaps.zip` |
| `santos` | `santos_no-pcaps.zip` |
| `shaw` | `shaw_no-pcaps.zip` |
| `wardbeck` | `wardbeck_no-pcaps.zip` |
| `wheeler` | `wheeler_no-pcaps.zip` |
| `wilson` | `wilson_no-pcaps.zip` |

Theo mô tả chính thức, log nằm trong `gather/<host>/logs/`; `labels/` phản chiếu đường dẫn log và dùng số dòng để tham chiếu sự kiện liên quan đến tấn công; `dataset.yml` ghi khoảng thời gian mô phỏng. Đây là thông tin do nguồn công bố và sẽ được kiểm chứng trên dữ liệu đã tải.

## Câu hỏi của lab

- Cả tám archive có đầy đủ, đúng checksum và đúng phạm vi no-pcaps không?
- Cấu trúc, định dạng và schema thực tế có khớp tài liệu không?
- Mỗi nguồn log bao phủ host và khoảng thời gian nào?
- Timestamp có đọc được, so sánh được giữa nguồn và nằm trong khoảng mô phỏng không?
- File nhãn có ghép đúng file log và số dòng nguồn không?
- Một dòng có thể mang bao nhiêu nhãn; cần phân biệt thế nào giữa dòng được gán nhãn, lượt gán nhãn, bước tấn công và sự cố?
- Phần không có annotation nên được diễn giải thế nào theo nguồn, và giới hạn của cách diễn giải đó là gì?
- Có thể nhận diện hoặc nối tài khoản, host, phiên và chuỗi sự kiện ở mức nào?
- Những tín hiệu nào chỉ tồn tại sau sự kiện hoặc có nguy cơ làm lộ nhãn?
- AIT-LDS v2.1 có thể trả lời câu hỏi hành vi tài khoản nào, và còn thiếu gì để phục vụ ABSG?

## Bằng chứng và cách báo cáo

Lab phân biệt rõ thông tin do tác giả công bố với số liệu tự đo:

| Ký hiệu | Trạng thái | Ý nghĩa |
|---|---|---|
| `[S]` | Source-reported | Thông tin từ tài liệu hoặc trang chính thức. |
| `[M]` | Measured | Kết quả đo trực tiếp từ dữ liệu bằng quy trình có thể chạy lại. |
| `[V]` | Verified | Kết quả đo khớp với công bố. |
| `[P]` | Partially verified | Công bố chỉ khớp một phần hoặc có ngoại lệ. |
| `[X]` | Contradicted | Kết quả đo không khớp công bố. |
| `[U]` | Unknown | Chưa có đủ thông tin để xác định. |
| `[N]` | Not measurable | Dữ liệu hiện có không cho phép đo hoặc kết luận. |

Mỗi thống kê phải ghi rõ:

- Dataset và nguồn log.
- Khoảng thời gian.
- Đơn vị đếm.
- Mẫu số dùng để tính tỷ lệ.
- Phạm vi toàn bộ hay mẫu và quy tắc lấy mẫu.
- Artifact hoặc phép đo làm căn cứ.
- Hệ quả đối với việc sử dụng dữ liệu.

Thông tin tài liệu không nêu được ghi là `Không rõ`; dữ liệu không cho phép kiểm chứng được ghi là `Không đo được`. Không nâng annotation của nguồn thành kết luận sự cố đã được xác minh độc lập.

## Đầu ra dự kiến

Đầu ra cuối cùng dự kiến gồm:

1. **Báo cáo Survey riêng**: nguồn gốc, mục đích, testbed, hệ thống, log, thời gian, nhãn, xử lý trước công bố, hạn chế và danh sách nội dung cần kiểm chứng.
2. **Báo cáo EDA riêng**: phương pháp, số liệu thực đo, chất lượng, thời gian, độ bao phủ, nhãn, hành vi, leakage và đánh giá mức phù hợp.
3. **Notebook EDA có thể chạy từ đầu đến cuối**: câu hỏi, code, bảng/hình và nhận xét đi cùng nhau.
4. **Evidence matrix**: nối từng khẳng định trong Survey với phép kiểm tra, artifact và trạng thái cuối.
5. **Manifest và Data Quality Log**: lưu phiên bản dữ liệu, checksum, số đếm, lỗi và mọi quyết định xử lý.
6. **Hình, bảng, log chạy và test**: bằng chứng hỗ trợ nghiệm thu và tái lập.

Đường dẫn đầu ra đã nghiệm thu nằm ở đầu README.

## Nguyên tắc thực hiện

- Dùng tài liệu tác giả và số liệu đo trực tiếp làm bằng chứng; phân biệt công bố, phép đo và diễn giải.
- Survey đi trước để tạo danh sách claim và câu hỏi kiểm chứng; EDA kiểm tra các claim rồi cập nhật trạng thái, không sửa âm thầm lịch sử bằng chứng.
- Có thể thử bộ đọc trên một archive, nhưng kết quả cuối phải bao phủ cả tám archive bằng cùng quy tắc.
- Giữ dataset, host, đường dẫn log gốc và số dòng để phép ghép nhãn có thể truy vết.
- Dùng khoảng mô phỏng trong `dataset.yml` khi phân tích thời gian.
- Không mặc định timestamp là UTC, host là tài khoản, IP là thiết bị hoặc phần không có nhãn là benign đã được xác minh.
- Không dùng thông tin chỉ xuất hiện sau thời điểm sự kiện như một tín hiệu có sẵn tại thời điểm chấm điểm.
- Không đưa archive, log thô, cache lớn, dữ liệu nhạy cảm hoặc secret vào Git.
- Chỉ báo cáo hoàn tất sau khi notebook chạy lại thành công và artifact được đối chiếu với manifest.

## Trạng thái và nội dung còn mở

M1–M8 đã hoàn tất. Các điểm còn mở về ngữ nghĩa nhãn, thời gian và khả năng nối tài khoản được ghi trong [biên bản nghiệm thu](docs/final_acceptance.md). Bảng chi tiết theo file và manifest của run lưu cục bộ dưới `outputs/`.

## Tài liệu tham khảo trong workspace

Thư mục `reference/` chứa bản sao tham khảo tại thời điểm chuẩn bị:

| Nội dung | Vị trí |
|---|---|
| Bối cảnh, nhiệm vụ và kế hoạch HKDN | `reference/hkdn/` |
| Data contract, privacy và mapping của Team 2 | `reference/hkdn/contracts/`, `reference/hkdn/mappings/` |
| Datasheet và label registry hiện có | `reference/hkdn/datasets/` |
| Quy trình, thiết kế và nghiệm thu Lab 2 | `reference/lab2/` |

Các bản sao này không thay thế nguồn gốc. Khi sử dụng trong kết luận, cần đối chiếu bản hiện hành hoặc nguồn chính thức tương ứng.

## Bản đồ tài liệu

| Tài liệu | Vai trò |
|---|---|
| [Project Define](docs/project_define.md) | Bài toán, người dùng, đầu vào, đầu ra và tiêu chí đánh giá. |
| [Project Design](docs/project_design.md) | Kiến trúc, module, cấu trúc thư mục và thiết kế kiểm tra. |
| [AI Usage](docs/AI_usage.md) | Công việc AI hỗ trợ, đóng góp sinh viên và cách kiểm chứng. |
| [Dàn ý hai báo cáo](docs/report_outlines.md) | Đề xuất 11 nhóm Survey, 18 bước EDA và cách cập nhật bằng chứng. |
| [Milestone cho AI agent](docs/milestones.md) | Công việc, phụ thuộc, đầu ra và tiêu chí nghiệm thu từng mốc. |
| [Hai form và nguồn bản sao](reference/forms/README.md) | Form Survey/EDA được sao chép từ Downloads, có SHA-256 đối chiếu. |
| [Bối cảnh HKDN](reference/hkdn/) | Nhiệm vụ, contract, privacy, nhãn và mapping tham khảo. |
| [Quy trình Lab 2](reference/lab2/) | Thiết kế, quy trình phát triển và nghiệm thu tham khảo. |

Các bản sao trong `reference/` được lưu cục bộ và đang nằm trong quy tắc loại khỏi Git. Khi clone repo cần chuẩn bị các nguồn tham khảo tương ứng. Hai báo cáo kết quả nằm trong docs/.

## Repository

- GitHub: [linhtd3993/Survey_EDA_AIT_LogDataSet_v2.1](https://github.com/linhtd3993/Survey_EDA_AIT_LogDataSet_v2.1)
- Thư mục làm việc của lab: `D:\CODE\HKND\CODE\Practice_Project\ait_lds_survey_eda`
- Repository HKDN của Team 2 chỉ được dùng để đọc và đối chiếu; không commit hoặc push thay đổi của lab vào repository đó.

Repository này dành riêng cho artifact có thể quản lý bằng Git như tài liệu, cấu hình, mã nguồn, notebook và test. Dữ liệu gốc cùng artifact lớn phải được loại khỏi version control và được truy vết bằng manifest/checksum.
