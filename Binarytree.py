import sys
import random
import matplotlib.pyplot as plt
import networkx as nx
from PyQt5 import QtWidgets, QtGui, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from collections import deque


# Định nghĩa lớp Node cho các loại cây
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key
        self.height = 1  # Chiều cao chỉ dùng cho AVL

# Các hàm chèn nút theo quy tắc của từng loại cây
def insert_binary(root, key):
    if root is None:
        return Node(key)
    else:
        if random.choice([True, False]):
            root.left = insert_binary(root.left, key)
        else:
            root.right = insert_binary(root.right, key)
    return root

def insert_bst(root, key):
    if root is None:
        return Node(key)
    else:
        if key < root.val:
            root.left = insert_bst(root.left, key)
        else:
            root.right = insert_bst(root.right, key)
    return root

def get_height(node):
    if not node:
        return 0
    return node.height

def update_height(node):
    if node:
        node.height = 1 + max(get_height(node.left), get_height(node.right))

def get_balance(node):
    if not node:
        return 0
    return get_height(node.left) - get_height(node.right)

def rotate_right(y):
    x = y.left
    T2 = x.right
    x.right = y
    y.left = T2
    update_height(y)
    update_height(x)
    return x

def rotate_left(x):
    y = x.right
    T2 = y.left
    y.left = x
    x.right = T2
    update_height(x)
    update_height(y)
    return y

def insert_avl(node, key):
    if not node:
        return Node(key)
    if key < node.val:
        node.left = insert_avl(node.left, key)
    else:
        node.right = insert_avl(node.right, key)
    update_height(node)

    balance = get_balance(node)
    if balance > 1:
        if key < node.left.val:
            return rotate_right(node)
        else:
            node.left = rotate_left(node.left)
            return rotate_right(node)
    if balance < -1:
        if key > node.right.val:
            return rotate_left(node)
        else:
            node.right = rotate_right(node.right)
            return rotate_left(node)
    return node

def delete_bst(node, key):
    if not node:
        return node
    if key < node.val:
        node.left = delete_bst(node.left, key)
    elif key > node.val:
        node.right = delete_bst(node.right, key)
    else:
        if not node.left:
            return node.right
        elif not node.right:
            return node.left
        temp = get_min_value_node(node.right)
        node.val = temp.val
        node.right = delete_bst(node.right, temp.val)
    return node

def delete_avl(root, key):
    if not root:
        return root
    if key < root.val:
        root.left = delete_avl(root.left, key)
    elif key > root.val:
        root.right = delete_avl(root.right, key)
    else:
        if not root.left:
            return root.right
        elif not root.right:
            return root.left
        temp = get_min_value_node(root.right)
        root.val = temp.val
        root.right = delete_avl(root.right, temp.val)

    update_height(root)
    balance = get_balance(root)

    if balance > 1 and get_balance(root.left) >= 0:
        return rotate_right(root)
    if balance > 1 and get_balance(root.left) < 0:
        root.left = rotate_left(root.left)
        return rotate_right(root)
    if balance < -1 and get_balance(root.right) <= 0:
        return rotate_left(root)
    if balance < -1 and get_balance(root.right) > 0:
        root.right = rotate_right(root.right)
        return rotate_left(root)
    return root


def delete_binary(node, key):
    """
    Xóa nút có giá trị 'key' trong cây nhị phân thông thường.
    """
    if node is None:
        return None  # Nút rỗng, không cần xử lý

    # Tìm nút cần xóa ở cây con trái hoặc cây con phải
    if random.choice([True, False]):  # Lựa chọn ngẫu nhiên (đặc trưng của cây nhị phân thông thường)
        node.left = delete_binary(node.left, key)
    else:
        node.right = delete_binary(node.right, key)

    if node.val == key:
        # Trường hợp 1: Nút lá (không có con)
        if node.left is None and node.right is None:
            return None

        # Trường hợp 2: Nút có 1 con
        if node.left is None:
            return node.right  # Gán con phải cho nút cha
        elif node.right is None:
            return node.left  # Gán con trái cho nút cha

        # Trường hợp 3: Nút có 2 con
        # Thay thế bằng giá trị nhỏ nhất trong cây con phải
        temp = get_min_value_node(node.right)
        node.val = temp.val
        node.right = delete_binary(node.right, temp.val)

    return node


def get_min_value_node(node):
    """
    Hàm tìm giá trị nhỏ nhất trong cây con phải.
    """
    current = node
    while current.left is not None:
        current = current.left
    return current


def generate_unique_random_numbers(count, min_val, max_val):
    if max_val - min_val + 1 < count:
        raise ValueError("Khoảng giá trị không đủ để tạo các giá trị ngẫu nhiên không trùng lặp!")
    return random.sample(range(min_val, max_val + 1), count)

def export_tree(root):
    """
    Xuất cây dưới dạng danh sách các cấp độ.
    """
    if not root:
        return []
    levels = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val if node else None)
            if node:
                queue.append(node.left)
                queue.append(node.right)
        levels.append(level)
    return levels


