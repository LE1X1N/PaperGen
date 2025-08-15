import React, { useState } from "react";
import {
  Home,
  PieChart,
  Users,
  FileText,
  Layout as LayoutIcon,
  Menu as MenuIcon,
  Coffee,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const menuItems = [
  {
    key: "1",
    label: "仪表盘",
    icon: <PieChart className="w-5 h-5 text-yellow-400" />,
  },
  {
    key: "2",
    label: "项目管理",
    icon: <LayoutIcon className="w-5 h-5 text-pink-400" />,
  },
  {
    key: "sub1",
    label: "用户管理",
    icon: <Users className="w-5 h-5 text-green-400" />,
    children: [
      { key: "3", label: "用户列表" },
      { key: "4", label: "权限设置" },
      { key: "5", label: "角色管理" },
    ],
  },
  {
    key: "sub2",
    label: "文件中心",
    icon: <FileText className="w-5 h-5 text-purple-400" />,
    children: [
      { key: "6", label: "文件列表" },
      { key: "7", label: "上传文件" },
    ],
  },
  {
    key: "8",
    label: "菜单管理",
    icon: <MenuIcon className="w-5 h-5 text-cyan-400" />,
  },
  {
    key: "9",
    label: "关于",
    icon: <Coffee className="w-5 h-5 text-amber-400" />,
  },
];

const sidebarVariants = {
  expanded: { width: 260, transition: { type: "spring", stiffness: 200 } },
  collapsed: { width: 72, transition: { type: "spring", stiffness: 200 } },
};

const submenuVariants = {
  open: { height: "auto", opacity: 1, transition: { duration: 0.3 } },
  closed: { height: 0, opacity: 0, transition: { duration: 0.2 } },
};

export default function App() {
  const [collapsed, setCollapsed] = useState(false);
  const [activeKey, setActiveKey] = useState("1");
  const [openSubmenus, setOpenSubmenus] = useState([]);

  const toggleCollapse = () => setCollapsed((v) => !v);

  const onMenuClick = (key, hasChildren) => {
    if (hasChildren) {
      setOpenSubmenus((prev) =>
        prev.includes(key) ? prev.filter((k) => k !== key) : [...prev, key]
      );
    } else {
      setActiveKey(key);
    }
  };

  // Find breadcrumb based on activeKey
  let breadcrumb = ["首页"];
  menuItems.forEach((item) => {
    if (item.key === activeKey) {
      breadcrumb = ["首页", item.label];
    } else if (item.children) {
      const child = item.children.find((c) => c.key === activeKey);
      if (child) {
        breadcrumb = ["首页", item.label, child.label];
      }
    }
  });

  return (
    <div className="flex min-h-screen bg-gradient-to-tr from-rose-50 via-teal-50 to-blue-50 font-sans select-none">
      {/* 侧边栏 */}
      <motion.aside
        aria-label="侧边栏导航"
        animate={collapsed ? "collapsed" : "expanded"}
        variants={sidebarVariants}
        className="bg-gradient-to-b from-pink-300 via-pink-200 to-pink-100 shadow-xl text-pink-900 flex flex-col rounded-tr-3xl rounded-br-3xl border border-pink-400"
      >
        <div className="flex items-center justify-between px-5 py-4 border-b border-pink-400">
          <h1
            className={`font-extrabold text-xl select-text tracking-widest whitespace-nowrap truncate transition-opacity duration-300 text-pink-700 ${
              collapsed ? "opacity-0" : "opacity-100"
            }`}
            style={{ fontFamily: "'Comic Sans MS', cursive, sans-serif" }}
          >
            趣味前端框架
          </h1>
          <button
            onClick={toggleCollapse}
            aria-label={collapsed ? "展开菜单" : "收起菜单"}
            className="p-2 rounded-full hover:bg-pink-400 hover:bg-opacity-30 focus:outline-none focus:ring-2 focus:ring-pink-500 transition"
          >
            <MenuIcon className="w-6 h-6" />
          </button>
        </div>

        <nav className="flex-1 overflow-y-auto py-4 no-scrollbar">
          <ul className="flex flex-col gap-2 px-2">
            {menuItems.map(({ key, label, icon, children }) => {
              const isActive =
                activeKey === key ||
                (children && children.some((c) => c.key === activeKey));
              const isOpen = openSubmenus.includes(key);

              return (
                <li key={key} className="select-none">
                  <div
                    onClick={() => onMenuClick(key, !!children)}
                    className={`flex items-center cursor-pointer rounded-xl px-4 py-3 
                    transition-colors duration-300 gap-3 relative
                    ${
                      isActive
                        ? "bg-pink-400 bg-opacity-70 text-white shadow-[0_4px_10px_rgba(236,72,153,0.4)]"
                        : "text-pink-700 hover:bg-pink-300 hover:bg-opacity-50"
                    }
                    `}
                    style={{ fontFamily: "'Comic Sans MS', cursive, sans-serif" }}
                  >
                    <span className="flex-shrink-0">{icon}</span>
                    {!collapsed && (
                      <span className="flex-1 text-base font-semibold tracking-wide select-text">
                        {label}
                      </span>
                    )}
                    {!collapsed && children && (
                      <motion.span
                        animate={{ rotate: isOpen ? 90 : 0 }}
                        className="inline-block transition-transform select-none text-pink-700"
                        style={{ fontWeight: "700" }}
                      >
                        ▶
                      </motion.span>
                    )}
                    {/* 卡通风格小圆点 */}
                    {!isActive && (
                      <span
                        aria-hidden="true"
                        className="absolute left-2 top-1/2 -translate-y-1/2 w-2.5 h-2.5 rounded-full bg-pink-500 opacity-60 animate-pulse"
                      />
                    )}
                  </div>
                  {children && (
                    <AnimatePresence initial={false}>
                      {isOpen && !collapsed && (
                        <motion.ul
                          key="submenu"
                          initial="closed"
                          animate="open"
                          exit="closed"
                          variants={submenuVariants}
                          className="pl-12 flex flex-col gap-1 overflow-hidden"
                        >
                          {children.map(({ key: cKey, label: cLabel }) => (
                            <li key={cKey}>
                              <button
                                onClick={() => setActiveKey(cKey)}
                                className={`w-full text-left rounded-lg px-4 py-2 text-sm font-medium transition-colors 
                                ${
                                  activeKey === cKey
                                    ? "bg-pink-400 bg-opacity-70 text-white shadow-inner"
                                    : "text-pink-700 hover:bg-pink-300 hover:bg-opacity-50"
                                }
                              `}
                                style={{ fontFamily: "'Comic Sans MS', cursive, sans-serif" }}
                              >
                                {cLabel}
                              </button>
                            </li>
                          ))}
                        </motion.ul>
                      )}
                    </AnimatePresence>
                  )}
                </li>
              );
            })}
          </ul>
        </nav>

        <div
          className={`text-xs text-pink-600 px-5 py-3 border-t border-pink-400 select-text transition-all duration-300 ${
            collapsed ? "text-center" : "text-left"
          } font-semibold font-comic`}
        >
          {collapsed ? "©23 趣味" : "© 2023 趣味前端框架"}
        </div>
      </motion.aside>

      {/* 主体内容 */}
      <main className="flex-1 flex flex-col px-8 py-8 max-w-full overflow-hidden">
        {/* 面包屑 */}
        <nav
          aria-label="面包屑"
          className="text-pink-700 text-sm mb-6 select-none flex flex-wrap items-center gap-1 font-comic"
          style={{ fontWeight: "600" }}
        >
          {breadcrumb.map((bc, idx) => (
            <span key={bc} className="inline-flex items-center">
              {idx > 0 && (
                <svg
                  className="w-5 h-5 mx-1 text-pink-400"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                  aria-hidden="true"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                </svg>
              )}
              <span>{bc}</span>
            </span>
          ))}
        </nav>

        {/* 内容卡片 */}
        <article
          className="bg-pink-50 rounded-3xl shadow-lg p-8 flex-1 overflow-auto border-4 border-pink-200 relative"
          style={{ fontFamily: "'Comic Sans MS', cursive, sans-serif" }}
        >
          <h2 className="text-3xl font-extrabold text-pink-700 mb-6 tracking-wider select-text">
            {breadcrumb[breadcrumb.length - 1]}
          </h2>
          <p className="text-pink-600 leading-relaxed text-lg max-w-prose">
            这是一个卡通风格的前端代码展示框架示例，使用React和TailwindCSS打造。侧边栏采用暖色渐变与圆角设计，按钮带轻微脉动动画，整体风格活泼可爱，配色柔和，适合趣味项目展示。
          </p>
          <p className="mt-6 text-pink-400 text-sm select-text tracking-wide">
            当前页面Key: <code className="bg-pink-200 rounded px-1 py-0.5">{activeKey}</code>
          </p>

          {/* 卡通元素装饰 */}
          <motion.div
            animate={{ rotate: [0, 8, -8, 8, -8, 0] }}
            transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
            className="absolute -top-10 -right-10 w-24 h-24 bg-pink-300 rounded-full shadow-lg flex items-center justify-center select-none"
            aria-hidden="true"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="w-12 h-12 text-pink-600 opacity-70"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={1.5}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M12 3v2m0 14v2m7-9h2M3 12H1m16.24-6.24l1.42 1.42M5.34 18.66l-1.42 1.42m12.02 0l1.42-1.42M5.34 5.34L3.92 3.92"
              />
            </svg>
          </motion.div>
        </article>

        {/* 页脚 */}
        <footer
          className="mt-10 text-center text-pink-300 text-xs select-none tracking-widest font-semibold font-comic"
          style={{ userSelect: "none" }}
        >
          © 2023 趣味前端框架 版权所有
        </footer>
      </main>
    </div>
  );
}