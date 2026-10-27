# Trả lời câu hỏi thảo luận – Lab 01

## Câu hỏi nhanh: cấu hình `--global` được lưu ở đâu? Khác gì `--local`?

- `--global` lưu trong `~/.gitconfig` của người dùng và áp dụng cho mọi repo trên máy.
- `--local` lưu trong `.git/config` của từng repo và chỉ áp dụng cho repo đó.
- Khi trùng khoá, `--local` ghi đè `--global`. Có thể xem nguồn từng giá trị bằng `git config --list --show-origin`.

## 1. Vì sao dùng `git mv`?

`git mv a b` tương đương `mv a b` rồi `git add` cả đường dẫn cũ và mới: thao tác đổi tên được đưa thẳng vào staging, không cần thêm bước.

Git không lưu "sự kiện đổi tên" mà tự phát hiện bằng độ giống nhau của nội dung khi chạy `git diff` hoặc `git log`. Vì file được chuyển nguyên vẹn (similarity 100%), Git hiển thị `cart.py => aims/cart.py` là đổi tên, và `git log --follow -- aims/cart.py` vẫn truy ngược được lịch sử cũ. Nhờ đó, PR hiện "renamed" thay vì "xoá một file và thêm một file mới", reviewer dễ kiểm tra và lịch sử cấu hình không bị đứt.

Lưu ý: nên chuyển file trong một commit riêng, chưa sửa nội dung (việc sửa import để ở commit sau), để nội dung giống nhau và Git nhận ra đổi tên chắc chắn.

## 2. `release/lab01` có phải baseline không?

Một phần. Baseline là phiên bản đã được thống nhất, đã đi qua quy trình kiểm soát thay đổi, và dùng làm điểm tham chiếu để phát hành hoặc phát triển tiếp.

- Đúng một phần: `release/lab01` trỏ vào commit `84b2b53`, đã qua Pull Request (PR #1), chạy được (`Total cost: 63.89 $`) và là phiên bản dùng để nộp bài. Nó định danh được phiên bản nộp.
- Chưa đầy đủ: đây mới là nhánh, không phải tag. Nhánh có thể di chuyển khi có commit mới, nên chưa bất biến. Baseline chính thức cần được đánh dấu bằng annotated tag (như `v0.1.0` ở Lab 04) để định danh chính xác một phiên bản và không bao giờ di chuyển.

## 3. Vì sao không commit thẳng lên `master` dù làm một mình?

- **Kiểm soát thay đổi:** `master` là dòng ổn định. Mọi thay đổi đi qua PR có mô tả mục đích, thay đổi, cách kiểm thử, nên có hồ sơ vì sao mỗi thay đổi tồn tại.
- **Truy vết:** nhánh có tên nêu mục đích (`refactor/...`) và PR gom các commit liên quan, giúp đọc lịch sử và liên kết với Issue về sau.
- **An toàn:** thay đổi sai chỉ nằm trên nhánh, `master` vẫn chạy được. Có thể tự xem lại diff ở tab Files changed trước khi merge.
- **Thói quen và công cụ:** quy trình giống khi làm nhóm, nên khi có người cùng làm hoặc khi bật branch protection (Lab 02) và CI (Lab 05) thì không phải đổi cách làm.
