import React from "react";
import {
  Laptop,
  Bell,
  User,
  Home,
  Grid,
  LayoutDashboard,
} from "lucide-react";

const navItems = ["导航1", "导航2", "导航3"];

const sidebarItems = [
  {
    key: "sub1",
    icon: <User className="w-5 h-5" />,
    label: "子导航 1",
    children: ["选项1", "选项2", "选项3", "选项4"],
  },
  {
    key: "sub2",
    icon: <Laptop className="w-5 h-5" />,
    label: "子导航 2",
    children: ["选项5", "选项6", "选项7", "选项8"],
  },
  {
    key: "sub3",
    icon: <Bell className="w-5 h-5" />,
    label: "子导航 3",
    children: ["选项9", "选项10", "选项11", "选项12"],
  },
];

export default function App() {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-b from-slate-50 to-slate-100 text-gray-800">
      {/* Header */}
      <header className="flex items-center bg-gradient-to-r from-indigo-600 to-indigo-800 px-6 py-3 shadow-md text-white select-none">
        <div className="mr-8 flex items-center gap-2">
          <LayoutDashboard className="w-8 h-8" />
          <span className="font-extrabold text-lg tracking-wide">品牌标志</span>
        </div>
        <nav className="flex space-x-6 flex-1 min-w-0">
          {navItems.map((item, i) => (
            <button
              key={i}
              className={`whitespace-nowrap font-medium transition-colors ${
                i === 1
                  ? "border-b-2 border-white"
                  : "text-indigo-200 hover:text-white"
              }`}
              style={{ minWidth: 60 }}
            >
              {item}
            </button>
          ))}
        </nav>
      </header>

      {/* Breadcrumb */}
      <nav
        className="flex items-center px-12 py-4 text-sm text-gray-600 select-none"
        aria-label="Breadcrumb"
      >
        <ol className="inline-flex items-center space-x-2">
          <li className="inline-flex items-center">
            <Home className="w-4 h-4 mr-1" />
            <span>首页</span>
            <span className="mx-2">/</span>
          </li>
          <li className="inline-flex items-center">
            <Grid className="w-4 h-4 mr-1" />
            <span>列表</span>
            <span className="mx-2">/</span>
          </li>
          <li aria-current="page" className="text-indigo-700 font-semibold">
            应用
          </li>
        </ol>
      </nav>

      {/* Main Content with Sidebar */}
      <main className="flex flex-1 px-12 pb-12">
        {/* Sidebar */}
        <aside className="w-48 bg-white rounded-lg shadow-inner p-4 sticky top-6 self-start">
          {sidebarItems.map(({ key, icon, label, children }) => (
            <div key={key} className="mb-6 last:mb-0">
              <div className="flex items-center mb-2 text-indigo-700 font-semibold">
                <div className="mr-2">{icon}</div>
                <span>{label}</span>
              </div>
              <ul className="space-y-1 text-gray-700 font-medium">
                {children.map((child, idx) => (
                  <li
                    key={idx}
                    className={`pl-6 relative cursor-pointer rounded-md py-1 hover:bg-indigo-50 transition ${
                      key === "sub1" && idx === 0
                        ? "bg-indigo-100 text-indigo-800 font-semibold"
                        : ""
                    }`}
                  >
                    {child}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </aside>

        {/* Content Area */}
        <section className="flex-1 bg-white rounded-lg shadow-inner ml-8 p-6 text-gray-700 min-h-[280px]">
          <div className="text-lg font-semibold">
            内容区域
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="text-center text-gray-500 text-sm py-4 select-none border-t border-slate-300">
        Ant Design ©{new Date().getFullYear()} 由 Ant UED 创建
      </footer>
    </div>
  );
}