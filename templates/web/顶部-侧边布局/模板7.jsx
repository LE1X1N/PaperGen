import React from "react";
import { Laptop, Bell, User, Menu, X } from "lucide-react";

const navItems = ["首页", "产品", "关于我们"];
const sidebarItems = [
  {
    key: "sub1",
    icon: <User size={18} className="text-indigo-500" />,
    label: "用户管理",
    children: ["用户列表", "权限设置", "角色管理", "操作日志"],
  },
  {
    key: "sub2",
    icon: <Laptop size={18} className="text-indigo-500" />,
    label: "设备监控",
    children: ["设备状态", "告警信息", "设备配置", "统计报表"],
  },
  {
    key: "sub3",
    icon: <Bell size={18} className="text-indigo-500" />,
    label: "系统通知",
    children: ["通知列表", "消息设置", "更新日志", "帮助中心"],
  },
];

export default function App() {
  const [selectNav, setSelectNav] = React.useState(0);
  const [selectSubMenu, setSelectSubMenu] = React.useState("sub1");
  const [selectSubItem, setSelectSubItem] = React.useState(0);
  const [sidebarOpen, setSidebarOpen] = React.useState(true);
  const [contentKey, setContentKey] = React.useState(`${selectSubMenu}-${selectSubItem}`);

  // 处理子菜单切换时更新内容区动画
  React.useEffect(() => {
    setContentKey(`${selectSubMenu}-${selectSubItem}`);
  }, [selectSubMenu, selectSubItem]);

  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-b from-indigo-50 via-indigo-100 to-white text-gray-900 select-none">
      {/* 顶部导航 */}
      <header className="flex items-center justify-between h-16 px-6 bg-gradient-to-r from-indigo-600 via-indigo-700 to-indigo-800 shadow-lg sticky top-0 z-40">
        <div className="flex items-center space-x-3">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="md:hidden p-2 rounded-md hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-white transition"
            aria-label={sidebarOpen ? "关闭侧边栏" : "打开侧边栏"}
          >
            {sidebarOpen ? (
              <X size={24} className="text-white" />
            ) : (
              <Menu size={24} className="text-white" />
            )}
          </button>
          <div className="text-white font-extrabold text-3xl tracking-widest select-text animate-fade-in">
            LOGO
          </div>
        </div>

        <nav className="hidden md:flex space-x-12 text-indigo-200 text-xl font-semibold tracking-wide">
          {navItems.map((item, idx) => (
            <button
              key={item}
              onClick={() => setSelectNav(idx)}
              className={`relative transition-colors duration-300 hover:text-white focus:outline-none ${
                selectNav === idx ? "text-white" : ""
              }`}
              aria-current={selectNav === idx ? "page" : undefined}
            >
              {item}
              {selectNav === idx && (
                <span
                  className="absolute left-0 -bottom-1 w-full h-1 bg-gradient-to-r from-pink-400 via-red-400 to-yellow-400 rounded-full shadow-xl transition-all duration-300 ease-in-out"
                />
              )}
            </button>
          ))}
        </nav>

        <button
          className="hidden md:inline-flex items-center space-x-2 bg-indigo-700 hover:bg-indigo-800 focus:ring-2 focus:ring-offset-1 focus:ring-indigo-400 rounded-full py-1.5 px-4 text-white font-semibold tracking-wide transition"
          aria-label="用户设置"
        >
          <User size={18} />
          <span>Admin</span>
        </button>
      </header>

      {/* 主体部分：侧边栏 + 内容 */}
      <div className="flex flex-1 max-w-[1280px] mx-auto mt-8 mb-12 px-4 sm:px-6 lg:px-8 w-full min-h-[calc(100vh-4rem-6rem)]">
        {/* 侧边栏 */}
        <aside
          className={`w-72 bg-gradient-to-b from-indigo-900 via-indigo-800 to-indigo-900 rounded-2xl shadow-2xl border border-indigo-700 sticky top-20 h-[calc(100vh-5rem)] overflow-y-auto py-8 custom-scrollbar transition-all duration-300 ease-in-out ${
            sidebarOpen ? 'translate-x-0 opacity-100' : '-translate-x-full opacity-0 md:translate-x-0 md:opacity-100'
          }`}
          style={{ display: sidebarOpen || window.innerWidth >= 768 ? 'block' : 'none' }}
        >
          {sidebarItems.map(({ key, icon, label, children }) => (
            <div key={key} className="mb-10 last:mb-0 px-6">
              <div className="flex items-center mb-4 text-indigo-300 font-bold text-lg tracking-wide select-none">
                <span className="mr-3">{icon}</span>
                {label}
              </div>
              <ul role="list" className="space-y-2">
                {children.map((child, i) => {
                  const isSelected = selectSubMenu === key && selectSubItem === i;
                  return (
                    <li key={child} className="list-none">
                      <button
                        onClick={() => {
                          setSelectSubMenu(key);
                          setSelectSubItem(i);
                        }}
                        className={`flex items-center w-full text-indigo-300 hover:text-white text-base rounded-lg py-2 px-5 transition-all duration-300 shadow-md hover:shadow-lg focus:outline-none focus-visible:ring-2 focus-visible:ring-indigo-400 ${
                          isSelected
                            ? "bg-gradient-to-r from-pink-500 via-red-500 to-yellow-500 font-semibold text-white shadow-xl scale-105"
                            : ""
                        }`}
                        aria-current={isSelected ? "true" : undefined}
                      >
                        {child}
                      </button>
                    </li>
                  );
                })}
              </ul>
            </div>
          ))}
        </aside>

        {/* 内容区 */}
        <main className="flex-1 bg-white rounded-3xl shadow-2xl border border-gray-200 p-10 min-h-[520px] select-text relative overflow-hidden">
          <div
            key={contentKey}
            className="max-w-4xl transition-all duration-500 ease-out opacity-0 translate-y-4 animate-fade-in-up"
          >
            <h1 className="text-4xl font-extrabold text-gray-900 mb-8 tracking-tight select-text drop-shadow-lg">
              {sidebarItems.find((item) => item.key === selectSubMenu)?.children[
                selectSubItem
              ] || "欢迎"}
            </h1>
            <section className="text-gray-700 leading-relaxed space-y-6 text-lg tracking-wide">
              <p className="bg-gradient-to-r from-pink-300 via-red-300 to-yellow-300 bg-clip-text text-transparent font-semibold drop-shadow-md">
                这是一个炫酷现代的【顶部-侧边栏】布局示例，结合渐变色彩、立体阴影与流畅动画，打造出灵动且高质感的用户界面体验。
              </p>
              <p>
                侧边栏采用渐变背景与霓虹选中效果，侧菜单项互动丰富，内容区配合动效及大字号排版，令阅读和导航都更加愉悦。
              </p>
              <p>
                导航栏响应式显示菜单切换按钮，支持移动端良好体验，整体设计兼顾视觉冲击和实用功能，适用于管理系统、内容平台及展示型应用。
              </p>
            </section>
          </div>
          {/* 底部发光渐变 */}
          <div className="pointer-events-none absolute bottom-8 left-1/2 -translate-x-1/2 w-3/4 h-48 rounded-3xl bg-gradient-to-r from-pink-500 via-red-400 to-yellow-400 opacity-30 blur-3xl" />
        </main>
      </div>

      {/* 底部 */}
      <footer className="py-4 text-center border-t border-indigo-200 bg-gradient-to-r from-indigo-600 via-indigo-700 to-indigo-800 text-indigo-200 text-sm select-none tracking-wide">
        版权所有 © 2024 优秀团队倾情打造
      </footer>

      {/* 样式定义 */}
      <style>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 8px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: transparent;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(255 255 255 / 0.2);
          border-radius: 9999px;
        }
        .custom-scrollbar:hover::-webkit-scrollbar-thumb {
          background: rgba(255 255 255 / 0.4);
        }
        @media (max-width: 767px) {
          aside {
            position: fixed;
            top: 4rem;
            left: 0;
            bottom: 0;
            z-index: 100;
            box-shadow: 8px 0 20px rgb(0 0 0 / 0.15);
          }
        }
        .animate-fade-in {
          animation: fadeIn 0.6s ease-out forwards;
        }
        @keyframes fadeIn {
          from {
            transform: scale(0.9);
            opacity: 0.7;
          }
          to {
            transform: scale(1);
            opacity: 1;
          }
        }
        .animate-fade-in-up {
          animation: fadeInUp 0.7s ease-out forwards;
        }
        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  );
}
