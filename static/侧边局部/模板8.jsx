import React from "react";
import { Home, Zap, Bell, MessageCircle, Settings, LogOut } from "lucide-react";

export default function App() {
  const menuItems = [
    { icon: <Home className="w-6 h-6 text-gray-300" />, label: "首页" },
    { icon: <Zap className="w-6 h-6 text-gray-300" />, label: "性能" },
    { icon: <Bell className="w-6 h-6 text-gray-300" />, label: "通知" },
    { icon: <MessageCircle className="w-6 h-6 text-gray-300" />, label: "消息" },
    { icon: <Settings className="w-6 h-6 text-gray-300" />, label: "设置" },
  ];

  return (
    <div className="flex min-h-screen bg-gradient-to-tr from-purple-900 via-indigo-900 to-purple-900 text-gray-100 font-sans select-none">
      {/* 侧边栏 */}
      <aside className="w-20 bg-gradient-to-b from-purple-800 to-indigo-900 shadow-xl flex flex-col items-center py-8 space-y-12 relative">
        <div
          className="mb-2 cursor-default font-extrabold text-3xl text-pink-400 select-none"
          aria-label="Logo"
          role="img"
        >
          ⚡
        </div>
        <nav className="flex flex-col space-y-8 flex-1" role="menu" aria-label="主导航">
          {menuItems.map(({ icon, label }) => (
            <div
              key={label}
              className="flex justify-center text-gray-300 cursor-default"
              title={label}
              aria-label={label}
              role="menuitem"
            >
              {icon}
            </div>
          ))}
        </nav>
        <div
          className="mb-4 text-gray-300 cursor-default"
          aria-label="退出登录"
          role="button"
          tabIndex={-1}
        >
          <LogOut className="w-6 h-6 mx-auto" />
        </div>
      </aside>

      {/* 主内容区 */}
      <main className="flex-1 p-12 flex flex-col min-w-0 bg-gradient-to-br from-indigo-900 via-purple-950 to-indigo-900">
        <div className="flex-1 overflow-auto">
          <div className="bg-gradient-to-r from-pink-500 via-pink-600 to-purple-600 rounded-3xl shadow-2xl p-16 max-w-4xl w-full mx-auto select-text">
            <h1 className="text-4xl font-bold text-white mb-6 leading-tight break-words">
              精简科技侧边栏通用左右布局
            </h1>
            <p className="text-pink-200 leading-relaxed text-lg break-words">
              这是一个通用的左右布局页面框架。左侧为固定宽度的垂直导航栏，采用紫色系渐变背景，图标居中，风格简洁无交互动画，适合静态展示。右侧为主内容区，自适应宽度，带有良好的内边距和可滚动区域，界面清爽且聚焦内容。
            </p>
            <section className="mt-10 text-gray-200 space-y-4 text-base leading-relaxed">
              <p>· 采用静态UI，无任何悬浮或点击动画，展现纯粹布局效果。</p>
              <p>· 导航栏图标颜色统一，突出清晰视觉层级。</p>
              <p>· 主区域支持任意内容扩展，结构稳健，适用于多种场景。</p>
            </section>
          </div>
        </div>
      </main>
    </div>
  );
}