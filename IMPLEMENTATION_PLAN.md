# Implementation checklist – N-Queens Solving

> Cập nhật: 17/10/2026
>
> Trạng thái được đối chiếu với mã nguồn, dữ liệu benchmark đã lưu, bản thảo report, test suite và Git tại ngày cập nhật.

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
- [x] Test suite hiện tại: `43 passed` trong `.venv` sau khi đồng bộ dependencies.
- [x] SAT encoding final-local batch: `45` rows cho `N = 8, 16, 32` với `5` repeats.
- [x] SAT encoding final-local batch: `9` rows cho `N = 64` với `3` repeats.
- [x] Cross-solver pilot core/extended batches: `25` rows mỗi batch.
- [x] Cross-solver repeated Pairwise batch: `150` rows; 3 runs cho mỗi 5 phương pháp và 10 kích thước.
- [x] Tạo bảng tổng hợp CSV trong `report/`.
- [x] Tạo biểu đồ SVG và PDF cho SAT encoding và cross-solver runtime.
- [x] Tạo ghi chú phân tích pilot trong `report/pilot_analysis.md`.
- [x] Hoàn tất matched cross-solver sau khi khôi phục CPLEX CP và xác nhận CPLEX MIP; vẫn ghi Gurobi `LICENSE_LIMIT` từ `N=45`.
- [x] Chốt protocol báo cáo hiện tại: 10 kích thước, 3 lần/configuration, timeout 600 giây; status `LICENSE_LIMIT` không được tính vào median.
- [x] Chạy lại test suite sau các cập nhật gần đây: `43 passed`.

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
- [x] Rebuilt the manuscript PDF on 17 October 2026 using MiKTeX 25.12; visually reviewed all six article pages.
- [x] Changed citations to author-year parenthetical style; fixed the invalid PDF `arc` operator and white chart labels.
- [x] Cập nhật nội dung, bảng và figures theo matched cross-solver batch có CPLEX CP/MIP.
- [x] Bổ sung bảng số biến/số mệnh đề cho Pairwise, Sequential Counter và Bitwise từ raw SAT benchmark; đối chiếu trade-off với runtime.
- [x] Reviewed manuscript content, citations, tables and figures after build; one internal `\maketitle` overfull warning remains, with no visible clipping.
- [x] Cập nhật abstract, discussion và conclusion theo matched five-method batch; nêu rõ giới hạn Gurobi.
- [x] Tạo hai commit cục bộ cho benchmark/dữ liệu và cập nhật report: `9fab7ed`, `f75bb3a`.
- [x] Hai commit benchmark/report mới nhất (`9fab7ed`, `f75bb3a`) đã có trên `origin/main` tại lần kiểm tra ngày 17/10/2026.
- [x] Đã đưa các cập nhật README, kế hoạch, raw results, mã phân tích và report vào commit cục bộ; không push.

## Trạng thái chờ license

- [x] PDF khớp nguồn hiện tại ở `report/manuscript.pdf` và được đưa vào commit cục bộ mới.
- [x] Trước commit này, `main` và `origin/main` cùng ở `f75bb3a` (17/10/2026); commit hiện tại chỉ nằm local, chưa push.
- [x] Giữ Gurobi `LICENSE_LIMIT` từ `N=45` khi chưa có academic license; chạy lại chỉ khi license thay đổi.
- [x] CPLEX MIP và CPLEX CP Optimizer pass smoke check 1.100 biến; cả hai giải mọi kích thước trong batch tới `N=128`.
- [x] Commit dữ liệu benchmark và cập nhật report đã tạo cục bộ; không push theo yêu cầu.
- [x] Chạy matched benchmark đủ năm phương pháp sau khi khôi phục CPLEX CP; 150 dòng, 138 nghiệm hợp lệ, 12 Gurobi license limit, không timeout/error.
- [x] Cập nhật bảng, biểu đồ, abstract và kết luận theo kết quả mới.

## 1. Nền tảng và môi trường

- [x] Khởi tạo cấu trúc project (`src/`, `experiments/`, `tests/`, `results/`, `report/`).
- [x] Thiết lập môi trường Python 3.11 và virtual environment.
- [x] Kiểm tra PySAT + Glucose3.
- [x] Kiểm tra OR-Tools CP-SAT.
- [x] CPLEX MIP và CPLEX CP Optimizer đã được kiểm tra lại; executable CP hiện ở `.venv/Scripts/cpoptimizer.exe`.
- [x] Kiểm tra Gurobi.
- [x] Test suite hiện tại: **43 passed** sau khi bổ sung dependencies còn thiếu bằng `uv`.

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
- [x] `cplex_activated_solver_comparison_repeat3.csv` (150 dòng; matched 5 phương pháp x 10 kích thước x 3 lần)
- [x] Các file smoke/license test ở thư mục `results/`.
- [x] Cập nhật summary CSV và biểu đồ solver theo batch Pairwise lặp.
- [x] Sửa bản thảo và `report/pilot_analysis.md` theo batch matched: CPLEX CP/MIP chạy toàn dải; Gurobi bị giới hạn từ `N=45`.
- [x] Ghi cấu hình phần mềm mới vào report (PySAT 1.9.dev16, CPLEX 22.2.0, DOcplex 2.32.264, OR-Tools 9.15.6755, Gurobi 13.0.3).
- [x] Sửa diễn giải encoding để khớp dữ liệu: Pairwise nhanh nhất tại 3/4 kích thước; Sequential Counter nhanh nhất tại `N = 16`.
- [x] Lưu batch Pairwise cũ trong commit `9fab7ed`; batch CPLEX-restored mới đang local, chưa commit.
- [x] Rebuilt the PDF after the latest edits using MiKTeX 25.12 installed at `E:\Apps\MiKTeX`.
- [x] MiKTeX executables are at `E:\Apps\MiKTeX\miktex\bin\x64`; User PATH contains this directory, so older terminals must be restarted.

