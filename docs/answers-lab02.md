# Trả lời câu hỏi thảo luận – Lab 02

## 1. Vì sao phải đồng bộ `master` trước khi gửi PR?

Nhánh được tách từ `master` ở một thời điểm cũ, trong khi `master` tiếp tục nhận PR khác. Nếu không đồng bộ:

- PR có thể xung đột với `master` mới, và GitHub báo "This branch has conflicts" ngay lúc review.
- Kiểm thử trên nhánh chỉ chứng minh mã chạy được trên bản `master` cũ. Khi hai thay đổi riêng lẻ đều đúng nhưng ghép lại sai, lỗi chỉ lộ ra sau khi merge.

Ví dụ trong lab: nhánh `feature/search-by-title` tách khi `master` chưa có `print_cart`. Trước khi gửi PR, ta `git fetch`, `git merge origin/master`, chạy `python main.py` để kiểm tra tích hợp rồi mới push. Người chịu trách nhiệm xử lý xung đột và kiểm thử là tác giả nhánh, không phải reviewer. Điều này cũng giữ nguyên tắc nhánh sống ngắn, càng gần `master` càng tốt.

## 2. Khi nào không nên dùng rebase?

- **Commit đã được chia sẻ:** nhánh đã push và người khác đã checkout, hoặc đã được review. Rebase viết lại SHA, nên người khác bị lệch lịch sử và phải dùng `push --force`, có thể ghi đè công việc của họ.
- **Nhánh dài hạn như `master` và `release/*`:** không bao giờ rebase, vì mọi tham chiếu (tag, PR, baseline) trỏ vào các SHA này.
- **Khi cần giữ bằng chứng về thời điểm merge:** merge commit cho biết nhánh nào được đưa vào, lúc nào, và có thể revert cả tính năng bằng `git revert -m 1`. Rebase làm mất thông tin đó.
- **Khi có nhiều xung đột:** rebase phải giải quyết xung đột lần lượt ở từng commit; merge chỉ giải một lần.

Quy tắc chung của Release Flow: chỉ viết lại lịch sử (amend, reset, rebase) trên commit chưa chia sẻ.

## 3. `feature/*` khác `topic/*` ra sao?

- `feature/*` dành cho tính năng mới có giá trị với người dùng, hiện trong CHANGELOG mục Added. Ví dụ `feature/cart-print`, `feature/search-by-title`.
- `topic/*` dành cho thay đổi hỗ trợ: tài liệu, cấu hình, tệp quy trình, không đổi hành vi sản phẩm. Ví dụ `topic/pr-template`, `topic/use-case-diagram`.

Cả hai đều tách từ `master` và merge về `master` qua PR. Sự khác nhau nằm ở mục đích, nên tên nhánh cho reviewer biết cần kiểm tra điều gì: feature cần review hành vi và test, topic chủ yếu cần review nội dung.

## So sánh ba kiểu merge (từ lịch sử repo)

| Kiểu | PR trong lab | Dấu hiệu trong `git log --graph` |
|---|---|---|
| Merge commit | #4, #5, #6 | Có nhánh phụ và dòng `Merge pull request #N` |
| Squash | #7 | Một commit duy nhất `feat: add search_by_title (#7).` |
| Rebase | PR của `topic/readme-usage` | Các commit tuyến tính, SHA mới, không có merge commit |

## Ghi chú thực hiện

### Các PR đã merge

| PR | Nhánh | Mục đích | Kiểu merge |
|---|---|---|---|
| #4 | `topic/pr-template` | Thêm `.github/pull_request_template.md` | Merge commit |
| #5 | `feature/cart-print` | Thêm `Cart.print_cart()`, có vòng review và sửa | Merge commit |
| #6 | `topic/use-case-diagram` | Thêm `docs/use-case.md` | Merge commit |
| #7 | `feature/search-by-title` | Thêm `aims/search.py` (`search_by_title`), nhánh Dev 2 | Squash |
| (sau #7) | `topic/readme-usage` | Bổ sung mục cách dùng vào README (2 commit) | Rebase |

### Môi trường và cách làm
- Làm một mình, không có partner. Branch protection cho `master` đặt Require a pull request, Required approvals = 0, bật Dismiss stale approvals, cấm xoá nhánh và cấm force push.
- Mô phỏng hai lập trình viên bằng hai bản clone: `aims` (Dev 1) và `aims-dev2` (Dev 2).
- Nhánh Dev 2 được tách từ `master` cũ (chưa có `print_cart`). Trước khi gửi PR, nhánh được đồng bộ bằng `git merge origin/master`, chạy lại `python main.py`, rồi mới push.
- Sau khi squash hoặc rebase, `git branch -d` báo `not fully merged`. Sau khi xác nhận PR đã merged, dùng `git branch -D` để xoá nhánh ở máy.

### Hạn chế so với yêu cầu bài lab
- Không có reviewer thứ hai, nên PR `cart-print` chỉ có review loại **Comment** (tác giả không tự Request changes hay Approve được trên PR của chính mình). Vòng "yêu cầu sửa, sửa tiếp trên cùng nhánh, PR tự cập nhật" vẫn được thực hiện: comment ở dòng `def print_cart`, sau đó commit `feat: handle empty cart in print_cart`.
- Do đó PR `cart-print` không có trạng thái Changes requested rồi Approved như checklist.

### Sự cố gặp phải
- Lúc đầu, rule bảo vệ `master` chưa có hiệu lực (chưa Active nên không chặn push). Một commit rỗng `test: verify master protection` đã được đẩy thẳng lên `master`. Sau khi sửa ruleset, API `rules/branches/master` xác nhận các rule `pull_request`, `deletion`, `non_fast_forward` đã áp dụng. Commit rỗng này không đổi nội dung nhưng vẫn nằm trong lịch sử, và không bị ghi đè vì force push bị cấm.
- Khi merge PR, GitHub báo `Could not delete head ref` do nhánh đã được tự xoá (đã bật Automatically delete head branches). Đây không phải lỗi thật; PR vẫn merge thành công.
