import json
import csv
import os
from typing import List, Dict
import matplotlib.pyplot as plt

DATA_CSV = "data.csv"
DATA_JSON = "data.json"
productList: List[Dict] = []


def calculate_gia_tri_ton(gia_ban: int, so_luong: int) -> int:
    """Tính giá trị tồn kho"""
    return gia_ban * so_luong


def calculate_trang_thai(so_luong: int) -> str:
    """Tính trạng thái sản phẩm"""
    if so_luong <= 5:
        return "Cần nhập"
    elif so_luong > 50:
        return "Khó bán"
    else:
        return "Bình thường"


def loadData():
    """Tải dữ liệu từ file CSV hoặc JSON"""
    global productList
    if os.path.exists(DATA_CSV):
        try:
            with open(DATA_CSV, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                productList = []
                for row in reader:
                    productList.append({
                        'masp': row['masp'],
                        'ten_sp': row['ten_sp'],
                        'gia_ban': int(row['gia_ban']),
                        'so_luong': int(row['so_luong']),
                        'gia_tri_ton': int(row['gia_tri_ton']),
                        'trang_thai': row['trang_thai']
                    })
                print(
                    f"Đã tải {len(productList)} sản phẩm từ file {DATA_CSV}")
                return
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu từ CSV: {e}")

    if os.path.exists(DATA_JSON):
        try:
            with open(DATA_JSON, mode="r", encoding="utf-8") as file:
                productList = json.load(file)
                print(
                    f"Đã tải {len(productList)} sản phẩm từ file {DATA_JSON}")
                return
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu từ JSON: {e}")

    productList = []
    print("Không tìm thấy file dữ liệu. Bắt đầu với danh sách trống.")


def displayProductLists():
    """Chức năng hiển thị danh sách sản phẩm dạng bảng"""
    if not productList:
        print("\nDanh sách sản phẩm trống!")
        return

    print("\n" + "="*110)
    print(f"{'STT':<5} {'Mã SP':<12} {'Tên SP':<30} {'Giá bán':<12} "
          f"{'Số lượng':<12} {'Giá trị tồn':<15} {'Trạng thái':<15}")
    print("-"*110)

    for idx, product in enumerate(productList, 1):
        print(
            f"{idx:<5} {product['masp']:<12} {product['ten_sp']:<30} "
            f"{product['gia_ban']:<12,} {product['so_luong']:<12} "
            f"{product['gia_tri_ton']:<15,} {product['trang_thai']:<15}"
        )

    print("="*110)
    print(f"\nTổng cộng: {len(productList)} sản phẩm")


def addProduct():
    """Thêm mới sản phẩm"""
    print("\n=== THÊM MỚI SẢN PHẨM ===")

    masp = input("Nhập Mã SP: ").strip()
    if not masp:
        print("Mã SP không được để trống!")
        return

    for product in productList:
        if product['masp'] == masp:
            print(f"Mã SP '{masp}' đã tồn tại! Vui lòng nhập mã khác.")
            return

    ten_sp = input("Nhập Tên SP: ").strip()
    if not ten_sp:
        print("Tên SP không được để trống!")
        return

    try:
        gia_ban = int(input("Nhập Giá bán: ").strip())
        if gia_ban <= 0:
            print("Giá bán phải lớn hơn 0!")
            return
    except ValueError:
        print("Giá bán phải là số nguyên dương!")
        return

    try:
        so_luong = int(input("Nhập Số lượng: ").strip())
        if so_luong <= 0:
            print("Số lượng phải lớn hơn 0!")
            return
    except ValueError:
        print("Số lượng phải là số nguyên dương!")
        return

    gia_tri_ton = calculate_gia_tri_ton(gia_ban, so_luong)
    trang_thai = calculate_trang_thai(so_luong)

    new_product = {
        'masp': masp,
        'ten_sp': ten_sp,
        'gia_ban': gia_ban,
        'so_luong': so_luong,
        'gia_tri_ton': gia_tri_ton,
        'trang_thai': trang_thai
    }
    productList.append(new_product)
    print(f"\nĐã thêm sản phẩm '{ten_sp}' thành công!")


def updateProduct():
    """Cập nhật sản phẩm"""
    print("\n=== CẬP NHẬT SẢN PHẨM ===")

    if not productList:
        print("Danh sách sản phẩm trống!")
        return

    masp = input("Nhập Mã SP cần cập nhật: ").strip()

    product = None
    for p in productList:
        if p['masp'] == masp:
            product = p
            break

    if not product:
        print(f"Không tìm thấy sản phẩm với mã '{masp}'!")
        return

    print("\nThông tin hiện tại:")
    print(f"  Mã SP: {product['masp']}")
    print(f"  Tên SP: {product['ten_sp']}")
    print(f"  Giá bán: {product['gia_ban']:,}")
    print(f"  Số lượng: {product['so_luong']}")
    print(f"  Giá trị tồn: {product['gia_tri_ton']:,}")
    print(f"  Trạng thái: {product['trang_thai']}")

    try:
        gia_ban_str = input(
            "\nNhập Giá bán mới (Enter để giữ nguyên): ").strip()
        if gia_ban_str:
            gia_ban = int(gia_ban_str)
            if gia_ban <= 0:
                print("Giá bán phải lớn hơn 0!")
                return
            product['gia_ban'] = gia_ban
    except ValueError:
        print("Giá bán phải là số nguyên dương!")
        return

    try:
        so_luong_str = input(
            "Nhập Số lượng mới (Enter để giữ nguyên): ").strip()
        if so_luong_str:
            so_luong = int(so_luong_str)
            if so_luong <= 0:
                print("Số lượng phải lớn hơn 0!")
                return
            product['so_luong'] = so_luong
    except ValueError:
        print("Số lượng phải là số nguyên dương!")
        return

    product['gia_tri_ton'] = calculate_gia_tri_ton(
        product['gia_ban'], product['so_luong'])
    product['trang_thai'] = calculate_trang_thai(product['so_luong'])

    print(f"\nĐã cập nhật sản phẩm '{product['ten_sp']}' thành công!")


def deleteProduct():
    """Xóa sản phẩm"""
    print("\n=== XÓA SẢN PHẨM ===")

    if not productList:
        print("Danh sách sản phẩm trống!")
        return

    masp = input("Nhập Mã SP cần xóa: ").strip()

    product = None
    for p in productList:
        if p['masp'] == masp:
            product = p
            break

    if not product:
        print(f"Không tìm thấy sản phẩm với mã '{masp}'!")
        return

    print("\nThông tin sản phẩm cần xóa:")
    print(f"  Mã SP: {product['masp']}")
    print(f"  Tên SP: {product['ten_sp']}")
    print(f"  Giá bán: {product['gia_ban']:,}")
    print(f"  Số lượng: {product['so_luong']}")

    confirm = input("\nBạn có chắc muốn xóa? (yes/no): ").strip().lower()
    if confirm in ['yes', 'y', 'có', 'co']:
        productList.remove(product)
        print(f"Đã xóa sản phẩm '{product['ten_sp']}' thành công!")
    else:
        print("Đã hủy thao tác xóa.")


def searchProduct():
    """Tìm kiếm sản phẩm"""
    print("\n=== TÌM KIẾM SẢN PHẨM ===")

    if not productList:
        print("Danh sách sản phẩm trống!")
        return

    keyword = input("Nhập từ khóa tìm kiếm (Mã SP hoặc Tên SP): ").strip()

    if not keyword:
        print("Từ khóa không được để trống!")
        return

    results = []
    for product in productList:
        if (keyword.lower() in product['masp'].lower() or
                keyword.lower() in product['ten_sp'].lower()):
            results.append(product)

    if not results:
        print(f"\nKhông tìm thấy sản phẩm nào với từ khóa '{keyword}'!")
        return

    print(f"\nTìm thấy {len(results)} sản phẩm:")
    print("="*110)
    print(f"{'STT':<5} {'Mã SP':<12} {'Tên SP':<30} {'Giá bán':<12} "
          f"{'Số lượng':<12} {'Giá trị tồn':<15} {'Trạng thái':<15}")
    print("-"*110)

    for idx, product in enumerate(results, 1):
        print(
            f"{idx:<5} {product['masp']:<12} {product['ten_sp']:<30} "
            f"{product['gia_ban']:<12,} {product['so_luong']:<12} "
            f"{product['gia_tri_ton']:<15,} {product['trang_thai']:<15}"
        )
    print("="*110)


def sortProductList():
    """Sắp xếp danh sách sản phẩm"""
    print("\n=== SẮP XẾP DANH SÁCH SẢN PHẨM ===")

    if not productList:
        print("Danh sách sản phẩm trống!")
        return

    print("1. Sắp xếp theo Giá bán tăng dần")
    print("2. Sắp xếp theo Giá trị tồn giảm dần")

    choice = input("Chọn cách sắp xếp (1 hoặc 2): ").strip()

    if choice == "1":
        productList.sort(key=lambda x: x['gia_ban'])
        print("\nĐã sắp xếp theo Giá bán tăng dần!")
    elif choice == "2":
        productList.sort(key=lambda x: x['gia_tri_ton'], reverse=True)
        print("\nĐã sắp xếp theo Giá trị tồn giảm dần!")
    else:
        print("Lựa chọn không hợp lệ!")
        return

    displayProductLists()


def statisticsProduct():
    """Thống kê điểm kho hàng"""
    print("\n=== THỐNG KÊ ĐIỂM KHO HÀNG ===")

    if not productList:
        print("Danh sách sản phẩm trống!")
        return

    can_nhap = sum(1 for p in productList if p['trang_thai'] == "Cần nhập")
    binh_thuong = sum(
        1 for p in productList if p['trang_thai'] == "Bình thường")
    kho_ban = sum(1 for p in productList if p['trang_thai'] == "Khó bán")

    print("\nSố lượng sản phẩm theo trạng thái:")
    print(f"  Cần nhập: {can_nhap} sản phẩm")
    print(f"  Bình thường: {binh_thuong} sản phẩm")
    print(f"  Khó bán: {kho_ban} sản phẩm")
    print(f"\nTổng cộng: {len(productList)} sản phẩm")

    return {
        'Cần nhập': can_nhap,
        'Bình thường': binh_thuong,
        'Khó bán': kho_ban
    }


def drawPieChart():
    """Vẽ biểu đồ hình tròn thống kê kho hàng"""
    print("\n=== VẼ BIỂU ĐỒ THỐNG KÊ ===")

    if not productList:
        print("Danh sách sản phẩm trống!")
        return

    stats = statisticsProduct()

    labels = []
    sizes = []
    colors = ['#ff9999', '#66b3ff', '#99ff99']

    for label, count in stats.items():
        if count > 0:
            labels.append(f"{label}\n({count} sản phẩm)")
            sizes.append(count)

    if not sizes:
        print("Không có dữ liệu để vẽ biểu đồ!")
        return

    plt.figure(figsize=(10, 8))
    plt.pie(sizes, labels=labels, colors=colors[:len(sizes)],
            autopct='%1.1f%%',
            startangle=90, textprops={'fontsize': 12})
    plt.title('Thống kê trạng thái kho hàng',
              fontsize=16, fontweight='bold', pad=20)
    plt.axis('equal')

    plt.savefig('thong_ke_kho_hang.png', dpi=300, bbox_inches='tight')
    print("\nĐã vẽ và lưu biểu đồ vào file 'thong_ke_kho_hang.png'")
    plt.show()


def saveToFile():
    """Lưu dữ liệu vào file CSV hoặc JSON"""
    print("\n=== LƯU DỮ LIỆU ===")

    if not productList:
        print("Danh sách sản phẩm trống, không có gì để lưu!")
        return

    print("1. Lưu vào file CSV")
    print("2. Lưu vào file JSON")

    choice = input("Chọn định dạng (1 hoặc 2): ").strip()

    if choice == "1":
        try:
            with open(DATA_CSV, mode="w", encoding="utf-8",
                      newline='') as file:
                fieldnames = ['masp', 'ten_sp', 'gia_ban',
                              'so_luong', 'gia_tri_ton', 'trang_thai']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(productList)
            print(
                f"Đã lưu {len(productList)} sản phẩm " +
                f" vào file {DATA_CSV} thành công!")
        except Exception as e:
            print(f"Lỗi khi lưu file CSV: {e}")

    elif choice == "2":
        try:
            with open(DATA_JSON, mode="w", encoding="utf-8") as file:
                json.dump(productList, file, ensure_ascii=False, indent=2)
            print(
                f"Đã lưu {len(productList)} sản phẩm " +
                f"vào file {DATA_JSON} thành công!")
        except Exception as e:
            print(f"Lỗi khi lưu file JSON: {e}")
    else:
        print("Lựa chọn không hợp lệ!")


def menu():
    print("\n" + "="*50)
    print("QUẢN LÝ SẢN PHẨM")
    print("="*50)
    print("1. Hiển thị danh sách sản phẩm")
    print("2. Thêm mới sản phẩm")
    print("3. Cập nhật thông tin sản phẩm")
    print("4. Xóa sản phẩm")
    print("5. Tìm kiếm sản phẩm")
    print("6. Sắp xếp danh sách sản phẩm")
    print("7. Thống kê điểm kho hàng")
    print("8. Vẽ biểu đồ thống kê kho hàng")
    print("9. Lưu vào file CSV/JSON")
    print("10. Thoát")
    print("="*50)


def main():
    loadData()
    while True:
        menu()
        choice = input("Vui lòng nhập lựa chọn của bạn: ").strip()

        match choice:
            case "1":
                displayProductLists()
            case "2":
                addProduct()
            case "3":
                updateProduct()
            case "4":
                deleteProduct()
            case "5":
                searchProduct()
            case "6":
                sortProductList()
            case "7":
                statisticsProduct()
            case "8":
                drawPieChart()
            case "9":
                saveToFile()
            case "10":
                if productList:
                    print("\nĐang lưu dữ liệu trước khi thoát...")
                    try:
                        if os.path.exists(DATA_CSV):
                            with open(DATA_CSV, mode="w", encoding="utf-8",
                                      newline='') as file:
                                fieldnames = ['masp', 'ten_sp', 'gia_ban',
                                              'so_luong', 'gia_tri_ton',
                                              'trang_thai']
                                writer = csv.DictWriter(
                                    file, fieldnames=fieldnames)
                                writer.writeheader()
                                writer.writerows(productList)
                            print(f"Đã tự động lưu vào {DATA_CSV}")
                        else:
                            with open(DATA_JSON, mode="w",
                                      encoding="utf-8") as file:
                                json.dump(productList, file,
                                          ensure_ascii=False, indent=2)
                            print(f"Đã tự động lưu vào {DATA_JSON}")
                    except Exception as e:
                        print(f"Lỗi khi lưu dữ liệu: {e}")
                print("\nCảm ơn bạn đã sử dụng chương trình!")
                break
            case _:
                print("Lựa chọn không hợp lệ. Vui lòng nhập lại!")


if __name__ == "__main__":
    main()
