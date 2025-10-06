import React from "react";

const navItems = Array.from({ length: 5 }).map((_, i) => `导航 ${i + 1}`);

export default function App() {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-b from-blue-50 via-white to-blue-50">
      <header className="flex items-center bg-gradient-to-r from-blue-700 to-blue-900 text-white px-8 shadow-lg select-none sticky top-0 z-30">
        <div 
          className="text-3xl font-extrabold tracking-wide mr-10"
        >
          LOGO
        </div>
        <nav className="flex flex-1 min-w-0 overflow-x-auto scrollbar-hide py-3">
          {navItems.map((item, idx) => (
            <button
              key={item}
              className={`whitespace-nowrap px-5 py-3 mx-0.5 transition-all duration-300 transform ${
                idx === 1
                  ? "bg-white text-blue-900 font-bold rounded-md shadow-md"
                  : "text-white hover:bg-white hover:text-blue-900 rounded-md hover:scale-110 active:scale-95"
              }`}
            >
              {item}
            </button>
          ))}
        </nav>
      </header>

      <main className="flex-1 px-8 py-10 max-w-7xl mx-auto w-full flex flex-col">
        <nav
          className="text-sm text-blue-600 font-medium select-none mb-6"
          aria-label="Breadcrumb"
        >
          <ol className="list-none flex space-x-3">
            <li>首页</li>
            <li>/</li>
            <li>列表</li>
            <li>/</li>
            <li className="font-semibold text-blue-900">应用</li>
          </ol>
        </nav>

        <section className="bg-white rounded-xl shadow-xl p-8 min-h-[300px] flex flex-col">
          <h2
            className="text-2xl font-bold mb-5 text-gray-900"
          >
            内容区域
          </h2>
          <p
            className="text-gray-700 leading-relaxed max-w-prose"
          >
            此布局以简洁现代为设计核心，采用流畅渐变和明快配色，融合卡片阴影与圆角元素，营造清新且专业的视觉感受。导航交互采用缓和动画改善用户体验，内容结构清晰，适配多终端响应。整体设计体现了当代前端设计优雅且高效的风格。
          </p>
        </section>
      </main>

      <footer className="text-center text-blue-600 py-6 select-none border-t border-blue-200 bg-gradient-to-t from-blue-50">
        <div
          className="text-sm"
        >
          通用前端布局 ©{new Date().getFullYear()} 设计示例
        </div>
      </footer>
    </div>
  );
}
