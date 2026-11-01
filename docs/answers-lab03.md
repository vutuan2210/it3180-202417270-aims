# Trả lời câu hỏi thảo luận – Lab 03

## 1. Merge base là gì?

Merge base là **commit tổ tiên chung gần nhất** của hai nhánh sắp được hợp nhất. Có thể xem bằng `git merge-base A B`.

Git dùng ba phiên bản để hợp nhất (3-way merge): merge base, đầu nhánh hiện tại ("ours") và đầu nhánh được gộp vào ("theirs"). Với mỗi vùng mã, Git so sánh từng nhánh với merge base:

- Chỉ một nhánh thay đổi vùng đó: lấy bản đã thay đổi, tự động.
- Cả hai nhánh cùng thay đổi vùng đó theo cách khác nhau: **xung đột**, Git đánh dấu `<<<<<<<`, `=======`, `>>>>>>>` để người dùng quyết định.

Ví dụ trong lab: `feature/vietnamese-messages` và `feature/show-added-title` cùng tách từ `master` (`4da7324`, merge base) và cùng sửa dòng `print("The disc has been added")`. Hai nhánh cùng khác merge base ở một dòng nên không tự gộp được.

## 2. Vì sao `master` và `release/*` phải dùng `revert`?

`reset` viết lại lịch sử bằng cách dời con trỏ nhánh về sau. Với nhánh dùng chung thì không chấp nhận được vì:

- **Phải force push** để đẩy lịch sử mới lên remote. Repo đã bật rule chặn `non_fast_forward`, và force push có thể ghi đè công việc của người khác.
- **Làm lệch bản sao của mọi người:** ai đã `pull` lịch sử cũ sẽ có commit mà remote không còn, dễ gây xung đột và mất đồng bộ.
- **Phá vỡ tham chiếu:** tag, baseline, PR và Issue đang trỏ vào các SHA cũ. `release/*` là bản đã phát hành nên càng không được đổi.
- **Mất dấu vết kiểm toán:** SCM cần biết thay đổi nào đã xảy ra, ai hoàn tác và vì sao.

`revert` tạo **commit mới** đảo ngược nội dung của commit cũ. Lịch sử chỉ tăng thêm, không bị sửa, nên an toàn cho nhánh chung và đi qua PR như mọi thay đổi khác. Với merge commit, phải thêm `-m 1` để chỉ định nhánh cha cần giữ (`master`).

| | `reset` | `revert` |
|---|---|---|
| Viết lại lịch sử | Có (dời con trỏ nhánh) | Không (thêm commit đảo ngược) |
| Dùng cho | Commit chưa push | `master`, `release/*` |

## Ghi chú thực hiện

### Các PR của Lab 03

| PR | Nhánh | Nội dung | Base |
|---|---|---|---|
| #11 | `bugfix/cart-limit-off-by-one` | Test tái hiện lỗi (FAIL) rồi sửa `>` thành `>=` (PASS), `Fixes #10` | `master` |
| #12 | `bugfix/discount-calculation` | Sửa `total_cost_with_discount` và kiểm tra `percent` | `feature/discount` |
| #13 | `feature/discount` | Thêm `total_cost_with_discount` (đã gồm bản sửa) | `master` |
| #14 | `feature/vietnamese-messages` | Thông báo thêm đĩa bằng tiếng Việt (Dev 1) | `master` |
| #15 | `feature/show-added-title` | Thêm tên đĩa vào thông báo; có xung đột với #14, giải quyết bằng merge | `master` |
| #16 | `bugfix/revert-show-added-title` | `git revert -m 1` hoàn tác merge của #15 | `master` |

### Truy vết thay đổi
Issue #10 được liên kết qua chuỗi: Issue #10, nhánh `bugfix/cart-limit-off-by-one`, commit `fix: ...` kèm `Fixes #10`, PR #11, rồi Issue tự động đóng khi PR merge vào `master`. Commit test (`test: reproduce cart limit bug (#10)`) nằm trước commit fix, và test đã FAIL (`True is not false`) trước khi sửa nên trở thành regression test.

### Xung đột
Dev 1 merge trước (#14). Với #15 của Dev 2, GitHub báo conflict. Giải quyết ở máy bằng `git merge origin/master`, kết hợp ý của cả hai dòng thành `print(f"Đã thêm đĩa '{dvd.title}' vào giỏ hàng")`, chạy test, rồi commit và push. Không còn dấu xung đột trong mã.

### Hoàn tác
Trên nhánh nháp `topic/undo-practice` (không push) đã thử `reset --soft` (về staging), `--mixed` (về working dir) và `--hard` (xoá thay đổi). Dùng `git reflog` để tìm lại commit `d498ff3` bị mất và khôi phục bằng `git reset --hard`. Với lịch sử chung, dùng `revert -m 1` qua PR #16.

### Lưu ý khi chạy
- Dòng tiếng Việt trong `print` gây `UnicodeEncodeError` trên console Windows (mã `cp1252`) khi chạy `python main.py` mà chưa đặt `PYTHONIOENCODING=utf-8`.
- Hiện có 3 test (`test_add_dvd_until_full`, `test_total_cost_with_discount`, `test_discount_percent_out_of_range`), ít hơn "4 tests OK" trong slide. Số test phụ thuộc cách cài đặt.
