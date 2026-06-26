# tsp-questions
基于遗传算法的旅行商问题研究--Python <br>
旅行商问题（Travelling Salesman Problem，TSP）是一个著名的组合优化问题，同
时也是一个 NP 完全问题，问题具体描述为：给定一组城市，寻求从城市中的某一个城
市出发访问其他城市一次且仅一次，最后回到该城市的最短回路。旅行商问题在实际应
用中有着强大的生命力和广泛的前景，例如在超大规模集成芯片制造、电路板设计、机
器人控制等领域。
构建了基于遗传算法的旅行商求解方案，以中国 51 个城市为研究对象，深入了解
遗传算法的起源、理论基础（模式定理、积木块假设等）及构成要素，涵盖编码方法、
适应度函数设计、遗传算子（选择、交叉、变异）和运行参数等内容。在算法实现阶段，
采用十进制编码方式将城市序列映射为基因串，将城市坐标转化为距离矩阵，通过轮盘
赌选择、顺序交叉和逆序变异等操作构建完整的遗传算法流程，并设计交互界面实现路
径规划与结果可视化。
通过实验分析种群规模、变异概率和迭代次数这三个关键参数对算法收敛性的影响，
经过不断试算得到最佳旅行路线，并确定最优的参数值。与暴力穷举法相比，遗传算法
的时间复杂度从 O(n!)降至 O(T×count×max{count, 2 n })，空间复杂度从 O(n!)降至 O(count
×n)，验证了其在求解大规模组合优化问题时的有效性和实用性。<br>
![image]https://github.com/guorenwei0121/tsp-questions/blob/main/TspProject/images/ui.png
![image]https://github.com/guorenwei0121/tsp-questions/blob/main/TspProject/images/answer.png
![image]https://github.com/guorenwei0121/tsp-questions/blob/main/TspProject/images/path1.png 
![image]https://github.com/guorenwei0121/tsp-questions/blob/main/TspProject/images/trend1.png  
![image]https://github.com/guorenwei0121/tsp-questions/blob/main/TspProject/images/path2.png   
![image]https://github.com/guorenwei0121/tsp-questions/blob/main/TspProject/images/trend2.png
