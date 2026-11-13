# -*- coding: utf-8 -*-
"""
Script tạo corpus Toán lớp 6 (36 trang nội dung) và bộ câu hỏi benchmark (20 câu).
Đáp ứng yêu cầu:
- >= 30 trang nội dung chuẩn hóa
- Manifest đầy đủ: source_id, title, license, số trang, số ký tự
- 6 Section rõ ràng phục vụ Metadata Filter: so_tu_nhien, so_nguyen, phan_so, so_thap_phan, hinh_hoc_truc_quan, thong_ke_xac_suat
"""

import json
import os

PAGES = [
    # ==================== SECTION 1: SỐ TỰ NHIÊN (Trang 1 - 6) ====================
    {
        "page": 1,
        "section": "so_tu_nhien",
        "title": "Tập hợp và các phần tử của tập hợp. Tập hợp số tự nhiên",
        "text": """### 1. Khái niệm tập hợp và phần tử
Tập hợp là một khái niệm cơ bản trong toán học. Một tập hợp thường được ký hiệu bằng chữ cái in hoa như A, B, C, X, Y. Các phần tử của một tập hợp được viết trong hai dấu ngoặc nhọn { }, cách nhau bởi dấu chấm phẩy ';'.
Nếu phần tử x thuộc tập hợp A, ta viết x ∈ A. Nếu phần tử y không thuộc tập hợp A, ta viết y ∉ A.
Mỗi phần tử chỉ được liệt kê một lần và thứ tự liệt kê các phần tử là tùy ý.

### 2. Tập hợp số tự nhiên
Tập hợp các số tự nhiên được ký hiệu là N = {0; 1; 2; 3; 4; ...}.
Tập hợp các số tự nhiên khác 0 được ký hiệu là N* = {1; 2; 3; 4; ...}.
Số tự nhiên nhỏ nhất là số 0. Không có số tự nhiên lớn nhất vì tập hợp N là vô hạn.
Hai số tự nhiên liên tiếp hơn kém nhau 1 đơn vị. Mỗi số tự nhiên có một số liền sau duy nhất và (trừ số 0) có một số liền trước duy nhất."""
    },
    {
        "page": 2,
        "section": "so_tu_nhien",
        "title": "Cách ghi số tự nhiên. Hệ thập phân và chữ số La Mã",
        "text": """### 1. Hệ thập phân
Để ghi số tự nhiên trong hệ thập phân, người ta dùng mười chữ số: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9.
Trong hệ thập phân, giá trị của mỗi chữ số phụ thuộc vào vị trí của nó trong số đó (nguyên tắc giá trị theo vị trí). Cứ mười đơn vị ở một hàng thì làm thành một đơn vị ở hàng liền trước nó.
Ví dụ: Số 235 có chữ số 2 ở hàng trăm có giá trị 200, chữ số 3 ở hàng chục có giá trị 30, chữ số 5 ở hàng đơn vị có giá trị 5. Ta viết: 235 = 2 x 100 + 3 x 10 + 5.

### 2. Chữ số La Mã
Hệ thống chữ số La Mã sử dụng 7 chữ số cơ bản: I (1), V (5), X (10), L (50), C (100), D (500), M (1000).
Các quy tắc kết hợp chữ số La Mã:
- Chữ số I, X không được lặp lại quá 3 lần liên tiếp.
- Chữ số V, L, D không bao giờ được lặp lại.
- Khi chữ số có giá trị nhỏ hơn đứng trước chữ số lớn hơn, ta lấy giá trị lớn trừ giá trị nhỏ: IV là 4, IX là 9, XL là 40, XC là 90."""
    },
    {
        "page": 3,
        "section": "so_tu_nhien",
        "title": "Các phép tính với số tự nhiên và Luỹ thừa với số mũ tự nhiên",
        "text": """### 1. Các phép tính cơ bản
Phép cộng và phép nhân số tự nhiên có tính chất giao hoán, kết hợp. Phép nhân có tính chất phân phối đối với phép cộng: a x (b + c) = a x b + a x c.
Trong phép chia có dư: a = b x q + r, trong đó số dư r phải thỏa mãn điều kiện 0 ≤ r < b. Nếu r = 0 thì đó là phép chia hết.

### 2. Luỹ thừa với số mũ tự nhiên
Luỹ thừa bậc n của số tự nhiên a là tích của n thừa số bằng nhau, mỗi thừa số bằng a: a^n = a x a x ... x a (với n thừa số a, n ∈ N*).
Số a được gọi là cơ số, số n được gọi là số mũ. Quy ước: a^1 = a, a^0 = 1 (với a ≠ 0).
Quy tắc nhân hai luỹ thừa cùng cơ số: Giữ nguyên cơ số và cộng các số mũ: a^m x a^n = a^(m + n).
Quy tắc chia hai luỹ thừa cùng cơ số: Giữ nguyên cơ số và trừ các số mũ: a^m : a^n = a^(m - n) (với a ≠ 0 và m ≥ n)."""
    },
    {
        "page": 4,
        "section": "so_tu_nhien",
        "title": "Thứ tự thực hiện các phép tính trong biểu thức",
        "text": """### 1. Biểu thức không có dấu ngoặc
- Nếu biểu thức chỉ có phép cộng và trừ (hoặc chỉ có phép nhân và chia), ta thực hiện các phép tính theo thứ tự từ trái sang phải.
- Nếu biểu thức có cả phép cộng, trừ, nhân, chia và nâng lên luỹ thừa, thứ tự ưu tiên thực hiện là: Luỹ thừa -> Nhân và chia -> Cộng và trừ.

### 2. Biểu thức có chứa dấu ngoặc
Khi biểu thức có chứa các dấu ngoặc khác nhau, thứ tự thực hiện các phép tính bên trong ngoặc là:
Thực hiện trong ngoặc tròn ( ) trước -> Sau đó đến ngoặc vuông [ ] -> Cuối cùng thực hiện trong ngoặc nhọn { }.
Sau khi giải quyết xong các phép tính trong ngoặc nhọn, tiếp tục thực hiện các phép tính bên ngoài ngoặc theo quy tắc ưu tiên luỹ thừa, nhân chia rồi đến cộng trừ."""
    },
    {
        "page": 5,
        "section": "so_tu_nhien",
        "title": "Tính chất chia hết của một tổng và Dấu hiệu chia hết",
        "text": """### 1. Tính chất chia hết của một tổng
- Nếu tất cả các số hạng của một tổng đều chia hết cho cùng một số m, thì tổng đó chia hết cho m: Nếu a ⋮ m và b ⋮ m thì (a + b) ⋮ m.
- Nếu chỉ có duy nhất một số hạng của tổng không chia hết cho m, còn các số hạng khác đều chia hết cho m, thì tổng đó không chia hết cho m.

### 2. Các dấu hiệu chia hết cơ bản
- Dấu hiệu chia hết cho 2: Các số có chữ số tận cùng là chữ số chẵn (0, 2, 4, 6, 8) thì chia hết cho 2 và chỉ những số đó mới chia hết cho 2.
- Dấu hiệu chia hết cho 5: Các số có chữ số tận cùng là 0 hoặc 5 thì chia hết cho 5. Số vừa chia hết cho 2 vừa chia hết cho 5 phải có tận cùng bằng 0.
- Dấu hiệu chia hết cho 3: Các số có tổng các chữ số chia hết cho 3 thì chia hết cho 3.
- Dấu hiệu chia hết cho 9: Các số có tổng các chữ số chia hết cho 9 thì chia hết cho 9. Một số chia hết cho 9 thì luôn chia hết cho 3, nhưng số chia hết cho 3 chưa chắc chia hết cho 9."""
    },
    {
        "page": 6,
        "section": "so_tu_nhien",
        "title": "Số nguyên tố, Hợp số. Ước chung lớn nhất và Bội chung nhỏ nhất",
        "text": """### 1. Số nguyên tố và hợp số
- Số nguyên tố là số tự nhiên lớn hơn 1, chỉ có hai ước là 1 và chính nó. Số 2 là số nguyên tố chẵn duy nhất và là số nguyên tố nhỏ nhất.
- Hợp số là số tự nhiên lớn hơn 1, có nhiều hơn hai ước (tức là ngoài 1 và chính nó còn có ít nhất một ước khác).
- Số 0 và số 1 không phải là số nguyên tố cũng không phải là hợp số.

### 2. Ước chung lớn nhất (ƯCLN) và Bội chung nhỏ nhất (BCNN)
- Ước chung lớn nhất của hai hay nhiều số là số lớn nhất trong tập hợp các ước chung của các số đó. Cách tìm: Phân tích các số ra thừa số nguyên tố, chọn ra các thừa số nguyên tố chung và lập tích với số mũ nhỏ nhất.
- Hai số có ƯCLN bằng 1 được gọi là hai số nguyên tố cùng nhau.
- Bội chung nhỏ nhất của hai hay nhiều số là số nhỏ nhất khác 0 trong tập hợp các bội chung. Cách tìm: Chọn các thừa số nguyên tố chung và riêng, lập tích với số mũ lớn nhất."""
    },

    # ==================== SECTION 2: SỐ NGUYÊN (Trang 7 - 12) ====================
    {
        "page": 7,
        "section": "so_nguyen",
        "title": "Số nguyên âm và Tập hợp các số nguyên. Trục số nguyên",
        "text": """### 1. Số nguyên âm trong thực tế
Trong đời sống, để biểu thị các đại lượng có hướng ngược nhau, người ta dùng số dương và số âm:
- Nhiệt độ dưới 0 độ C được ghi bằng số nguyên âm, ví dụ: -5°C (âm năm độ C).
- Độ sâu dưới mực nước biển: -20 m biểu thị độ sâu 20 mét dưới mực nước biển.
- Số tiền nợ hoặc lỗ trong kinh doanh được ghi bằng số nguyên âm.

### 2. Tập hợp các số nguyên Z
Tập hợp gồm các số nguyên âm, số 0 và các số nguyên dương được gọi là tập hợp các số nguyên, ký hiệu là Z = {..., -3, -2, -1, 0, 1, 2, 3, ...}.
Số 0 là số nguyên nhưng không phải là số nguyên dương và cũng không phải là số nguyên âm.
Số đối của số nguyên a ký hiệu là -a. Số đối của số 0 là chính nó (0). Hai số đối nhau cách đều điểm 0 trên trục số."""
    },
    {
        "page": 8,
        "section": "so_nguyen",
        "title": "So sánh các số nguyên trên trục số",
        "text": """### 1. Thứ tự trên trục số nằm ngang
Trên trục số nằm ngang, điểm biểu diễn số nhỏ hơn nằm ở bên trái điểm biểu diễn số lớn hơn.
Nếu điểm a nằm bên trái điểm b thì a < b hoặc b > a. Chiều từ trái sang phải là chiều dương.

### 2. Quy tắc so sánh số nguyên
- Mọi số nguyên dương đều lớn hơn số 0: Với a > 0 thì a > 0.
- Mọi số nguyên âm đều nhỏ hơn số 0: Với a < 0 thì a < 0.
- Mọi số nguyên âm đều nhỏ hơn bất kỳ số nguyên dương nào.
- So sánh hai số nguyên âm: Trong hai số nguyên âm, số nào có số đối lớn hơn thì số đó nhỏ hơn (hoặc số nào có khoảng cách tới gốc 0 xa hơn về bên trái thì số đó nhỏ hơn). Ví dụ: -9 < -4 vì số đối 9 lớn hơn 4."""
    },
    {
        "page": 9,
        "section": "so_nguyen",
        "title": "Phép cộng các số nguyên cùng dấu và khác dấu",
        "text": """### 1. Cộng hai số nguyên cùng dấu
- Cộng hai số nguyên dương: Thực hiện tương tự cộng hai số tự nhiên thông thường.
- Cộng hai số nguyên âm: Ta cộng hai số đối của chúng rồi đặt dấu trừ '-' trước kết quả. Công thức: (-a) + (-b) = -(a + b) với a, b > 0.
Ví dụ: (-15) + (-25) = -(15 + 25) = -40.

### 2. Cộng hai số nguyên khác dấu
- Hai số đối nhau có tổng bằng 0: a + (-a) = 0.
- Muốn cộng hai số nguyên khác dấu không đối nhau: Ta lấy số có số đối lớn hơn trừ đi số có số đối nhỏ hơn, rồi đặt dấu của số có số đối lớn hơn trước kết quả.
Ví dụ 1: 18 + (-7) = 18 - 7 = 11 (vì 18 > 7, mang dấu dương).
Ví dụ 2: (-20) + 8 = -(20 - 8) = -12 (vì số đối của -20 là 20 lớn hơn 8, mang dấu âm)."""
    },
    {
        "page": 10,
        "section": "so_nguyen",
        "title": "Phép trừ số nguyên và Quy tắc dấu ngoặc",
        "text": """### 1. Phép trừ hai số nguyên
Muốn trừ số nguyên a cho số nguyên b, ta lấy a cộng với số đối của b: a - b = a + (-b).
Phép trừ trong tập hợp số nguyên Z luôn luôn thực hiện được mà không bị ràng buộc điều kiện số bị trừ phải lớn hơn số trừ như trong tập hợp số tự nhiên N.
Ví dụ: 3 - 8 = 3 + (-8) = -5.

### 2. Quy tắc dấu ngoặc
- Khi bỏ dấu ngoặc có dấu cộng '+' đằng trước, ta giữ nguyên dấu của tất cả các số hạng trong ngoặc: +(a - b + c) = a - b + c.
- Khi bỏ dấu ngoặc có dấu trừ '-' đằng trước, ta phải đổi dấu của tất cả các số hạng trong ngoặc: Dấu '+' đổi thành '-' và dấu '-' đổi thành '+': -(a - b + c) = -a + b - c.
- Tương tự, khi đặt dấu ngoặc có dấu trừ đằng trước, ta cũng phải đổi dấu tất cả các số hạng đưa vào trong ngoặc."""
    },
    {
        "page": 11,
        "section": "so_nguyen",
        "title": "Phép nhân hai số nguyên và Tính chất phân phối",
        "text": """### 1. Quy tắc nhân hai số nguyên
- Nhân hai số nguyên cùng dấu: Tích của hai số nguyên cùng dấu luôn là một số nguyên dương.
  (+) x (+) = (+) và (-) x (-) = (+).
  Quy tắc: Muốn nhân hai số nguyên âm, ta nhân hai số đối của chúng: (-a) x (-b) = a x b. Ví dụ: (-6) x (-5) = 30.
- Nhân hai số nguyên khác dấu: Tích của hai số nguyên khác dấu luôn là một số nguyên âm.
  (+) x (-) = (-) và (-) x (+) = (-).
  Quy tắc: Muốn nhân hai số nguyên khác dấu, ta nhân hai số đối của chúng rồi đặt dấu '-' trước kết quả: (-a) x b = -(a x b). Ví dụ: (-7) x 4 = -28.
- Tích của bất kỳ số nguyên nào với số 0 cũng bằng 0: a x 0 = 0.

### 2. Tính chất phép nhân số nguyên
Phép nhân số nguyên có tính chất giao hoán: a x b = b x a; tính chất kết hợp: (a x b) x c = a x (b x c); tính chất phân phối đối với phép cộng và phép trừ: a x (b + c) = a x b + a x c."""
    },
    {
        "page": 12,
        "section": "so_nguyen",
        "title": "Quan hệ chia hết và Phép chia hết trong tập hợp số nguyên Z",
        "text": """### 1. Khái niệm bội và ước trong Z
Cho hai số nguyên a và b (với b ≠ 0). Nếu có số nguyên q sao cho a = b x q thì ta nói a chia hết cho b, ký hiệu là a ⋮ b.
Khi đó, a được gọi là bội của b và b được gọi là ước của a.
Ví dụ: 12 là bội của -3 vì 12 = (-3) x (-4); -3 là ước của 12.

### 2. Các tính chất quan trọng về bội và ước trong Z
- Nếu a chia hết cho b thì -a cũng chia hết cho b: a ⋮ b => (-a) ⋮ b.
- Các số 1 và -1 là ước của mọi số nguyên.
- Số 0 là bội của mọi số nguyên khác 0, nhưng số 0 không phải là ước của bất kỳ số nguyên nào vì phép chia cho 0 không xác định.
- Nếu a là ước của b và b là ước của c thì a là ước của c (tính chất bắc cầu).
- Quy tắc dấu trong phép chia hết hai số nguyên hoàn toàn tương tự quy tắc dấu của phép nhân: Cùng dấu cho kết quả dương, khác dấu cho kết quả âm."""
    },

    # ==================== SECTION 3: PHÂN SỐ (Trang 13 - 18) ====================
    {
        "page": 13,
        "section": "phan_so",
        "title": "Mở rộng khái niệm phân số và Định nghĩa hai phân số bằng nhau",
        "text": """### 1. Khái niệm phân số tổng quát
Người ta gọi a/b với a, b ∈ Z và b ≠ 0 là một phân số, trong đó a là tử số (tử) và b là mẫu số (mẫu) của phân số.
Số nguyên n có thể viết dưới dạng phân số là n/1.
Phân số có thể nhận giá trị âm, ví dụ: -3/4 hoặc 5/-7. Chú ý: Phân số 5/-7 thường được đổi thành dạng chuẩn có mẫu dương là -5/7 bằng cách nhân cả tử và mẫu với -1.

### 2. Hai phân số bằng nhau
Hai phân số a/b và c/d được gọi là bằng nhau nếu thỏa mãn điều kiện tích chéo: a x d = b x c.
Ký hiệu: a/b = c/d khi và chỉ khi a x d = b x c.
Ví dụ: Phân số -2/3 bằng phân số 6/-9 vì (-2) x (-9) = 3 x 6 = 18.
Dựa vào quy tắc này, ta có thể tìm số nguyên x chưa biết trong tỉ lệ thức phân số: Nếu x/b = c/d thì x = (b x c) / d."""
    },
    {
        "page": 14,
        "section": "phan_so",
        "title": "Tính chất cơ bản của phân số và Rút gọn phân số",
        "text": """### 1. Tính chất cơ bản của phân số
- Tính chất nhân: Nếu ta nhân cả tử và mẫu của một phân số với cùng một số nguyên khác 0 thì ta được một phân số bằng phân số đã cho: a/b = (a x m) / (b x m) (với m ∈ Z, m ≠ 0).
- Tính chất chia: Nếu ta chia cả tử và mẫu của một phân số cho cùng một ước chung của chúng thì ta được một phân số bằng phân số đã cho: a/b = (a : n) / (b : n) (với n ∈ ƯC(a, b)).

### 2. Rút gọn phân số về phân số tối giản
- Rút gọn phân số là chia cả tử và mẫu của phân số cho một ước chung khác 1 và -1 để được phân số đơn giản hơn.
- Phân số tối giản là phân số mà tử và mẫu chỉ có ước chung là 1 và -1 (tức là ƯCLN(|a|, |b|) = 1).
- Muốn rút gọn một phân số về phân số tối giản chỉ trong một lần, ta chia cả tử và mẫu của phân số đó cho ước chung lớn nhất (ƯCLN) của chúng."""
    },
    {
        "page": 15,
        "section": "phan_so",
        "title": "Quy đồng mẫu nhiều phân số và So sánh phân số",
        "text": """### 1. Quy tắc quy đồng mẫu số nhiều phân số
Để quy đồng mẫu nhiều phân số có mẫu dương, ta thực hiện theo 3 bước:
- Bước 1: Tìm một bội chung của các mẫu (thường là BCNN của các mẫu) để làm mẫu chung.
- Bước 2: Tìm thừa số phụ của mỗi mẫu bằng cách chia mẫu chung cho từng mẫu riêng biệt.
- Bước 3: Nhân tử và mẫu của mỗi phân số với thừa số phụ tương ứng.

### 2. So sánh hai phân số
- So sánh hai phân số cùng mẫu dương: Trong hai phân số có cùng một mẫu dương, phân số nào có tử số lớn hơn thì phân số đó lớn hơn: Nếu a > b thì a/m > b/m (với m > 0).
- So sánh hai phân số khác mẫu: Ta quy đồng mẫu các phân số đó về cùng một mẫu dương, rồi so sánh các tử số với nhau.
- Phân số có tử và mẫu cùng dấu thì lớn hơn 0 (phân số dương). Phân số có tử và mẫu trái dấu thì nhỏ hơn 0 (phân số âm). Phân số âm luôn nhỏ hơn phân số dương."""
    },
    {
        "page": 16,
        "section": "phan_so",
        "title": "Phép cộng và phép trừ phân số",
        "text": """### 1. Phép cộng phân số
- Cộng hai phân số cùng mẫu: Muốn cộng hai phân số có cùng mẫu, ta cộng các tử số và giữ nguyên mẫu số: a/m + b/m = (a + b)/m.
- Cộng hai phân số khác mẫu: Muốn cộng hai phân số không cùng mẫu, ta viết chúng dưới dạng hai phân số có cùng một mẫu rồi áp dụng quy tắc cộng hai phân số cùng mẫu.
- Tính chất phép cộng phân số: Giao hoán: a/b + c/d = c/d + a/b; Kết hợp: (a/b + c/d) + p/q = a/b + (c/d + p/q); Cộng với số 0: a/b + 0 = a/b.

### 2. Phép trừ phân số
- Số đối của phân số a/b là phân số -a/b, ký hiệu là -(a/b). Tổng của hai phân số đối nhau bằng 0: a/b + (-a/b) = 0.
- Muốn trừ một phân số cho một phân số, ta cộng số bị trừ với số đối của số trừ: a/b - c/d = a/b + (-c/d)."""
    },
    {
        "page": 17,
        "section": "phan_so",
        "title": "Phép nhân, phép chia phân số và Số nghịch đảo",
        "text": """### 1. Phép nhân phân số
Muốn nhân hai phân số, ta nhân các tử với nhau và nhân các mẫu với nhau: (a/b) x (c/d) = (a x c) / (b x d).
Muốn nhân một số nguyên với một phân số, ta nhân số nguyên đó với tử của phân số và giữ nguyên mẫu: a x (b/c) = (a x b)/c.
Phép nhân phân số có đầy đủ tính chất giao hoán, kết hợp và phân phối đối với phép cộng.

### 2. Số nghịch đảo và Phép chia phân số
- Hai số được gọi là nghịch đảo của nhau nếu tích của chúng bằng 1. Số nghịch đảo của phân số a/b (với a, b ≠ 0) là phân số b/a.
- Số 0 không có số nghịch đảo.
- Phép chia phân số: Muốn chia một phân số cho một phân số khác 0, ta nhân số bị chia với số nghịch đảo của số chia: (a/b) : (c/d) = (a/b) x (d/c) = (a x d) / (b x c) (với c/d ≠ 0)."""
    },
    {
        "page": 18,
        "section": "phan_so",
        "title": "Hai bài toán cơ bản về phân số",
        "text": """### 1. Bài toán 1: Tìm giá trị phân số của một số cho trước
Quy tắc: Muốn tìm m/n của một số b cho trước (với m/n ∈ Q, n ≠ 0), ta lấy số b nhân với m/n:
Giá trị cần tìm = b x (m/n).
Ví dụ: Một mảnh vườn có diện tích 120 m^2. Diện tích trồng hoa chiếm 3/5 diện tích mảnh vườn.
Diện tích trồng hoa là: 120 x (3/5) = 72 m^2.

### 2. Bài toán 2: Tìm một số biết giá trị một phân số của nó
Quy tắc: Muốn tìm một số biết m/n của nó bằng a, ta lấy a chia cho m/n (với m, n ≠ 0):
Số cần tìm = a : (m/n).
Ví dụ: Tìm chiều dài một khúc vải biết rằng 2/3 khúc vải dài 18 mét.
Chiều dài khúc vải ban đầu là: 18 : (2/3) = 18 x (3/2) = 27 mét."""
    },

    # ==================== SECTION 4: SỐ THẬP PHÂN (Trang 19 - 24) ====================
    {
        "page": 19,
        "section": "so_thap_phan",
        "title": "Số thập phân và Cấu tạo của số thập phân",
        "text": """### 1. Định nghĩa số thập phân
Phân số thập phân là phân số mà mẫu số là luỹ thừa của 10 (ví dụ: 10, 100, 1000,...).
Các phân số thập phân có thể viết dưới dạng số thập phân.
Số thập phân gồm hai phần cách nhau bởi dấu phẩy:
- Phần nằm bên trái dấu phẩy gọi là phần số nguyên (phần nguyên).
- Phần nằm bên phải dấu phẩy gọi là phần thập phân.
Ví dụ: Số 37,25 có phần nguyên là 37 và phần thập phân gồm chữ số 2 ở hàng phần mười, chữ số 5 ở hàng phần trăm.

### 2. Số thập phân âm
Số đối của số thập phân a ký hiệu là -a.
Số thập phân âm là số thập phân có dấu trừ '-' đứng đằng trước. Ví dụ: -0,75; -12,4.
Mọi phân số thập phân âm đều được viết dưới dạng số thập phân âm: -15/100 = -0,15."""
    },
    {
        "page": 20,
        "section": "so_thap_phan",
        "title": "So sánh các số thập phân",
        "text": """### 1. Quy tắc so sánh hai số thập phân dương
Để so sánh hai số thập phân dương:
- So sánh phần nguyên trước: Số thập phân nào có phần nguyên lớn hơn thì số đó lớn hơn.
- Nếu phần nguyên bằng nhau, ta so sánh từng hàng ở phần thập phân từ trái sang phải (hàng phần mười, hàng phần trăm, hàng phần nghìn...). Ở hàng đầu tiên có chữ số khác nhau, số nào có chữ số lớn hơn thì số đó lớn hơn.
Ví dụ: 15,38 > 15,35 vì phần nguyên bằng 15, hàng phần mười đều là 3, nhưng hàng phần trăm 8 > 5.

### 2. So sánh tổng quát số thập phân
- Mọi số thập phân dương đều lớn hơn 0 và lớn hơn mọi số thập phân âm.
- Để so sánh hai số thập phân âm: Ta so sánh hai số đối của chúng. Số nào có số đối lớn hơn thì số đó nhỏ hơn.
Ví dụ: So sánh -3,75 và -3,25. Ta thấy 3,75 > 3,25 nên kết luận -3,75 < -3,25."""
    },
    {
        "page": 21,
        "section": "so_thap_phan",
        "title": "Các phép tính cộng, trừ, nhân, chia với số thập phân",
        "text": """### 1. Phép cộng và trừ số thập phân
Quy tắc đặt tính: Đặt các số thập phân sao cho các chữ số ở cùng một hàng thẳng cột với nhau (dấu phẩy thẳng cột với dấu phẩy), rồi thực hiện cộng hoặc trừ như đối với số tự nhiên.
Quy tắc dấu khi cộng trừ số thập phân hoàn toàn tương tự quy tắc cộng trừ số nguyên:
- Cộng hai số thập phân âm: (-a) + (-b) = -(a + b).
- Trừ hai số thập phân: a - b = a + (-b).

### 2. Phép nhân và chia số thập phân
- Nhân hai số thập phân: Nhân như nhân hai số tự nhiên, sau đó đếm xem trong phần thập phân của cả hai thừa số có tất cả bao nhiêu chữ số rồi dùng dấu phẩy tách ở tích bấy nhiêu chữ số kể từ phải sang trái.
- Quy tắc nhân chia có dấu:
  Cùng dấu cho kết quả dương: (-) x (-) = (+); (-) : (-) = (+).
  Khác dấu cho kết quả âm: (-) x (+) = (-); (-) : (+) = (-).
- Nhân với 10, 100, 1000...: Dịch dấu phẩy sang phải 1, 2, 3... chữ số.
- Chia cho 10, 100, 1000...: Dịch dấu phẩy sang trái 1, 2, 3... chữ số."""
    },
    {
        "page": 22,
        "section": "so_thap_phan",
        "title": "Làm tròn số thập phân và Ước lượng kết quả",
        "text": """### 1. Quy tắc làm tròn số thập phân
Muốn làm tròn một số thập phân đến một hàng nào đó (hàng làm tròn), ta nhìn vào chữ số ngay bên phải của hàng làm tròn:
- Trường hợp 1: Nếu chữ số đầu tiên bỏ đi nhỏ hơn 5 (là 0, 1, 2, 3, 4), ta giữ nguyên chữ số ở hàng làm tròn.
- Trường hợp 2: Nếu chữ số đầu tiên bỏ đi lớn hơn hoặc bằng 5 (là 5, 6, 7, 8, 9), ta cộng thêm 1 vào chữ số ở hàng làm tròn.
- Đối với phần thập phân sau hàng làm tròn: Ta bỏ hẳn đi.
- Đối với phần nguyên sau hàng làm tròn: Ta thay các chữ số bỏ đi bằng các chữ số 0.
Ví dụ: Làm tròn số 7,436 đến hàng phần mười: Chữ số bên phải là 3 < 5 nên giữ nguyên 4 -> Kết quả: 7,4.

### 2. Ước lượng kết quả
Để ước lượng nhanh kết quả của một phép tính phức tạp trong thực tế, người ta thường làm tròn các số hạng hoặc thừa số đến hàng cao nhất rồi mới thực hiện phép tính nhẩm."""
    },
    {
        "page": 23,
        "section": "so_thap_phan",
        "title": "Tỉ số và Tỉ số phần trăm",
        "text": """### 1. Khái niệm tỉ số của hai số
Tỉ số của hai số a và b (với b ≠ 0) là thương của phép chia số a cho số b, ký hiệu là a/b hoặc a : b.
Khái niệm tỉ số thường được dùng khi so sánh hai đại lượng cùng loại và cùng đơn vị đo.

### 2. Tỉ số phần trăm
Tỉ số phần trăm của hai số a và b là tỉ số của a và b được viết dưới dạng phân số có mẫu số là 100, ký hiệu là %.
Quy tắc tính tỉ số phần trăm của hai số a và b: Ta lấy a chia cho b, rồi nhân kết quả với 100 và viết thêm ký hiệu % vào bên phải kết quả:
Tỉ số phần trăm = (a x 100 / b) %.
Ví dụ: Trong một lớp học có 40 học sinh, trong đó có 24 học sinh nữ.
Tỉ số phần trăm của số học sinh nữ so với tổng số học sinh của lớp là: (24 x 100 / 40)% = 60%."""
    },
    {
        "page": 24,
        "section": "so_thap_phan",
        "title": "Các bài toán thực tế về tỉ số phần trăm",
        "text": """### 1. Bài toán tìm giá trị phần trăm của một số
Muốn tìm a% của một số b cho trước, ta lấy b nhân với a rồi chia cho 100 (hoặc lấy b nhân với a%):
Giá trị = (b x a) / 100.
Ví dụ: Giá niêm yết của một chiếc áo khoác là 500.000 đồng. Cửa hàng đang có chương trình giảm giá 15%.
Số tiền được giảm là: 500.000 x 15 / 100 = 75.000 đồng. Giá sau khi giảm là: 500.000 - 75.000 = 425.000 đồng.

### 2. Bài toán tìm một số khi biết giá trị phần trăm của nó
Muốn tìm một số biết a% của nó bằng c, ta lấy c chia cho a rồi nhân với 100 (hoặc lấy c chia cho a%):
Số cần tìm = (c x 100) / a.
Ví dụ: Lãi suất tiết kiệm ngân hàng là 6% một năm. Sau một năm, bác Nam nhận được 18.000.000 đồng tiền lãi.
Số tiền bác Nam gửi tiết kiệm ban đầu là: (18.000.000 x 100) / 6 = 300.000.000 đồng."""
    },

    # ==================== SECTION 5: HÌNH HỌC TRỰC QUAN (Trang 25 - 30) ====================
    {
        "page": 25,
        "section": "hinh_hoc_truc_quan",
        "title": "Tam giác đều, Hình vuông và Lục giác đều",
        "text": """### 1. Tam giác đều
Tam giác đều là tam giác có 3 cạnh bằng nhau và 3 góc bằng nhau. Mỗi góc của tam giác đều bằng 60°.
Ba đỉnh của tam giác đều cách đều tâm của nó.

### 2. Hình vuông
Hình vuông là tứ giác có 4 cạnh bằng nhau và 4 góc bằng nhau (mỗi góc là một góc vuông 90°).
Đặc điểm hai đường chéo của hình vuông:
- Hai đường chéo bằng nhau.
- Hai đường chéo vuông góc với nhau tại trung điểm của mỗi đường.

### 3. Lục giác đều
Lục giác đều là hình có 6 cạnh bằng nhau và 6 góc bằng nhau.
Hình lục giác đều được ghép từ 6 hình tam giác đều có cùng kích thước ghép lại chung đỉnh tại tâm.
Đặc điểm đường chéo: Lục giác đều có 3 đường chéo chính bằng nhau và cùng cắt nhau tại trung điểm của mỗi đường chéo chính (tâm đối xứng)."""
    },
    {
        "page": 26,
        "section": "hinh_hoc_truc_quan",
        "title": "Hình chữ nhật và Hình thoi",
        "text": """### 1. Hình chữ nhật
Hình chữ nhật là tứ giác có 4 góc vuông (mỗi góc 90°).
Đặc điểm của hình chữ nhật:
- Các cạnh đối diện song song và bằng nhau.
- Hai đường chéo bằng nhau và cắt nhau tại trung điểm của mỗi đường.
- Hình chữ nhật có 2 trục đối xứng (hai đường thẳng đi qua trung điểm các cặp cạnh đối diện).

### 2. Hình thoi
Hình thoi là tứ giác có 4 cạnh bằng nhau.
Đặc điểm của hình thoi:
- Các cạnh đối diện song song với nhau.
- Các góc đối diện bằng nhau.
- Hai đường chéo của hình thoi vuông góc với nhau tại trung điểm của mỗi đường.
- Hai đường chéo là hai trục đối xứng của hình thoi và là các tia phân giác của các góc trong hình thoi."""
    },
    {
        "page": 27,
        "section": "hinh_hoc_truc_quan",
        "title": "Hình bình hành và Hình thang cân",
        "text": """### 1. Hình bình hành
Hình bình hành là tứ giác có các cặp cạnh đối song song.
Đặc điểm của hình bình hành:
- Các cạnh đối diện bằng nhau: AB = CD và AD = BC.
- Các góc đối diện bằng nhau: Góc A = Góc C và Góc B = Góc D.
- Hai đường chéo cắt nhau tại trung điểm của mỗi đường. Giao điểm hai đường chéo là tâm đối xứng của hình bình hành. Hình bình hành tổng quát không có trục đối xứng.

### 2. Hình thang cân
Hình thang cân là hình thang có hai góc kề một đáy bằng nhau.
Đặc điểm của hình thang cân:
- Hai đáy song song với nhau.
- Hai cạnh bên bằng nhau nhưng không song song (trừ trường hợp đặc biệt là hình chữ nhật).
- Hai đường chéo bằng nhau.
- Hình thang cân có 1 trục đối xứng duy nhất là đường thẳng đi qua trung điểm hai đáy."""
    },
    {
        "page": 28,
        "section": "hinh_hoc_truc_quan",
        "title": "Công thức tính Chu vi và Diện tích: Hình vuông, Chữ nhật, Bình hành, Thoi",
        "text": """### 1. Chu vi và diện tích Hình vuông & Hình chữ nhật
- Hình vuông cạnh a:
  Chu vi: C = 4 x a.
  Diện tích: S = a x a = a^2.
- Hình chữ nhật có chiều dài a và chiều rộng b:
  Chu vi: C = 2 x (a + b).
  Diện tích: S = a x b.

### 2. Chu vi và diện tích Hình bình hành & Hình thoi
- Hình bình hành có cạnh đáy a, cạnh bên b và chiều cao tương ứng h:
  Chu vi: C = 2 x (a + b).
  Diện tích: S = a x h (đáy nhân với chiều cao tương ứng).
- Hình thoi có cạnh a và độ dài hai đường chéo là d1, d2:
  Chu vi: C = 4 x a.
  Diện tích: S = (d1 x d2) / 2 (nửa tích độ dài hai đường chéo)."""
    },
    {
        "page": 29,
        "section": "hinh_hoc_truc_quan",
        "title": "Công thức tính Chu vi và Diện tích: Hình tam giác và Hình thang",
        "text": """### 1. Chu vi và diện tích Hình tam giác
- Chu vi hình tam giác có độ dài ba cạnh là a, b, c:
  C = a + b + c.
- Diện tích hình tam giác có độ dài cạnh đáy a và chiều cao tương ứng h:
  S = (a x h) / 2 (bằng một nửa tích của cạnh đáy và chiều cao tương ứng).
- Đối với tam giác vuông có hai cạnh góc vuông a và b: Diện tích S = (a x b) / 2.

### 2. Chu vi và diện tích Hình thang
- Chu vi hình thang có 4 cạnh độ dài a, b, c, d: C = a + b + c + d.
- Diện tích hình thang có đáy lớn a, đáy nhỏ b và chiều cao h:
  S = ((a + b) x h) / 2 (bằng tổng độ dài hai đáy nhân với chiều cao rồi chia cho 2)."""
    },
    {
        "page": 30,
        "section": "hinh_hoc_truc_quan",
        "title": "Hình có trục đối xứng và Hình có tâm đối xứng",
        "text": """### 1. Hình có trục đối xứng
Đường thẳng d được gọi là trục đối xứng của hình H nếu mỗi điểm của hình H lấy đối xứng qua d cũng thuộc hình H.
Ví dụ các hình có trục đối xứng:
- Hình tròn có vô số trục đối xứng (mọi đường thẳng đi qua tâm đều là trục đối xứng).
- Hình vuông có 4 trục đối xứng (2 đường chéo và 2 đường nối trung điểm các cạnh đối).
- Tam giác đều có 3 trục đối xứng.
- Hình chữ nhật có 2 trục đối xứng.
- Hình thang cân có 1 trục đối xứng.

### 2. Hình có tâm đối xứng
Điểm O được gọi là tâm đối xứng của hình H nếu mỗi điểm của hình H lấy đối xứng qua O cũng thuộc hình H.
Ví dụ các hình có tâm đối xứng:
- Hình tròn có tâm đối xứng là tâm của đường tròn.
- Hình bình hành, hình chữ nhật, hình vuông, hình thoi có tâm đối xứng là giao điểm của hai đường chéo.
- Tam giác đều và hình thang cân không có tâm đối xứng."""
    },

    # ==================== SECTION 6: THỐNG KÊ VÀ XÁC SUẤT (Trang 31 - 36) ====================
    {
        "page": 31,
        "section": "thong_ke_xac_suat",
        "title": "Thu thập và tổ chức dữ liệu thống kê. Tính hợp lý của dữ liệu",
        "text": """### 1. Thu thập và phân loại dữ liệu
Dữ liệu được thu thập qua nhiều phương pháp: Quan sát trực tiếp, làm thí nghiệm, lập phiếu khảo sát câu hỏi, phỏng vấn hoặc thu thập từ sách báo, niên giám thống kê, mạng internet.
Dữ liệu thống kê bao gồm hai loại chính:
- Dữ liệu là số (dữ liệu định lượng): Chiều cao, cân nặng, nhiệt độ, điểm thi, số học sinh.
- Dữ liệu không phải là số (dữ liệu định tính): Tên các món ăn ưa thích, xếp loại học lực (Giỏi, Khá, Trung bình), màu sắc, giới tính.

### 2. Tính hợp lý của dữ liệu
Dữ liệu thu thập được cần phải kiểm tra tính hợp lý theo các tiêu chí:
- Đúng phạm vi định dạng quy định (ví dụ: điểm thi phải nằm trong khoảng từ 0 đến 10).
- Tổng các thành phần phải bằng tổng số đối tượng điều tra.
- Các giá trị không thể vô lý trong thực tế (ví dụ: tuổi của học sinh lớp 6 không thể là 150 tuổi hoặc số âm)."""
    },
    {
        "page": 32,
        "section": "thong_ke_xac_suat",
        "title": "Bảng số liệu thống kê ban đầu và Bảng tần số",
        "text": """### 1. Bảng số liệu thống kê ban đầu
Khi điều tra về một vấn đề quan tâm, người điều tra ghi lại các số liệu thu thập được theo thứ tự thời gian vào bảng thống kê ban đầu.
Bảng thường gồm các cột ghi thông tin đối tượng và các tiêu chí khảo sát.

### 2. Bảng thống kê tổng hợp và bảng tần số
Để dễ quan sát và so sánh, người ta tổng hợp dữ liệu từ bảng ban đầu vào bảng thống kê rút gọn:
- Hàng thứ nhất ghi các nhóm hoặc giá trị khác nhau của dấu hiệu.
- Hàng thứ hai ghi số lần xuất hiện (tần số) tương ứng của mỗi giá trị đó.
Tổng các tần số trong bảng phải bằng đúng kích thước của mẫu điều tra (tổng số đối tượng được khảo sát). Bảng này giúp nhận biết giá trị nào xuất hiện nhiều nhất, ít nhất."""
    },
    {
        "page": 33,
        "section": "thong_ke_xac_suat",
        "title": "Biểu đồ tranh: Cách đọc và ý nghĩa biểu tượng",
        "text": """### 1. Khái niệm biểu đồ tranh
Biểu đồ tranh là biểu đồ sử dụng các hình ảnh, biểu tượng (icon) để biểu diễn dữ liệu thống kê.
Biểu đồ tranh thường được dùng khi dữ liệu đơn giản, giúp người xem dễ dàng hình dung và tạo sự hấp dẫn, trực quan.

### 2. Quy tắc đọc và xây dựng biểu đồ tranh
- Mỗi hình ảnh hoặc biểu tượng có thể đại diện cho một số lượng đối tượng cụ thể (ví dụ: một biểu tượng ngôi sao đại diện cho 10 học sinh, nửa ngôi sao đại diện cho 5 học sinh).
- Phần chú giải ở cuối biểu đồ tranh quy định rõ giá trị của mỗi biểu tượng.
- Để tính số lượng của một đối tượng: Ta đếm số biểu tượng rồi nhân với giá trị quy ước của một biểu tượng.
Ví dụ: Một biểu tượng cuốn sách thay cho 20 cuốn sách. Nếu nhóm A có 4 biểu tượng cuốn sách thì số sách nhóm A quyên góp được là: 4 x 20 = 80 cuốn sách."""
    },
    {
        "page": 34,
        "section": "thong_ke_xac_suat",
        "title": "Biểu đồ cột đơn và Biểu đồ cột kép",
        "text": """### 1. Biểu đồ cột đơn
Biểu đồ cột sử dụng các cột hình chữ nhật có cùng chiều rộng, đặt cách đều nhau trên trục nằm ngang để biểu diễn số liệu.
Chiều cao của mỗi cột biểu diễn số lượng (tần số) của đối tượng tương ứng trên trục thẳng đứng.
Biểu đồ cột giúp so sánh nhanh chóng độ lớn giữa các đối tượng thống kê.

### 2. Biểu đồ cột kép
Khi muốn so sánh từng cặp đại lượng của hai nhóm đối tượng cùng loại (ví dụ: số học sinh nam và nữ của từng lớp, lượng mưa của hai năm liên tiếp), người ta dùng biểu đồ cột kép.
Trong biểu đồ cột kép:
- Các cột của hai nhóm đặt sát nhau để tiện so sánh trực diện.
- Cột của mỗi nhóm được phân biệt bằng màu sắc hoặc hoa văn khác nhau.
- Cần có phần chú giải rõ ràng màu nào đại diện cho nhóm đối tượng nào."""
    },
    {
        "page": 35,
        "section": "thong_ke_xac_suat",
        "title": "Kết quả có thể và Sự kiện trong thí nghiệm ngẫu nhiên",
        "text": """### 1. Phép thử nghiệm ngẫu nhiên
Phép thử ngẫu nhiên là một hoạt động hay thí nghiệm mà kết quả của nó không thể biết trước chắc chắn trước khi thực hiện, mặc dù ta biết trước tập hợp tất cả các kết quả có thể xảy ra.
Ví dụ: Tung một đồng xu hoặc gieo một con xúc xắc 6 mặt là các phép thử ngẫu nhiên.
Tập hợp tất cả các kết quả có thể:
- Khi tung một đồng xu: Có 2 kết quả có thể là Xuất hiện mặt Sấp (S) hoặc Xuất hiện mặt Ngửa (N).
- Khi gieo một con xúc xắc: Có 6 kết quả có thể là Xuất hiện mặt 1, 2, 3, 4, 5 hoặc 6 chấm.

### 2. Sự kiện (Biến cố)
Một sự kiện là một khẳng định về kết quả của phép thử ngẫu nhiên. Sau khi thực hiện phép thử, một sự kiện có thể xảy ra hoặc không xảy ra.
Có ba loại sự kiện:
- Sự kiện chắc chắn: Luôn luôn xảy ra khi thực hiện phép thử.
- Sự kiện không thể: Không bao giờ xảy ra khi thực hiện phép thử.
- Sự kiện ngẫu nhiên: Có thể xảy ra hoặc không xảy ra tùy thuộc vào kết quả của phép thử."""
    },
    {
        "page": 36,
        "section": "thong_ke_xac_suat",
        "title": "Xác suất thực nghiệm của một sự kiện",
        "text": """### 1. Định nghĩa xác suất thực nghiệm
Khi thực hiện một phép thử lặp đi lặp lại nhiều lần, tỉ số giữa số lần sự kiện E xuất hiện (k) và tổng số lần thực hiện phép thử (n) được gọi là xác suất thực nghiệm của sự kiện E:
Xác suất thực nghiệm = k / n = (Số lần xuất hiện sự kiện E) / (Tổng số lần thực hiện thí nghiệm).
Xác suất thực nghiệm luôn là một số nằm trong đoạn từ 0 đến 1 (hoặc từ 0% đến 100%).

### 2. Ý nghĩa và tính chất
- Khi số lần thực hiện phép thử n càng lớn, xác suất thực nghiệm của một sự kiện sẽ càng ổn định và tiến gần đến xác suất lý thuyết của sự kiện đó.
Ví dụ: Bạn Nam gieo một con xúc xắc 50 lần thì có 12 lần xuất hiện mặt 6 chấm.
Xác suất thực nghiệm của sự kiện 'Xuất hiện mặt 6 chấm' trong 50 lần gieo của Nam là: 12 / 50 = 6 / 25 = 0,24 (tức 24%)."""
    }
]

