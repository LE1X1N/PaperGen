import React from "react";
import {
  Grid,
  Users,
  ClipboardCheck,
  BarChart2,
  Settings,
  BellRing,
  Calendar,
} from "lucide-react";

const navItems = [
  { label: "仪表盘", icon: Grid, color: "text-teal-500" },
  { label: "团队", icon: Users, color: "text-orange-500" },
  { label: "任务", icon: ClipboardCheck, color: "text-purple-500" },
  { label: "报表", icon: BarChart2, color: "text-pink-500" },
  { label: "设置", icon: Settings, color: "text-cyan-500" },
  { label: "提醒", icon: BellRing, color: "text-red-400" },
  { label: "日历", icon: Calendar, color: "text-yellow-400" },
];

export default function App() {
  return (
    <div className="flex flex-col min-h-screen bg-gray-900 text-gray-200 font-sans">
      {/* Header */}
      <header className="bg-gray-800 shadow-md">
        <div className="max-w-6xl mx-auto flex items-center justify-between px-8 py-4 select-none">
          <h1 className="text-3xl font-extrabold tracking-tight text-teal-400">
            控制台
          </h1>
          <nav className="flex gap-8">
            {navItems.map(({ label, icon: Icon, color }) => (
              <a
                key={label}
                href="#"
                className="flex items-center gap-1.5 text-gray-300 hover:text-white transition-colors duration-200"
              >
                <Icon className={`${color} w-5 h-5`} />
                <span className="text-sm font-medium">{label}</span>
              </a>
            ))}
          </nav>
        </div>
      </header>

      {/* Content */}
      <main className="flex-grow max-w-6xl mx-auto px-8 py-10">
        {/* Breadcrumb */}
        <nav className="flex items-center space-x-2 text-gray-500 text-sm mb-8 select-none">
          <Grid className="w-4 h-4" />
          <span>仪表盘</span>
          <span>/</span>
          <Users className="w-4 h-4" />
          <span>团队</span>
          <span>/</span>
          <ClipboardCheck className="w-4 h-4" />
          <span>任务</span>
        </nav>

        {/* Main card */}
        <section className="bg-gray-800 rounded-lg shadow-xl p-8 min-h-[280px]">
          <h2 className="text-xl font-semibold text-teal-400 mb-5">
            主要内容区域
          </h2>
          <p className="text-gray-300 leading-relaxed">
            本模板采用深色模式，风格偏现代科技感，配色沉稳且有色彩点缀，界面层次分明，适合后台管理系统、数据控制台等应用场景。
            导航图标和文字清晰易识别，整体布局简洁，使用者能快速聚焦核心信息。
          </p>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-gray-400 text-center py-4 select-none">
        © {new Date().getFullYear()} 深色风格前端布局模板
      </footer>
    </div>
  );
}