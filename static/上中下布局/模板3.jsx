import React from "react";

export default function App() {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-b from-blue-50 to-blue-100 font-sans text-gray-800">
      {/* 上部 Header */}
      <header className="bg-white shadow-md py-6 px-8 flex items-center justify-between">
        <h1 className="text-3xl font-semibold text-blue-700 select-none">网站标题</h1>
        <nav className="space-x-6 text-blue-600 font-medium">
          <a href="#home" className="hover:text-blue-800 transition-colors">
            首页
          </a>
          <a href="#about" className="hover:text-blue-800 transition-colors">
            关于我们
          </a>
          <a href="#contact" className="hover:text-blue-800 transition-colors">
            联系方式
          </a>
        </nav>
      </header>

      {/* 中部内容区 */}
      <main className="flex-grow container mx-auto px-6 py-12 grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* 主要内容 */}
        <section className="md:col-span-2 bg-white rounded-lg shadow-lg p-8 flex flex-col">
          <h2 className="text-2xl font-bold text-blue-700 mb-4 select-none">主要内容区域</h2>
          <p className="text-gray-600 leading-relaxed mb-6 flex-grow">
            这是页面中间的主要内容区域，可以放置文章、产品介绍、或者其他展示内容。采用卡片式设计，增加阴影和圆角，使内容更显层次感。此区域响应式良好，大屏幕时占据主列，小屏幕时自动叠加展示。
          </p>
          <button
            aria-label="了解更多"
            className="self-start bg-blue-600 text-white rounded-md px-6 py-2 font-medium shadow-md hover:bg-blue-700 transition-colors"
          >
            了解更多
          </button>
        </section>

        {/* 侧边栏 */}
        <aside className="bg-white rounded-lg shadow-lg p-6 flex flex-col space-y-6">
          <div>
            <h3 className="text-xl font-semibold text-blue-700 mb-3 select-none">信息卡片 1</h3>
            <p className="text-gray-600 leading-relaxed">
              这里可以放置一些辅助信息、公告或者快速链接，提升用户的浏览效率与体验。
            </p>
          </div>
          <div>
            <h3 className="text-xl font-semibold text-blue-700 mb-3 select-none">信息卡片 2</h3>
            <p className="text-gray-600 leading-relaxed">
              结合渐变背景与阴影，视觉层次分明，现代感十足，提升整体设计质感。
            </p>
          </div>
          <button className="mt-auto bg-gradient-to-r from-blue-400 to-blue-600 text-white py-2 rounded-md font-medium hover:from-blue-500 hover:to-blue-700 transition-colors">
            更多信息
          </button>
        </aside>
      </main>

      {/* 底部 Footer */}
      <footer className="bg-blue-700 text-blue-200 text-center py-5 select-none">
        <p>© 2024 示例公司 版权所有 | 沪ICP备12345678号</p>
      </footer>
    </div>
  );
}