import sys
import random
import matplotlib.pyplot as plt
import networkx as nx
from PyQt5 import QtWidgets, QtGui, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

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
    if not node:
        return node
    if key == node.val:
        if not node.left:
            return node.right
        elif not node.right:
            return node.left
        temp = get_min_value_node(node.right)
        node.val = temp.val
        node.right = delete_binary(node.right, temp.val)
    else:
        if random.choice([True, False]):
            node.left = delete_binary(node.left, key)
        else:
            node.right = delete_binary(node.right, key)
    return node

def get_min_value_node(node):
    current = node
    while current.left is not None:
        current = current.left
    return current

def generate_unique_random_numbers(count, min_val, max_val):
    if max_val - min_val + 1 < count:
        raise ValueError("Khoảng giá trị không đủ để tạo các giá trị ngẫu nhiên không trùng lặp!")
    return random.sample(range(min_val, max_val + 1), count)

class TreeCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig, self.ax = plt.subplots(figsize=(10, 8))
        super().__init__(fig)
        self.setParent(parent)
        self.selected_nodes = set()
        self.node_positions = {}

    def display_tree(self, root):
        self.ax.clear()
        G = nx.DiGraph()
        self.node_positions.clear()

        def add_edges(node, x=0, y=0, dx=1.5):
            if node is not None:
                self.node_positions[node.val] = (x, y)
                G.add_node(node.val)

                if node.left is not None:
                    G.add_edge(node.val, node.left.val)
                    add_edges(node.left, x - dx, y - 1, dx / 1.5)
                if node.right is not None:
                    G.add_edge(node.val, node.right.val)
                    add_edges(node.right, x + dx, y - 1, dx / 1.5)

        add_edges(root)

        nx.draw(G, self.node_positions, with_labels=True, labels={n: n for n in G.nodes()},
                node_size=2000, node_color=['red' if n in self.selected_nodes else 'lightblue' for n in G.nodes()],
                font_size=12, font_weight='bold', ax=self.ax, arrows=False)

        self.draw()

    def mousePressEvent(self, event):
        node_radius = 3.5
        x, y = self.ax.transData.inverted().transform(
            (event.x(), event.y()))
        closest_node = None
        min_distance = float('inf')

        for node, pos in self.node_positions.items():
            distance = ((x - pos[0]) ** 2 + (y - pos[1]) ** 2) ** 0.5
            if distance <= node_radius and distance < min_distance:
                closest_node = node
                min_distance = distance

        if closest_node is not None:
            if event.button() == QtCore.Qt.LeftButton:
                self.toggle_node_selection(closest_node)
            elif event.button() == QtCore.Qt.RightButton and closest_node in self.selected_nodes:
                self.show_context_menu(closest_node, QtCore.QPoint(event.globalX(), event.globalY()))

    def toggle_node_selection(self, node):
        if node in self.selected_nodes:
            self.selected_nodes.remove(node)
        else:
            self.selected_nodes.add(node)
        self.display_tree(self.parent().tree_root)

    def show_context_menu(self, node, pos):
        menu = QtWidgets.QMenu(self)
        add_action = menu.addAction("Thêm nút")
        delete_action = menu.addAction("Xóa nút")

        add_action.triggered.connect(lambda: self.parent().add_node(node))
        delete_action.triggered.connect(lambda: self.parent().delete_node(node))

        menu.exec_(pos)

