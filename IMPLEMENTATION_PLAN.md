# Implementation checklist – N-Queens Solving

> Cập nhật: 17/10/2026
>
> Trạng thái được đối chiếu với mã nguồn, dữ liệu benchmark đã lưu, bản thảo report và Git tại ngày cập nhật. Bộ test gần nhất được ghi nhận là 43 passed trước các cập nhật script phân tích/report; chưa chạy lại trong lượt rà soát này.

## Thông tin bài tập và báo cáo đã chốt

- [x] Chủ đề: N-Queens Solver.
- [x] Ngôn ngữ báo cáo: English.
- [x] Định dạng: scientific manuscript theo mẫu Elsevier được cung cấp.
- [x] Tác giả: Nguyễn Nhật Minh.
- [x] Mã sinh viên: `23021631`.
- [x] Đơn vị: Khoa Công Nghệ Thông Tin, Đại Học Công Nghệ, ĐHQGHN.
- [x] GitHub/Data Availability: <https://github.com/nNm205/n-queens-solving>.
- [x] Hạn nộp chính thức: `19/10/2026`.
- [x] Mốc nội bộ hoàn thành bản đầy đủ để chỉnh sửa: `16/10/2026` (đã qua; bản report vẫn cần hoàn thiện).
- [x] Chấp nhận ghi rõ `LICENSE_LIMIT` và `TIMEOUT` trong report khi chưa có academic license.

## Protocol thực nghiệm ban đầu đã chốt

- [x] SAT encoding sizes: `N = 8, 16, 32, 64, 96, 128`.
- [x] Cross-solver core sizes: `N = 8, 16, 24, 31, 32`.
- [x] Cross-solver extended sizes: `N = 44, 45, 64, 100, 128`.
- [x] SAT encoding repeats: `5` lần tại `N = 8, 16, 32`; `3` lần tại `N = 64`; `1` lần exploratory tại `N = 96, 128`.
- [x] Cross-solver repeated batch: `3` lần mỗi solver/kích thước tại `N = 8, 16, 24, 31, 32, 44, 45, 64, 100, 128`.
- [x] Timeout ban đầu: `600 giây/configuration`.
- [x] Baseline SAT tạm thời cho cross-solver: `pairwise`, dựa trên batch encoding lặp mới nhất.
- [x] Ghi nhận `LICENSE_LIMIT` và `TIMEOUT` mà không dừng toàn bộ experiment.
- [x] Chọn baseline SAT tạm thời sau khi phân tích batch lặp: Pairwise thắng ở `N = 8, 32, 64`; Sequential Counter thắng ở `N = 16`.

## Kết quả triển khai mới nhất

- [x] Bổ sung hard timeout theo configuration vào benchmark CLI (`--timeout`, mặc định `600s`).
- [x] Test suite sau thay đổi timeout ghi nhận `43 passed` (lần chạy gần nhất được biết; chưa chạy lại sau cập nhật report).
- [x] SAT encoding final-local batch: `45` rows cho `N = 8, 16, 32` với `5` repeats.
- [x] SAT encoding final-local batch: `9` rows cho `N = 64` với `3` repeats.
- [x] Cross-solver pilot core/extended batches: `25` rows mỗi batch.
- [x] Cross-solver repeated Pairwise batch: `150` rows; 3 runs cho mỗi 5 phương pháp và 10 kích thước.
- [x] Tạo bảng tổng hợp CSV trong `report/`.
- [x] Tạo biểu đồ SVG và PDF cho SAT encoding và cross-solver runtime.
- [x] Tạo ghi chú phân tích pilot trong `report/pilot_analysis.md`.
- [ ] Hoàn tất matched cross-solver khi CPLEX CP Optimizer khả dụng và tình trạng license được xử lý; nếu license vẫn giới hạn, giữ rõ các outcome `LICENSE_LIMIT`.
- [ ] Chốt protocol cuối (kích thước, số lần lặp và cách báo cáo cấu hình không chạy được) trước khi gọi benchmark là final.
- [ ] Chạy lại test suite sau các cập nhật gần đây cho script tổng hợp và báo cáo.

## Tiến độ report