def import_tree(levels):
    """
    Tạo lại cây từ danh sách các cấp độ.
    """
    if not levels or not levels[0]:
        return None
    root = Node(levels[0][0])
    queue = deque([root])
    index = 1
    while queue and index < len(levels):
        node = queue.popleft()
        if node:
            left_val = levels[index].pop(0) if levels[index] else None
            right_val = levels[index].pop(0) if levels[index] else None

            node.left = Node(left_val) if left_val is not None else None
            node.right = Node(right_val) if right_val is not None else None

            queue.append(node.left)
            queue.append(node.right)

        if not levels[index]:
            index += 1
    return root
class TreeCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig, self.ax = plt.subplots(figsize=(10, 8))
        super().__init__(fig)
        self.setParent(parent)
        self.selected_nodes = set()  # Nút đã được chọn
        self.node_positions = {}  # Tọa độ logic của các nút
        self.context_menu = QtWidgets.QMenu(self)  # Menu chuột phải

        # Kết nối sự kiện chuột
        self.mpl_connect("button_press_event", self.on_mouse_click)

    def display_tree(self, root):
        """
        Vẽ cây theo dạng từ trên xuống với các node không nằm chồng chéo nhau.
        """
        self.ax.clear()
        G = nx.DiGraph()
        self.node_positions.clear()

        # Tính toán vị trí x, y của các nút
        def calculate_positions(node, depth=0, x_pos=0, x_gap=1.5):
            if node is not None:
                self.node_positions[node.val] = (x_pos, -depth)  # Y ngược xuống dưới
                G.add_node(node.val)

                if node.left:
                    G.add_edge(node.val, node.left.val)
                    calculate_positions(node.left, depth + 1, x_pos - x_gap, x_gap / 2)

                if node.right:
                    G.add_edge(node.val, node.right.val)
                    calculate_positions(node.right, depth + 1, x_pos + x_gap, x_gap / 2)

        calculate_positions(root)

        # Tô màu các nút
        node_colors = ["red" if n in self.selected_nodes else "lightblue" for n in G.nodes()]
        nx.draw(G, self.node_positions, with_labels=True, labels={n: n for n in G.nodes()},
                node_size=1500, node_color=node_colors, font_size=12, font_weight='bold', ax=self.ax, arrows=False)
        self.draw()

    def on_mouse_click(self, event):
        """
        Xử lý sự kiện click chuột để chọn nút hoặc hiện context menu.
        """
        if event.xdata is None or event.ydata is None:
            return  # Không click vào vùng hợp lệ

        clicked_node = None
        min_distance = float('inf')

        # Xác định nút gần nhất với vị trí chuột
        for node, (x, y) in self.node_positions.items():
            distance = ((event.xdata - x) ** 2 + (event.ydata - y) ** 2) ** 0.5
            if distance < 0.5 and distance < min_distance:  # Ngưỡng 0.5 để xác định nút
                clicked_node = node
                min_distance = distance

        if clicked_node:
            if event.button == 1:  # Chuột trái
                self.toggle_node_selection(clicked_node)
            elif event.button == 3:  # Chuột phải
                self.show_context_menu(event, clicked_node)

    def toggle_node_selection(self, node):
        """
        Chuyển đổi trạng thái chọn của nút.
        """
        if node in self.selected_nodes:
            self.selected_nodes.remove(node)
        else:
            self.selected_nodes.add(node)
        self.display_tree(self.parent().tree_root)  # Cập nhật lại cây

    def show_context_menu(self, event, node):
        """
        Hiển thị context menu với các tùy chọn thêm và xóa nút.
        """
        self.context_menu.clear()

        # Hiển thị thông tin nút
        node_info = QtWidgets.QAction(f"Nút đang chọn: {node}", self.context_menu)
        node_info.setEnabled(False)
        self.context_menu.addAction(node_info)

        # Thêm nút
        add_action = QtWidgets.QAction("Thêm nút", self.context_menu)
        add_action.triggered.connect(lambda checked=False: self.parent().add_node(node))
        self.context_menu.addAction(add_action)

        # Xóa nút
        delete_action = QtWidgets.QAction("Xóa nút", self.context_menu)
        delete_action.triggered.connect(lambda checked=False: self.parent().delete_node(node))
        self.context_menu.addAction(delete_action)

        # Hiển thị menu tại vị trí chuột
        self.context_menu.exec_(self.mapToGlobal(QtCore.QPoint(event.x, event.y)))


