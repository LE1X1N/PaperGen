import React from "react";
import { Home, User, Settings, BarChart2, Bell, Info, Phone, Layers, Menu } from "lucide-react";

const navItems = [
  { name: "导航1", icon: Home, key: "nav1" },
  { name: "导航2", icon: User, key: "nav2" },
  { name: "导航3", icon: Settings, key: "nav3" },
  { name: "导航4", icon: BarChart2, key: "nav4" },
  { name: "导航5", icon: Bell, key: "nav5" },
];

const featureItems = [
  {
    title: "优雅设计",
    desc: "甄选配色和字型，构建高雅和谐的视觉语言。",
    icon: Layers,
  },
  {
    title: "响应式布局",
    desc: "无论电脑、平板还是手机，都能完美适配。",
    icon: BarChart2,
  },
  {
    title: "流畅动画",
    desc: "微动效提升用户体验，细节体现专业。",
    icon: Bell,
  },
];

export default function App() {
  const [activeNav, setActiveNav] = React.useState(navItems[0].key);

  return (
    <div
      className="w-[1920px] h-[1080px] bg-white font-sans text-gray-800 flex flex-col select-none overflow-hidden"
      style={{ userSelect: "none" }}
    >
      {/* 顶部导航 固定高度 不可滚动 */}
      <header className="flex items-center justify-between px-10 h-20 bg-gray-100 shadow-sm border-b border-gray-300 flex-shrink-0">
        <h1 className="flex items-center space-x-3 text-2xl font-bold text-gray-900 select-none">
          <Home size={28} />
          <span>管理系统模板</span>
        </h1>
        <nav className="flex space-x-10 text-base text-gray-700 font-medium select-none">
          {navItems.map(({ name, icon: Icon, key }) => (
            <button
              key={key}
              onClick={() => setActiveNav(key)}
              className={`flex items-center space-x-2 px-4 py-2 rounded-md transition-colors duration-200 focus:outline-none ${
                activeNav === key
                  ? "bg-indigo-600 text-white shadow-md"
                  : "hover:bg-indigo-50"
              }`}
              aria-current={activeNav === key ? "page" : undefined}
              type="button"
              tabIndex={0}
            >
              <Icon size={18} />
              <span>{name}</span>
            </button>
          ))}
        </nav>
        <div className="md:hidden text-gray-700 cursor-pointer select-none">
          <Menu size={24} />
        </div>
      </header>

      {/* 内容区：固定高度 不能滚动 */}
      <div className="flex-grow flex flex-col" style={{ flexBasis: 0, overflow: "hidden" }}>
        {/* 上部分 固定不滚动 */}
        <section
          aria-label="欢迎部分"
          className="flex-shrink-0 px-10 py-8 border-b border-gray-200 bg-indigo-50 select-text"
          style={{ userSelect: "text" }}
        >
          <h2 className="text-3xl font-extrabold text-indigo-700 select-none">
            欢迎使用现代简约的管理系统模板
          </h2>
          <p className="mt-3 text-gray-600 text-lg max-w-4xl select-none">
            本模板专为管理类系统设计，简洁大方，且固定1920x1080全屏显示，无需任何滚动操作，助力高效办公。
          </p>
        </section>

        {/* 中部分 固定不滚动 */}
        <section
          aria-label="功能展示"
          className="flex-grow px-10 py-8 bg-white grid grid-cols-3 gap-8 overflow-hidden"
        >
          {featureItems.map(({ title, desc, icon: Icon }) => (
            <article
              key={title}
              className="flex flex-col bg-gray-50 rounded-xl shadow-sm hover:shadow-md transition-shadow duration-300 p-8 select-none"
            >
              <div className="flex items-center space-x-4 text-indigo-600 mb-4">
                <Icon size={36} />
                <h3 className="text-xl font-semibold">{title}</h3>
              </div>
              <p className="text-gray-600 flex-grow">{desc}</p>
              <button
                type="button"
                className="mt-6 w-max bg-indigo-600 text-white px-5 py-2 rounded-lg shadow-md hover:bg-indigo-700 transition-colors duration-300 select-none"
              >
                了解更多
              </button>
            </article>
          ))}
        </section>

        {/* 下部分 固定不滚动 */}
        <footer
          aria-label="页脚信息"
          className="flex-shrink-0 px-10 py-6 bg-gray-100 border-t border-gray-300 flex justify-between items-center text-gray-700 text-sm select-none"
        >
          <div className="flex items-center space-x-3">
            <Home size={18} />
            <span>上海市浦东新区未来大道100号</span>
          </div>
          <div className="flex items-center space-x-3">
            <Phone size={18} />
            <span>电话：021-12345678</span>
          </div>
          <div className="flex items-center space-x-1">
            <Info size={18} />
            <span>© 2024 现代管理系统 版权所有</span>
          </div>
        </footer>
      </div>
    </div>
  );
}