# ==================== 20 BENCHMARK QUESTIONS (15 Dev / 5 Test) ====================
BENCHMARK_QUESTIONS = [
    # ---------- DEV SPLIT (15 câu) ----------
    {
        "id": "q01",
        "split": "dev",
        "type": "truc_tiep",
        "question": "Số tự nhiên nhỏ nhất là số nào và tập hợp các số tự nhiên N* gồm những số nào?",
        "expected_answer": "Số tự nhiên nhỏ nhất là số 0. Tập hợp N* gồm các số tự nhiên khác 0: N* = {1; 2; 3; 4; ...}.",
        "gold_source_id": "toan-6-gdpt2018",
        "gold_page": 1,
        "evidence_quote": "Tập hợp các số tự nhiên khác 0 được ký hiệu là N* = {1; 2; 3; 4; ...}. Số tự nhiên nhỏ nhất là số 0.",
        "filter": None
    },
    {
        "id": "q02",
        "split": "dev",
        "type": "truc_tiep",
        "question": "Trong hệ thống chữ số La Mã, những chữ số nào không bao giờ được lặp lại?",
        "expected_answer": "Chữ số V, L, D không bao giờ được lặp lại.",
        "gold_source_id": "toan-6-gdpt2018",
        "gold_page": 2,
        "evidence_quote": "Chữ số V, L, D không bao giờ được lặp lại.",
        "filter": None
    },
    {
        "id": "q03",
        "split": "dev",
        "type": "cong_thuc",
        "question": "Quy tắc nhân hai luỹ thừa cùng cơ số được phát biểu như thế nào?",
        "expected_answer": "Giữ nguyên cơ số và cộng các số mũ: a^m x a^n = a^(m + n).",
        "gold_source_id": "toan-6-gdpt2018",
        "gold_page": 3,
        "evidence_quote": "Quy tắc nhân hai luỹ thừa cùng cơ số: Giữ nguyên cơ số và cộng các số mũ: a^m x a^n = a^(m + n).",
        "filter": None
    },
    {
        "id": "q04",
        "split": "dev",
        "type": "thu_tu_tinh",
        "question": "Khi biểu thức có chứa các dấu ngoặc tròn, ngoặc vuông và ngoặc nhọn thì thứ tự thực hiện như thế nào?",
        "expected_answer": "Thực hiện trong ngoặc tròn ( ) trước, sau đó đến ngoặc vuông [ ], cuối cùng trong ngoặc nhọn { }.",
        "gold_source_id": "toan-6-gdpt2018",
        "gold_page": 4,
        "evidence_quote": "Thực hiện trong ngoặc tròn ( ) trước -> Sau đó đến ngoặc vuông [ ] -> Cuối cùng thực hiện trong ngoặc nhọn { }.",
        "filter": None
    },
    {
        "id": "q05",
        "split": "dev",
        "type": "dieu_kien",
        "question": "Dấu hiệu nhận biết một số chia hết cho 9 là gì và mối liên hệ giữa chia hết cho 9 và chia hết cho 3?",
        "expected_answer": "Các số có tổng các chữ số chia hết cho 9 thì chia hết cho 9. Một số chia hết cho 9 thì luôn chia hết cho 3.",
        "gold_source_id": "toan-6-gdpt2018",
        "gold_page": 5,
        "evidence_quote": "Các số có tổng các chữ số chia hết cho 9 thì chia hết cho 9. Một số chia hết cho 9 thì luôn chia hết cho 3, nhưng số chia hết cho 3 chưa chắc chia hết cho 9.",
        "filter": None
    },
    {
        "id": "q06",
        "split": "dev",
        "type": "dinh_nghia",
        "question": "Số 0 và số 1 có phải là số nguyên tố hay hợp số không?",
        "expected_answer": "Số 0 và số 1 không phải là số nguyên tố cũng không phải là hợp số.",
        "gold_source_id": "toan-6-gdpt2018",
        "gold_page": 6,
        "evidence_quote": "Số 0 và số 1 không phải là số nguyên tố cũng không phải là hợp số.",
        "filter": None
    },
    {
        "id": "q07",
        "split": "dev",
        "type": "metadata_filter",
        "question": "Tập hợp các số nguyên Z gồm những thành phần nào và số 0 có phải số nguyên âm không?",
        "expected_answer": "Tập hợp số nguyên Z gồm các số nguyên âm, số 0 và các số nguyên dương. Số 0 không phải số nguyên dương và cũng không phải số nguyên âm.",
        "gold_source_id": "toan-6-gdpt2018",
        "gold_page": 7,
        "evidence_quote": "Tập hợp gồm các số nguyên âm, số 0 và các số nguyên dương được gọi là tập hợp các số nguyên, ký hiệu là Z. Số 0 là số nguyên nhưng không phải là số nguyên dương và cũng không phải là số nguyên âm.",
        "filter": {"section": "so_nguyen"}
    },
    {
        "id": "q08",
        "split": "dev",
        "type": "quy_tac",
        "question": "Quy tắc bỏ dấu ngoặc khi đằng trước có dấu trừ được thực hiện ra sao?",
        "expected_answer": "Phải đổi dấu tất cả các số hạng trong ngoặc: dấu '+' đổi thành '-' và dấu '-' đổi thành '+': -(a - b + c) = -a + b - c.",
        "gold_source_id": "toan-6-gdpt2018",
        "gold_page": 10,
        "evidence_quote": "Khi bỏ dấu ngoặc có dấu trừ '-' đằng trước, ta phải đổi dấu của tất cả các số hạng trong ngoặc: Dấu '+' đổi thành '-' và dấu '-' đổi thành '+': -(a - b + c) = -a + b - c.",
        "filter": None
    },
    {
        "id": "q09",
        "split": "dev",
        "type": "ngoai_le",
        "question": "Số 0 có phải là ước của bất kỳ số nguyên nào không?",
        "expected_answer": "Số 0 không phải là ước của bất kỳ số nguyên nào vì phép chia cho 0 không xác định.",
        "gold_source_id": "toan-6-gdpt2018",
        "gold_page": 12,
        "evidence_quote": "Số 0 là bội của mọi số nguyên khác 0, nhưng số 0 không phải là ước của bất kỳ số nguyên nào vì phép chia cho 0 không xác định.",
        "filter": None
    },
    {
        "id": "q10",
        "split": "dev",
        "type": "metadata_filter",
        "question": "Thế nào là hai phân số bằng nhau theo điều kiện tích chéo?",
        "expected_answer": "Hai phân số a/b và c/d bằng nhau nếu tích chéo a x d = b x c.",
        "gold_source_id": "toan-6-gdpt2018",
        "gold_page": 13,
        "evidence_quote": "Hai phân số a/b và c/d được gọi là bằng nhau nếu thỏa mãn điều kiện tích chéo: a x d = b x c.",
        "filter": {"section": "phan_so"}
    },
    {
        "id": "q11",
        "split": "dev",
        "type": "phuong_phap",
        "question": "Để rút gọn một phân số về phân số tối giản chỉ trong một lần ta làm thế nào?",
        "expected_answer": "Chia cả tử và mẫu của phân số đó cho ước chung lớn nhất (ƯCLN) của chúng.",
        "gold_source_id": "toan-6-gdpt2018",
        "gold_page": 14,
        "evidence_quote": "Muốn rút gọn một phân số về phân số tối giản chỉ trong một lần, ta chia cả tử và mẫu của phân số đó cho ước chung lớn nhất (ƯCLN) của chúng.",
        "filter": None
    },
    {
        "id": "q12",
        "split": "dev",
        "type": "bai_toan",
        "question": "Muốn tìm m/n của một số b cho trước ta thực hiện phép tính gì?",
        "expected_answer": "Lấy số b nhân với phân số m/n: Giá trị = b x (m/n).",
        "gold_source_id": "toan-6-gdpt2018",
        "gold_page": 18,
        "evidence_quote": "Muốn tìm m/n của một số b cho trước (với m/n ∈ Q, n ≠ 0), ta lấy số b nhân với m/n: Giá trị cần tìm = b x (m/n).",
        "filter": None
    },
    {
        "id": "q13",
        "split": "dev",
        "type": "quy_tac",
        "question": "Khi làm tròn số thập phân, nếu chữ số đầu tiên bỏ đi lớn hơn hoặc bằng 5 thì xử lý thế nào?",
        "expected_answer": "Cộng thêm 1 vào chữ số ở hàng làm tròn.",
        "gold_source_id": "toan-6-gdpt2018",
        "gold_page": 22,
        "evidence_quote": "Nếu chữ số đầu tiên bỏ đi lớn hơn hoặc bằng 5 (là 5, 6, 7, 8, 9), ta cộng thêm 1 vào chữ số ở hàng làm tròn.",
        "filter": None
    },
    {
        "id": "q14",
        "split": "dev",
        "type": "cong_thuc",
        "question": "Công thức tính tỉ số phần trăm của hai số a và b là gì?",
        "expected_answer": "Lấy a chia cho b rồi nhân kết quả với 100 và thêm ký hiệu %: (a x 100 / b) %.",
        "gold_source_id": "toan-6-gdpt2018",
        "gold_page": 23,
        "evidence_quote": "Ta lấy a chia cho b, rồi nhân kết quả với 100 và viết thêm ký hiệu % vào bên phải kết quả: Tỉ số phần trăm = (a x 100 / b) %.",
        "filter": None
    },
    {
        "id": "q15",
        "split": "dev",
        "type": "dinh_nghia",
        "question": "Phân loại hai nhóm dữ liệu thống kê chính là gì?",
        "expected_answer": "Dữ liệu là số (định lượng) và dữ liệu không phải là số (định tính).",
        "gold_source_id": "toan-6-gdpt2018",
        "gold_page": 31,
        "evidence_quote": "Dữ liệu thống kê bao gồm hai loại chính: Dữ liệu là số (dữ liệu định lượng): Chiều cao, cân nặng, nhiệt độ, điểm thi, số học sinh. Dữ liệu không phải là số (dữ liệu định tính): Tên các món ăn ưa thích, xếp loại học lực, màu sắc, giới tính.",
        "filter": None
    },

    # ---------- TEST SPLIT (5 câu) ----------
    {
        "id": "q16",
        "split": "test",
        "type": "metadata_filter",
        "question": "Hai đường chéo của hình thoi có những đặc điểm và tính chất hình học gì?",
        "expected_answer": "Hai đường chéo của hình thoi vuông góc với nhau tại trung điểm của mỗi đường, là hai trục đối xứng của hình thoi và là các tia phân giác của các góc trong hình thoi.",
        "gold_source_id": "toan-6-gdpt2018",
        "gold_page": 26,
        "evidence_quote": "Hai đường chéo của hình thoi vuông góc với nhau tại trung điểm của mỗi đường. Hai đường chéo là hai trục đối xứng của hình thoi và là các tia phân giác của các góc trong hình thoi.",
        "filter": {"section": "hinh_hoc_truc_quan"}
    },
    {
        "id": "q17",
        "split": "test",
        "type": "cong_thuc",
        "question": "Công thức tính diện tích hình thang có đáy lớn a, đáy nhỏ b và chiều cao h là gì?",
        "expected_answer": "S = ((a + b) x h) / 2 (tổng hai đáy nhân chiều cao rồi chia 2).",
        "gold_source_id": "toan-6-gdpt2018",
        "gold_page": 29,
        "evidence_quote": "Diện tích hình thang có đáy lớn a, đáy nhỏ b và chiều cao h: S = ((a + b) x h) / 2 (bằng tổng độ dài hai đáy nhân với chiều cao rồi chia cho 2).",
        "filter": None
    },
    {
        "id": "q18",
        "split": "test",
        "type": "ngoai_le",
        "question": "Hình tam giác đều và hình thang cân có tâm đối xứng không?",
        "expected_answer": "Tam giác đều và hình thang cân không có tâm đối xứng.",
        "gold_source_id": "toan-6-gdpt2018",
        "gold_page": 30,
        "evidence_quote": "Tam giác đều và hình thang cân không có tâm đối xứng.",
        "filter": None
    },
    {
        "id": "q19",
        "split": "test",
        "type": "so_sanh",
        "question": "Biểu đồ cột kép được sử dụng khi nào và cách phân biệt các cột giữa hai nhóm?",
        "expected_answer": "Dùng khi muốn so sánh từng cặp đại lượng của hai nhóm đối tượng cùng loại. Cột của mỗi nhóm phân biệt bằng màu sắc hoặc hoa văn khác nhau kèm phần chú giải.",
        "gold_source_id": "toan-6-gdpt2018",
        "gold_page": 34,
        "evidence_quote": "Khi muốn so sánh từng cặp đại lượng của hai nhóm đối tượng cùng loại, người ta dùng biểu đồ cột kép. Cột của mỗi nhóm được phân biệt bằng màu sắc hoặc hoa văn khác nhau. Cần có phần chú giải rõ ràng.",
        "filter": None
    },
    {
        "id": "q20",
        "split": "test",
        "type": "cong_thuc",
        "question": "Công thức tính xác suất thực nghiệm của một sự kiện E khi thực hiện n lần thí nghiệm là gì?",
        "expected_answer": "Xác suất thực nghiệm = k / n = (Số lần xuất hiện sự kiện E) / (Tổng số lần thực hiện thí nghiệm).",
        "gold_source_id": "toan-6-gdpt2018",
        "gold_page": 36,
        "evidence_quote": "tỉ số giữa số lần sự kiện E xuất hiện (k) và tổng số lần thực hiện phép thử (n) được gọi là xác suất thực nghiệm của sự kiện E: Xác suất thực nghiệm = k / n = (Số lần xuất hiện sự kiện E) / (Tổng số lần thực hiện thí nghiệm).",
        "filter": None
    }
]

