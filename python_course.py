import streamlit as st
import streamlit.components.v1 as components


def render_python_course():
    # 注入与 app.py 一致的全局样式
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stApp { background-color: #F8FDFF; }
        [data-testid="stSidebar"] { 
            background-color: #012a4a; 
            min-width: 260px !important;
        }
        [data-testid="stSidebar"] * { color: white !important; }
        </style>
    """, unsafe_allow_html=True)

    # 侧边栏内容
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;'>Be.Robot</h2>", unsafe_allow_html=True)
        st.divider()
        st.markdown("#### 🐍 Py启蒙坊")
        st.info("照着学 · 随手改 · 立即跑")
        st.divider()
        st.caption("当前章节：Python 基础启蒙")

    # 嵌入增强版交互实验室
    html_code = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="utf-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <!-- 使用更稳定的 CDN 链接 -->
        <script src="https://cdn.jsdelivr.net/npm/skulpt@1.2.0/dist/skulpt.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/skulpt@1.2.0/dist/skulpt-stdlib.js"></script>

        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.12/codemirror.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.12/theme/dracula.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.12/codemirror.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.12/mode/python/python.min.js"></script>
        <style>
            .CodeMirror { height: 100%; border-radius: 0 0 1.5rem 1.5rem; font-family: 'Fira Code', monospace; font-size: 14px; }
            .tutorial-card { transition: all 0.2s; border: 1px solid #f1f5f9; cursor: pointer; }
            .tutorial-card:hover { border-color: #22c55e; background: #f0fdf4; }
            .active-card { border-left: 5px solid #22c55e; background: #f0fdf4; }
            ::-webkit-scrollbar { width: 4px; }
            ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
        </style>
    </head>
    <body class="bg-[#F8FDFF] p-2">
        <div class="flex h-[96vh] gap-4">
            <!-- 左侧教程面板 (严格遵循 .docx 文档) -->
            <div class="w-1/3 flex flex-col space-y-3 overflow-y-auto pr-2">
                <div class="p-5 bg-white rounded-3xl shadow-sm border border-green-100">
                    <h2 class="text-xl font-black text-gray-800">📘 Python 启蒙手册</h2>
                    <p class="text-[11px] text-gray-500 mt-2">Python 是一种让计算机“听懂我们的话”的魔法语言。点击卡片载入代码，点击释放魔法查看结果。</p>
                </div>

                <div class="space-y-3">
                    <!-- 卡片 1 -->
                    <div onclick="updateEditor('print(\\'Hello, 编程少年!\\')\\nprint(\\'Python 很有趣!\\')', this)" class="tutorial-card active-card p-4 bg-white rounded-2xl shadow-sm">
                        <div class="flex justify-between font-bold text-[10px] mb-1">
                            <span class="text-green-600 uppercase">Level 1</span>
                            <span class="text-gray-400">▶ 试试看</span>
                        </div>
                        <h3 class="font-bold text-gray-800 text-sm">让计算机“说话”</h3>
                        <p class="text-[11px] text-gray-500 mt-1">print 就像计算机的“嘴巴”。</p>
                    </div>

                    <!-- 卡片 2 -->
                    <div onclick="updateEditor('name = \\'小明\\'\\nage = 10\\nprint(\\'我叫\\', name, \\'今年\\', age, \\'岁\\')', this)" class="tutorial-card p-4 bg-white rounded-2xl shadow-sm">
                        <div class="flex justify-between font-bold text-[10px] mb-1">
                            <span class="text-blue-600 uppercase">Level 2</span>
                            <span class="text-gray-400">▶ 试试看</span>
                        </div>
                        <h3 class="font-bold text-gray-800 text-sm">贴标签的小盒子</h3>
                        <p class="text-[11px] text-gray-500 mt-1">变量用来存东西，并给它起个名字。</p>
                    </div>

                    <!-- 卡片 3 -->
                    <div onclick="updateEditor('score = 85\\nif score >= 60:\\n    print(\\'及格了，真棒！\\')\\nelse:\\n    print(\\'还要加油哦！\\')', this)" class="tutorial-card p-4 bg-white rounded-2xl shadow-sm">
                        <div class="flex justify-between font-bold text-[10px] mb-1">
                            <span class="text-purple-600 uppercase">Level 3</span>
                            <span class="text-gray-400">▶ 试试看</span>
                        </div>
                        <h3 class="font-bold text-gray-800 text-sm">智能选择</h3>
                        <p class="text-[11px] text-gray-500 mt-1">if 语句让程序变聪明，能做决定。</p>
                    </div>

                    <!-- 卡片 4 -->
                    <div onclick="updateEditor('for i in range(1, 6):\\n    print(f\\'第 {i} 次: 我爱编程\\')', this)" class="tutorial-card p-4 bg-white rounded-2xl shadow-sm">
                        <div class="flex justify-between font-bold text-[10px] mb-1">
                            <span class="text-orange-600 uppercase">Level 4</span>
                            <span class="text-gray-400">▶ 试试看</span>
                        </div>
                        <h3 class="font-bold text-gray-800 text-sm">重复执行</h3>
                        <p class="text-[11px] text-gray-500 mt-1">for 循环像数数，重复做同样的事。</p>
                    </div>

                    <!-- 卡片 5 -->
                    <div onclick="updateEditor('name = input(\\'你叫什么名字？\\')\\nprint(\\'你好呀，\\', name, \\'一起探索 Python 吧！\\')', this)" class="tutorial-card p-4 bg-white rounded-2xl shadow-sm">
                        <div class="flex justify-between font-bold text-[10px] mb-1">
                            <span class="text-pink-600 uppercase">Level 5</span>
                            <span class="text-gray-400">▶ 试试看</span>
                        </div>
                        <h3 class="font-bold text-gray-800 text-sm">交互输入</h3>
                        <p class="text-[11px] text-gray-500 mt-1">input() 让用户打字告诉计算机信息。</p>
                    </div>
                </div>

                <div class="mt-auto p-4 bg-blue-600 rounded-3xl text-white shadow-lg">
                    <p class="text-[10px] font-bold opacity-80 underline">✨ 小提示</p>
                    <p class="text-[11px] mt-1">使用 input 会弹出输入框，输入后程序才会继续！</p>
                </div>
            </div>

            <!-- 右侧编辑器和控制台 -->
            <div class="w-2/3 flex flex-col gap-4">
                <div class="flex-grow bg-[#282a36] rounded-[2rem] shadow-xl flex flex-col overflow-hidden border-[4px] border-white relative">
                    <div class="bg-[#191a21] px-6 py-3 flex justify-between items-center">
                        <div class="flex space-x-2">
                            <div class="w-3 h-3 rounded-full bg-red-500"></div>
                            <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
                            <div class="w-3 h-3 rounded-full bg-green-500"></div>
                        </div>
                        <span class="text-[10px] text-gray-500 font-bold uppercase tracking-widest">Magic_Editor.py</span>
                    </div>
                    <textarea id="code-editor"></textarea>

                    <button onclick="runPython()" id="run-btn" class="absolute bottom-6 right-6 bg-green-500 hover:bg-green-600 text-white px-8 py-4 rounded-2xl font-black shadow-2xl transition-all active:scale-95 z-20">
                        释放魔法 ▶
                    </button>
                </div>

                <div class="h-1/3 bg-white rounded-[2rem] shadow-lg border border-gray-100 flex flex-col overflow-hidden">
                    <div class="px-6 py-3 border-b bg-gray-50/50 flex justify-between items-center">
                        <span class="text-[10px] font-black text-gray-400 uppercase tracking-widest">📟 执行输出</span>
                        <button onclick="clearOutput()" class="text-[10px] text-gray-400 hover:text-red-500">清空</button>
                    </div>
                    <div id="output" class="p-6 font-mono text-gray-700 overflow-y-auto text-sm leading-relaxed whitespace-pre-wrap">✨ 等待魔法启动...</div>
                </div>
            </div>
        </div>

        <script>
            let editor;

            // 确保页面加载完成后初始化
            window.onload = function() {
                editor = CodeMirror.fromTextArea(document.getElementById("code-editor"), {
                    mode: "python",
                    theme: "dracula",
                    lineNumbers: true,
                    autoCloseBrackets: true,
                    lineWrapping: true,
                    indentUnit: 4
                });
                editor.setValue("print('🎉 你好，编程小探险家！')\\nprint('点击右下角的【释放魔法】试试看！')");
                console.log("Editor Initialized");
            };

            function outf(text) { 
                const outputArea = document.getElementById("output");
                if(outputArea.innerText.includes("等待") || outputArea.innerText.includes("已清空") || outputArea.innerText.includes("正在运行")) {
                    outputArea.innerText = "";
                }
                outputArea.innerText += text;
                outputArea.scrollTop = outputArea.scrollHeight;
            }

            function builtinRead(x) {
                if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
                    throw "File not found: '" + x + "'";
                return Sk.builtinFiles["files"][x];
            }

            function clearOutput() {
                document.getElementById("output").innerText = "🧹 输出已清空，请编写新咒语。";
            }

            async function runPython() {
                const code = editor.getValue();
                const outputArea = document.getElementById("output");
                const runBtn = document.getElementById("run-btn");

                outputArea.innerText = "⚙️ 正在运行 Python 代码...";
                runBtn.disabled = true;
                runBtn.style.opacity = "0.5";

                // 强制 Skulpt 配置
                Sk.configure({
                    output: outf,
                    read: builtinRead,
                    inputfun: (prompt) => window.prompt(prompt),
                    inputfunTakesPrompt: true,
                    __future__: Sk.python3
                });

                try {
                    await Sk.misceval.asyncToPromise(() => 
                        Sk.importMainWithBody("<stdin>", false, code, true)
                    );
                    runBtn.disabled = false;
                    runBtn.style.opacity = "1";
                    if(outputArea.innerText === "⚙️ 正在运行 Python 代码...") {
                        outputArea.innerText = "✅ 程序执行完毕（无打印内容）。";
                    }
                } catch (err) {
                    runBtn.disabled = false;
                    runBtn.style.opacity = "1";
                    outputArea.innerHTML = `<span class="text-red-500 font-bold">❌ 报错啦:</span>\\n<span class="text-red-400 font-mono">${err.toString()}</span>`;
                }
            }

            function updateEditor(code, el) {
                editor.setValue(code);
                document.querySelectorAll('.tutorial-card').forEach(c => c.classList.remove('active-card'));
                el.classList.add('active-card');
                // 延迟一下再运行，确保文字已载入
                setTimeout(runPython, 200);
            }
        </script>
    </body>
    </html>
    """

    components.html(html_code, height=880, scrolling=False)


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    render_python_course()