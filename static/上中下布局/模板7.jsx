import React from "react";

const navItems = Array.from({ length: 5 }).map((_, i) => `菜单 ${i + 1}`);

export default function App() {
  return (
    <div className="min-h-screen flex flex-col bg-neutral-900 text-neutral-100">
      {/* 顶部导航 - 深色模式+分割线+简洁按钮 */}
      <header className="flex items-center justify-between px-8 py-4 border-b border-neutral-700 select-none">
        <div className="text-2xl font-semibold tracking-widest">品牌</div>
        <nav className="flex space-x-6 overflow-x-auto scrollbar-hide text-neutral-300">
          {navItems.map((item, idx) => (
            <button
              key={item}
              className={`whitespace-nowrap px-3 py-2 rounded-md transition-colors duration-200 text-sm font-medium ${
                idx === 1
                  ? "bg-neutral-700 text-white shadow-md"
                  : "hover:bg-neutral-700/50"
              }`}
            >
              {item}
            </button>
          ))}
        </nav>
      </header>

      {/* 中间内容 - 两栏布局+卡片阴影+暗色渐变背景 */}
      <main className="flex-1 max-w-7xl mx-auto px-8 py-10 w-full grid grid-cols-1 md:grid-cols-3 gap-8">
        <section className="md:col-span-2 bg-neutral-800 rounded-lg shadow-lg p-8 flex flex-col">
          <nav
            aria-label="Breadcrumb"
            className="text-neutral-400 mb-6 select-none tracking-wide text-sm"
          >
            <ol className="inline-flex list-none p-0 space-x-2">
              <li>首页</li>
              <li>/</li>
              <li>目录</li>
              <li>/</li>
              <li className="font-semibold text-neutral-100">详情</li>
            </ol>
          </nav>
          <h2 className="text-3xl font-bold mb-4 text-neutral-100">主要内容</h2>
          <p className="text-neutral-300 leading-relaxed flex-grow">
            采用暗色主题并结合多栏网格布局，左侧以优雅的阴影卡片呈现主内容区域，提升内容层次感和阅读体验。面包屑导航简洁明了，配合整体暗色调氛围，适合夜间使用和专业应用。
          </p>
        </section>

        <aside className="bg-neutral-800 rounded-lg shadow-md p-6 flex flex-col space-y-4">
          <h3 className="text-xl font-semibold text-neutral-100">侧边栏</h3>
          <p className="text-neutral-400 text-sm leading-relaxed">
            这里可以放置辅助信息、快捷链接或者活动通知，保持界面信息丰富但不拥挤。
          </p>
          <button className="mt-auto px-4 py-2 bg-indigo-600 rounded-md font-semibold hover:bg-indigo-500 transition-colors">
            操作按钮
          </button>
        </aside>
      </main>

      {/* 底部页脚 - 简洁浅色文字 */}
      <footer className="text-center text-neutral-500 text-xs py-5 border-t border-neutral-700 select-none bg-neutral-900">
        © {new Date().getFullYear()} 暗色风格前端布局设计示例
      </footer>
    </div>
  );
}