class ManualTreeDialog(QtWidgets.QDialog):
    def __init__(self, parent, tree_type):
        super().__init__(parent)
        self.tree_type = tree_type
        self.tree_root = None
        self.parent = parent  # Tham chiếu đến lớp cha để cập nhật canvas
        self.node_list = []  # Danh sách các nút đã được thêm
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"Tạo cây thủ công - {self.tree_type}")
        self.setGeometry(200, 100, 200, 200)

        layout = QtWidgets.QVBoxLayout(self)

        # Nhập giá trị nút gốc
        self.root_input = QtWidgets.QLineEdit()
        self.root_input.setPlaceholderText("Nhập giá trị nút gốc...")
        layout.addWidget(QtWidgets.QLabel("Nút gốc:"))
        layout.addWidget(self.root_input)

        # Nút xác nhận thêm gốc
        self.add_root_button = QtWidgets.QPushButton("Thêm nút gốc")
        self.add_root_button.clicked.connect(self.add_root)
        layout.addWidget(self.add_root_button)

        # Nhập giá trị nút con
        self.child_input = QtWidgets.QLineEdit()
        self.child_input.setPlaceholderText("Nhập giá trị nút con...")
        self.child_input.textChanged.connect(self.update_buttons)  # Kích hoạt kiểm tra nút khi nhập
        layout.addWidget(QtWidgets.QLabel("Thêm nút:"))
        layout.addWidget(self.child_input)

        # Chọn thêm vào bên trái hay phải
        self.add_left_button = QtWidgets.QPushButton("Thêm vào trái")
        self.add_right_button = QtWidgets.QPushButton("Thêm vào phải")
        self.add_left_button.clicked.connect(lambda: self.add_child("left"))
        self.add_right_button.clicked.connect(lambda: self.add_child("right"))

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.add_left_button)
        button_layout.addWidget(self.add_right_button)
        layout.addLayout(button_layout)

        # Danh sách các nút đã thêm
        layout.addWidget(QtWidgets.QLabel("Danh sách các nút:"))
        self.node_list_widget = QtWidgets.QListWidget()
        layout.addWidget(self.node_list_widget)

        # Nút đổi vị trí (chỉ cho cây nhị phân thông thường)
        self.swap_button = QtWidgets.QPushButton("Đổi vị trí trái và phải")
        self.swap_button.clicked.connect(self.swap_child)
        self.swap_button.setVisible(self.tree_type == "Cây nhị phân thông thường")
        layout.addWidget(self.swap_button)

        # Nút hoàn tất
        self.done_button = QtWidgets.QPushButton("Hoàn tất")
        self.done_button.clicked.connect(self.done_button_pressed)
        layout.addWidget(self.done_button)

    def add_root(self):
        try:
            value = int(self.root_input.text())
            if self.tree_root:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "Nút gốc đã tồn tại!")
                return

            self.tree_root = Node(value)
            self.node_list.append(f"Root: {value}")
            self.update_node_list()
            self.add_root_button.setDisabled(True)  # Không cho thêm nút gốc lần nữa
            self.update_buttons()
            self.parent.canvas.display_tree(self.tree_root)  # Cập nhật canvas
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng nhập một số nguyên hợp lệ!")

    def add_child(self, side):
        try:
            value = int(self.child_input.text())
            if not self.tree_root:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng thêm nút gốc trước!")
                return

            if side == "left":
                if self.tree_type == "BST" or self.tree_type == "AVL":
                    if value >= self.tree_root.val:
                        QtWidgets.QMessageBox.warning(self, "Lỗi", "Giá trị không hợp lệ cho cây BST hoặc AVL!")
                        return
                self.tree_root.left = insert_binary(self.tree_root.left, value)
                self.node_list.append(f"Left: {value}")
            elif side == "right":
                if self.tree_type == "BST" or self.tree_type == "AVL":
                    if value <= self.tree_root.val:
                        QtWidgets.QMessageBox.warning(self, "Lỗi", "Giá trị không hợp lệ cho cây BST hoặc AVL!")
                        return
                self.tree_root.right = insert_binary(self.tree_root.right, value)
                self.node_list.append(f"Right: {value}")

            self.update_node_list()  # Cập nhật danh sách các nút đã thêm
            self.update_buttons()  # Cập nhật trạng thái của các nút
            self.child_input.clear()  # Xóa nội dung nhập
            self.parent.canvas.display_tree(self.tree_root)  # Hiển thị cây trên canvas
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng nhập một số nguyên hợp lệ!")

    def swap_child(self):
        """
        Đổi vị trí các nút con trái và phải.
        """
        if self.tree_root and self.tree_root.left and self.tree_root.right:
            self.tree_root.left, self.tree_root.right = self.tree_root.right, self.tree_root.left
            QtWidgets.QMessageBox.information(self, "Thành công", "Đã đổi vị trí trái và phải!")
            self.node_list.append("Swapped children")
            self.update_node_list()
            self.parent.canvas.display_tree(self.tree_root)

    def update_node_list(self):
        """
        Cập nhật danh sách các nút đã thêm vào widget.
        """
        self.node_list_widget.clear()
        self.node_list_widget.addItems(self.node_list)

    def update_buttons(self):
        """
        Cập nhật trạng thái của các nút thêm trái/phải dựa trên logic của từng loại cây.
        """
        try:
            value = int(self.child_input.text())
        except ValueError:
            self.add_left_button.setDisabled(True)
            self.add_right_button.setDisabled(True)
            return

        if self.tree_type == "BST":
            self.add_left_button.setDisabled(value >= self.tree_root.val if self.tree_root else True)
            self.add_right_button.setDisabled(value <= self.tree_root.val if self.tree_root else True)
        elif self.tree_type == "AVL":
            self.add_left_button.setDisabled(value >= self.tree_root.val if self.tree_root else True)
            self.add_right_button.setDisabled(value <= self.tree_root.val if self.tree_root else True)
        else:
            self.add_left_button.setDisabled(False)
            self.add_right_button.setDisabled(False)

    def done_button_pressed(self):
        """
        Khi nút 'Hoàn tất' được nhấn, kiểm tra cây và trả về kết quả.
        """
        if self.tree_root is None:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng tạo ít nhất một nút gốc trước khi hoàn tất!")
            return
        self.accept()


