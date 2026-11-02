# Trả lời câu hỏi thảo luận – Lab 04

## Vì sao chuẩn bị phát hành trên `master` trước, không sửa trên nhánh release?

Nhánh `release/*` bị khoá (bắt buộc PR, cấm force push, cấm xoá) và chỉ nhận thay đổi theo một chiều. Nếu nâng version và viết CHANGELOG trực tiếp trên release thì `master` không có các thay đổi đó, và bản phát hành sau sẽ "quên" chúng. Chuẩn bị trên `master` qua PR (`topic/prepare-release-1.0.0`) rồi mới cắt `release/lab04` bảo đảm `master` luôn là nguồn chính xác, còn release chỉ là bản sao tại thời điểm cắt.

## 1. Vì sao `release/*` không bao giờ merge ngược vào `master`?

- `master` đã đi tiếp: sau khi cắt release, `master` nhận thêm tính năng (ví dụ `sort_by_title`, `sort_by_cost`), còn release chỉ nhận sửa lỗi. Merge ngược sẽ trộn hai dòng phát triển và dễ gây xung đột.
- Release chứa những commit chỉ đúng cho riêng nó, như nâng version `1.0.1` ở hotfix. Đưa chúng về `master` có thể đặt lại số phiên bản sai hoặc đè lên `[Unreleased]` trong CHANGELOG.
- Dòng chảy một chiều làm lịch sử dễ đọc: `master` là nơi phát triển, `release/*` là nơi bảo trì. Bản sửa lỗi cần có ở cả hai nơi thì được đưa qua bằng `cherry-pick -x` để truy được nguồn gốc (Lab 05), không merge cả nhánh.

## 2. So sánh với GitFlow

| | Release Flow (học phần) | GitFlow |
|---|---|---|
| Nhánh dài hạn | Chỉ `master` (cộng các `release/*` khi cắt) | `main` và `develop` luôn tồn tại |
| Cắt release | Từ `master` | Từ `develop` |
| Kết thúc release | Giữ nhánh để bảo trì, không merge ngược | Merge vào `main` (gắn tag) và vào `develop` |
| Hotfix | Từ `release/*`, rồi cherry-pick về `master` | Từ `main`, merge vào `main` và `develop` |
| Độ phức tạp | Ít nhánh, không phải merge hai chiều | Nhiều nhánh, phải nhớ merge về hai nơi |

Release Flow gọn hơn vì chỉ có một dòng phát triển, hợp với nhóm nhỏ và phát hành thường xuyên. GitFlow hợp với sản phẩm phát hành theo chu kỳ dài, cần nhiều giai đoạn ổn định, nhưng dễ sai sót khi quên merge một chiều và tốn công đồng bộ `main` với `develop`.

## 3. Vì sao lên 1.0.0 mà không phải 0.4.0?

Theo Semantic Versioning, `0.y.z` nghĩa là giai đoạn phát triển ban đầu: API có thể thay đổi bất cứ lúc nào, chưa cam kết ổn định. `1.0.0` là cam kết: bản đầu tiên được coi là ổn định để giao cho người dùng, từ đó thay đổi phải tuân quy ước (MAJOR cho thay đổi phá vỡ, MINOR cho tính năng tương thích, PATCH cho sửa lỗi).

Ba bài đầu (`v0.1.0`, `v0.2.0`, `v0.3.0`) là các bước làm quen, còn bản lab 04 đã có: package `aims/` rõ ràng, test, CHANGELOG, bảo vệ nhánh và có đủ chức năng giỏ hàng, tìm kiếm, giảm giá. Đó là điểm có thể gọi là bản phát hành chính thức, nên đánh số 1.0.0. Đánh 0.4.0 sẽ báo hiệu rằng sản phẩm vẫn chưa ổn định.

## Ghi chú thực hiện

### Các bước đã làm
| Phần | Việc | Kết quả |
|---|---|---|
| A | `topic/prepare-release-1.0.0`: nâng version, thêm CHANGELOG | Đã merge qua PR #18 |
| B | Tạo `release/lab04` từ `master`; bảo vệ `release/**` bằng ruleset | Đã áp dụng |
| C | Gắn tag annotated cho 4 bản | Đã push |
| D | GitHub Release `v1.0.0` | Đã publish |
| E | Phát triển tiếp `feature/sort-cart` trên `master` | Đã merge qua PR #19, không ảnh hưởng release |
| F | Status accounting | Xem bên dưới |
| G | Tái tạo phiên bản cũ và kiểm toán | Xem bên dưới |

### Tag

| Tag | Commit | Nhánh |
|---|---|---|
| `v0.1.0` | `c3c366f` | `release/lab01` |
| `v0.2.0` | `25f23a1` | `release/lab02` |
| `v0.3.0` | `6d21289` | `release/lab03` |
| `v1.0.0` | `76d6af4` | `release/lab04` |

### Status accounting (Phần F)
- `git log release/lab04..master`: hai commit sort-cart (`0333636` và merge `09adefd`), tức `master` đi trước release.
- `git log master..release/lab04`: rỗng, release không có gì mà `master` thiếu.
- `git describe --tags`: `v1.0.0-2-g09adefd`.
- `git diff --stat v0.3.0 v1.0.0`: 3 file (`CHANGELOG.md`, `aims/__init__.py`, `main.py`). `git diff --stat v1.0.0 master`: 3 file (`CHANGELOG.md`, `aims/cart.py`, `tests/test_cart.py`).

### Kiểm toán v1.0.0 (Phần G)
- Dựng lại bằng `git worktree add ../aims-v1.0.0 v1.0.0`: in `AIMS-mini v1.0.0`, 3 test OK, và không có `sort_by_title`.
- Đóng gói bằng `git archive` thành `aims-1.0.0.zip` (15 file).
- `git show v1.0.0:aims/__init__.py` cho `__version__ = "1.0.0"`; `git ls-tree` của tag không có `__pycache__`, `.pyc` hay `.zip`.
- Bản `v0.2.0` ở trạng thái detached HEAD vẫn chạy được (`Total cost: 63.89 $`).

### Lưu ý
- Trang GitHub Release hiển thị target là `master` thay vì `release/lab04` vì tag `v1.0.0` đã tồn tại. Hai nhánh cùng trỏ `76d6af4` nên nội dung không đổi.
- File này được đưa vào `master` qua PR trước, sau đó đưa sang `release/lab04` bằng `cherry-pick -x` qua một PR có base là `release/lab04` (nhánh được bảo vệ). Tag `v1.0.0` vẫn ở commit cũ.
