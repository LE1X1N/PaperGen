import React, { useState } from "react";
import { Home, Users, Settings, Menu, Layout } from "lucide-react";

export default function App() {
  const [active, setActive] = useState("home");
  const menuItems = [
    { id: "home", label: "首页", icon: <Home size={20} /> },
    { id: "users", label: "用户管理", icon: <Users size={20} /> },
    { id: "settings", label: "设置", icon: <Settings size={20} /> },
  ];

  return (
    <div className="flex min-h-screen bg-gray-50 text-gray-800">
      {/* 侧边栏 */}
      <aside className="flex flex-col w-60 bg-white border-r border-gray-200 shadow-sm">
        <div className="flex items-center h-16 px-6 border-b border-gray-200 font-bold text-xl text-indigo-600 tracking-wide">
          通用模板
        </div>
        <nav className="flex flex-col flex-1 px-2 py-6 space-y-1">
          {menuItems.map(({ id, label, icon }) => (
            <button
              key={id}
              onClick={() => setActive(id)}
              className={`group flex items-center px-4 py-2 rounded-md text-sm font-medium gap-3 transition-colors duration-200
                ${
                  active === id
                    ? "bg-indigo-600 text-white shadow-md"
                    : "text-gray-600 hover:bg-indigo-100 hover:text-indigo-600"
                }`}
              aria-current={active === id ? "page" : undefined}
            >
              <span
                className={`transition-colors duration-200 ${
                  active === id ? "text-white" : "text-gray-400 group-hover:text-indigo-500"
                }`}
              >
                {icon}
              </span>
              {label}
            </button>
          ))}
        </nav>
        <div className="px-6 py-4 border-t border-gray-200 text-sm text-gray-500 select-none flex items-center gap-2">
          <Layout size={18} />
          侧边栏布局
        </div>
      </aside>

      {/* 主内容区 */}
      <main className="flex-1 flex flex-col">
        <header className="h-16 bg-white border-b border-gray-200 flex items-center px-6 shadow-sm">
          <button
            aria-label="切换侧边栏"
            className="text-gray-600 hover:text-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 rounded-md"
            onClick={() =>
              document.querySelector("aside")?.classList.toggle("-translate-x-full")
            }
          >
            <Menu size={24} />
          </button>
          <h1 className="ml-4 text-lg font-semibold text-gray-900">仪表盘</h1>
        </header>

        <section className="flex-1 overflow-auto p-8 bg-gradient-to-b from-white to-indigo-50">
          {active === "home" && (
            <>
              <h2 className="text-2xl font-semibold mb-6 text-indigo-700">欢迎来到首页</h2>
              <p className="max-w-xl text-gray-700 leading-relaxed">
                这是一个简洁大方的通用网站模板。侧边布局带来清晰的导航体验，主区域的内容区域有充足空间展示信息，配合柔和的渐变背景提升视觉舒适度。
              </p>
            </>
          )}
          {active === "users" && (
            <>
              <h2 className="text-2xl font-semibold mb-6 text-indigo-700">用户管理</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {[1, 2, 3, 4, 5, 6].map((user) => (
                  <article
                    key={user}
                    className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow cursor-pointer"
                  >
                    <div className="h-24 w-24 bg-indigo-100 rounded-full flex items-center justify-center mb-4 text-indigo-500 font-bold text-xl mx-auto">
                      U{user}
                    </div>
                    <h3 className="text-lg font-semibold mb-1 text-center">用户姓名 {user}</h3>
                    <p className="text-gray-600 text-sm mb-2 text-center">
                      用户邮箱 user{user}@example.com
                    </p>
                    <div className="flex justify-center">
                      <button className="text-indigo-600 hover:text-indigo-800 font-medium text-sm">
                        查看详情 &rarr;
                      </button>
                    </div>
                  </article>
                ))}
              </div>
            </>
          )}
          {active === "settings" && (
            <>
              <h2 className="text-2xl font-semibold mb-6 text-indigo-700">设置</h2>
              <form className="max-w-lg bg-white p-6 rounded-lg shadow space-y-6">
                <div>
                  <label className="block text-gray-700 mb-1 font-medium" htmlFor="username">
                    用户名
                  </label>
                  <input
                    id="username"
                    type="text"
                    placeholder="请输入用户名"
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
                <div>
                  <label className="block text-gray-700 mb-1 font-medium" htmlFor="email">
                    电子邮件
                  </label>
                  <input
                    id="email"
                    type="email"
                    placeholder="请输入电子邮件"
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
                <div>
                  <label className="block text-gray-700 mb-1 font-medium" htmlFor="notifications">
                    邮件通知
                  </label>
                  <select
                    id="notifications"
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  >
                    <option>开启</option>
                    <option>关闭</option>
                  </select>
                </div>
                <button
                  type="submit"
                  className="bg-indigo-600 text-white px-6 py-2 rounded-md hover:bg-indigo-700 transition"
                >
                  保存设置
                </button>
              </form>
            </>
          )}
        </section>
      </main>
    </div>
  );
}
