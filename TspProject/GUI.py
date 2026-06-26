import tkinter as tk
from tkinter import ttk, messagebox
from GA import *  # 导入遗传算法模块
import matplotlib
matplotlib.use("TkAgg")  # 配置Tkinter后端
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class TravelPlannerGUI:
    def __init__(self, master):
        import os
        os.environ['MATPLOTLIB_IGNORE_PNG_WARNINGS'] = '1'
        self.master = master
        self.master.title("旅行规划路径优化")
        self.master.geometry("1200x800")
        self.master.configure(bg=BG_COLOR)

        # 全局变量
        self.select_site = []  # 已选景点列表（第一个为起点）
        self.site_buttons = {}  # 存储景点按钮对象（名称: 按钮）
        self.sites = [  # 51个景点与zuobiao.txt一致）
            "北京", "上海", "天津", "重庆", "哈尔滨", "长春", "沈阳", "呼和浩特",
            "石家庄", "太原", "济南", "郑州", "西安", "兰州", "银川", "西宁",
            "乌鲁木齐", "合肥", "南京", "杭州", "长沙", "南昌", "武汉", "成都",
            "贵阳", "福州", "台北", "广州", "海口", "南宁", "昆明", "拉萨",
            "香港", "澳门", "唐山", "洛阳", "黄山", "衡阳", "海东", "德阳",
            "白银", "铜川", "阳泉", "青岛", "芜湖", "三亚", "庆阳", "桂林",
            "肇庆", "衡水", "周口"
        ]

        # 初始化界面
        self.create_widgets()

    def create_widgets(self):
        # 标题标签
        tk.Label(
            self.master,
            text="旅行路径优化",
            font=("微软雅黑", 18, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=10)

        # 操作提示标签
        tk.Label(
            self.master,
            text="请先选择起点，再选择其他要经过的景点",
            font=FONT,
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=5)

        # 景点按钮网格布局（8行7列）
        btn_frame = tk.Frame(self.master, bg=BG_COLOR)
        btn_frame.pack(pady=10, padx=20, fill="x")

        # 动态创建景点按钮（保存按钮引用以便修改样式）
        for idx, site in enumerate(self.sites):
            row = idx // 7
            col = idx % 7
            btn = ttk.Button(
                btn_frame,
                text=site,
                style="TButton",
                command=lambda s=site: self.select_site_handler(s)
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            self.site_buttons[site] = btn  # 保存按钮到字典
            # 列/行权重设置（自适应大小）
            btn_frame.grid_columnconfigure(col, weight=1)
            btn_frame.grid_rowconfigure(row, weight=1)

        # 全选/清空按钮区域
        control_frame = tk.Frame(self.master, bg=BG_COLOR)
        control_frame.pack(pady=10)

        ttk.Button(
            control_frame,
            text="全选",
            command=self.select_all,
            style="Accent.TButton"
        ).pack(side="left", padx=10)

        ttk.Button(
            control_frame,
            text="清空",
            command=self.clear_all,
            style="Danger.TButton"
        ).pack(side="left", padx=10)

        # 已选景点显示区域
        tk.Label(
            self.master,
            text="已选景点（第一个为起点）：",
            font=FONT,
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=5)

        self.selected_text = tk.Text(
            self.master,
            height=3,
            width=80,
            font=FONT,
            bg="white",
            bd=2,
            relief="groove"
        )
        self.selected_text.pack(pady=5)

        # 输出方案数量输入
        tk.Label(
            self.master,
            text="请输入输出方案个数：",
            font=FONT,
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=5)

        self.output_entry = ttk.Entry(
            self.master,
            font=FONT,
            width=10
        )
        self.output_entry.pack(pady=5)

        # 运行按钮
        ttk.Button(
            self.master,
            text="生成可能最优路径",
            command=self.run_ga,
            style="Primary.TButton",
            width=20
        ).pack(pady=20)

        # 配置ttk样式（需在创建按钮前注册）
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton",
                        background=BUTTON_BG,
                        foreground=TEXT_COLOR,
                        font=FONT,
                        padding=5,
                        borderwidth=1)
        style.map("TButton",
                  background=[("active", BUTTON_ACTIVE_BG), ("pressed", BUTTON_ACTIVE_BG)])
        style.configure("Accent.TButton", background="#4CAF50", foreground="white", padding=5)  # 全选（绿色）
        style.configure("Danger.TButton", background="#f44336", foreground="white", padding=5)  # 清空（红色）
        style.configure("Primary.TButton",
                        background="#2196F3",
                        foreground="white",
                        padding=5,
                        font=FONT)

    def select_site_handler(self, site):
        """景点按钮点击事件：添加/移除景点并更新按钮颜色"""
        if site in self.select_site:
            # 记录原起点索引
            old_origin_index = 0 if self.select_site else -1
            # 记录删除的是否是原起点
            is_deleting_origin = site == self.select_site[0] if self.select_site else False
            # 移除景点
            self.select_site.remove(site)
            # 更新文本框：使用空格连接所有景点
            self.selected_text.delete("1.0", tk.END)
            self.selected_text.insert(tk.END, " ".join(self.select_site))
            # 恢复按钮颜色（未选中）
            self.site_buttons[site].configure(style="TButton")
            messagebox.showinfo("提示", f"已取消选择：{site}")
            # 如果删除的是原起点且还有其他景点，更新新起点的颜色
            if is_deleting_origin and self.select_site:
                new_origin = self.select_site[0]
                self.site_buttons[new_origin].configure(style="Accent.TButton")
        else:
            # 添加景点（第一个为起点）
            if not self.select_site:
                self.select_site.append(site)
                # 更新文本框：直接插入景点名称（带空格）
                self.selected_text.insert(tk.END, site + " ")
                # 起点按钮设为绿色
                self.site_buttons[site].configure(style="Accent.TButton")
                messagebox.showinfo("提示", f"已设置起点：{site}")
            else:
                self.select_site.append(site)
                # 获取当前文本框内容
                current_text = self.selected_text.get("1.0", tk.END).strip()
                # 清空并重新插入内容（确保末尾有空格）
                self.selected_text.delete("1.0", tk.END)
                self.selected_text.insert(tk.END, current_text + " " + site + " ")
                # 途经点按钮设为蓝色
                self.site_buttons[site].configure(style="Primary.TButton")
                #messagebox.showinfo("提示", f"已添加景点：{site}")
    def select_all(self):
        """全选所有景点（第一个为起点）"""
        self.select_site = self.sites.copy()
        self.selected_text.delete("1.0", tk.END)
        self.selected_text.insert(tk.END, " ".join(self.select_site))
        # 更新所有按钮颜色（起点绿色，其他蓝色）
        for idx, site in enumerate(self.sites):
            if idx == 0:
                self.site_buttons[site].configure(style="Accent.TButton")
            else:
                self.site_buttons[site].configure(style="Primary.TButton")

    def clear_all(self):
        """清空所有选择并恢复按钮颜色"""
        self.select_site.clear()
        self.selected_text.delete("1.0", tk.END)
        # 恢复所有按钮颜色
        for site in self.sites:
            self.site_buttons[site].configure(style="TButton")
        self.output_entry.delete(0, tk.END)

    def run_ga(self):
        # 获得输出方案个数

        # 检查是否选择了景点（第一个为起点）
        if len(self.select_site) < 1:  # 改为 self.select_site
            messagebox.showerror("未选择地点", "请至少选择起点和一个其他景点！")
            return

        # 起点及地点对应整数编码（传递 self.select_site）
        origin, select_site_index = get_origin(self.select_site)  # 改为 self.select_site
        if not select_site_index:  # 没有其他景点时
            messagebox.showinfo("提示", "仅选择了起点，无需规划路径。")
            return

        try:
            output = int(self.output_entry.get())
            if output <= 0:
                raise ValueError
        except:
            messagebox.showerror("输入错误", "请输入正整数作为输出方案个数！")
            return

        # 初始化种群并迭代进化
        population = generate_population(select_site_index)
        register = []  # 记录每代最优距离
        for i in range(itter_time):
            parents = selection(population, origin)
            children = crossover(parents)
            mutation(children)
            population = parents + children
            # 更新最优解记录
            DistanceAndPath = get_result(population, origin)
            register.append(DistanceAndPath[0][0])

        # 处理输出结果
        DistanceAndPath = get_result(population, origin)
        if len(DistanceAndPath) < output:
            output = len(DistanceAndPath)
            messagebox.showwarning("提示", f"当前仅找到{output}个有效方案，将输出所有可用方案。")

        best_path = [index_site_dict[origin]] + [index_site_dict[idx] for idx in DistanceAndPath[0][1]]

        graded = get_result(population, origin)
        best_results = graded[:output]  # 取前output个最优方案

        # 转换结果为景点名称并显示
        result_msg = "最优路径方案（按距离由短到长排序）：\n\n"
        for idx, (distance, path_indices) in enumerate(best_results):
            # 将索引转换为景点名称（起点→路径→起点）
            path_sites = [index_site_dict[origin]]  # 起点
            path_sites += [index_site_dict[i] for i in path_indices]  # 途经点
            path_sites.append(index_site_dict[origin])  # 返回起点
            result_msg += f"方案 {idx + 1}（总距离：{distance:.2f}）：\n"
            result_msg += " → ".join(path_sites) + "\n\n"

        # 显示结果消息框
        messagebox.showinfo("最优路径结果", result_msg)

        # 生成每个方案的路径图和趋势图
        for j in range(output):
            # 提取当前方案的路径和距离
            result_path = DistanceAndPath[j][1]
            distance = DistanceAndPath[j][0]
            path_name = [index_site_dict[origin]] + [index_site_dict[idx] for idx in result_path]

            # 绘制路径图（独立窗口）
            plt.figure(f"方案{j + 1}_路径图", figsize=(8, 6))
            draw(origin, result_path, distance)  # 复用原draw函数

            # 绘制迭代趋势图（独立窗口）
            plt.figure(f"方案{j + 1}_趋势图", figsize=(8, 6))
            plt.plot(range(len(register)), register, color='blue')
            plt.title(f"方案{j + 1}迭代趋势（总距离：{distance:.2f}）")
            plt.xlabel("迭代次数")
            plt.ylabel("最优路径总距离")
            plt.grid(True)

        # 显示所有图形（阻塞模式，关闭所有窗口后继续）
        plt.show()

    def draw_path_window(self, origin, path_indices, distance):
        """弹出新窗口显示路径图"""
        top = tk.Toplevel(self.master)
        top.title("路径可视化")
        top.geometry("1000x600")

        # 创建matplotlib图表
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111)

        # 绘制所有景点散点
        ax.scatter(site_coordinate[:, 0], site_coordinate[:, 1], color='blue', label='景点')
        for i in range(len(site_coordinate)):
            ax.text(site_coordinate[i, 0], site_coordinate[i, 1], site_name[i], fontsize=8)

        # 绘制最优路径（起点→路径→起点）
        x_coords = [site_coordinate[origin, 0]]
        y_coords = [site_coordinate[origin, 1]]
        for idx in path_indices:
            x_coords.append(site_coordinate[idx, 0])
            y_coords.append(site_coordinate[idx, 1])
        x_coords.append(site_coordinate[origin, 0])
        y_coords.append(site_coordinate[origin, 1])

        ax.plot(x_coords, y_coords, 'r-', label='最优路径')
        ax.scatter(x_coords, y_coords, color='red', s=50)
        ax.scatter([x_coords[0]], [y_coords[0]], color='green', s=150, label='起点')  # 起点特殊标记
        ax.set_title(f"最优路径（总距离：{distance:.2f}）")
        ax.legend()

        # 将图表嵌入Tkinter窗口
        canvas = FigureCanvasTkAgg(fig, master=top)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


if __name__ == "__main__":
    # 全局配置（与GA.py兼容）
    BG_COLOR = "#E6F4F1"  # 主背景色（浅蓝）
    BUTTON_BG = "#F0F0F0"  # 按钮默认背景色（浅灰）
    BUTTON_ACTIVE_BG = "#2196F3"  # 按钮激活背景色（亮蓝）
    TEXT_COLOR = "#333333"  # 文字颜色（深灰）
    FONT = ("微软雅黑", 10)  # 统一字体

    root = tk.Tk()
    app = TravelPlannerGUI(root)
    root.mainloop()