- [x] Tạo bản thảo tiếng Anh theo cấu trúc Elsevier trong `report/manuscript.tex`.
- [x] Thêm bibliography trong `report/references.bib`.
- [x] Thêm hướng dẫn biên dịch trong `report/README.md`.
- [x] Đưa kết quả pilot hiện tại vào phần Experimental Results.
- [x] Ghi rõ license limitation và declaration về AI-assisted technologies.
- [x] Cài/copy bộ CAS template, gồm `cas-sc.cls`, `cas-common.sty` và bibliography style.
- [x] Chuẩn hóa và đưa các CAS assets cần thiết vào repository để report có thể tái lập.
- [x] Tạo commit riêng cho CAS assets và tài liệu report: `3aabc20`, `23fb570`.
- [x] Cấu hình CTAN repository, cập nhật MiKTeX package database và cài các package phụ thuộc.
- [x] Biên dịch thành công một bản CAS trước đây; PDF hiện tại cũ hơn nguồn LaTeX mới nhất.
- [ ] Biên dịch lại PDF từ nguồn mới và rà soát layout.
- [ ] Rà soát nội dung, citations, figures và bảng sau khi có kết quả CPLEX CP/license mới.
- [ ] Hoàn thiện abstract, discussion và conclusion sau benchmark final.
- [x] Tạo hai commit cục bộ cho benchmark/dữ liệu và cập nhật report: `9fab7ed`, `f75bb3a`.
- [x] Hai commit benchmark/report mới nhất (`9fab7ed`, `f75bb3a`) đã có trên `origin/main` tại lần kiểm tra ngày 17/10/2026.
- [ ] Commit các cập nhật tiến độ trong `README.md` và `IMPLEMENTATION_PLAN.md`.

## Trạng thái chờ license

- [ ] Bản PDF tương ứng với nguồn mới; `report/manuscript.pdf` hiện là artifact cũ, chưa được đưa vào hai commit mới.
- [x] `main` và `origin/main` cùng ở `f75bb3a` tại lần kiểm tra ngày 17/10/2026; thay đổi README/kế hoạch trong lượt này chưa commit.
- [ ] Kích hoạt Gurobi Academic License.
- [ ] Kích hoạt CPLEX Academic License.
- [x] Commit dữ liệu benchmark và cập nhật report đã tạo cục bộ; không push theo yêu cầu.
- [ ] Chạy matched benchmark sau khi CPLEX CP Optimizer được khôi phục và license được xử lý.
- [ ] Cập nhật bảng, biểu đồ và kết luận bằng kết quả benchmark cuối.

## 1. Nền tảng và môi trường

- [x] Khởi tạo cấu trúc project (`src/`, `experiments/`, `tests/`, `results/`, `report/`).
- [x] Thiết lập môi trường Python 3.11 và virtual environment.
- [x] Kiểm tra PySAT + Glucose3.
- [x] Kiểm tra OR-Tools CP-SAT.
- [x] Kiểm tra CPLEX MIP; CPLEX CP Optimizer đã chạy ở pilot trước nhưng executable không được tìm thấy trong batch lặp mới nhất.
- [x] Kiểm tra Gurobi.
- [x] Lịch sử kiểm thử gần nhất ghi nhận **43 passed**; chưa chạy lại sau cập nhật report mới.

## 2. Mô hình và solver đã hoàn thành

### SAT

- [x] Mô hình N-Queens bằng biến board `x[row, col]`.
- [x] Ràng buộc exactly-one cho từng hàng và từng cột.
- [x] Ràng buộc at-most-one cho hai loại đường chéo.
- [x] Kiến trúc encoder SAT dùng chung.
- [x] Pairwise AMO encoding.
- [x] Sequential Counter AMO encoding.
- [x] Bitwise AMO encoding.
- [x] Quản lý biến phụ dùng chung bằng `IDPool`, tránh trùng ID.
- [x] Solver Glucose3.
- [x] Decode nghiệm SAT về dạng `queens[row] = column`.
- [x] Validator độc lập kiểm tra nghiệm.
- [x] Ghi nhận số biến, số clause, encoding time, solve time và total time.

### CP và MIP

- [x] OR-Tools CP-SAT với các ràng buộc `AllDifferent`.
- [x] CPLEX CP Optimizer.
- [x] CPLEX MIP với biến nhị phân `N²`.
- [x] Gurobi MIP với biến nhị phân `N²`.
- [x] Validator dùng chung cho tất cả phương pháp.
- [x] Ghi nhận build time, solve time và total time.
- [x] Ghi nhận số biến và số ràng buộc cho MIP.

