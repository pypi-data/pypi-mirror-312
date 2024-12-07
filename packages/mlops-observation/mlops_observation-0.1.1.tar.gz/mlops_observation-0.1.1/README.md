Yêu cầu input đầu vào:
https://docs.evidentlyai.com/user-guide/input-data/column-mapping

Phiên bản Evidently: 0.4.39

Data Quality, Data Drift đã custom lại theo template metrics của DucLH21 đề xuất
- Đã tính toán được các metrics đã define, xuất ra file JSON

Phát triển thêm phần UI của dashboard, có thể làm 2 hướng
- Phát triển Dashboard HTML giống như của Evidently, bằng cách viết lại hàm render html
- Sử dụng BI tools ở bên ngoài, sử dụng file JSON xuất ra làm Input


Presquite:
- Phải truyền giá trị cho reference data và current data
- Phải define column map

1. Data Quality (done)
Yêu cầu Input:
- Data đầu vào là DataFrame
- Cần define list categorical features và numerical feature
- Phải có current data (reference data là optional)


2. Data Drift (done)
Yêu cầu Input: 
- Data đầu vào là DataFrame
- Cần define list categorical features và numerical feature
- Phải có cả current và reference data

3. Model Quality (done phase 1)
- Phải có current data (reference data là optional)
- Data đầu vào là DataFrame
- Cần có ground truth (true label) và kết quả dự đoán\

a. Regression (done)
b. Binary Classification (done)
c. Multiclass Classification (done) 
d. Forecasting (regression overlap -> stop)
e. Ranking (phase 2)
f. Recommendation (phase 2)


3. Model Drift
(Đang phát triển)

4. Model Explain
(Đang phát triển)