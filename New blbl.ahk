#Warn
#SingleInstance Force


; 鼠标按键映射
XButton1::Right
XButton2::Left

; 鼠标中键 → 切换到屏幕1（固定编号1）
MButton::MoveToScreen(2)

; Ctrl+鼠标右键 → 切换到屏幕2（固定编号2）
^RButton::MoveToScreen(1)

; 初始化设置
HotkeyModifiers := "!^"  ; Alt+Ctrl
NumModifiers := StrLen(HotkeyModifiers)

; 存储各显示器中心坐标
MoveToX := Map()
MoveToY := Map()

; 获取显示器信息
CoordMode "Mouse", "Screen"
global NumMons := MonitorGetCount()  ; 全局变量

; 注册Alt+Ctrl+0返回主显示器
Hotkey HotkeyModifiers "0", MoveMousePrimary

; 遍历所有显示器并存储中心坐标
Loop NumMons {
    MonNum := A_Index
    if MonitorGet(MonNum, &Left, &Top, &Right, &Bottom) {
        ; 计算显示器中心坐标
        MoveX := Floor(0.5 * (Right - Left))
        MoveY := Floor(0.5 * (Bottom - Top))
        MoveToX[MonNum] := Left + MoveX
        MoveToY[MonNum] := Top + MoveY
        
        ; 注册Alt+Ctrl+数字键热键
        Hotkey HotkeyModifiers MonNum, MoveToScreen.Bind(MonNum)
    }
}

; 通用显示器切换函数
MoveToScreen(MonNum) {
    global MoveToX, MoveToY, NumMons
    
    ; 检查显示器编号是否有效
    if (MonNum > 0 && MonNum <= NumMons) {
        if MoveToX.Has(MonNum) && MoveToY.Has(MonNum) {
            MouseMove MoveToX[MonNum], MoveToY[MonNum]
        }
    } else {
        MsgBox "无效的显示器编号: " MonNum
    }
}

; 主显示器切换函数（Alt+Ctrl+0仍然有效）
MoveMousePrimary(*) {
    PrimaryMonNum := MonitorGetPrimary()
    global MoveToX, MoveToY
    
    if MoveToX.Has(PrimaryMonNum) && MoveToY.Has(PrimaryMonNum) {
        MouseMove MoveToX[PrimaryMonNum], MoveToY[PrimaryMonNum]
    }
}