import React from "react";

const navItems = Array.from({ length: 5 }).map((_, i) => `导航 ${i + 1}`);

export default function App() {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-indigo-50 via-purple-100 to-pink-50">
      {/* 顶部导航 - 使用玻璃拟态风格 */}
      <header className="flex items-center backdrop-blur-sm bg-white/30 text-indigo-900 px-8 shadow-md select-none">
        <div className="text-3xl font-extrabold tracking-widest mr-10">LOGO</div>
        <nav className="flex flex-1 min-w-0 overflow-x-auto scrollbar-hide space-x-4">
          {navItems.map((item, idx) => (
            <button
              key={item}
              className={`whitespace-nowrap px-5 py-3 rounded-lg text-sm font-medium transition-colors duration-300 ${
                idx === 1
                  ? "bg-indigo-700 text-white shadow-lg shadow-indigo-500/40"
                  : "text-indigo-700 hover:bg-indigo-300/70 hover:shadow-md hover:shadow-indigo-300/40"
              }`}
            >
              {item}
            </button>
          ))}
        </nav>
      </header>

      {/* 中间内容区域 - 卡片风与渐变边框 */}
      <main className="flex-1 px-16 py-10 max-w-6xl mx-auto w-full">
        <nav
          className="text-sm text-indigo-600/70 mb-6 select-none"
          aria-label="Breadcrumb"
        >
          <ol className="list-none p-0 inline-flex space-x-3 font-semibold tracking-wide">
            <li>首页</li>
            <li>/</li>
            <li>列表</li>
            <li>/</li>
            <li className="text-indigo-900">应用</li>
          </ol>
        </nav>

        <section className="bg-white rounded-2xl shadow-xl border border-transparent bg-gradient-to-r from-pink-300 via-purple-300 to-indigo-300 p-1">
          <div className="bg-white rounded-xl p-8 min-h-[280px] flex flex-col justify-center">
            <h2 className="text-3xl font-extrabold mb-5 text-indigo-800 tracking-tight">
              内容区域
            </h2>
            <p className="text-indigo-700 leading-relaxed text-lg max-w-prose">
              本示例采用明快的渐变与玻璃拟态风格，结合卡片式有层次感的设计，带来清新且现代的视觉体验。导航、面包屑与内容区相辅相成，整体布局协调，适应多种设备屏幕。
            </p>
          </div>
        </section>
      </main>

      {/* 底部页脚 - 极简渐变分割线与细文字 */}
      <footer className="text-center text-indigo-700 text-sm py-6 border-t border-indigo-300 select-none bg-gradient-to-t from-indigo-50">
        通用前端布局 ©{new Date().getFullYear()} 设计示例
      </footer>
    </div>
  );
}