class ManualTreeDialog(QtWidgets.QDialog):
    def __init__(self, parent, tree_type):
        super().__init__(parent)
        self.tree_type = tree_type
        self.tree_root = None
        self.node_dict = {}  # Lưu {node_value: [left_child, right_child]}
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"Tạo cây thủ công - {self.tree_type}")
        self.setGeometry(200, 100, 600, 400)

        main_layout = QtWidgets.QHBoxLayout(self)

        # Bên trái: Danh sách nút hiển thị dạng bảng
        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addWidget(QtWidgets.QLabel("Danh sách các nút (Hiển thị chuẩn):"))
        self.node_table = QtWidgets.QTableWidget()
        self.node_table.setColumnCount(3)
        self.node_table.setHorizontalHeaderLabels(["Nút", "Con trái", "Con phải"])
        self.node_table.horizontalHeader().setStretchLastSection(True)
        left_layout.addWidget(self.node_table)
        main_layout.addLayout(left_layout)

        # Bên phải: Phần nhập nút và các chức năng
        right_layout = QtWidgets.QVBoxLayout()

        # Nút thêm gốc
        self.root_input = QtWidgets.QLineEdit()
        self.root_input.setPlaceholderText("Nhập giá trị nút gốc...")
        right_layout.addWidget(QtWidgets.QLabel("Thêm nút gốc:"))
        right_layout.addWidget(self.root_input)
        self.add_root_button = QtWidgets.QPushButton("Thêm nút gốc")
        self.add_root_button.clicked.connect(self.add_root)
        right_layout.addWidget(self.add_root_button)

        # Chọn nút cha từ danh sách
        right_layout.addWidget(QtWidgets.QLabel("Chọn nút cha:"))
        self.parent_combo = QtWidgets.QComboBox()
        self.parent_combo.currentIndexChanged.connect(self.update_add_buttons)
        right_layout.addWidget(self.parent_combo)

        # Nhập giá trị nút con
        self.node_input = QtWidgets.QLineEdit()
        self.node_input.setPlaceholderText("Nhập giá trị nút con...")
        self.node_input.setDisabled(True)  # Vô hiệu hóa cho đến khi có nút gốc
        self.node_input.textChanged.connect(self.update_add_buttons)  # Kiểm tra nút nhập hợp lệ
        right_layout.addWidget(QtWidgets.QLabel("Nhập giá trị nút con:"))
        right_layout.addWidget(self.node_input)

        # Nút thêm trái/phải
        self.add_left_button = QtWidgets.QPushButton("Thêm vào trái")
        self.add_right_button = QtWidgets.QPushButton("Thêm vào phải")
        self.add_left_button.setDisabled(True)
        self.add_right_button.setDisabled(True)
        self.add_left_button.clicked.connect(lambda: self.add_child("left"))
        self.add_right_button.clicked.connect(lambda: self.add_child("right"))
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.add_left_button)
        button_layout.addWidget(self.add_right_button)
        right_layout.addLayout(button_layout)

        # Chọn nút muốn đổi vị trí
        right_layout.addWidget(QtWidgets.QLabel("Chọn nút muốn đổi vị trí:"))
        self.swap_combo = QtWidgets.QComboBox()
        self.swap_combo.setDisabled(True)
        right_layout.addWidget(self.swap_combo)

        self.swap_button = QtWidgets.QPushButton("Đổi vị trí trái-phải")
        self.swap_button.setDisabled(True)
        self.swap_button.clicked.connect(self.swap_child)
        right_layout.addWidget(self.swap_button)

        # Nút hoàn tất
        self.done_button = QtWidgets.QPushButton("Hoàn tất")
        self.done_button.clicked.connect(self.done_button_pressed)
        right_layout.addWidget(self.done_button)

        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

    def add_root(self):
        try:
            value = int(self.root_input.text())
            if self.tree_root:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "Nút gốc đã tồn tại!")
                return

            self.tree_root = Node(value)
            self.node_dict[value] = [None, None]
            self.update_table()
            self.update_parent_combo()
            self.update_swap_combo()
            self.root_input.clear()
            self.add_root_button.setDisabled(True)
            self.node_input.setDisabled(False)
            self.swap_combo.setDisabled(False)
            self.swap_button.setDisabled(False)
            self.parent().canvas.display_tree(self.tree_root)
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng nhập một số nguyên hợp lệ!")

    def add_child(self, side):
        try:
            value = int(self.node_input.text())
            parent_value = int(self.parent_combo.currentText())
            if parent_value not in self.node_dict:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "Nút cha không tồn tại!")
                return

            parent_node = self.find_node(self.tree_root, parent_value)
            if side == "left":
                if parent_node.left is not None:
                    QtWidgets.QMessageBox.warning(self, "Lỗi", "Nút con trái đã tồn tại!")
                    return
                parent_node.left = Node(value)
                self.node_dict[parent_value][0] = value
            elif side == "right":
                if parent_node.right is not None:
                    QtWidgets.QMessageBox.warning(self, "Lỗi", "Nút con phải đã tồn tại!")
                    return
                parent_node.right = Node(value)
                self.node_dict[parent_value][1] = value

            self.node_dict[value] = [None, None]
            self.update_table()
            current_index = self.parent_combo.currentIndex()
            self.update_parent_combo()
            self.parent_combo.setCurrentIndex(current_index)
            self.update_swap_combo()
            self.node_input.clear()
            self.parent().canvas.display_tree(self.tree_root)
            self.update_add_buttons()
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng nhập một số nguyên hợp lệ!")

    def swap_child(self):
        try:
            value = int(self.swap_combo.currentText())
            if value not in self.node_dict:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "Nút này không tồn tại trong cây!")
                return

            left, right = self.node_dict[value]
            self.node_dict[value] = [right, left]
            node = self.find_node(self.tree_root, value)
            if node:
                node.left, node.right = node.right, node.left
                self.update_table()
                self.parent().canvas.display_tree(self.tree_root)
                QtWidgets.QMessageBox.information(self, "Thành công", "Đã đổi vị trí trái và phải!")
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng nhập một số nguyên hợp lệ!")

    def update_table(self):
        self.node_table.setRowCount(len(self.node_dict))
        for i, (node, children) in enumerate(self.node_dict.items()):
            self.node_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(node)))
            self.node_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(children[0]) if children[0] else ""))
            self.node_table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(children[1]) if children[1] else ""))

    def update_parent_combo(self):
        current_text = self.parent_combo.currentText()
        self.parent_combo.blockSignals(True)
        self.parent_combo.clear()
        self.parent_combo.addItems(map(str, self.node_dict.keys()))
        if current_text in self.node_dict:
            self.parent_combo.setCurrentText(current_text)
        self.parent_combo.blockSignals(False)

    def update_swap_combo(self):
        self.swap_combo.clear()
        self.swap_combo.addItems(map(str, self.node_dict.keys()))

    def update_add_buttons(self):
        try:
            parent_value = int(self.parent_combo.currentText())
            new_value = int(self.node_input.text())
            parent_node = self.find_node(self.tree_root, parent_value)

            if self.tree_type in ["BST", "AVL"]:
                min_value, max_value = self.get_valid_range(self.tree_root, parent_value)
                if new_value < min_value or new_value > max_value:
                    self.add_left_button.setDisabled(True)
                    self.add_right_button.setDisabled(True)
                    return

                self.add_left_button.setDisabled(new_value >= parent_value or parent_node.left is not None)
                self.add_right_button.setDisabled(new_value <= parent_value or parent_node.right is not None)
            else:
                self.add_left_button.setDisabled(parent_node.left is not None)
                self.add_right_button.setDisabled(parent_node.right is not None)

        except ValueError:
            self.add_left_button.setDisabled(True)
            self.add_right_button.setDisabled(True)

    def get_valid_range(self, root, target_value, min_val=float('-inf'), max_val=float('inf')):
        if not root:
            return min_val, max_val
        if root.val == target_value:
            return min_val, max_val
        if target_value < root.val:
            return self.get_valid_range(root.left, target_value, min_val, root.val)
        else:
            return self.get_valid_range(root.right, target_value, root.val, max_val)

    def find_node(self, root, value):
        if not root or root.val == value:
            return root
        left = self.find_node(root.left, value)
        return left if left else self.find_node(root.right, value)

    def done_button_pressed(self):
        if not self.tree_root:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng thêm ít nhất một nút gốc trước khi hoàn tất!")
            return
        self.accept()


class TreeApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.tree_root = None
        self.manual_tree_type = None  # Loại cây thủ công đang được chọn
        self.paused = False  # Trạng thái tạm dừng
        self.traversal_timer = QtCore.QTimer(self)
        self.traversal_index = 0  # Chỉ số cho quá trình duyệt cây
        self.traversal_nodes = []  # Danh sách các nút để duyệt
        self.traversal_result = []
        self.initUI()
        self.showMaximized()

    def show_search_dialog(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Chọn kiểu tìm kiếm")
        dialog.setFixedSize(300, 200)

        layout = QtWidgets.QVBoxLayout(dialog)
        layout.addWidget(QtWidgets.QLabel("Chọn kiểu tìm kiếm:"))

        search_type_combo = QtWidgets.QComboBox(dialog)
        search_type_combo.addItems(["DFS (Tìm tuyến tính)", "BFS (Tìm theo cấp)", "BST (Tìm nhị phân)"])
        layout.addWidget(search_type_combo)

        value_input = QtWidgets.QLineEdit(dialog)
        value_input.setPlaceholderText("Nhập giá trị cần tìm...")
        layout.addWidget(value_input)

        button_layout = QtWidgets.QHBoxLayout()
        search_button = QtWidgets.QPushButton("Tìm kiếm")
        cancel_button = QtWidgets.QPushButton("Hủy")
        button_layout.addWidget(search_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        # Xử lý khi nhấn nút
        def handle_search():
            try:
                value = int(value_input.text())
                search_type = search_type_combo.currentText()
                dialog.accept()
                self.start_search(search_type, value)
            except ValueError:
                QtWidgets.QMessageBox.warning(dialog, "Lỗi", "Vui lòng nhập số nguyên hợp lệ!")

        search_button.clicked.connect(handle_search)
        cancel_button.clicked.connect(dialog.reject)

        dialog.exec_()


    def initUI(self):
        self.setWindowTitle('Binary Tree Manager')
        self.setGeometry(200, 100, 800, 600)
        self.setStyleSheet("background-color: #f0f8ff;")

        # Layout chính
        main_layout = QtWidgets.QVBoxLayout(self)

        # Lựa chọn loại cây và nhập số lượng nút
        input_layout = QtWidgets.QHBoxLayout()
        self.tree_type_combo = QtWidgets.QComboBox()
        self.tree_type_combo.addItems(["Cây nhị phân thông thường", "BST", "AVL"])
        input_layout.addWidget(QtWidgets.QLabel("Chọn loại cây:"))
        input_layout.addWidget(self.tree_type_combo)

        self.node_count_input = QtWidgets.QLineEdit()
        self.node_count_input.setText("5")
        input_layout.addWidget(QtWidgets.QLabel("Số lượng nút:"))
        input_layout.addWidget(self.node_count_input)

        # Nhập min và max cho cây ngẫu nhiên
        self.min_input = QtWidgets.QLineEdit()
        self.min_input.setText("1")
        input_layout.addWidget(QtWidgets.QLabel("Min:"))
        input_layout.addWidget(self.min_input)

        self.max_input = QtWidgets.QLineEdit()
        self.max_input.setText("100")
        input_layout.addWidget(QtWidgets.QLabel("Max:"))
        input_layout.addWidget(self.max_input)


        # Nút tạo cây ngẫu nhiên
        self.create_random_tree_button = QtWidgets.QPushButton("Tạo cây ngẫu nhiên")
        self.create_random_tree_button.setStyleSheet(
            "background-color: #4682B4; color: white; font-weight: bold; font-size: 14px;")
        self.create_random_tree_button.clicked.connect(self.create_random_tree)
        input_layout.addWidget(self.create_random_tree_button)

        # Nút tạo cây thủ công
        self.create_manual_tree_button = QtWidgets.QPushButton("Tạo cây thủ công")
        self.create_manual_tree_button.setStyleSheet(
            "background-color: #4682B4; color: white; font-weight: bold; font-size: 14px;")
        self.create_manual_tree_button.clicked.connect(self.create_manual_tree)
        input_layout.addWidget(self.create_manual_tree_button)

        # Lựa chọn kiểu duyệt cây
        self.traversal_type_combo = QtWidgets.QComboBox()
        self.traversal_type_combo.addItems(["Preorder", "Inorder", "Postorder"])
        input_layout.addWidget(QtWidgets.QLabel("Chọn kiểu duyệt cây:"))
        input_layout.addWidget(self.traversal_type_combo)

        # Nút duyệt cây
        self.traverse_button = QtWidgets.QPushButton("Duyệt cây")
        self.traverse_button.setStyleSheet(
            "background-color: #4682B4; color: white; font-weight: bold; font-size: 14px;")
        self.traverse_button.clicked.connect(self.start_traversal)
        input_layout.addWidget(self.traverse_button)

        # Thêm layout các nút vào layout chính
        main_layout.addLayout(input_layout)

        # Khu vực để hiển thị sơ đồ đã vẽ (Tree Canvas)
        self.canvas = TreeCanvas(self)
        main_layout.addWidget(self.canvas)

        # Hộp văn bản để hiển thị danh sách các nút của cây
        self.node_list_textbox = QtWidgets.QTextEdit()
        self.node_list_textbox.setReadOnly(True)
        self.node_list_textbox.setPlaceholderText("Danh sách các nút sẽ hiển thị ở đây...")
        main_layout.addWidget(QtWidgets.QLabel("Danh sách các nút của cây:"))
        main_layout.addWidget(self.node_list_textbox)

        # Thêm nút tìm giá trị vào giao diện trong initUI
        self.search_value_button = QtWidgets.QPushButton("🔍Tìm giá trị")
        self.search_value_button.setFixedSize(90, 30)
        self.search_value_button.setStyleSheet("background-color: #4682B4; color: white; font-weight: bold; font-size: 12px;")
        self.search_value_button.clicked.connect(self.show_search_dialog)
        input_layout.addWidget(self.search_value_button)

        # Thanh trượt tốc độ và khu vực cho nút tạm dừng
        slider_layout = QtWidgets.QHBoxLayout()

        slider_layout.addWidget(QtWidgets.QLabel("Tốc độ duyệt:"))
        self.speed_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.speed_slider.setMinimum(0)
        self.speed_slider.setMaximum(100)
        self.speed_slider.setValue(50)
        self.speed_slider.setFixedWidth(150)
        self.speed_slider.valueChanged.connect(self.update_speed_label)
        slider_layout.addWidget(self.speed_slider)

        self.speed_label = QtWidgets.QLabel("50")
        slider_layout.addWidget(self.speed_label)

        # Đặt nút tạm dừng vào góc bên phải, bên dưới thanh trượt
        self.pause_button = QtWidgets.QPushButton("Tạm dừng")
        self.pause_button.setStyleSheet(
            "background-color: #4682B4; color: white; font-weight: bold; font-size: 12px;")
        self.pause_button.clicked.connect(self.toggle_pause)
        slider_layout.addWidget(self.pause_button, alignment=QtCore.Qt.AlignRight)

        # Nút export cây
        self.export_tree_button = QtWidgets.QPushButton("Xuất cây")
        self.export_tree_button.setStyleSheet(
            "background-color: #4682B4; color: white; font-weight: bold; font-size: 14px;")
        self.export_tree_button.clicked.connect(self.export_tree_to_file)
        input_layout.addWidget(self.export_tree_button)

        # Nút import cây
        self.import_tree_button = QtWidgets.QPushButton("Nhập cây")
        self.import_tree_button.setStyleSheet(
            "background-color: #4682B4; color: white; font-weight: bold; font-size: 14px;")
        self.import_tree_button.clicked.connect(self.import_tree_from_file)
        input_layout.addWidget(self.import_tree_button)

        main_layout.addLayout(slider_layout)
    def create_random_tree(self):
        try:
            node_count = int(self.node_count_input.text())
            if node_count <= 0:
                raise ValueError
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Lỗi đầu vào", "Vui lòng nhập số lượng nút hợp lệ!")
            return

        try:
            min_val = int(self.min_input.text())
            max_val = int(self.max_input.text())
            if min_val >= max_val:
                raise ValueError
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Lỗi đầu vào", "Vui lòng nhập giá trị min và max hợp lệ!")
            return

        tree_type = self.tree_type_combo.currentText()
        self.tree_root = None

        try:
            keys = generate_unique_random_numbers(node_count, min_val, max_val)
        except ValueError as e:
            QtWidgets.QMessageBox.warning(self, "Lỗi đầu vào", str(e))
            return

        for key in keys:
            if tree_type == "Cây nhị phân thông thường":
                self.tree_root = insert_binary(self.tree_root, key)
            elif tree_type == "BST":
                self.tree_root = insert_bst(self.tree_root, key)
            elif tree_type == "AVL":
                self.tree_root = insert_avl(self.tree_root, key)
        self.display_tree()

    def create_manual_tree(self):
        """
        Hiển thị hộp thoại để tạo cây thủ công.
        Cập nhật cây và hiển thị trên canvas sau khi hoàn thành.
        """
        tree_type = self.tree_type_combo.currentText()
        dialog = ManualTreeDialog(self, tree_type)

        # Nếu người dùng nhấn "Hoàn tất" và tạo cây thành công
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.tree_root = dialog.tree_root  # Lấy cây thủ công đã tạo
            self.display_tree()  # Hiển thị cây trên canvas
            self.traversal_nodes.clear()  # Reset danh sách nút duyệt cũ
            QtWidgets.QMessageBox.information(self, "Thành công",
                                              "Cây thủ công đã được tạo thành công và sẵn sàng để duyệt!")

    def display_tree(self):
        """
        Cập nhật và hiển thị cây hiện tại trên canvas.
        """
        if self.tree_root:
            self.canvas.display_tree(self.tree_root)  # Hiển thị cây trên canvas
            levels = self.get_levels(self.tree_root)  # Lấy các cấp độ trong cây
            levels_text = "\n".join([", ".join(map(str, level)) for level in levels])
            self.node_list_textbox.setPlainText(levels_text)  # Hiển thị danh sách các nút

    # Trong lớp ManualTreeDialog, đảm bảo cập nhật canvas khi cây thay đổi
    def add_child(self, side):
        """
        Thêm nút con vào cây theo bên trái hoặc phải.
        """
        try:
            value = int(self.child_input.text())
            if not self.tree_root:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng thêm nút gốc trước!")
                return

            if side == "left":
                self.tree_root.left = insert_binary(self.tree_root.left, value)
                self.node_list.append(f"Left: {value}")
            elif side == "right":
                self.tree_root.right = insert_binary(self.tree_root.right, value)
                self.node_list.append(f"Right: {value}")

            self.update_node_list()  # Cập nhật danh sách nút đã thêm
            self.update_buttons()  # Cập nhật trạng thái nút
            self.parent.canvas.display_tree(self.tree_root)  # Hiển thị cây hiện tại trên canvas
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng nhập một số nguyên hợp lệ!")

    # Cập nhật nút "Hoàn tất" để truyền cây về TreeApp khi người dùng hoàn tất
    def done_button_pressed(self):
        """
        Khi nút 'Hoàn tất' được nhấn, trả về cây đã tạo về lớp cha.
        """
        if self.tree_root is None:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng tạo ít nhất một nút gốc!")
            return
        self.accept()  # Đóng hộp thoại và trả về cây cho TreeApp

    def get_levels(self, root):
        if not root:
            return []
        levels = []
        current_level = [root]
        while current_level:
            levels.append([node.val for node in current_level])
            next_level = []
            for node in current_level:
                if node.left:
                    next_level.append(node.left)
                if node.right:
                    next_level.append(node.right)
            current_level = next_level
        return levels

    def export_tree_to_file(self):
        """
        Xuất cây hiện tại vào file theo dạng:
        parent_value,left_child_value,right_child_value
        Duyệt toàn bộ cây con trái trước rồi mới đến cây con phải.
        """
        if not self.tree_root:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Cây hiện tại trống, không thể xuất!")
            return

        # Chọn đường dẫn file để lưu
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Lưu cây vào file", "", "Text Files (*.txt)",
                                                             options=options)
        if not file_path:
            return

        # Duyệt cây con trái trước, rồi tới cây con phải
        def dfs_export_left_to_right(node, file):
            if not node:
                return

            left_val = node.left.val if node.left else "null"
            right_val = node.right.val if node.right else "null"
            file.write(f"{node.val},{left_val},{right_val}\n")  # Ghi giá trị nút cha và con trái/phải

            # Duyệt cây con trái trước toàn bộ
            dfs_export_left_to_right(node.left, file)
            # Sau đó mới duyệt cây con phải
            dfs_export_left_to_right(node.right, file)

        # Ghi vào file
        with open(file_path, 'w') as file:
            dfs_export_left_to_right(self.tree_root, file)

        QtWidgets.QMessageBox.information(self, "Thành công", "Cây đã được xuất thành công!")

    def import_tree_from_file(self):
        """
        Nhập cây từ file theo định dạng:
        parent_value,left_child_value,right_child_value
        """
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Nhập cây từ file", "", "Text Files (*.txt)",
                                                             options=options)
        if not file_path:
            return

        nodes = {}  # Dictionary để lưu các nút đã tạo
        root = None

        # Đọc file và tạo các nút
        with open(file_path, 'r') as file:
            for line in file:
                parent, left, right = line.strip().split(',')
                parent_val = int(parent)
                left_val = int(left) if left != "null" else None
                right_val = int(right) if right != "null" else None

                # Tạo nút cha nếu chưa tồn tại
                if parent_val not in nodes:
                    nodes[parent_val] = Node(parent_val)
                current_node = nodes[parent_val]

                # Gán nút gốc nếu chưa có
                if root is None:
                    root = current_node

                # Tạo và gán con trái
                if left_val is not None and left_val not in nodes:
                    nodes[left_val] = Node(left_val)
                current_node.left = nodes[left_val] if left_val else None

                # Tạo và gán con phải
                if right_val is not None and right_val not in nodes:
                    nodes[right_val] = Node(right_val)
                current_node.right = nodes[right_val] if right_val else None

        self.tree_root = root  # Gán lại cây gốc
        self.display_tree()  # Hiển thị cây trên giao diện
        QtWidgets.QMessageBox.information(self, "Thành công", "Cây đã được nhập thành công!")

    def add_node(self, parent_node_val):
        """
        Thêm nút con mới vào cây.
        """
        try:
            tree_type = self.tree_type_combo.currentText()
            parent_node = self.find_node(self.tree_root, parent_node_val)
            if not parent_node:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "Không tìm thấy nút cha!")
                return

            new_val, ok = QtWidgets.QInputDialog.getInt(self, "Thêm nút", "Nhập giá trị nút mới:")
            if not ok:
                return

            if tree_type == "Cây nhị phân thông thường":
                # Kiểm tra trạng thái nút con trái và phải
                if parent_node.left and parent_node.right:
                    QtWidgets.QMessageBox.information(self, "Thông báo", "Nút đã có đủ 2 con, không thể thêm!")
                    return

                # Xác định vị trí cần thêm
                options = []
                if not parent_node.left:
                    options.append("Trái")
                if not parent_node.right:
                    options.append("Phải")

                side, ok = QtWidgets.QInputDialog.getItem(self, "Chọn vị trí", "Thêm vào vị trí:", options, 0, False)
                if not ok:
                    return

                if side == "Trái":
                    parent_node.left = Node(new_val)
                elif side == "Phải":
                    parent_node.right = Node(new_val)

            elif tree_type == "BST":
                self.tree_root = insert_bst(self.tree_root, new_val)
            elif tree_type == "AVL":
                self.tree_root = insert_avl(self.tree_root, new_val)
            else:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "Loại cây không hỗ trợ thêm nút!")
                return

            self.display_tree()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Lỗi", f"Không thể thêm nút: {e}")

    def delete_node(self, node_val):
        """
        Xóa nút theo logic của từng loại cây.
        """
        try:
            tree_type = self.tree_type_combo.currentText()
            if tree_type == "Cây nhị phân thông thường":
                self.tree_root = delete_binary(self.tree_root, node_val)
            elif tree_type == "BST":
                self.tree_root = delete_bst(self.tree_root, node_val)
            elif tree_type == "AVL":
                self.tree_root = delete_avl(self.tree_root, node_val)
            else:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "Loại cây không hỗ trợ xóa nút!")
                return

            self.display_tree()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Lỗi", f"Không thể xóa nút: {e}")

    def find_node(self, root, val):
        """
        Tìm nút có giá trị val trong cây, hoạt động với cả cây nhị phân thông thường.
        """
        if root is None:
            return None
        if root.val == val:
            return root
        # Tìm ở cây con trái
        left_result = self.find_node(root.left, val)
        if left_result:
            return left_result
        # Tìm ở cây con phải
        return self.find_node(root.right, val)

    def start_search(self, search_type, value):
        if not self.tree_root:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng tạo cây trước khi tìm kiếm!")
            return

        # Xác định kiểu tìm kiếm
        if search_type == "DFS (Tìm tuyến tính)":
            self.search_nodes = self.dfs_search_steps(self.tree_root, value)
        elif search_type == "BFS (Tìm theo cấp)":
            self.search_nodes = self.bfs_search_steps(self.tree_root, value)
        elif search_type == "BST (Tìm nhị phân)":
            self.search_nodes = self.bst_search_steps(self.tree_root, value)

        self.search_index = 0
        self.search_value = value
        self.paused = False
        self.pause_button.setText("Tạm dừng")
        self.search_step()

    def search_step(self):
        if self.paused or self.search_index >= len(self.search_nodes):
            if self.search_index >= len(self.search_nodes):
                QtWidgets.QMessageBox.information(self, "Kết quả",
                                                  f"Giá trị {self.search_value} {'được tìm thấy!' if self.search_value in self.search_nodes else 'không tồn tại trong cây!'}")
            return

        current_node = self.search_nodes[self.search_index]
        self.canvas.selected_nodes.clear()
        self.canvas.selected_nodes.add(current_node)
        self.canvas.display_tree(self.tree_root)

        if current_node == self.search_value:
            QtWidgets.QMessageBox.information(self, "Tìm kiếm thành công", f"Đã tìm thấy giá trị {self.search_value}!")
            return

        self.search_index += 1
        QtCore.QTimer.singleShot(500, self.search_step)

    def dfs_search_steps(self, node, value):
        steps = []

        def dfs(node):
            if not node:
                return
            steps.append(node.val)
            if node.val == value:
                return
            dfs(node.left)
            dfs(node.right)

        dfs(node)
        return steps

    def bfs_search_steps(self, root, value):
        steps = []
        queue = deque([root])
        while queue:
            node = queue.popleft()
            steps.append(node.val)
            if node.val == value:
                break
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return steps

    def bst_search_steps(self, node, value):
        steps = []
        while node:
            steps.append(node.val)
            if node.val == value:
                break
            if value < node.val:
                node = node.left
            else:
                node = node.right
        return steps

    def highlight_tree_not_found(self):
        for _ in range(3):
            self.canvas.selected_nodes = set(self.get_all_nodes(self.tree_root))
            self.canvas.display_tree(self.tree_root)
            QtCore.QThread.msleep(300)
            self.canvas.selected_nodes.clear()
            self.canvas.display_tree(self.tree_root)

    def update_speed_label(self):
        # Cập nhật giá trị của nhãn khi giá trị của thanh trượt thay đổi
        self.speed_label.setText(str(self.speed_slider.value()))

    def toggle_pause(self):
        """
        Thay đổi trạng thái tạm dừng hoặc tiếp tục.
        """
        if not self.traversal_nodes:  # Nếu không có gì để duyệt, vô hiệu hóa
            return

        self.paused = not self.paused
        if self.paused:
            self.pause_button.setText("Tiếp tục")
        else:
            self.pause_button.setText("Tạm dừng")
            self.traversal_step()  # Tiếp tục duyệt cây

    def start_traversal(self):
        """
        Khởi động duyệt cây từ đầu và kích hoạt nút tạm dừng.
        """
        if not self.tree_root:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng tạo một cây trước khi duyệt!")
            return

        # Reset các trạng thái
        self.traversal_index = 0
        self.traversal_result = []
        self.traversal_nodes = []
        self.canvas.selected_nodes.clear()
        self.canvas.display_tree(self.tree_root)

        # Lấy kiểu duyệt cây
        traversal_type = self.traversal_type_combo.currentText()
        if traversal_type == "Preorder":
            self.traversal_nodes = self.preorder(self.tree_root)
        elif traversal_type == "Inorder":
            self.traversal_nodes = self.inorder(self.tree_root)
        elif traversal_type == "Postorder":
            self.traversal_nodes = self.postorder(self.tree_root)

        # Kích hoạt nút tạm dừng và cập nhật trạng thái
        self.paused = False
        self.pause_button.setEnabled(True)
        self.pause_button.setText("Tạm dừng")

        # Vô hiệu hóa các nút khác trong quá trình duyệt
        self.create_random_tree_button.setEnabled(False)
        self.create_manual_tree_button.setEnabled(False)
        self.traverse_button.setEnabled(False)

        self.traversal_step()

    def traversal_step(self):
        """
        Thực hiện từng bước duyệt cây. Hỗ trợ tạm dừng và vô hiệu hóa nút khi hoàn tất.
        """
        if self.paused:  # Nếu đang tạm dừng, không thực hiện bước tiếp theo
            return

        if self.traversal_index < len(self.traversal_nodes):
            current_node = self.traversal_nodes[self.traversal_index]
            self.traversal_result.append(current_node)

            # Cập nhật danh sách các nút đã duyệt ngay lập tức
            self.node_list_textbox.setPlainText(" → ".join(map(str, self.traversal_result)))

            # Hiển thị trạng thái trên cây
            self.canvas.selected_nodes.clear()
            self.canvas.selected_nodes.add(current_node)
            self.canvas.display_tree(self.tree_root)

            self.traversal_index += 1

            # Tính toán thời gian chờ theo tốc độ thanh trượt
            delay = max(100, (100 - self.speed_slider.value()) * 10)
            QtCore.QTimer.singleShot(delay, self.traversal_step)
        else:
            # Hoàn thành duyệt cây -> reset trạng thái
            QtWidgets.QMessageBox.information(self, "Hoàn tất", "Duyệt cây đã hoàn thành!")
            self.reset_tree_colors()

            # Disable nút tạm dừng
            self.pause_button.setEnabled(False)

            # Kích hoạt lại các nút khác
            self.create_random_tree_button.setEnabled(True)
            self.create_manual_tree_button.setEnabled(True)
            self.traverse_button.setEnabled(True)

    def reset_tree_colors(self):
        self.canvas.selected_nodes.clear()
        self.canvas.display_tree(self.tree_root)

    def preorder(self, node):
        return [node.val] + self.preorder(node.left) + self.preorder(node.right) if node else []

    def inorder(self, node):
        return self.inorder(node.left) + [node.val] + self.inorder(node.right) if node else []

    def postorder(self, node):
        return self.postorder(node.left) + self.postorder(node.right) + [node.val] if node else []


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = TreeApp()
    window.show()
    sys.exit(app.exec_())