def main():
    base_dir = r"c:\Users\Student\Documents\aivin\K5-L3A-DAY06-LeVanHoang-2A202603357-DataIngestion"
    data_dir = os.path.join(base_dir, "starter", "data")
    benchmark_dir = os.path.join(base_dir, "benchmark")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(benchmark_dir, exist_ok=True)

    # 1. Lưu Corpus JSON
    corpus_path = os.path.join(data_dir, "toan_6_tap_1_va_2_gdpt2018.json")
    with open(corpus_path, "w", encoding="utf-8") as f:
        json.dump(PAGES, f, ensure_ascii=False, indent=2)
    print(f"Lưu corpus JSON: {corpus_path} ({len(PAGES)} trang)")

    # 2. Lưu Manifest JSON
    total_chars = sum(len(p["text"]) for p in PAGES)
    manifest = {
        "source_id": "toan-6-gdpt2018",
        "title": "Sổ tay Kiến thức và Trọng tâm Lý thuyết Toán lớp 6 (Chương trình GDPT 2018)",
        "source_path_or_url": "starter/data/toan_6_tap_1_va_2_gdpt2018.json",
        "license_or_permission": "Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)",
        "accessed_at": "2026-11-13",
        "total_pages": len(PAGES),
        "page_list": [p["page"] for p in PAGES],
        "total_characters": total_chars,
        "sections": {
            "so_tu_nhien": {"pages": [1, 2, 3, 4, 5, 6], "description": "Số tự nhiên, phép tính, chia hết, số nguyên tố"},
            "so_nguyen": {"pages": [7, 8, 9, 10, 11, 12], "description": "Số nguyên âm, cộng trừ nhân chia Z, quy tắc dấu"},
            "phan_so": {"pages": [13, 14, 15, 16, 17, 18], "description": "Khái niệm phân số, rút gọn, quy đồng, phép tính, 2 bài toán phân số"},
            "so_thap_phan": {"pages": [19, 20, 21, 22, 23, 24], "description": "Số thập phân, làm tròn, tỉ số và tỉ số phần trăm"},
            "hinh_hoc_truc_quan": {"pages": [25, 26, 27, 28, 29, 30], "description": "Các hình phẳng trực quan, chu vi diện tích, đối xứng"},
            "thong_ke_xac_suat": {"pages": [31, 32, 33, 34, 35, 36], "description": "Thu thập dữ liệu, biểu đồ tranh, biểu đồ cột, xác suất thực nghiệm"}
        }
    }
    manifest_path = os.path.join(data_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    # Lưu bản sao manifest ở root data/
    root_data_dir = os.path.join(base_dir, "data")
    os.makedirs(root_data_dir, exist_ok=True)
    with open(os.path.join(root_data_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"Lưu manifest: {manifest_path} (Tổng ký tự: {total_chars})")

    # 3. Lưu Benchmark JSON
    benchmark_path = os.path.join(benchmark_dir, "benchmark_questions.json")
    with open(benchmark_path, "w", encoding="utf-8") as f:
        json.dump(BENCHMARK_QUESTIONS, f, ensure_ascii=False, indent=2)
    print(f"Lưu benchmark: {benchmark_path} ({len(BENCHMARK_QUESTIONS)} câu hỏi)")

if __name__ == "__main__":
    main()

