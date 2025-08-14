import React from "react";

export default function App() {
  return (
    <div className="min-h-screen bg-gradient-to-r from-indigo-50 via-purple-50 to-pink-50 text-gray-800 font-sans flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-extrabold tracking-wide text-indigo-700 select-none">
            前端代码模板
          </h1>
          <nav>
            <ul className="flex space-x-6 text-indigo-600 font-medium">
              <li>
                <a
                  href="#overview"
                  className="hover:text-indigo-800 transition-colors duration-300"
                >
                  概览
                </a>
              </li>
              <li>
                <a
                  href="#features"
                  className="hover:text-indigo-800 transition-colors duration-300"
                >
                  特性
                </a>
              </li>
              <li>
                <a
                  href="#usage"
                  className="hover:text-indigo-800 transition-colors duration-300"
                >
                  使用指南
                </a>
              </li>
              <li>
                <a
                  href="#contact"
                  className="hover:text-indigo-800 transition-colors duration-300"
                >
                  联系我们
                </a>
              </li>
            </ul>
          </nav>
        </div>
      </header>

      {/* Main content */}
      <main className="flex-grow max-w-7xl mx-auto px-6 py-12 space-y-20">
        {/* Overview Section */}
        <section
          id="overview"
          className="bg-white rounded-lg shadow-lg p-8 animate-fadeIn"
        >
          <h2 className="text-3xl font-bold mb-4 text-indigo-700">概览</h2>
          <p className="text-lg leading-relaxed text-gray-700 max-w-4xl">
            这个前端代码模板为现代React开发提供了一个精致、响应迅速的起点。结合TailwindCSS的强大实用工具，确保代码简洁且易于扩展。模板适合快速构建专业级网站和应用，包含清晰的模块划分和一致的设计语言。
          </p>
        </section>

        {/* Features Section */}
        <section
          id="features"
          className="bg-gradient-to-r from-indigo-100 via-purple-100 to-pink-100 rounded-lg shadow-lg p-8 grid grid-cols-1 md:grid-cols-3 gap-8"
        >
          <FeatureCard
            title="响应式设计"
            description="无缝适配各种屏幕尺寸，手机、平板和桌面设备均拥有出色的浏览体验。"
            emoji="📱"
          />
          <FeatureCard
            title="简洁代码"
            description="采用TailwindCSS结合React最佳实践，代码结构清晰易维护。"
            emoji="🧹"
          />
          <FeatureCard
            title="现代用户界面"
            description="时尚的渐变背景、卡片设计和细致排版，带来高级视觉体验。"
            emoji="🎨"
          />
        </section>

        {/* Usage Section */}
        <section
          id="usage"
          className="bg-white rounded-lg shadow-lg p-8"
        >
          <h2 className="text-3xl font-bold mb-6 text-indigo-700">使用指南</h2>
          <ol className="list-decimal list-inside space-y-3 text-gray-700 max-w-3xl leading-relaxed">
            <li>复制本模板代码到您的项目文件夹中。</li>
            <li>根据需要修改颜色、字体和布局配置，确保符合项目设计规范。</li>
            <li>安装TailwindCSS依赖并进行初始化（若您的项目尚未集成）。</li>
            <li>开始构建自定义组件和内容模块，保持一致的设计语言。</li>
            <li>定期优化和重构代码，提升性能和用户体验。</li>
          </ol>
        </section>

        {/* Contact Section */}
        <section
          id="contact"
          className="bg-gradient-to-r from-pink-100 via-purple-100 to-indigo-100 rounded-lg shadow-lg p-8 max-w-3xl mx-auto"
        >
          <h2 className="text-3xl font-bold mb-4 text-indigo-700 text-center">
            联系我们
          </h2>
          <p className="text-center text-gray-700 mb-6">
            如果您需要帮助，或者有任何建议，欢迎通过以下方式联系我们。
          </p>
          <form className="flex flex-col space-y-4">
            <input
              type="text"
              placeholder="姓名"
              className="px-4 py-3 border border-indigo-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-400 transition"
            />
            <input
              type="email"
              placeholder="电子邮件"
              className="px-4 py-3 border border-indigo-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-400 transition"
            />
            <textarea
              rows={4}
              placeholder="留言内容"
              className="px-4 py-3 border border-indigo-300 rounded-md resize-none focus:outline-none focus:ring-2 focus:ring-indigo-400 transition"
            />
            <button
              type="submit"
              className="self-center bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-8 py-3 rounded-md shadow-md transition"
            >
              发送
            </button>
          </form>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-indigo-700 text-indigo-50 py-6 mt-auto">
        <div className="max-w-7xl mx-auto px-6 text-center text-sm select-none">
          © 2024 前端代码模板，保留所有权利。
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({ title, description, emoji }) {
  return (
    <div className="bg-white rounded-xl shadow-md p-6 flex flex-col items-center text-center transition-transform transform hover:scale-105 hover:shadow-xl">
      <div className="text-5xl mb-4">{emoji}</div>
      <h3 className="text-xl font-semibold text-indigo-700 mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
}