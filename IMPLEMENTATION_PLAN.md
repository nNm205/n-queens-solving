# Implementation checklist – N-Queens Solving

> Cập nhật: 10/10/2026
>
> Trạng thái được tổng hợp từ mã nguồn hiện tại, README, test suite và các file CSV trong `results/`.

## Thông tin bài tập và báo cáo đã chốt

- [x] Chủ đề: N-Queens Solver.
- [x] Ngôn ngữ báo cáo: English.
- [x] Định dạng: scientific manuscript theo mẫu Elsevier được cung cấp.
- [x] Tác giả: Nguyễn Nhật Minh.
- [x] Mã sinh viên: `23021631`.
- [x] Đơn vị: Khoa Công Nghệ Thông Tin, Đại Học Công Nghệ, ĐHQGHN.
- [x] GitHub/Data Availability: <https://github.com/nNm205/n-queens-solving>.
- [x] Hạn nộp chính thức: `19/10/2026`.
- [x] Mục tiêu hoàn thành bản đầy đủ để chỉnh sửa: `16/10/2026`.
- [x] Chấp nhận ghi rõ `LICENSE_LIMIT` và `TIMEOUT` trong report khi chưa có academic license.

## Protocol thực nghiệm ban đầu đã chốt

- [x] SAT encoding sizes: `N = 8, 16, 32, 64, 96, 128`.
- [x] Cross-solver core sizes: `N = 8, 16, 24, 31, 32`.
- [x] Cross-solver extended sizes: `N = 44, 45, 64, 100, 128`.
- [x] Repeats: `5` lần cho `N <= 32`, `3` lần cho `N = 64`, `1` lần ban đầu cho `N >= 96`.
- [x] Timeout ban đầu: `600 giây/configuration`.
- [x] Candidate baseline cho cross-solver: `bitwise`.
- [x] Ghi nhận `LICENSE_LIMIT` và `TIMEOUT` mà không dừng toàn bộ experiment.
- [ ] Xác nhận encoding baseline cuối cùng sau khi phân tích đầy đủ pilot.

## Kết quả triển khai mới nhất

- [x] Bổ sung hard timeout theo configuration vào benchmark CLI (`--timeout`, mặc định `600s`).
- [x] Test suite sau thay đổi timeout: `43 passed`.
- [x] SAT encoding final-local batch: `45` rows cho `N = 8, 16, 32` với `5` repeats.
- [x] SAT encoding final-local batch: `9` rows cho `N = 64` với `3` repeats.
- [x] Cross-solver core batch: `25` rows cho `N = 8, 16, 24, 31, 32`.
- [x] Cross-solver extended batch: `25` rows cho `N = 44, 45, 64, 100, 128`.
- [x] Tạo bảng tổng hợp CSV trong `report/`.
- [x] Tạo biểu đồ SVG cho SAT encoding và cross-solver runtime.
- [x] Tạo ghi chú phân tích pilot trong `report/pilot_analysis.md`.
- [ ] Chạy lại core/extended cross-solver sau khi academic license được kích hoạt.
- [ ] Chốt SAT encoding baseline cuối cùng sau khi đánh giá độ biến thiên runtime.

## Tiến độ report

- [x] Tạo bản thảo tiếng Anh theo cấu trúc Elsevier trong `report/manuscript.tex`.
- [x] Thêm bibliography trong `report/references.bib`.
- [x] Thêm hướng dẫn biên dịch trong `report/README.md`.
- [x] Đưa kết quả pilot hiện tại vào phần Experimental Results.
- [x] Ghi rõ license limitation và declaration về AI-assisted technologies.
- [x] Cài/copy bộ CAS template, gồm `cas-sc.cls`, `cas-common.sty` và bibliography style.
- [ ] Cài các package phụ thuộc còn thiếu của MiKTeX để biên dịch PDF.
- [ ] Rà soát nội dung, citations, figures và bảng sau khi có kết quả license mới.
- [ ] Hoàn thiện abstract, discussion và conclusion sau benchmark final.

