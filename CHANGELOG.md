# Changelog

Theo định dạng [Keep a Changelog](https://keepachangelog.com) và [Semantic Versioning](https://semver.org).

## [Unreleased]
### Added
- `Cart.sort_by_title()` và `Cart.sort_by_cost()` sắp xếp giỏ hàng.

## [1.0.0] - 2026-11-01
### Added
- `Cart.print_cart()` in giỏ hàng, báo "The cart is empty" khi giỏ trống.
- `search_by_title()` tìm đĩa theo tiêu đề.
- `Cart.total_cost_with_discount()` tính tổng tiền sau giảm giá, kiểm tra `percent` trong khoảng 0 đến 100.
- Thông báo thêm đĩa vào giỏ bằng tiếng Việt.
- Mẫu Pull Request, tài liệu use case và câu trả lời các lab.

### Changed
- Mã nguồn chuyển vào package `aims/`.

### Fixed
- Giỏ hàng nhận đĩa thứ 21 dù giới hạn là 20 (#10).
