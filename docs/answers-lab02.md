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
| Rebase | #8 | Các commit tuyến tính, SHA mới, không có merge commit |
