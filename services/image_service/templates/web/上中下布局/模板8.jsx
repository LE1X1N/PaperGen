import React from "react";
import {
  Home,
  List,
  AppWindow,
  User,
  Settings,
  Bell,
  Calendar,
  MessageCircle,
} from "lucide-react";

const navItems = [
  { label: "首页", icon: Home, color: "text-blue-500" },
  { label: "列表", icon: List, color: "text-purple-500" },
  { label: "应用", icon: AppWindow, color: "text-green-500" },
  { label: "用户", icon: User, color: "text-pink-500" },
  { label: "设置", icon: Settings, color: "text-yellow-500" },
  { label: "通知", icon: Bell, color: "text-red-500" },
  { label: "日历", icon: Calendar, color: "text-indigo-500" },
];

export default function App() {
  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-b from-gray-50 to-white text-gray-900">
      {/* 顶部 Header */}
      <header className="flex items-center bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white px-6 py-3 shadow-md select-none">
        <div className="flex items-center space-x-6 w-full max-w-7xl mx-auto">
          <div className="text-2xl font-bold tracking-wide select-none">
            现代网站Logo
          </div>
          <nav className="flex space-x-8 ml-auto">
            {navItems.map(({ label, icon: Icon, color }) => (
              <a
                key={label}
                href="#"
                className="flex items-center space-x-2 hover:underline"
              >
                <Icon className={`${color} w-5 h-5`} />
                <span className="font-medium">{label}</span>
              </a>
            ))}
          </nav>
        </div>
      </header>

      {/* 中部内容 Content */}
      <main className="flex-grow px-6 py-10 max-w-7xl mx-auto w-full">
        {/* 面包屑导航 */}
        <nav className="text-sm text-gray-500 mb-6 flex items-center space-x-2 select-none">
          <Home className="w-4 h-4" />
          <span>首页</span>
          <span>/</span>
          <List className="w-4 h-4" />
          <span>列表</span>
          <span>/</span>
          <AppWindow className="w-4 h-4" />
          <span>应用</span>
        </nav>

        {/* 内容卡片 */}
        <section className="bg-white rounded-lg shadow-lg p-8 min-h-[280px] select-text">
          <h2 className="text-2xl font-semibold mb-4">内容区域</h2>
          <p className="text-gray-700 leading-relaxed">
            这是网站的主体内容区，布局简洁明快，配色现代，图标与文字配合使用，提供良好用户体验。在此处可写任意自定义内容。
          </p>
        </section>
      </main>

      {/* 底部 Footer */}
      <footer className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white text-center py-4 select-none">
        © {new Date().getFullYear()} 通用网站布局模板
      </footer>
    </div>
  );
}