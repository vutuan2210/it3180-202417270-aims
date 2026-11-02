def search_by_category(items, category):
    """Trả về các đĩa thuộc thể loại category (không phân biệt hoa thường)."""
    return [dvd for dvd in items if dvd.category.lower() == category.lower()]


def search_by_title(items, keyword):
    """Trả về các đĩa có tiêu đề chứa keyword."""
    return [dvd for dvd in items if keyword.lower() in dvd.title.lower()]
