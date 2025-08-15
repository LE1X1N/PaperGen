import React, { useState } from "react";
import {
  Laptop,
  Bell,
  User,
  Home,
  Grid,
  LayoutDashboard,
  Smile,
} from "lucide-react";
import { motion } from "framer-motion";

const navItems = ["导航1", "导航2", "导航3"];

const sidebarItems = [
  {
    key: "sub1",
    icon: <User className="w-5 h-5 text-pink-400" />,
    label: "子导航 1",
    children: ["选项1", "选项2", "选项3", "选项4"],
  },
  {
    key: "sub2",
    icon: <Laptop className="w-5 h-5 text-pink-400" />,
    label: "子导航 2",
    children: ["选项5", "选项6", "选项7", "选项8"],
  },
  {
    key: "sub3",
    icon: <Bell className="w-5 h-5 text-pink-400" />,
    label: "子导航 3",
    children: ["选项9", "选项10", "选项11", "选项12"],
  },
];

export default function App() {
  const [activeNav, setActiveNav] = useState(1);
  const [activeSidebar, setActiveSidebar] = useState({ subKey: "sub1", idx: 0 });

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-b from-pink-50 to-pink-100 text-pink-900 font-sans select-none">
      {/* Header */}
      <header className="flex items-center bg-gradient-to-r from-pink-400 to-pink-600 px-6 py-3 shadow-lg text-white rounded-b-3xl">
        <div className="mr-8 flex items-center gap-2">
          <LayoutDashboard className="w-8 h-8 stroke-white" />
          <span className="font-extrabold text-lg tracking-widest drop-shadow-sm">
            可爱品牌
          </span>
          <Smile className="w-5 h-5 text-yellow-300 animate-bounce ml-1" />
        </div>
        <nav className="flex space-x-6 flex-1 min-w-0">
          {navItems.map((item, i) => (
            <motion.button
              key={i}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setActiveNav(i)}
              className={`whitespace-nowrap font-semibold px-3 py-1 rounded-xl transition-colors ${
                i === activeNav
                  ? "bg-white bg-opacity-30 shadow-md"
                  : "text-pink-200 hover:text-white"
              }`}
              style={{ minWidth: 60 }}
              aria-current={i === activeNav ? "page" : undefined}
            >
              {item}
            </motion.button>
          ))}
        </nav>
      </header>

      {/* Breadcrumb */}
      <nav
        className="flex items-center px-12 py-4 text-sm text-pink-600 select-none space-x-1"
        aria-label="Breadcrumb"
      >
        <ol className="inline-flex items-center space-x-1">
          <li className="inline-flex items-center gap-1">
            <Home className="w-4 h-4" />
            <span>首页</span>
            <span className="mx-2 select-none">/</span>
          </li>
          <li className="inline-flex items-center gap-1">
            <Grid className="w-4 h-4" />
            <span>列表</span>
            <span className="mx-2 select-none">/</span>
          </li>
          <li
            aria-current="page"
            className="text-pink-700 font-semibold select-text"
          >
            应用
          </li>
        </ol>
      </nav>

      {/* Main Content with Sidebar */}
      <main className="flex flex-1 px-12 pb-12 max-xl:px-6 max-lg:flex-col max-lg:items-center max-lg:space-y-6">
        {/* Sidebar */}
        <aside className="w-52 bg-pink-50 rounded-3xl shadow-lg p-6 sticky top-6 self-start max-lg:self-auto max-lg:w-full max-lg:shadow-none max-lg:bg-transparent max-lg:sticky max-lg:top-0 max-lg:flex max-lg:flex-row max-lg:justify-around max-lg:space-x-6">
          {sidebarItems.map(({ key, icon, label, children }) => (
            <div
              key={key}
              className="mb-8 last:mb-0 max-lg:mb-0 max-lg:flex max-lg:flex-col max-lg:items-center"
            >
              <div className="flex items-center mb-3 text-pink-600 font-semibold select-none justify-center max-lg:mb-1">
                <div className="mr-2">{icon}</div>
                <span className="text-lg">{label}</span>
              </div>
              <ul className="space-y-2 text-pink-700 font-medium max-lg:flex max-lg:space-y-0 max-lg:space-x-2 max-lg:text-sm max-lg:overflow-auto max-lg:whitespace-nowrap max-lg:scrollbar-thin max-lg:scrollbar-thumb-pink-300 max-lg:scrollbar-track-transparent">
                {children.map((child, idx) => {
                  const isActive =
                    activeSidebar.subKey === key && activeSidebar.idx === idx;
                  return (
                    <li
                      key={idx}
                      onClick={() => setActiveSidebar({ subKey: key, idx })}
                      className={`px-4 py-1 rounded-full cursor-pointer select-text transition shadow-sm flex items-center justify-center ${
                        isActive
                          ? "bg-pink-400 text-white shadow-pink-400/70 font-bold"
                          : "hover:bg-pink-100 active:bg-pink-200"
                      }`}
                      tabIndex={0}
                      role="button"
                      onKeyDown={(e) => {
                        if (e.key === "Enter" || e.key === " ") {
                          setActiveSidebar({ subKey: key, idx });
                        }
                      }}
                    >
                      {child}
                    </li>
                  );
                })}
              </ul>
            </div>
          ))}
        </aside>

        {/* Content Area */}
        <section className="flex-1 bg-white rounded-3xl shadow-lg ml-10 p-8 text-pink-800 min-h-[320px] max-lg:ml-0 max-lg:w-full">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-2xl font-extrabold mb-4 select-text"
          >
            欢迎来到可爱风格前端框架
          </motion.div>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="text-pink-700 text-base max-w-prose leading-relaxed"
          >
            这是一个顶部-侧边布局的前端框架示例，采用明亮活泼的粉色系配色，配合圆润的边角和柔和的阴影，营造出可爱、温暖的视觉氛围。导航和侧边栏的交互设计简洁流畅，支持键盘操作，满足易用性和美观性的需求。请随意点击侧边导航和顶部导航按钮，体验页面的动态效果！
          </motion.p>
          <motion.img
            src="https://placehold.co/600x300/png?text=可爱风格示意图"
            alt="可爱风格示意图"
            className="mt-8 rounded-2xl shadow-lg"
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.6, type: "spring", stiffness: 100 }}
            loading="lazy"
          />
        </section>
      </main>

      {/* Footer */}
      <footer className="text-center text-pink-400 text-sm py-6 select-none border-t border-pink-200 mt-auto font-mono tracking-wide">
        © {new Date().getFullYear()} 可爱前端框架 ♥ 保留所有权利
      </footer>
    </div>
  );
}