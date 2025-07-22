import React from "react";
import { Grid, UserCircle2, Settings, ChevronLeft, ChevronRight } from "lucide-react";

export default function App() {
  const collapsed = false;

  const menuItems = [
    { id: "dashboard", label: "仪表盘", icon: <Grid size={22} /> },
    { id: "profile", label: "个人资料", icon: <UserCircle2 size={22} /> },
    { id: "settings", label: "设置", icon: <Settings size={22} /> },
  ];

  return (
    <div className="flex h-screen bg-gradient-to-tr from-cyan-50 to-blue-50 text-gray-900 font-sans select-none">
      {/* 侧边栏 */}
      <aside
        style={{ width: 240 }}
        className="relative bg-gradient-to-b from-blue-700 to-blue-900 text-white flex flex-col shadow-lg"
      >
        <div className="flex items-center justify-between h-16 px-4 border-b border-blue-600">
          {!collapsed ? (
            <h1 className="text-xl font-bold tracking-wide">多彩模板</h1>
          ) : (
            <Grid size={28} />
          )}
          <button
            aria-label="切换侧边栏"
            className="p-1 rounded-md hover:bg-blue-600 transition-colors cursor-default"
            tabIndex={-1}
          >
            {collapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
          </button>
        </div>

        <nav className="flex flex-col mt-6 space-y-2 px-2">
          {menuItems.map(({ id, label, icon }) => {
            const activeStyle = "bg-blue-600 shadow-lg";
            return (
              <button
                key={id}
                className={`flex items-center gap-4 rounded-md px-4 py-3 font-semibold transition-colors duration-200 ${activeStyle} focus:outline-none cursor-default`}
                tabIndex={-1}
                type="button"
              >
                <span className="text-white">{icon}</span>
                {!collapsed && <span className="text-white">{label}</span>}
              </button>
            );
          })}
        </nav>

        <div className="mt-auto px-4 py-6 border-t border-blue-600 flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-blue-800 flex items-center justify-center text-blue-300 font-extrabold tracking-wide">
            A
          </div>
          {!collapsed && (
            <div className="flex flex-col">
              <span className="font-semibold">管理员</span>
              <span className="text-sm text-blue-300">admin@example.com</span>
            </div>
          )}
        </div>
      </aside>

      {/* 主内容区 */}
      <main className="flex-1 overflow-auto p-8">
        <section className="max-w-4xl mx-auto mb-16">
          <h2 className="text-3xl font-bold text-blue-900 mb-6">仪表盘</h2>
          <p className="mb-6 text-lg text-gray-700">
            欢迎使用这款色彩丰富的侧边布局模板。它采用了渐变背景和浓郁配色，适合打造现代感强烈的管理后台或企业网站。
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
            {[
              { title: "用户总数", value: "1,028" },
              { title: "活跃用户", value: "785" },
              { title: "销售额", value: "¥230,000" },
            ].map(({ title, value }) => (
              <div
                key={title}
                className="bg-gradient-to-tr from-blue-600 to-cyan-600 rounded-lg shadow-lg p-5 text-white flex flex-col"
              >
                <span className="uppercase text-xs font-semibold tracking-wider">{title}</span>
                <span className="mt-2 text-2xl font-extrabold">{value}</span>
              </div>
            ))}
          </div>
        </section>

        <section className="max-w-2xl mx-auto bg-white rounded-xl shadow-lg p-8 mb-16">
          <h2 className="text-3xl font-bold text-blue-900 mb-6 flex items-center gap-3">
            <UserCircle2 size={28} />
            个人资料
          </h2>
          <form className="space-y-6">
            <div>
              <label htmlFor="name" className="block text-gray-700 font-semibold mb-1">
                姓名
              </label>
              <input
                id="name"
                type="text"
                placeholder="张三"
                className="w-full rounded-md border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
                readOnly
              />
            </div>
            <div>
              <label htmlFor="email" className="block text-gray-700 font-semibold mb-1">
                电子邮件
              </label>
              <input
                id="email"
                type="email"
                placeholder="zhangsan@example.com"
                className="w-full rounded-md border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
                readOnly
              />
            </div>
            <div>
              <label htmlFor="bio" className="block text-gray-700 font-semibold mb-1">
                简介
              </label>
              <textarea
                id="bio"
                rows={4}
                placeholder="写点什么介绍自己吧..."
                className="w-full rounded-md border border-gray-300 px-4 py-2 resize-none focus:outline-none focus:ring-2 focus:ring-cyan-500"
                readOnly
              />
            </div>
            <button
              type="button"
              className="bg-blue-700 cursor-default text-white font-semibold rounded-md px-6 py-2 opacity-60"
              disabled
            >
              保存
            </button>
          </form>
        </section>

        <section className="max-w-2xl mx-auto bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-3xl font-bold text-blue-900 mb-6 flex items-center gap-3">
            <Settings size={28} />
            设置
          </h2>
          <form className="space-y-6">
            <div>
              <label htmlFor="theme" className="block text-gray-700 font-semibold mb-1">
                主题模式
              </label>
              <select
                id="theme"
                className="w-full rounded-md border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 cursor-not-allowed bg-gray-100"
                defaultValue="light"
                disabled
              >
                <option value="light">浅色</option>
                <option value="dark">深色</option>
              </select>
            </div>
            <div>
              <label htmlFor="notifications" className="block text-gray-700 font-semibold mb-1">
                通知设置
              </label>
              <select
                id="notifications"
                className="w-full rounded-md border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 cursor-not-allowed bg-gray-100"
                defaultValue="enabled"
                disabled
              >
                <option value="enabled">启用</option>
                <option value="disabled">禁用</option>
              </select>
            </div>
            <button
              type="button"
              className="bg-blue-700 cursor-default text-white font-semibold rounded-md px-6 py-2 opacity-60"
              disabled
            >
              保存设置
            </button>
          </form>
        </section>
      </main>
    </div>
  );
}