## 3. Test và kiểm thử hồi quy

- [x] Kiểm thử các trường hợp `N = 1, 2, 3, 4, 8`.
- [x] Kiểm thử nghiệm SAT hợp lệ bằng validator độc lập.
- [x] Kiểm thử cả ba SAT encoding.
- [x] Kiểm thử regression số clause của Pairwise.
- [x] Kiểm thử CP-SAT, CPLEX CP, CPLEX MIP và Gurobi MIP.
- [x] Kiểm thử regression kích thước model MIP.
- [x] Kiểm thử benchmark normalization và CSV export.
- [x] Kiểm thử benchmark SAT encoding và cross-solver.

## 4. Benchmark infrastructure

- [x] Unified benchmark runner trong `experiments/`.
- [x] Unified result schema cho SAT, CP-SAT, CPLEX CP, CPLEX MIP và Gurobi MIP.
- [x] Chạy lặp benchmark bằng tùy chọn `--repeats`.
- [x] Xuất kết quả CSV.
- [x] Chế độ benchmark so sánh SAT encoding.
- [x] Chế độ benchmark so sánh các solver.
- [x] Bắt lỗi từng solver để experiment không dừng toàn bộ.
- [x] Phân loại lỗi giới hạn license thành `LICENSE_LIMIT`.

## 5. Kết quả thực nghiệm hiện đã có

- [x] Smoke test SAT encoding ở `N = 4, 8`.
- [x] Smoke test cross-solver ở `N = 4, 8`.
- [x] SAT encoding pilot round 1 ở `N = 8, 16, 32, 64`.
- [x] SAT encoding pilot round 2 ở `N = 96, 128`.
- [x] Cross-solver pilot round 1 ở `N = 8, 16, 24, 31`.
- [x] Cross-solver test tại `N = 32`.
- [x] Cross-solver pilot lớn ở `N = 64, 100, 128`.
- [x] Kiểm tra biên license ở `N = 44, 45`.
- [x] Chạy lại cross-solver với Pairwise, 3 lần/cấu hình ở `N = 8, 16, 24, 31, 32, 44, 45, 64, 100, 128`.
- [x] Ghi nhận kết quả SAT/CP/CP-SAT và lỗi license trong cùng schema.

Các artifact hiện có trong `results/` gồm:

- [x] `pilot/sat_encodings_round1.csv`
- [x] `pilot/sat_encodings_round2.csv`
- [x] `pilot/solver_comparison_round1.csv`
- [x] `pilot/solver_comparison_n32.csv`
- [x] `pilot/solver_comparison_license_boundary.csv`
- [x] `pilot/solver_comparison_large.csv`
- [x] `pairwise_solver_comparison_repeat3.csv` (150 dòng; 3 lần cho mỗi solver/kích thước, Pairwise SAT baseline)
- [x] Các file smoke/license test ở thư mục `results/`.
- [x] Cập nhật summary CSV và biểu đồ solver theo batch Pairwise lặp.
- [x] Sửa bản thảo và `report/pilot_analysis.md` để giải thích baseline, dải N, timeout, số lần lặp, giới hạn license và CPLEX CP không khả dụng.
- [x] Ghi cấu hình phần cứng/phần mềm của batch mới vào report.
- [x] Sửa diễn giải encoding để khớp dữ liệu: Pairwise nhanh nhất tại 3/4 kích thước; Sequential Counter nhanh nhất tại `N = 16`.
- [x] Lưu dữ liệu pilot, batch lặp, bảng tổng hợp và biểu đồ trong các commit cục bộ `9fab7ed` và `f75bb3a`.
- [ ] Biên dịch lại PDF sau các chỉnh sửa; `report/manuscript.pdf` hiện là bản cũ.
- [ ] Khôi phục công cụ MiKTeX trong shell: `pdflatex` không có trong PATH/cài đặt được tìm thấy; `miktex-bibtex.exe` không khởi động được (exit `-1073741515`).

## 6. Giới hạn hiện tại cần lưu ý

