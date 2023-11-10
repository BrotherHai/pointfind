import numpy as np
import streamlit as st  
import pandas as pd  
import matplotlib.pyplot as plt  
  
@st.cache  
def load_data(file_path): 
    data = file_path.getvalue().decode("utf-8")
    
    # 将文本数据转换为行列表
    lines = data.split('\n')
    
    # 找到数据开始的行数
    data_start_line = 0
    for i, line in enumerate(lines):
        if line.startswith("Potential/V"):
            data_start_line = i
            break
    df=pd.read_csv(file_path,skiprows=data_start_line-1,encoding="gbk",engine='python',sep=',',delimiter=None,skipinitialspace=True)
     
    df['C']=-1/(2*3.1415926*1000*df['Z"/ohm'])
    df['1/(C*C)']=1/(df['C']*df['C'])   
    return df
# buttons = st.sidebar.button("")
  
def select_axes(data):  
    x_axis_options = data.columns  
    y_axis_options = data.columns  
    selected_x_axis = st.sidebar.selectbox("选择X轴", x_axis_options)  
    selected_y_axis = st.sidebar.selectbox("选择Y轴", y_axis_options)  
    buttons = st.sidebar.button("生成曲线图")
    return selected_x_axis, selected_y_axis, buttons 
  
def draw_plot(df):  
    # plot the curve
    x = df['Potential/V']
    y = df['1/(C*C)']
    plt.plot(x, y)

    # find the maximum slope row
    slope = np.gradient(y, x)
    max_slope_row = np.argmax(slope)
    x_intercept = -y[max_slope_row]/slope[max_slope_row]

    # plot the tangent line
    tangent_x = np.linspace(x.iloc[0], x.iloc[-1], 100)
    tangent_y = slope[max_slope_row]*(tangent_x-x.iloc[max_slope_row])+y.iloc[max_slope_row]
    plt.plot(tangent_x, tangent_y)
    # 使用numpy的polyfit函数找到最佳拟合直线的斜率和截距  
    slope, intercept = np.polyfit(tangent_x, tangent_y, 1)  
    
    # 使用斜率和截距计算直线与x轴的交点  
    x_intercept = -intercept / slope  
    
    print("The intersection point is at x =", x_intercept)
    plt.scatter(x_intercept, 0, c='r')
    plt.text(x_intercept+0.02, 0.5, '({:.2f}, {:.2f})'.format(x_intercept, 0))
    # plot the intercepts
    # plt.plot([x_intercept, x_intercept], [0, y.iloc[max_slope_row]], 'r--')
    # plt.plot([0, x.iloc[max_slope_row]], [y.iloc[max_slope_row], y.iloc[max_slope_row]], 'r--')

    # set the labels and title
    plt.xlabel('Potential/V')
    plt.ylabel('1/(C*C)')
    plt.title('Curve with maximum slope tangent line')
    # plt.ylim(0, max(y))
    plt.axhline(0,color='black')
    # show the plot
    # plt.show()
    st.pyplot(plt)  
  
if __name__ == "__main__":  
    # st.set_page_config(layout="centered", width="80%")  
    st.title("用Potential/V为横坐标，1/c方做纵坐标，画曲线")  
    st.write("上传你的文件txt，自动计算1/c方并找到最大斜率的切线及与X轴的交点")  
  
    # 文件上传  
    uploaded_file = st.file_uploader("上传文件")  
    if uploaded_file is not None :  
        data = load_data(uploaded_file)  
        draw_plot(data)
