# Use case – AIMS-mini

## Biểu đồ

```mermaid
flowchart LR
    Customer((Khách hàng))
    Customer --> UC1[Thêm đĩa DVD vào giỏ]
    Customer --> UC2[Xoá đĩa DVD khỏi giỏ]
    Customer --> UC3[Xem giỏ hàng]
    Customer --> UC4[Tìm đĩa theo tiêu đề]
    UC3 -. include .-> UC5[Tính tổng tiền]
```

## Mô tả

| Use case | Mô tả | Ghi chú |
|---|---|---|
| Thêm đĩa DVD vào giỏ | Khách thêm một đĩa vào giỏ hàng | Giỏ chứa tối đa 20 đĩa |
| Xoá đĩa DVD khỏi giỏ | Khách bỏ một đĩa khỏi giỏ | Báo nếu đĩa không có trong giỏ |
| Xem giỏ hàng | In danh sách đĩa và tổng tiền | `Cart.print_cart()` |
| Tìm đĩa theo tiêu đề | Lọc đĩa theo từ khoá | `search_by_title()` |
| Tính tổng tiền | Cộng giá các đĩa trong giỏ | `Cart.total_cost()` |