- [x] CPLEX Community Edition chạy được model nhỏ nhưng bị giới hạn ở model lớn; ví dụ `N = 32` có `1024` biến và bị `LICENSE_LIMIT`.
- [x] Gurobi hiện hoạt động với restricted license; repeated batch chấp nhận đến `N = 44` và báo `LICENSE_LIMIT` từ `N = 45`.
- [x] Lần chạy lại hiện tại không tìm thấy `cpoptimizer.exe`; các dòng CPLEX CP được ghi `ERROR` và loại khỏi bảng median so sánh lặp.
- [x] Chọn Pairwise làm baseline SAT tạm thời cho cross-solver: nhanh nhất tại `N = 8, 32, 64`; Sequential Counter nhanh nhất tại `N = 16`.
- [ ] Kích hoạt Gurobi Academic License trước benchmark chính thức quy mô lớn.
- [ ] Cài/kích hoạt CPLEX academic license không giới hạn nếu có thể.
- [ ] Quyết định rõ cách xử lý các phương pháp bị license limit trong bảng so sánh cuối.

## 7. Việc còn phải làm

### Chốt thiết kế thực nghiệm

- [x] Phân tích pilot và chọn dải kích thước board tạm thời cho cross-solver.
- [x] Chọn 3 lần lặp/cấu hình làm protocol tạm thời; cần xác nhận số lần cuối cho benchmark nộp bài.
- [x] Giữ timeout 600 giây và chính sách ghi `TIMEOUT`, `LICENSE_LIMIT`, `ERROR` riêng.
- [x] Chọn Pairwise làm baseline SAT tạm thời cho cross-solver; không kết luận Pairwise nhanh nhất ở mọi kích thước.
- [ ] Xác định bộ metric và quy tắc báo cáo kết quả cuối.

### Chạy benchmark chính thức

- [x] Chạy batch SAT encoding lặp tại `N = 8, 16, 32` (5 lần) và `N = 64` (3 lần); `N = 96, 128` mới có dữ liệu pilot một lần.
- [ ] Chạy/hoàn tất matched SAT, CP-SAT, CPLEX CP, CPLEX MIP và Gurobi MIP sau khi CPLEX CP khả dụng; xử lý license theo khả năng thực tế.
- [ ] Quyết định có cần chạy lại các case lớn khi license được nâng cấp hay báo cáo riêng các giới hạn hiện tại.
- [ ] Kiểm tra tính lặp lại, metadata môi trường và tính đầy đủ của CSV sau batch cuối.

### Phân tích và báo cáo

- [x] Tổng hợp dữ liệu benchmark Pairwise mới và giữ raw CSV cho từng run.
- [x] Cập nhật bảng median và biểu đồ cho batch Pairwise mới; 90 lượt hợp lệ, 30 lượt license limit, 30 lỗi CPLEX CP do thiếu executable, không có timeout.
- [ ] Bổ sung/hoàn thiện phân tích trade-off giữa số biến, số clause, encoding time và solving time.
- [ ] Hoàn thiện phân tích giới hạn thực tế của từng solver sau khi nhận kết quả CPLEX CP/license.
- [x] Tạo/cập nhật bảng kết quả và figures/plots cho batch hiện tại.
- [x] Cập nhật methodology, experimental setup, results, discussion và limitations trong bản thảo pilot.
- [ ] Hoàn thiện scientific report trong `report/`.
- [ ] Rà soát README, lệnh chạy và artifact trước khi nộp; loại các file build/template thừa khỏi phần giao nộp nếu không cần.

## 8. Trạng thái tổng quan

**Đã hoàn thành:** phần triển khai solver, validation, test và benchmark framework; đã có pilot experiments thực tế.

**Đang ở:** chờ người dùng khắc phục CPLEX CP Optimizer/license. Hai commit benchmark/report đã có trên `origin/main`; cập nhật README/kế hoạch trong lượt này chưa commit. Bản LaTeX đã sửa theo số liệu encoding, còn cần biên dịch PDF mới và rà soát.

**Chưa hoàn thành:** matched benchmark đủ năm phương pháp nếu môi trường cho phép; chốt protocol cuối và xử lý license-limited cases; xác nhận metadata cho các batch cũ; chạy lại test suite, biên dịch PDF mới và rà soát report. Commit cập nhật README/kế hoạch; push do người dùng thực hiện.
