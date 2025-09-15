import React from "react";

const navItems = Array.from({ length: 5 }).map((_, i) => `导航 ${i + 1}`);

export default function App() {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <header className="flex items-center bg-gray-900 text-white px-6 shadow-md">
        <div className="text-2xl font-bold mr-8 select-none">Logo</div>
        <nav className="flex flex-1 min-w-0 overflow-x-auto scrollbar-hide">
          {navItems.map((item, idx) => (
            <button
              key={item}
              className={`whitespace-nowrap px-4 py-3 focus:outline-none ${
                idx === 1
                  ? "bg-gray-700 font-semibold rounded-md"
                  : "hover:bg-gray-700 rounded-md"
              }`}
            >
              {item}
            </button>
          ))}
        </nav>
      </header>

      <main className="flex-1 px-12 py-6 max-w-7xl mx-auto w-full">
        <nav className="text-sm text-gray-500 mb-4 select-none" aria-label="Breadcrumb">
          <ol className="list-none p-0 inline-flex space-x-2">
            <li>首页</li>
            <li>/</li>
            <li>列表</li>
            <li>/</li>
            <li className="font-semibold text-gray-900">应用</li>
          </ol>
        </nav>

        <section className="bg-white rounded-lg shadow-md p-6 min-h-[280px]">
          <h2 className="text-xl font-semibold mb-4 text-gray-800">内容区域</h2>
          <p className="text-gray-600 leading-relaxed">
            使用此布局作为通用前端代码结构示例，包含响应式导航、面包屑导航及内容卡片式布局，符合当代设计语言及可用性原则。
          </p>
        </section>
      </main>

      <footer className="text-center text-gray-500 py-4 select-none border-t border-gray-200">
        通用前端布局 ©{new Date().getFullYear()} 设计示例
      </footer>
    </div>
  );
}