# Lớp ứng dụng PyQt5 cho giao diện chính
class TreeApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.tree_root = None
        self.manual_tree_type = None  # Loại cây thủ công đang được chọn
        self.initUI()
        self.traversal_timer = QtCore.QTimer(self)
        self.traversal_index = 0  # Chỉ số cho quá trình duyệt cây
        self.traversal_nodes = []  # Danh sách các nút để duyệt
        self.traversal_result = []
        self.traversal_timer.setSingleShot(True)  # Đảm bảo timer chỉ chạy một lần
        self.showMaximized()

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

        # Thêm thanh trượt tốc độ và nhãn vào `input_layout`
        input_layout.addWidget(QtWidgets.QLabel("Tốc độ duyệt:"))

        # Thanh trượt tốc độ duyệt cây
        self.speed_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.speed_slider.setMinimum(0)
        self.speed_slider.setMaximum(100)
        self.speed_slider.setValue(50)  # Giá trị mặc định
        self.speed_slider.setFixedWidth(100)  # Giới hạn chiều rộng để hiển thị nhỏ
        self.speed_slider.valueChanged.connect(self.update_speed_label)
        input_layout.addWidget(self.speed_slider)

        # Nhãn hiển thị giá trị hiện tại của thanh trượt
        self.speed_label = QtWidgets.QLabel("50")
        input_layout.addWidget(self.speed_label)

        # Thêm layout các nút và thanh trượt vào layout chính
        main_layout.addLayout(input_layout)
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

    def add_node(self, parent_node_val):
        # Thêm nút con cho một nút cụ thể
        key, ok = QtWidgets.QInputDialog.getInt(self, "Thêm nút", "Nhập giá trị nút mới:")
        if ok:
            tree_type = self.tree_type_combo.currentText()
            parent_node = self.find_node(self.tree_root, parent_node_val)
            if parent_node is None:
                return
            if tree_type == "Cây nhị phân thông thường":
                position, ok = QtWidgets.QInputDialog.getItem(self, "Vị trí thêm nút", "Chọn vị trí thêm nút:",
                                                              ["left", "right"], 0, False)
                if ok:
                    if position == "left":
                        parent_node.left = insert_binary(parent_node.left, key)
                    elif position == "right":
                        parent_node.right = insert_binary(parent_node.right, key)
            elif tree_type == "BST":
                insert_bst(parent_node, key)
            elif tree_type == "AVL":
                self.tree_root = insert_avl(self.tree_root, key)
            self.display_tree()

    def delete_node(self, node_val):
        # Xóa một nút đã chọn cụ thể trong cây
        if node_val not in self.canvas.selected_nodes:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một nút để xóa!")
            return
        tree_type = self.tree_type_combo.currentText()
        if tree_type == "BST":
            self.tree_root = delete_bst(self.tree_root, node_val)
        elif tree_type == "AVL":
            self.tree_root = delete_avl(self.tree_root, node_val)
        elif tree_type == "Cây nhị phân thông thường":
            self.tree_root = delete_binary(self.tree_root, node_val)
        else:
            QtWidgets.QMessageBox.warning(self, "Lỗi",
                                          "Xóa nút chỉ hỗ trợ cho cây BST, AVL và cây nhị phân thông thường!")
            return
        self.canvas.selected_nodes.remove(node_val)
        self.display_tree()

    def find_node(self, root, val):
        # Tìm và trả về nút có giá trị val trong cây
        if root is None or root.val == val:
            return root
        if val < root.val:
            return self.find_node(root.left, val)
        return self.find_node(root.right, val)

    def update_speed_label(self):
        # Cập nhật giá trị của nhãn khi giá trị của thanh trượt thay đổi
        self.speed_label.setText(str(self.speed_slider.value()))

    def start_traversal(self):
        if not self.tree_root:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng tạo một cây trước khi duyệt!")
            return

        self.traversal_index = 0
        self.traversal_result = []
        self.traversal_nodes = []
        self.canvas.selected_nodes.clear()
        self.canvas.display_tree(self.tree_root)

        traversal_type = self.traversal_type_combo.currentText()
        if traversal_type == "Preorder":
            self.traversal_nodes = self.preorder(self.tree_root)
        elif traversal_type == "Inorder":
            self.traversal_nodes = self.inorder(self.tree_root)
        elif traversal_type == "Postorder":
            self.traversal_nodes = self.postorder(self.tree_root)

        self.traversal_step()

    def traversal_step(self):
        if self.traversal_index < len(self.traversal_nodes):
            current_node = self.traversal_nodes[self.traversal_index]
            self.traversal_result.append(current_node)

            # Cập nhật danh sách các nút đã duyệt ngay lập tức
            self.node_list_textbox.setPlainText(" -> ".join(map(str, self.traversal_result)))

            self.canvas.selected_nodes.clear()
            self.canvas.selected_nodes.add(current_node)
            self.canvas.display_tree(self.tree_root)
            self.traversal_index += 1

            # Tính toán thời gian chờ theo giá trị của thanh trượt
            delay = max(100, (100 - self.speed_slider.value()) * 10)
            QtCore.QTimer.singleShot(delay, self.traversal_step)
        else:
            QtCore.QTimer.singleShot(1000, self.reset_tree_colors)

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
