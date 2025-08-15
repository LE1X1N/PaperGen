import React from "react";

export default function App() {
  return (
    <div className="flex h-screen bg-gray-50 font-sans text-gray-800">
      {/* 侧边栏 */}
      <aside className="flex flex-col w-64 bg-gradient-to-b from-indigo-600 to-indigo-800 text-white shadow-lg">
        <div className="px-6 py-8 text-2xl font-bold tracking-wide border-b border-indigo-500">
          侧边导航
        </div>
        <nav className="flex flex-col flex-grow px-4 py-6 space-y-3">
          <a
            href="#"
            className="px-3 py-2 rounded-md hover:bg-indigo-500 transition-colors duration-300"
          >
            首页
          </a>
          <a
            href="#"
            className="px-3 py-2 rounded-md hover:bg-indigo-500 transition-colors duration-300"
          >
            发现
          </a>
          <a
            href="#"
            className="px-3 py-2 rounded-md hover:bg-indigo-500 transition-colors duration-300"
          >
            消息
          </a>
          <a
            href="#"
            className="px-3 py-2 rounded-md hover:bg-indigo-500 transition-colors duration-300"
          >
            设置
          </a>
          <a
            href="#"
            className="mt-auto px-3 py-2 rounded-md hover:bg-indigo-500 transition-colors duration-300"
          >
            退出登录
          </a>
        </nav>
      </aside>

      {/* 主内容区域 */}
      <main className="flex flex-col flex-grow overflow-auto">
        {/* 顶部栏 */}
        <header className="flex items-center justify-between px-8 h-16 bg-white shadow-sm border-b border-gray-200">
          <h1 className="text-xl font-semibold text-gray-900">仪表盘</h1>
          <div className="text-gray-600 text-sm">欢迎，用户</div>
        </header>

        {/* 内容卡片列表 */}
        <section className="flex-grow p-8 bg-gray-100 overflow-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <article className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-300">
              <h2 className="text-lg font-semibold mb-3 text-indigo-700">
                统计数据
              </h2>
              <p className="text-gray-600 leading-relaxed">
                这里是统计数据的简短描述，展示重要指标和趋势。
              </p>
            </article>

            <article className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-300">
              <h2 className="text-lg font-semibold mb-3 text-indigo-700">
                用户活动
              </h2>
              <p className="text-gray-600 leading-relaxed">
                显示最新用户的活动动态，帮助快速了解系统使用情况。
              </p>
            </article>

            <article className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-300">
              <h2 className="text-lg font-semibold mb-3 text-indigo-700">
                通知提醒
              </h2>
              <p className="text-gray-600 leading-relaxed">
                查看待处理的重要通知和消息，保证及时响应。
              </p>
            </article>

            <article className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-300">
              <h2 className="text-lg font-semibold mb-3 text-indigo-700">
                系统状态
              </h2>
              <p className="text-gray-600 leading-relaxed">
                系统运行情况一览，监控服务器、数据库等状态信息。
              </p>
            </article>

            <article className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-300">
              <h2 className="text-lg font-semibold mb-3 text-indigo-700">
                最新新闻
              </h2>
              <p className="text-gray-600 leading-relaxed">
                收集和展示最新行业新闻和动态，帮助保持信息更新。
              </p>
            </article>

            <article className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-300">
              <h2 className="text-lg font-semibold mb-3 text-indigo-700">
                资源管理
              </h2>
              <p className="text-gray-600 leading-relaxed">
                管理和分配各项资源，确保项目和团队高效运作。
              </p>
            </article>
          </div>
        </section>
      </main>
    </div>
  );
}