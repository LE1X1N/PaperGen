import React from "react";
import {
  Home,
  UserCheck,
  BarChart2,
  Settings,
  Bell,
  Users,
  ClipboardList,
} from "lucide-react";

export default function App() {
  const functions = [
    { icon: Home, label: "功能1" },
    { icon: UserCheck, label: "功能2" },
    { icon: BarChart2, label: "功能3" },
    { icon: Settings, label: "功能4" },
    { icon: Bell, label: "功能5" },
    { icon: Users, label: "功能6" },
    { icon: ClipboardList, label: "功能7" },
  ];

  return (
    <div className="min-h-screen flex flex-col bg-gray-100 text-gray-900">
      {/* 顶部 */}
      <header className="bg-gradient-to-r from-cyan-600 to-blue-500 text-white px-6 py-4 shadow-lg flex flex-col md:flex-row md:items-center md:justify-between">
        <h1 className="text-3xl font-extrabold tracking-wide mb-4 md:mb-0 drop-shadow-sm">
          管理系统
        </h1>
        <nav className="flex flex-wrap justify-center md:justify-end gap-3 md:gap-5">
          {functions.map(({ icon: Icon, label }) => (
            <button
              key={label}
              type="button"
              className="flex items-center space-x-2 bg-white bg-opacity-25 hover:bg-opacity-40 transition rounded-lg px-4 py-2 font-semibold shadow-md shadow-cyan-400/30 select-none cursor-default text-cyan-900"
            >
              <Icon className="w-5 h-5 text-cyan-900" />
              <span>{label}</span>
            </button>
          ))}
        </nav>
      </header>

      {/* 中间内容区 */}
      <main className="flex-grow px-8 py-12 max-w-7xl w-full mx-auto">
        {/* 中间区域用卡片分区展示 */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-10">
          <div className="bg-white rounded-xl shadow-xl p-8 border border-cyan-100 hover:shadow-cyan-300 transition-shadow">
            <h2 className="text-xl font-semibold text-cyan-700 mb-4 border-b border-cyan-200 pb-3">
              仪表盘
            </h2>
            <p className="text-gray-700 leading-relaxed text-base">
              这里展示系统关键数据概览，帮助快速了解整体运行情况。
            </p>
          </div>

          <div className="bg-white rounded-xl shadow-xl p-8 border border-cyan-100 hover:shadow-cyan-300 transition-shadow">
            <h2 className="text-xl font-semibold text-cyan-700 mb-4 border-b border-cyan-200 pb-3">
              用户管理
            </h2>
            <p className="text-gray-700 leading-relaxed text-base">
              管理用户信息、角色权限及访问控制等操作。
            </p>
          </div>

          <div className="bg-white rounded-xl shadow-xl p-8 border border-cyan-100 hover:shadow-cyan-300 transition-shadow">
            <h2 className="text-xl font-semibold text-cyan-700 mb-4 border-b border-cyan-200 pb-3">
              报表统计
            </h2>
            <p className="text-gray-700 leading-relaxed text-base">
              查看系统运行数据报表，支持导出和筛选功能。
            </p>
          </div>
        </section>
      </main>

      {/* 底部 */}
      <footer className="bg-white border-t border-cyan-200 text-cyan-600 text-center py-5 text-sm select-none font-medium">
        © 2024 管理系统模板框架 版权所有
      </footer>
    </div>
  );
}