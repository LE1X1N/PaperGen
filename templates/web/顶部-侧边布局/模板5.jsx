import React from "react";
import { Laptop, Bell, User } from "lucide-react";

const navItems = [
  { key: "1", label: "导航 1" },
  { key: "2", label: "导航 2" },
  { key: "3", label: "导航 3" },
];

const sideMenuItems = [
  {
    key: "sub1",
    icon: User,
    label: "子导航 1",
    children: [
      { key: "1", label: "选项 1" },
      { key: "2", label: "选项 2" },
      { key: "3", label: "选项 3" },
      { key: "4", label: "选项 4" },
    ],
  },
  {
    key: "sub2",
    icon: Laptop,
    label: "子导航 2",
    children: [
      { key: "5", label: "选项 5" },
      { key: "6", label: "选项 6" },
      { key: "7", label: "选项 7" },
      { key: "8", label: "选项 8" },
    ],
  },
  {
    key: "sub3",
    icon: Bell,
    label: "子导航 3",
    children: [
      { key: "9", label: "选项 9" },
      { key: "10", label: "选项 10" },
      { key: "11", label: "选项 11" },
      { key: "12", label: "选项 12" },
    ],
  },
];

export default function App() {
  return (
    <div className="flex flex-col min-h-screen">
      {/* 顶部导航 */}
      <header className="flex items-center bg-gradient-to-r from-blue-600 to-cyan-500 text-white h-14 px-4">
        <div className="text-lg font-bold select-none">应用网站</div>
        <nav className="flex flex-1 justify-center space-x-10 text-sm font-medium">
          {navItems.map((item) => (
            <button
              key={item.key}
              className="relative px-3 py-1 rounded-md hover:bg-white/20 transition-colors"
              type="button"
            >
              {item.label}
              <span
                className="absolute bottom-0 left-0 right-0 h-0.5 bg-white rounded transform scale-x-0 group-hover:scale-x-100 transition-transform origin-left"
              />
            </button>
          ))}
        </nav>
        <button className="text-sm px-3 py-1 rounded bg-white/20 hover:bg-white/30 transition-colors select-none">
          登出
        </button>
      </header>

      {/* 主内容区，左右无边距 */}
      <main className="flex flex-1 bg-gray-50">
        {/* 侧边栏 */}
        <aside className="w-56 bg-white border-r border-gray-200 flex flex-col select-none">
          <div className="text-gray-700 font-semibold px-4 py-3 border-b border-gray-200">
            侧边菜单
          </div>
          <nav className="flex-1 overflow-auto">
            {sideMenuItems.map(({ key, icon: Icon, label, children }) => (
              <div key={key} className="border-b border-gray-100">
                <div className="flex items-center gap-2 px-4 py-3 text-gray-800 font-semibold hover:bg-blue-100 cursor-pointer transition-colors">
                  <Icon size={16} />
                  <span>{label}</span>
                </div>
                <div className="pl-10 bg-blue-50">
                  {children.map((child) => (
                    <div
                      key={child.key}
                      className="px-4 py-2 text-sm text-gray-600 hover:text-blue-700 cursor-pointer transition-colors rounded"
                    >
                      {child.label}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </nav>
        </aside>

        {/* 通栏内容区 */}
        <section className="flex-1 bg-white flex flex-col">
          {/* 面包屑导航 */}
          <div className="px-6 py-4 border-b border-gray-200 text-gray-500 text-sm select-none">
            首页 / 列表 / 应用
          </div>
          {/* 内容部分 */}
          <article className="flex-1 p-6 overflow-auto text-gray-800 leading-relaxed">
            <h1 className="text-2xl font-bold mb-4">欢迎使用应用型布局</h1>
            <p className="mb-4">
              此布局采用了顶部导航、无边距侧边栏及通栏内容区设计，适合各类企业级应用和管理后台。
            </p>
            <p>
              侧边栏与顶部导航紧贴页面边缘，最大化利用空间，同时保持清晰分区和操作便利。主内容区通栏铺满剩余区域，适合多样内容展示。
            </p>
            <div className="mt-12 p-6 bg-gradient-to-r from-cyan-100 to-blue-100 rounded-md shadow-inner text-center font-semibold text-blue-900">
              这里是通栏内容演示区域
            </div>
          </article>
        </section>
      </main>
    </div>
  );
}