## 6. Giới hạn hiện tại cần lưu ý

- [x] CPLEX Community Edition từng giới hạn batch cũ tại `N = 32`; môi trường CPLEX mới đã pass license check 1.100 biến và giải N-Queens đến `N = 128`.
- [x] Gurobi hiện hoạt động với restricted license; repeated batch chấp nhận đến `N = 44` và báo `LICENSE_LIMIT` từ `N = 45`.
- [x] CPLEX CP Optimizer hiện khả dụng; các lỗi không tìm executable chỉ thuộc batch lịch sử `pairwise_solver_comparison_repeat3.csv`.
- [x] Chọn Pairwise làm baseline SAT tạm thời cho cross-solver: nhanh nhất tại `N = 8, 32, 64`; Sequential Counter nhanh nhất tại `N = 16`.
- [x] Ghi rõ lựa chọn hiện tại: giữ các kết quả Gurobi lớn là `LICENSE_LIMIT`; chỉ rerun nếu có Academic License.
- [x] Xác nhận CPLEX MIP/CP có thể giải vượt các ngưỡng license cũ trong batch mới.
- [x] Quyết định ghi Gurobi license-limited cases trong bảng cuối dưới dạng `LL`, không đưa vào median runtime.

## 7. Việc còn phải làm

### Chốt thiết kế thực nghiệm

- [x] Phân tích pilot và chọn dải kích thước board tạm thời cho cross-solver.
- [x] Chọn 3 lần lặp/cấu hình làm protocol tạm thời; cần xác nhận số lần cuối cho benchmark nộp bài.
- [x] Giữ timeout 600 giây và chính sách ghi `TIMEOUT`, `LICENSE_LIMIT`, `ERROR` riêng.
- [x] Chọn Pairwise làm baseline SAT tạm thời cho cross-solver; không kết luận Pairwise nhanh nhất ở mọi kích thước.
- [x] Bộ metric và quy tắc báo cáo: median total time cho 3 run; status riêng cho success, timeout, error và license limit.

### Chạy benchmark chính thức

- [x] Chạy batch SAT encoding lặp tại `N = 8, 16, 32` (5 lần) và `N = 64` (3 lần); `N = 96, 128` mới có dữ liệu pilot một lần.
- [x] Chạy matched SAT, CP-SAT, CPLEX CP, CPLEX MIP và Gurobi MIP: 3 lần tại 10 kích thước, timeout 600 giây.
- [x] Ghi rõ không chạy lại Gurobi `N >= 45` khi license chưa đổi; kết quả hiện tại giữ `LICENSE_LIMIT`.
- [x] Kiểm tra số dòng/trạng thái và xác nhận 138 nghiệm hợp lệ, 12 license limit, không timeout/error.

### Phân tích và báo cáo

- [x] Tổng hợp dữ liệu benchmark Pairwise mới và giữ raw CSV cho từng run.
- [x] Cập nhật bảng median và biểu đồ cho batch mới; 138 lượt hợp lệ, 12 Gurobi license limit, không timeout/error.
- [x] Bổ sung bảng kích thước CNF và phân tích trade-off số biến/số clause/runtime; encoding/solve times được báo cáo riêng.
- [x] Cập nhật phân tích giới hạn thực tế: CPLEX CP/MIP giải đến `N=128`; Gurobi bị limit từ `N=45`.
- [x] Tạo/cập nhật bảng kết quả và figures/plots cho batch hiện tại.
- [x] Cập nhật methodology, experimental setup, results, discussion và limitations trong bản thảo pilot.
- [x] Hoàn thiện nội dung report và rebuild/kiểm tra trực quan PDF; còn một overfull warning ở `\\maketitle` nhưng không thấy nội dung bị cắt.
- [x] Rà soát README, lệnh chạy và artifacts; chỉ đưa file nguồn/kết quả/PDF cần thiết vào commit, bỏ qua file build và tài liệu template dư.

## 8. Trạng thái tổng quan

**Đã hoàn thành:** phần triển khai solver, validation, test, benchmark framework và matched five-method batch (trừ Gurobi bị giới hạn ở kích thước lớn).

**Current status:** Solver implementations, tests, benchmark protocol, matched results, analysis, and report are complete. CPLEX CP/MIP solve through `N=128`; Gurobi results from `N=45` are `LICENSE_LIMIT` and are documented. MiKTeX works; the current PDF was rebuilt and visually reviewed. No external license change is needed to finish the current report.

**Remaining:** push the local commit when ready. Historical SAT batches lack environment metadata and are explicitly treated as historical; rerun large Gurobi cases only if an academic license becomes available.
