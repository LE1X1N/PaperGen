import React from "react";
import { Cpu, LayoutDashboard, Activity, Settings, Users, ChartBar } from "lucide-react";

export default function App() {
  const menuItems = [
    { icon: <LayoutDashboard className="w-5 h-5" />, label: "仪表盘" },
    { icon: <Cpu className="w-5 h-5" />, label: "系统监控" },
    { icon: <Activity className="w-5 h-5" />, label: "活动日志" },
    { icon: <Users className="w-5 h-5" />, label: "用户管理" },
    { icon: <ChartBar className="w-5 h-5" />, label: "数据分析" },
    { icon: <Settings className="w-5 h-5" />, label: "设置" },
  ];

  return (
    <div className="flex min-h-screen bg-gradient-to-tr from-[#0f172a] via-[#1e293b] to-[#334155] text-slate-300 font-sans">
      {/* 侧边栏 */}
      <aside className="w-64 bg-gradient-to-b from-[#111827] via-[#1f2937] to-[#111827] shadow-lg flex flex-col">
        <div className="flex items-center justify-center h-16 border-b border-slate-700">
          <Cpu className="w-8 h-8 text-cyan-400 mr-2" />
          <span className="text-cyan-400 text-xl font-semibold tracking-wide select-none">
            科技前端
          </span>
        </div>
        <nav className="flex-1 mt-6">
          {menuItems.map(({ icon, label }, idx) => (
            <div
              key={label}
              className="flex items-center px-6 py-3 space-x-3 cursor-pointer text-slate-300 hover:text-cyan-400 hover:bg-[rgba(14,116,144,0.7)] transition-colors duration-200"
              style={{ userSelect: "none" }}
              aria-label={label}
              tabIndex={0}
            >
              <div className="">{icon}</div>
              <span className="text-base font-medium">{label}</span>
            </div>
          ))}
        </nav>
        <div className="p-4 border-t border-slate-700 text-sm text-slate-500 select-none">
          © 2025 科技公司
        </div>
      </aside>

      {/* 主内容区 */}
      <main className="flex-1 p-10">
        <h1
          className="text-3xl font-extrabold text-cyan-400 mb-6 select-none"
        >
          欢迎来到科技感前端框架
        </h1>

        <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {[1, 2, 3, 4, 5, 6].map((card) => (
            <div
              key={card}
              className="bg-gradient-to-tr from-[#0f172a] to-[#134e4a] rounded-xl border border-cyan-500/60 p-6 shadow-md backdrop-blur-sm hover:scale-105 hover:shadow-[0_12px_24px_rgba(14,116,144,0.6)] transition-all duration-300"
            >
              <h2 className="text-xl font-semibold mb-2 text-cyan-300 select-none">
                科技卡片 #{card}
              </h2>
              <p className="text-slate-400 leading-relaxed select-text">
                这是一个静态示例卡片，展示侧边栏布局的科技感设计风格。使用渐变、阴影和现代排版营造氛围。
              </p>
            </div>
          ))}
        </section>
      </main>
    </div>
  );
}
    