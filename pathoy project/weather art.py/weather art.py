import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
import os
from datetime import datetime, timedelta

class WeatherDataVisualizer:
    def __init__(self):
        # 设置中文字体支持 (可选)
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 创建图形和轴
        self.fig, self.ax = plt.subplots(figsize=(12, 8), facecolor='black')
        self.fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
        
        # 设置轴属性
        self.ax.set_facecolor('black')
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(-3, 3)
        self.ax.axis('off')
        
        # 创建自定义颜色映射 - 从冷色到暖色
        self.cmap = LinearSegmentedColormap.from_list(
            'weather_cmap', 
            ['#2E3192', '#1BFFFF', '#FFFFFF', '#FFD700', '#FF4500']
        )
        
        # 初始化数据
        self.data = self.generate_sample_data()
        self.lines = []
        self.setup_visual_elements()
        
    def setup_visual_elements(self):
        """初始化可视化元素"""
        # 创建多条波形线
        for i in range(5):
            line, = self.ax.plot([], [], lw=2.5, alpha=0.7)
            self.lines.append(line)
            
        # 添加标题
        self.title = self.ax.text(
            5, 2.5, "气象数据艺术可视化", 
            color='white', ha='center', fontsize=16, alpha=0.8
        )
        
        # 添加日期文本
        self.date_text = self.ax.text(
            0.5, -2.5, "", 
            color='white', ha='center', fontsize=12, alpha=0.7
        )
        
        # 添加数据说明文本
        self.info_text = self.ax.text(
            9.5, -2.5, "", 
            color='white', ha='right', fontsize=10, alpha=0.6
        )
    
    def generate_sample_data(self):
        """生成示例气象数据"""
        print("生成模拟气象数据...")
        
        # 创建日期范围（最近30天）
        dates = [datetime.now() - timedelta(days=i) for i in range(30)]
        
        # 生成更有规律的气象数据（不是完全随机）
        base_temp = 20 + 5 * np.sin(np.linspace(0, 2*np.pi, 30))
        base_humidity = 60 + 15 * np.sin(np.linspace(0, 2*np.pi, 30) + 0.5)
        base_wind = 5 + 3 * np.sin(np.linspace(0, 2*np.pi, 30) + 1)
        
        # 添加一些随机变化
        data = {
            'date': [d.strftime('%Y-%m-%d') for d in dates],
            'temperature': base_temp + np.random.normal(0, 1, 30),
            'humidity': base_humidity + np.random.normal(0, 3, 30),
            'wind_speed': np.abs(base_wind + np.random.normal(0, 1, 30))  # 确保风速不为负
        }
        
        return pd.DataFrame(data)
    
    def process_data(self, frame):
        """处理数据用于可视化"""
        # 选择数据点（循环播放）
        idx = frame % len(self.data)
        
        # 获取气象数据
        temp = self.data['temperature'].iloc[idx]
        humidity = self.data['humidity'].iloc[idx]
        wind = self.data['wind_speed'].iloc[idx]
        
        # 将气象数据转换为可视化参数
        temp_min = self.data['temperature'].min()
        temp_max = self.data['temperature'].max()
        
        frequency = 0.5 + 1.5 * (temp - temp_min) / (temp_max - temp_min)
        amplitude = 0.5 + 1.0 * humidity / 100
        complexity = 1 + wind / 5
        
        return idx, frequency, amplitude, complexity
    
    def generate_waveform(self, frequency, amplitude, complexity, line_idx):
        """生成波形数据"""
        x = np.linspace(0, 10, 1000)
        
        # 基础波形
        y = amplitude * np.sin(frequency * x + line_idx * np.pi/2)
        
        # 添加谐波增加复杂性
        for i in range(1, int(complexity) + 1):
            harmonic_amp = amplitude / (i * 2)
            harmonic_freq = frequency * (i + 0.5)
            phase_shift = line_idx * np.pi / (i + 1)
            y += harmonic_amp * np.sin(harmonic_freq * x + phase_shift)
        
        # 添加噪声模拟自然变化
        noise = np.random.normal(0, 0.05 * complexity, len(x))
        y += noise
        
        return x, y
    
    def update(self, frame):
        """动画更新函数"""
        idx, frequency, amplitude, complexity = self.process_data(frame)
        
        # 更新每条波形线
        for i, line in enumerate(self.lines):
            x, y = self.generate_waveform(frequency, amplitude, complexity, i)
            
            # 根据温度数据设置颜色
            norm_temp = (self.data['temperature'].iloc[idx] - 
                         self.data['temperature'].min()) / (
                         self.data['temperature'].max() - self.data['temperature'].min())
            color = self.cmap(norm_temp)
            
            line.set_data(x, y)
            line.set_color(color)
            line.set_alpha(0.5 + 0.5 * (i / len(self.lines)))
        
        # 更新日期文本
        current_date = self.data['date'].iloc[idx]
        self.date_text.set_text(f"日期: {current_date}")
        
        # 更新数据信息文本
        temp = self.data['temperature'].iloc[idx]
        humidity = self.data['humidity'].iloc[idx]
        wind = self.data['wind_speed'].iloc[idx]
        self.info_text.set_text(f"温度: {temp:.1f}°C, 湿度: {humidity:.1f}%, 风速: {wind:.1f}m/s")
        
        return self.lines + [self.date_text, self.info_text]
    
    def create_animation(self):
        """创建动画"""
        print("创建动画...")
        frames = len(self.data) * 2  # 播放两次数据周期
        interval = 300  # 毫秒
        
        ani = FuncAnimation(
            self.fig, self.update, frames=frames, 
            interval=interval, blit=True, repeat=True
        )
        
        return ani

def main():
    # 创建输出目录
    os.makedirs('output', exist_ok=True)
    
    # 创建可视化器
    visualizer = WeatherDataVisualizer()
    
    # 创建动画
    ani = visualizer.create_animation()
    
    # 尝试保存动画
    try:
        print("保存动画为MP4文件...")
        ani.save('output/weather_visualization.mp4', writer='ffmpeg', fps=5, dpi=100, 
                 extra_args=['-vcodec', 'libx264'])
        print("动画已保存到 output/weather_visualization.mp4")
    except Exception as e:
        print(f"无法保存MP4文件: {e}")
        print("尝试保存为GIF...")
        try:
            ani.save('output/weather_visualization.gif', writer='pillow', fps=5, dpi=100)
            print("动画已保存到 output/weather_visualization.gif")
        except Exception as e2:
            print(f"也无法保存GIF文件: {e2}")
    
    # 显示动画
    print("显示动画...关闭窗口以退出")
    plt.show()

if __name__ == "__main__":
    main()