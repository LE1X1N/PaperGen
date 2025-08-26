import React, { useState } from "react";
import { Home, List, AppWindow, User, Settings, LogOut } from "lucide-react";

const navItems = Array.from({ length: 7 }).map((_, i) => ({
  key: i + 1,
  label: `导航 ${i + 1}`,
}));

const sideMenuItems = [
  { key: "1", label: "首页", icon: <Home size={18} /> },
  { key: "2", label: "列表", icon: <List size={18} /> },
  { key: "3", label: "应用", icon: <AppWindow size={18} /> },
  { key: "4", label: "个人中心", icon: <User size={18} /> },
  { key: "5", label: "设置", icon: <Settings size={18} /> },
  { key: "6", label: "退出登录", icon: <LogOut size={18} /> },
];

export default function App() {
  const [selectedNav, setSelectedNav] = useState("2");
  const [selectedSide, setSelectedSide] = useState("1");
  const [breadcrumb, setBreadcrumb] = useState(["首页"]);

  function handleTopNavClick(key) {
    setSelectedNav(key);
    setBreadcrumb([navItems.find((item) => item.key.toString() === key)?.label || "首页"]);
  }
  
  function handleSideMenuClick(key) {
    setSelectedSide(key);
    setBreadcrumb((prev) => [...prev.slice(0, 1), sideMenuItems.find((item) => item.key === key)?.label || ""]);
  }

  return (
    <div className="flex flex-col h-screen bg-gradient-to-b from-indigo-100 to-indigo-50">
      {/* 顶部 Header */}
      <header className="flex items-center px-6 bg-indigo-700 shadow-lg select-none">
        <div className="text-white font-extrabold text-xl tracking-widest mr-12">LOGO</div>
        <nav className="flex space-x-6 flex-1 overflow-x-auto scrollbar-hide">
          {navItems.map(({ key, label }) => (
            <button
              key={key}
              onClick={() => handleTopNavClick(key.toString())}
              className={`relative px-4 py-2 rounded-md font-medium text-white whitespace-nowrap transition-colors duration-300 ${
                selectedNav === key.toString() ? "bg-indigo-900 shadow-lg" : "hover:bg-indigo-600"
              }`}
              aria-current={selectedNav === key.toString() ? "page" : undefined}
            >
              {label}
              {selectedNav === key.toString() && (
                <div
                  className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-purple-400 via-pink-500 to-red-500 rounded-t"
                />
              )}
            </button>
          ))}
        </nav>
      </header>

      {/* 主体内容区 */}
      <main className="flex flex-1 overflow-hidden">
        {/* 侧边栏 */}
        <aside className="w-52 bg-white border-r border-gray-200 flex flex-col select-none">
          <div className="py-6 px-5 border-b border-gray-100 font-semibold text-lg text-indigo-700 tracking-wide">主菜单</div>
          <nav className="flex-1 overflow-y-auto">
            {sideMenuItems.map(({ key, label, icon }) => (
              <button
                key={key}
                onClick={() => handleSideMenuClick(key)}
                className={`flex items-center gap-3 w-full px-5 py-3 transition-colors duration-200 border-l-4 ${
                  selectedSide === key
                    ? "bg-indigo-100 border-indigo-600 font-semibold text-indigo-700"
                    : "border-transparent hover:bg-indigo-50 hover:text-indigo-600"
                }`}
                aria-current={selectedSide === key ? "page" : undefined}
              >
                {icon}
                <span>{label}</span>
              </button>
            ))}
          </nav>
        </aside>

        {/* 内容区 */}
        <section className="flex-1 p-8 overflow-auto">
          {/* 面包屑 */}
          <nav aria-label="面包屑" className="mb-6 text-sm text-gray-600 select-text">
            {breadcrumb.map((crumb, i) => (
              <span key={crumb} className="inline-flex items-center">
                {i > 0 && <span className="mx-2">/</span>}
                <span className={`${i === breadcrumb.length - 1 ? "font-semibold text-indigo-800" : ""}`}>{crumb}</span>
              </span>
            ))}
          </nav>

          {/* 内容卡片 */}
          <div
            className="bg-white rounded-md shadow-lg p-8 min-h-[300px] max-w-5xl mx-auto text-gray-800 text-lg leading-relaxed"
          >
            <h2 className="text-indigo-700 font-semibold text-2xl mb-4">内容区域</h2>
            <p>
              这里是内容展示区域，当前选中顶部导航为 <strong>{navItems.find((i) => i.key.toString() === selectedNav)?.label}</strong>，侧边菜单为{" "}
              <strong>{sideMenuItems.find((i) => i.key === selectedSide)?.label}</strong> 。<br />
              该界面基于顶部-侧边布局设计，整体色调统一为靛蓝与白色，采用 TailwindCSS 实现响应式和现代视觉效果，并增加了微动画提升使用体验。
            </p>
            <div className="mt-6 bg-indigo-50 border border-indigo-200 rounded p-4 text-indigo-600 text-sm select-text">
              这是用于占位的内容区域示例。未来可根据业务需求灵活替换为实际组件或内容。
            </div>
          </div>
        </section>
      </main>

      {/* 底部 Footer */}
      <footer className="text-center py-4 text-gray-500 text-sm select-none border-t border-gray-200 bg-indigo-50">
        设计示例 ©{new Date().getFullYear()} 版权所有
      </footer>
    </div>
  );
}