## 1. Nền tảng và môi trường

- [x] Khởi tạo cấu trúc project (`src/`, `experiments/`, `tests/`, `results/`, `report/`).
- [x] Thiết lập môi trường Python 3.11 và virtual environment.
- [x] Kiểm tra PySAT + Glucose3.
- [x] Kiểm tra OR-Tools CP-SAT.
- [x] Kiểm tra CPLEX MIP và CPLEX CP Optimizer.
- [x] Kiểm tra Gurobi.
- [x] Chạy test suite thành công: **43 passed**.

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
- [x] Ghi nhận kết quả SAT/CP/CP-SAT và lỗi license trong cùng schema.

Các artifact hiện có trong `results/` gồm:

- [x] `pilot/sat_encodings_round1.csv`
- [x] `pilot/sat_encodings_round2.csv`
- [x] `pilot/solver_comparison_round1.csv`
- [x] `pilot/solver_comparison_n32.csv`
- [x] `pilot/solver_comparison_license_boundary.csv`
- [x] `pilot/solver_comparison_large.csv`
- [x] Các file smoke/license test ở thư mục `results/`.

## 6. Giới hạn hiện tại cần lưu ý

- [x] CPLEX Community Edition chạy được model nhỏ nhưng bị giới hạn ở model lớn; ví dụ `N = 32` có `1024` biến và bị `LICENSE_LIMIT`.
- [x] Gurobi hiện hoạt động với restricted license; các model lớn như `N = 64` và cao hơn có thể bị giới hạn license.
- [ ] Kích hoạt Gurobi Academic License trước benchmark chính thức quy mô lớn.
- [ ] Cài/kích hoạt CPLEX academic license không giới hạn nếu có thể.
- [ ] Quyết định rõ cách xử lý các phương pháp bị license limit trong bảng so sánh cuối.

## 7. Việc còn phải làm

### Chốt thiết kế thực nghiệm

- [ ] Phân tích pilot để chọn dải kích thước board chính thức.
- [ ] Chốt số lần lặp cho từng thí nghiệm.
- [ ] Chốt timeout và chính sách xử lý solver timeout/error.
- [ ] Chọn SAT encoding làm baseline cho cross-solver dựa trên kết quả pilot.
- [ ] Xác định bộ metric và quy tắc báo cáo kết quả cuối.

### Chạy benchmark chính thức

- [ ] Chạy SAT encoding comparison cuối với kích thước và số lần lặp đã chốt.
- [ ] Chạy SAT vs CP-SAT vs CPLEX CP vs CPLEX MIP vs Gurobi MIP.
- [ ] Chạy lại các case lớn sau khi license được nâng cấp (nếu có).
- [ ] Kiểm tra tính lặp lại và tính đầy đủ của toàn bộ CSV.

### Phân tích và báo cáo

- [ ] Làm sạch và tổng hợp dữ liệu benchmark.
- [ ] Phân tích trade-off giữa số biến, số clause, encoding time và solving time.
- [ ] Phân tích giới hạn thực tế của từng solver.
- [ ] Tạo các bảng kết quả.
- [ ] Tạo figures/plots cho báo cáo.
- [ ] Viết phần methodology và experimental setup.
- [ ] Viết phần results, discussion và threats/limitations.
- [ ] Hoàn thiện scientific report trong `report/`.
- [ ] Rà soát README, lệnh chạy và artifact trước khi nộp.

## 8. Trạng thái tổng quan

**Đã hoàn thành:** phần triển khai solver, validation, test và benchmark framework; đã có pilot experiments thực tế.

**Đang ở:** pilot analysis và chuẩn bị benchmark chính thức.

**Chưa hoàn thành:** chốt protocol cuối, xử lý license cho thí nghiệm lớn, chạy benchmark final, phân tích dữ liệu, tạo bảng/biểu đồ và viết report.
